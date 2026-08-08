import re
from typing import Any
from urllib.parse import urlparse, unquote

import tldextract
from bs4 import BeautifulSoup

from app.agents.base import AgentFinding, BaseAgent
from app.services.gemini_service import gemini_service
from app.services.threat_intel_service import threat_intel_service
from app.services.whois_service import whois_service
from app.services.ssl_service import ssl_service
from app.services.webpage_service import webpage_service
from app.services.safebrowsing_service import safe_browsing_service


# ============================================================
# KNOWN BRANDS
# ============================================================

KNOWN_BRANDS = [
    "paypal",
    "google",
    "microsoft",
    "apple",
    "amazon",
    "netflix",
    "facebook",
    "instagram",
    "bankofamerica",
    "wellsfargo",
    "chase",
    "dhl",
    "fedex",
    "linkedin",
    "instagram",
    "whatsapp",
    "telegram",
    "coinbase",
    "binance",
    "adobe",
    "dropbox",
    "github",
]


# ============================================================
# COMMON PHISHING KEYWORDS
# ============================================================

PHISHING_KEYWORDS = {
    "login",
    "signin",
    "sign-in",
    "verify",
    "verification",
    "secure",
    "security",
    "update",
    "confirm",
    "confirmation",
    "account",
    "password",
    "credential",
    "wallet",
    "payment",
    "billing",
    "invoice",
    "recover",
    "recovery",
    "unlock",
    "suspended",
    "support",
    "authenticate",
    "authentication",
    "kyc",
    "otp",
}


# ============================================================
# SUSPICIOUS TLDs
# NOTE:
# TLD ALONE IS NEVER TREATED AS A SCAM.
# ============================================================

SUSPICIOUS_TLDS = {
    "tk",
    "ml",
    "ga",
    "cf",
    "gq",
    "xyz",
    "top",
    "click",
    "work",
}


# ============================================================
# BRAND CHARACTER SUBSTITUTIONS
# Used for:
# paypal  -> paypa1
# google  -> g00gle
# microsoft -> micr0soft
# ============================================================

CHAR_SUBSTITUTIONS = str.maketrans(
    {
        "0": "o",
        "1": "l",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "8": "b",
        "@": "a",
    }
)


# ============================================================
# LEVENSHTEIN DISTANCE
# ============================================================

def _levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        return _levenshtein(b, a)

    if len(b) == 0:
        return len(a)

    previous = list(range(len(b) + 1))

    for i, ca in enumerate(a):
        current = [i + 1]

        for j, cb in enumerate(b):
            insertions = previous[j + 1] + 1
            deletions = current[j] + 1
            substitutions = previous[j] + (ca != cb)

            current.append(
                min(
                    insertions,
                    deletions,
                    substitutions,
                )
            )

        previous = current

    return previous[-1]


# ============================================================
# NORMALIZE BRAND-LIKE TEXT
# ============================================================

def _normalize_brand_text(value: str) -> str:
    value = value.lower().strip()

    # Replace common digit substitutions.
    value = value.translate(CHAR_SUBSTITUTIONS)

    # Remove separators.
    value = re.sub(r"[^a-z]", "", value)

    return value


# ============================================================
# DOMAIN TOKEN EXTRACTION
# ============================================================

def _domain_tokens(domain: str) -> list[str]:
    """
    Converts:

        paypa1-login-security

    into:

        ["paypa1", "login", "security"]
    """

    return [
        token
        for token in re.split(r"[-_.]+", domain.lower())
        if token
    ]


# ============================================================
# BRAND DETECTION
# ============================================================

def _detect_brand_impersonation(domain: str) -> dict[str, Any]:
    """
    Detects:

        paypal-login-security.com
        paypa1-login-security.com
        secure-paypal-account.com
        paypaI-security.com
    """

    labels = domain.lower().split(".")

    # Only inspect the registered domain name,
    # not the TLD.
    main_domain = labels[0] if labels else domain

    tokens = _domain_tokens(main_domain)

    normalized_full = _normalize_brand_text(main_domain)

    best_match = None
    best_distance = 999
    best_token = None
    exact_brand_present = False

    for brand in KNOWN_BRANDS:
        normalized_brand = _normalize_brand_text(brand)

        # ----------------------------------------------------
        # Exact brand in domain
        # ----------------------------------------------------

        if normalized_brand in normalized_full:
            exact_brand_present = True

            if normalized_full != normalized_brand:
                return {
                    "detected": True,
                    "brand": brand,
                    "token": main_domain,
                    "distance": 0,
                    "type": "brand_in_domain",
                }

        # ----------------------------------------------------
        # Token-level comparison
        # ----------------------------------------------------

        for token in tokens:
            normalized_token = _normalize_brand_text(token)

            if not normalized_token:
                continue

            distance = _levenshtein(
                normalized_token,
                normalized_brand,
            )

            if distance < best_distance:
                best_distance = distance
                best_match = brand
                best_token = token

    # Strong typo / lookalike.
    if (
        best_match
        and best_token
        and best_distance <= 2
        and _normalize_brand_text(best_token)
        != _normalize_brand_text(best_match)
    ):
        return {
            "detected": True,
            "brand": best_match,
            "token": best_token,
            "distance": best_distance,
            "type": "typosquat",
        }

    if exact_brand_present:
        return {
            "detected": True,
            "brand": best_match,
            "token": main_domain,
            "distance": 0,
            "type": "brand_reference",
        }

    return {
        "detected": False,
        "brand": None,
        "token": None,
        "distance": None,
        "type": None,
    }


# ============================================================
# PHISHING KEYWORD DETECTION
# ============================================================

def _detect_phishing_keywords(url: str) -> list[str]:
    decoded = unquote(url.lower())

    found = []

    for keyword in PHISHING_KEYWORDS:
        if re.search(
            rf"(?<![a-z]){re.escape(keyword)}(?![a-z])",
            decoded,
        ):
            found.append(keyword)

    return sorted(found)


# ============================================================
# URL STRUCTURE ANALYSIS
# ============================================================

def _analyze_url_structure(
    parsed,
    ext,
) -> tuple[float, list[str], dict[str, Any]]:
    score = 0.0
    signatures = []
    evidence = {}

    hostname = (parsed.hostname or "").lower()
    raw_url = parsed.geturl()

    # --------------------------------------------------------
    # HTTP
    # --------------------------------------------------------

    if parsed.scheme == "http":
        score += 5
        signatures.append("no_https")

    # --------------------------------------------------------
    # IP address instead of normal hostname
    # --------------------------------------------------------

    if re.fullmatch(
        r"\d{1,3}(?:\.\d{1,3}){3}",
        hostname,
    ):
        score += 25
        signatures.append("ip_address_host")
        evidence["ip_host"] = True

    # --------------------------------------------------------
    # Punycode
    # --------------------------------------------------------

    if "xn--" in hostname:
        score += 20
        signatures.append("punycode")

    # --------------------------------------------------------
    # Too many subdomains
    # --------------------------------------------------------

    subdomain_parts = (
        ext.subdomain.split(".")
        if ext.subdomain
        else []
    )

    subdomain_count = len(
        [x for x in subdomain_parts if x]
    )

    evidence["subdomain_count"] = subdomain_count

    if subdomain_count >= 4:
        score += 15
        signatures.append("many_subdomains")

    elif subdomain_count >= 3:
        score += 8
        signatures.append("multiple_subdomains")

    # --------------------------------------------------------
    # @ symbol
    # --------------------------------------------------------

    if "@" in raw_url:
        score += 20
        signatures.append("at_symbol_in_url")

    # --------------------------------------------------------
    # Very long URL
    # --------------------------------------------------------

    if len(raw_url) > 180:
        score += 10
        signatures.append("very_long_url")

    elif len(raw_url) > 120:
        score += 5
        signatures.append("long_url")

    # --------------------------------------------------------
    # Excessive hyphens
    # --------------------------------------------------------

    hyphen_count = hostname.count("-")

    evidence["hyphen_count"] = hyphen_count

    if hyphen_count >= 4:
        score += 10
        signatures.append("many_hyphens")

    elif hyphen_count >= 2:
        score += 4
        signatures.append("multiple_hyphens")

    # --------------------------------------------------------
    # URL encoded suspicious characters
    # --------------------------------------------------------

    if "%" in raw_url:
        decoded = unquote(raw_url)

        if decoded != raw_url:
            score += 3
            signatures.append("encoded_url")

    # --------------------------------------------------------
    # Suspicious TLD
    # --------------------------------------------------------

    tld = (
        ext.suffix.split(".")[-1].lower()
        if ext.suffix
        else ""
    )

    evidence["tld"] = tld

    if tld in SUSPICIOUS_TLDS:
        score += 7
        signatures.append("suspicious_tld")

    return score, signatures, evidence


# ============================================================
# RISK SCORE HELPERS
# ============================================================

def _add_signal(
    score: float,
    signatures: list[str],
    signature: str,
    weight: float,
) -> float:
    signatures.append(signature)
    return score + weight


# ============================================================
# URL AGENT
# ============================================================

class URLAnalysisAgent(BaseAgent):

    name = "url_analysis_agent"

    async def analyze(
        self,
        context: dict[str, Any],
    ) -> AgentFinding:

        print("\n========== URL AGENT START ==========")

        url = (context.get("text_value") or "").strip()

        if not url:
            return AgentFinding(
                self.name,
                0,
                0,
                {"reason": "no_url"},
            )

        # ====================================================
        # NORMALIZE URL
        # ====================================================

        if not url.startswith(
            ("http://", "https://")
        ):
            url = "https://" + url

        url = url.strip()

        parsed = urlparse(url)

        if not parsed.hostname:
            return AgentFinding(
                self.name,
                70,
                0.90,
                {
                    "reason": "invalid_url",
                    "url": url,
                },
                ["invalid_url"],
            )

        # Remove trailing dot from hostname.
        hostname = (
            parsed.hostname.lower().rstrip(".")
        )

        ext = tldextract.extract(hostname)

        if ext.domain and ext.suffix:
            domain = f"{ext.domain}.{ext.suffix}"
        else:
            domain = hostname

        score = 0.0
        signatures: list[str] = []

        evidence: dict[str, Any] = {
            "url": url,
            "hostname": hostname,
            "domain": domain,
        }

        # ====================================================
        # URL STRUCTURE
        # ====================================================

        structure_score, structure_signatures, structure_evidence = (
            _analyze_url_structure(
                parsed,
                ext,
            )
        )

        score += structure_score
        signatures.extend(structure_signatures)
        evidence.update(structure_evidence)

        # ====================================================
        # BRAND / TYPOSQUATTING
        # ====================================================

        brand_result = _detect_brand_impersonation(
            hostname
        )

        evidence["brand_analysis"] = brand_result

        if brand_result["detected"]:

            brand = brand_result["brand"]
            detection_type = brand_result["type"]

            if detection_type == "typosquat":

                score += 35

                signatures.append(
                    f"typosquat:{brand}"
                )

            elif detection_type == "brand_in_domain":

                # Brand + suspicious context is more dangerous.
                score += 18

                signatures.append(
                    f"brand_in_domain:{brand}"
                )

            else:

                score += 5

                signatures.append(
                    f"brand_reference:{brand}"
                )

        # ====================================================
        # PHISHING KEYWORDS
        # ====================================================

        phishing_keywords = (
            _detect_phishing_keywords(url)
        )

        evidence["phishing_keywords"] = (
            phishing_keywords
        )

        if phishing_keywords:

            # One keyword alone should not create a
            # confirmed scam.
            keyword_score = min(
                15,
                5 + (len(phishing_keywords) - 1) * 2,
            )

            score += keyword_score

            signatures.append(
                "phishing_keywords"
            )

        # ====================================================
        # BRAND + PHISHING CONTEXT
        # ====================================================

        brand_detected = brand_result["detected"]

        if brand_detected and phishing_keywords:

            score += 20

            signatures.append(
                "brand_phishing_combination"
            )

            evidence[
                "brand_phishing_combination"
            ] = True

        # ====================================================
        # WHOIS / DOMAIN AGE
        # ====================================================

        whois_data = None

        try:
            whois_data = await whois_service.lookup(
                domain
            )
        except Exception as exc:
            print(
                "WHOIS lookup failed:",
                repr(exc),
            )

        evidence["whois"] = whois_data

        if whois_data:

            whois_risk = whois_data.get(
                "risk"
            )

            evidence["domain_risk"] = whois_risk

            if whois_risk == "very_new_domain":

                score += 18

                signatures.append(
                    "very_new_domain"
                )

            elif whois_risk == "new_domain":

                score += 10

                signatures.append(
                    "new_domain"
                )

            elif whois_risk == "young_domain":

                score += 5

                signatures.append(
                    "young_domain"
                )

        # ====================================================
        # SSL
        # ====================================================

        ssl_data = {}

        try:
            ssl_data = await ssl_service.lookup(
                url
            )

            if not isinstance(
                ssl_data,
                dict,
            ):
                ssl_data = {}

        except Exception as exc:

            print(
                "SSL lookup failed:",
                repr(exc),
            )

        evidence["ssl"] = ssl_data

        # SSL is supporting evidence only.
        # It must NOT independently make a website
        # a confirmed scam.

        if ssl_data:

            if ssl_data.get("valid") is False:

                score += 10

                signatures.append(
                    "invalid_ssl"
                )

            elif ssl_data.get("expired"):

                score += 8

                signatures.append(
                    "expired_ssl"
                )

            elif ssl_data.get("self_signed"):

                score += 6

                signatures.append(
                    "self_signed_ssl"
                )

        # ====================================================
        # THREAT INTELLIGENCE
        # ====================================================

        ioc_hit = None

        try:

            ioc_hit = await threat_intel_service.lookup(
                "domain",
                domain,
            )

        except Exception as exc:

            print(
                "Threat intelligence lookup failed:",
                repr(exc),
            )

        evidence[
            "threat_intel_match"
        ] = ioc_hit

        if ioc_hit:

            # Strong external evidence.
            score = max(score, 92)

            signatures.append(
                f"threat_intel:{ioc_hit.get('source', 'unknown')}"
            )

        # ====================================================
        # GOOGLE SAFE BROWSING
        # ====================================================

        safe_hit = None

        try:

            safe_hit = await safe_browsing_service.lookup(
                url
            )

        except Exception as exc:

            print(
                "Safe Browsing lookup failed:",
                repr(exc),
            )

        evidence[
            "google_safe_browsing"
        ] = safe_hit

        if safe_hit:

            score = max(score, 96)

            signatures.append(
                "google_safe_browsing"
            )

        # ====================================================
        # WEBPAGE ANALYSIS
        # ====================================================

        page = None

        try:

            page = await webpage_service.fetch(
                url
            )

        except Exception as exc:

            print(
                "Webpage fetch failed:",
                repr(exc),
            )

        if not isinstance(page, dict):
            page = {
                "success": False,
            }

        page_success = bool(
            page.get("success")
        )

        evidence[
            "html_fetched"
        ] = page_success

        page_title = None

        if page_success:

            html = page.get(
                "html",
                "",
            )

            soup = BeautifulSoup(
                html,
                "html.parser",
            )

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            if (
                soup.title
                and soup.title.string
            ):

                page_title = (
                    soup.title.string.strip()
                )

            # ------------------------------------------------
            # FORMS
            # ------------------------------------------------

            forms = soup.find_all(
                "form"
            )

            forms_count = len(forms)

            # ------------------------------------------------
            # PASSWORD INPUTS
            # ------------------------------------------------

            password_inputs = soup.find_all(
                "input",
                {
                    "type": "password"
                },
            )

            password_count = len(
                password_inputs
            )

            # ------------------------------------------------
            # IFRAME
            # ------------------------------------------------

            iframe_count = len(
                soup.find_all("iframe")
            )

            evidence[
                "forms_count"
            ] = forms_count

            evidence[
                "password_inputs"
            ] = password_count

            evidence[
                "iframe_count"
            ] = iframe_count

            # ------------------------------------------------
            # PASSWORD FORM
            # ------------------------------------------------

            if password_count:

                score += 6

                signatures.append(
                    "password_form"
                )

            # ------------------------------------------------
            # MANY FORMS
            # ------------------------------------------------

            if forms_count >= 5:

                score += 8

                signatures.append(
                    "many_forms"
                )

            elif forms_count >= 3:

                score += 4

                signatures.append(
                    "multiple_forms"
                )

            # ------------------------------------------------
            # IFRAMES
            # ------------------------------------------------

            if iframe_count >= 4:

                score += 8

                signatures.append(
                    "many_iframes"
                )

            elif iframe_count >= 2:

                score += 4

                signatures.append(
                    "multiple_iframes"
                )

            # ------------------------------------------------
            # PAGE BRAND IMPERSONATION
            # ------------------------------------------------

            lower_html = html.lower()

            page_brands = [
                "paypal",
                "google",
                "microsoft",
                "amazon",
                "apple",
                "netflix",
                "facebook",
                "instagram",
                "bank of america",
                "wells fargo",
                "chase",
                "dhl",
                "fedex",
                "linkedin",
                "whatsapp",
                "coinbase",
                "binance",
            ]

            page_brand = None

            for brand in page_brands:

                compact_brand = brand.replace(
                    " ",
                    "",
                )

                if (
                    brand in lower_html
                    or compact_brand in lower_html
                ):

                    page_brand = brand
                    break

            evidence[
                "page_brand"
            ] = page_brand

            # If page contains a brand but the
            # registered domain is not that brand,
            # treat as impersonation.
            if page_brand:

                domain_compact = (
                    domain.lower()
                    .replace("-", "")
                )

                if (
                    page_brand.replace(
                        " ",
                        "",
                    )
                    not in domain_compact
                ):

                    score += 18

                    signatures.append(
                        f"brand_impersonation:{page_brand}"
                    )

        evidence[
            "page_title"
        ] = page_title

        # ====================================================
        # COMBINED HIGH-CONFIDENCE SIGNALS
        # ====================================================

        strong_signal_count = 0

        strong_signals = {
            "typosquat",
            "threat_intel",
            "google_safe_browsing",
            "brand_phishing_combination",
            "brand_impersonation",
            "very_new_domain",
        }

        for signature in signatures:

            if any(
                signature.startswith(prefix)
                for prefix in strong_signals
            ):
                strong_signal_count += 1

        evidence[
            "strong_signal_count"
        ] = strong_signal_count

        # ====================================================
        # GEMINI SECONDARY ANALYSIS
        # ====================================================

        ai_reasoning = None
        ai_boost = 0

        # Only use Gemini when deterministic signals
        # leave uncertainty.
        if (
            25 <= score <= 75
            and not ioc_hit
            and not safe_hit
        ):

            try:

                result = await (
                    gemini_service.generate_structured(
                        task_prompt="""
Analyze this URL for phishing risk.

You are a SECONDARY analyst.
Do not blindly assume that HTTP, HTTPS,
a suspicious TLD, a password form, or a
single keyword means the website is a scam.

Look for:

1. Brand impersonation
2. Typosquatting
3. Suspicious login/verification context
4. Domain structure
5. Phishing indicators
6. Whether the domain and apparent brand
   are inconsistent

Return ONLY:

{
  "risk_boost_0_to_20": number,
  "reasoning": string
}

The boost must be between 0 and 20.
""",
                        untrusted_content=url,
                        response_schema_hint="""
{
  "risk_boost_0_to_20": number,
  "reasoning": string
}
""",
                    )
                )

                if (
                    result
                    and not result.get(
                        "_fallback"
                    )
                ):

                    ai_boost = max(
                        0,
                        min(
                            int(
                                result.get(
                                    "risk_boost_0_to_20",
                                    0,
                                )
                            ),
                            20,
                        ),
                    )

                    ai_reasoning = result.get(
                        "reasoning"
                    )

                    score += ai_boost

            except Exception as exc:

                print(
                    "Gemini URL analysis failed:",
                    repr(exc),
                )

        evidence[
            "ai_reasoning"
        ] = ai_reasoning

        evidence[
            "ai_boost"
        ] = ai_boost

        # ====================================================
        # FINAL SCORE
        # ====================================================

        score = max(
            0,
            min(
                round(score),
                100,
            ),
        )

        # ====================================================
        # FINAL CONFIDENCE
        # ====================================================

        # Confidence is based on quality of evidence,
        # not simply whether any signature exists.

        confidence = 0.55

        if signatures:
            confidence += 0.05

        if brand_detected:
            confidence += 0.10

        if whois_data:
            confidence += 0.05

        if ssl_data:
            confidence += 0.05

        if ioc_hit:
            confidence += 0.20

        if safe_hit:
            confidence += 0.20

        if strong_signal_count >= 2:
            confidence += 0.08

        confidence = min(
            round(confidence, 2),
            0.99,
        )

        # ====================================================
        # DEBUG
        # ====================================================

        print("\n========================================")
        print("              URL AGENT")
        print("========================================")
        print("URL:", url)
        print("Domain:", domain)
        print("Brand:", brand_result)
        print("Phishing keywords:", phishing_keywords)
        print("WHOIS:", whois_data)
        print("SSL:", ssl_data)
        print("Threat Intel:", ioc_hit)
        print("Safe Browsing:", safe_hit)
        print("Page fetched:", page_success)
        print("AI boost:", ai_boost)
        print("Score:", score)
        print("Confidence:", confidence)
        print("Signatures:", signatures)
        print("========================================\n")

        # ====================================================
        # RETURN
        # ====================================================

        return AgentFinding(
            agent_name=self.name,
            raw_score=score,
            confidence=confidence,
            evidence=evidence,
            matched_signatures=signatures,
        )


# ============================================================
# SINGLE AGENT INSTANCE
# ============================================================

url_analysis_agent = URLAnalysisAgent()