"""
Email Analysis Agent ("Email Shield")

Analyzes raw email content including:
- Email headers
- SPF / DKIM / DMARC results
- From / Reply-To mismatch
- Display-name spoofing
- Subject
- Phishing language
- Credential / OTP / payment requests
- Suspicious URLs
- Shortened URLs
- Urgency / social engineering
- Suspicious attachments
- Gemini reasoning for borderline cases
"""

import re
from typing import Any
from urllib.parse import urlparse

from app.agents.base import AgentFinding, BaseAgent
from app.services.gemini_service import gemini_service


# ============================================================
# PATTERNS
# ============================================================

URGENCY_PATTERNS = [
    r"\bverify\s+your\s+account\b",
    r"\bverify\s+your\s+identity\b",
    r"\bact\s+now\b",
    r"\baction\s+required\b",
    r"\bimmediately\b",
    r"\burgent\b",
    r"\bwithin\s+\d+\s+(minutes?|hours?|days?)\b",
    r"\blimited\s+time\b",
    r"\bexpires?\s+(today|soon|within)\b",
    r"\baccount\s+(will\s+be|has\s+been)\s+(closed|locked|suspended)\b",
    r"\bunusual\s+(login|activity|sign[- ]?in)\b",
]

CREDENTIAL_PATTERNS = [
    r"\benter\s+your\s+password\b",
    r"\bconfirm\s+your\s+password\b",
    r"\bverify\s+your\s+password\b",
    r"\bpassword\s+required\b",
    r"\blogin\s+details\b",
    r"\bsign\s*in\s+details\b",
    r"\busername\s+and\s+password\b",
    r"\bcredentials?\b",
]

OTP_PATTERNS = [
    r"\benter\s+(the\s+)?otp\b",
    r"\bshare\s+(the\s+)?otp\b",
    r"\botp\s+verification\b",
    r"\bone[- ]time\s+password\b",
    r"\bverification\s+code\b",
    r"\bsecurity\s+code\b",
]

PAYMENT_PATTERNS = [
    r"\bpayment\s+required\b",
    r"\bpay\s+now\b",
    r"\bmake\s+a\s+payment\b",
    r"\bpayment\s+failed\b",
    r"\bpayment\s+verification\b",
    r"\bbank\s+account\b",
    r"\bcredit\s+card\b",
    r"\bdebit\s+card\b",
    r"\bcvv\b",
    r"\bupi\s+pin\b",
    r"\baccount\s+number\b",
]

PHISHING_PATTERNS = [
    r"\bclick\s+(here|below|the\s+link)\b",
    r"\bclick\s+the\s+link\b",
    r"\bopen\s+the\s+link\b",
    r"\bconfirm\s+your\s+account\b",
    r"\bupdate\s+your\s+account\b",
    r"\bsecure\s+your\s+account\b",
    r"\brestore\s+access\b",
    r"\bunlock\s+your\s+account\b",
    r"\bclaim\s+your\s+(reward|prize|gift)\b",
]

GENERIC_GREETING_PATTERNS = [
    r"^\s*dear\s+customer\b",
    r"^\s*dear\s+user\b",
    r"^\s*dear\s+valued\s+customer\b",
    r"^\s*dear\s+valued\s+member\b",
    r"^\s*hello\s+customer\b",
    r"^\s*dear\s+account\s+holder\b",
]

SHORTENED_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "rb.gy",
    "t.co",
    "cutt.ly",
    "is.gd",
    "ow.ly",
    "shorturl.at",
}

FREE_EMAIL_DOMAINS = {
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com",
    "proton.me",
    "protonmail.com",
    "icloud.com",
}

SUSPICIOUS_ATTACHMENT_EXTENSIONS = {
    ".exe",
    ".scr",
    ".bat",
    ".cmd",
    ".com",
    ".js",
    ".vbs",
    ".ps1",
    ".msi",
    ".jar",
    ".hta",
}


# ============================================================
# REGEX
# ============================================================

EMAIL_PATTERN = re.compile(
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    re.I,
)

LINK_PATTERN = re.compile(
    r"https?://[^\s<>\]\)\"']+",
    re.I,
)


# ============================================================
# HELPERS
# ============================================================

def extract_header(
    content: str,
    header_name: str,
) -> str | None:

    pattern = rf"^{re.escape(header_name)}\s*:\s*(.+)$"

    match = re.search(
        pattern,
        content,
        re.I | re.M,
    )

    if not match:
        return None

    return match.group(1).strip()


def extract_domain(
    email_value: str | None,
) -> str | None:

    if not email_value:
        return None

    match = EMAIL_PATTERN.search(
        email_value
    )

    if not match:
        return None

    return match.group(0).split("@")[-1].lower()


def extract_display_name(
    email_value: str | None,
) -> str | None:

    if not email_value:
        return None

    match = re.search(
        r"^\s*[\"']?(.+?)[\"']?\s*<[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}>",
        email_value,
        re.I,
    )

    if match:
        return match.group(1).strip()

    return None


def get_body(
    content: str,
) -> str:

    parts = re.split(
        r"\r?\n\r?\n",
        content,
        maxsplit=1,
    )

    if len(parts) == 2:
        return parts[1]

    return content


def find_patterns(
    text: str,
    patterns: list[str],
) -> list[str]:

    hits = []

    for pattern in patterns:
        if re.search(
            pattern,
            text,
            re.I,
        ):
            hits.append(pattern)

    return hits


def extract_urls(
    content: str,
) -> list[str]:

    urls = LINK_PATTERN.findall(content)

    # Remove duplicates while preserving order
    unique_urls = list(
        dict.fromkeys(urls)
    )

    return unique_urls[:20]


def analyze_url(
    url: str,
) -> dict[str, Any]:

    try:
        parsed = urlparse(url)

        domain = (
            parsed.hostname or ""
        ).lower()

        is_https = (
            parsed.scheme.lower()
            == "https"
        )

        is_shortened = (
            domain in SHORTENED_DOMAINS
        )

        suspicious_domain = False

        # IP address instead of normal domain
        if re.fullmatch(
            r"\d{1,3}(?:\.\d{1,3}){3}",
            domain,
        ):
            suspicious_domain = True

        # Excessive subdomain depth
        if domain.count(".") >= 4:
            suspicious_domain = True

        # Punycode can indicate IDN lookalikes
        if "xn--" in domain:
            suspicious_domain = True

        return {
            "url": url,
            "domain": domain,
            "https": is_https,
            "shortened": is_shortened,
            "suspicious_structure": suspicious_domain,
        }

    except Exception:
        return {
            "url": url,
            "domain": None,
            "https": False,
            "shortened": False,
            "suspicious_structure": True,
        }


# ============================================================
# EMAIL AGENT
# ============================================================

class EmailAnalysisAgent(BaseAgent):

    name = "email_analysis_agent"

    async def analyze(
        self,
        context: dict[str, Any],
    ) -> AgentFinding:

        content = (
            context.get(
                "text_value",
                "",
            )
            or ""
        )

        if not content.strip():

            return AgentFinding(
                agent_name=self.name,
                raw_score=0,
                confidence=0,
                evidence={
                    "reason": "no_email_content",
                },
                matched_signatures=[],
            )

        # ----------------------------------------------------
        # BASIC PARTS
        # ----------------------------------------------------

        subject = (
            extract_header(
                content,
                "Subject",
            )
            or ""
        )

        from_header = (
            extract_header(
                content,
                "From",
            )
            or ""
        )

        reply_to = (
            extract_header(
                content,
                "Reply-To",
            )
            or ""
        )

        return_path = (
            extract_header(
                content,
                "Return-Path",
            )
            or ""
        )

        authentication_results = (
            extract_header(
                content,
                "Authentication-Results",
            )
            or ""
        )

        body = get_body(
            content
        )

        # ----------------------------------------------------
        # HEADER INFORMATION
        # ----------------------------------------------------

        from_domain = extract_domain(
            from_header
        )

        reply_domain = extract_domain(
            reply_to
        )

        return_path_domain = extract_domain(
            return_path
        )

        display_name = extract_display_name(
            from_header
        )

        headers_present = bool(
            from_header
            or subject
            or reply_to
            or return_path
        )

        # ----------------------------------------------------
        # AUTHENTICATION
        # ----------------------------------------------------

        auth_text = (
            authentication_results
            + "\n"
            + content
        )

        spf_fail = bool(
            re.search(
                r"\bspf\s*=\s*(fail|softfail|neutral)\b",
                auth_text,
                re.I,
            )
        )

        spf_pass = bool(
            re.search(
                r"\bspf\s*=\s*pass\b",
                auth_text,
                re.I,
            )
        )

        dkim_fail = bool(
            re.search(
                r"\bdkim\s*=\s*(fail|neutral|temperror|permerror)\b",
                auth_text,
                re.I,
            )
        )

        dkim_pass = bool(
            re.search(
                r"\bdkim\s*=\s*pass\b",
                auth_text,
                re.I,
            )
        )

        dmarc_fail = bool(
            re.search(
                r"\bdmarc\s*=\s*(fail|temperror|permerror)\b",
                auth_text,
                re.I,
            )
        )

        dmarc_pass = bool(
            re.search(
                r"\bdmarc\s*=\s*pass\b",
                auth_text,
                re.I,
            )
        )

        # ----------------------------------------------------
        # SCORING
        # ----------------------------------------------------

        score = 0.0

        signatures: list[str] = []

        evidence: dict[str, Any] = {}

        # ====================================================
        # SPF
        # ====================================================

        if spf_fail:

            score += 20

            signatures.append(
                "spf_failure"
            )

        # ====================================================
        # DKIM
        # ====================================================

        if dkim_fail:

            score += 20

            signatures.append(
                "dkim_failure"
            )

        # ====================================================
        # DMARC
        # ====================================================

        if dmarc_fail:

            score += 25

            signatures.append(
                "dmarc_failure"
            )

        # ====================================================
        # FROM / REPLY-TO
        # ====================================================

        if (
            from_domain
            and reply_domain
            and from_domain
            != reply_domain
        ):

            score += 20

            signatures.append(
                "reply_to_domain_mismatch"
            )

        # ====================================================
        # RETURN PATH
        # ====================================================

        if (
            from_domain
            and return_path_domain
            and from_domain
            != return_path_domain
        ):

            score += 12

            signatures.append(
                "return_path_domain_mismatch"
            )

        # ====================================================
        # DISPLAY NAME SPOOFING
        # ====================================================

        if (
            display_name
            and from_domain
        ):

            display_lower = (
                display_name.lower()
            )

            suspicious_brands = [
                "paypal",
                "amazon",
                "google",
                "microsoft",
                "apple",
                "netflix",
                "sbi",
                "hdfc",
                "icici",
                "axis",
                "bank",
                "upi",
            ]

            if any(
                brand in display_lower
                for brand in suspicious_brands
            ):

                if (
                    from_domain
                    not in {
                        "paypal.com",
                        "amazon.com",
                        "google.com",
                        "microsoft.com",
                        "apple.com",
                        "netflix.com",
                    }
                ):

                    score += 18

                    signatures.append(
                        "suspicious_display_name"
                    )

        # ====================================================
        # SUBJECT
        # ====================================================

        subject_urgency = find_patterns(
            subject,
            URGENCY_PATTERNS,
        )

        subject_phishing = find_patterns(
            subject,
            PHISHING_PATTERNS,
        )

        if subject_urgency:

            score += min(
                len(subject_urgency) * 7,
                14,
            )

            signatures.append(
                "suspicious_subject_urgency"
            )

        if subject_phishing:

            score += min(
                len(subject_phishing) * 8,
                16,
            )

            signatures.append(
                "phishing_subject"
            )

        # ====================================================
        # BODY ANALYSIS
        # ====================================================

        urgency_hits = find_patterns(
            body,
            URGENCY_PATTERNS,
        )

        credential_hits = find_patterns(
            body,
            CREDENTIAL_PATTERNS,
        )

        otp_hits = find_patterns(
            body,
            OTP_PATTERNS,
        )

        payment_hits = find_patterns(
            body,
            PAYMENT_PATTERNS,
        )

        phishing_hits = find_patterns(
            body,
            PHISHING_PATTERNS,
        )

        if urgency_hits:

            score += min(
                len(urgency_hits) * 7,
                21,
            )

            signatures.append(
                "urgency_social_engineering_language"
            )

        if credential_hits:

            score += min(
                len(credential_hits) * 12,
                24,
            )

            signatures.append(
                "credential_request"
            )

        if otp_hits:

            score += min(
                len(otp_hits) * 15,
                30,
            )

            signatures.append(
                "otp_request"
            )

        if payment_hits:

            score += min(
                len(payment_hits) * 10,
                20,
            )

            signatures.append(
                "financial_information_request"
            )

        if phishing_hits:

            score += min(
                len(phishing_hits) * 8,
                20,
            )

            signatures.append(
                "phishing_language"
            )

        # ====================================================
        # GENERIC GREETING
        # ====================================================

        generic_greeting = any(
            re.search(
                pattern,
                body,
                re.I | re.M,
            )
            for pattern in GENERIC_GREETING_PATTERNS
        )

        if generic_greeting:

            score += 5

            signatures.append(
                "generic_greeting"
            )

        # ====================================================
        # URL ANALYSIS
        # ====================================================

        links = extract_urls(
            content
        )

        analyzed_urls = [
            analyze_url(url)
            for url in links
        ]

        shortened_urls = [
            item
            for item in analyzed_urls
            if item["shortened"]
        ]

        suspicious_structure_urls = [
            item
            for item in analyzed_urls
            if item["suspicious_structure"]
        ]

        if len(links) >= 4:

            score += 8

            signatures.append(
                "high_link_density"
            )

        if shortened_urls:

            score += min(
                len(shortened_urls) * 8,
                16,
            )

            signatures.append(
                "shortened_url"
            )

        if suspicious_structure_urls:

            score += min(
                len(suspicious_structure_urls) * 10,
                20,
            )

            signatures.append(
                "suspicious_url_structure"
            )

        # ====================================================
        # ATTACHMENTS
        # ====================================================

        attachment_matches = re.findall(
            r"(?:filename|name)\s*=\s*[\"']?([^\"'\s;>]+)",
            content,
            re.I,
        )

        suspicious_attachments = []

        for filename in attachment_matches:

            filename_lower = filename.lower()

            if any(
                filename_lower.endswith(ext)
                for ext in SUSPICIOUS_ATTACHMENT_EXTENSIONS
            ):
                suspicious_attachments.append(
                    filename
                )

        if suspicious_attachments:

            score += 20

            signatures.append(
                "suspicious_attachment"
            )

        # ====================================================
        # LIMIT SCORE
        # ====================================================

        score = min(
            round(score, 2),
            100,
        )

        # ====================================================
        # BASE CONFIDENCE
        # ====================================================

        signal_count = len(
            signatures
        )

        if (
            spf_pass
            or dkim_pass
            or dmarc_pass
        ):
            confidence = 0.75

        elif headers_present:
            confidence = 0.65

        else:
            confidence = 0.50

        # More independent signals = higher confidence
        if signal_count >= 5:

            confidence += 0.15

        elif signal_count >= 3:

            confidence += 0.10

        confidence = min(
            confidence,
            0.95,
        )

        # ====================================================
        # GEMINI SECONDARY ANALYSIS
        # ====================================================

        ai_reasoning = None
        ai_boost = 0.0

        # Ask AI when there is meaningful content.
        # Do not let Gemini completely control the score.
        if (
            len(body.strip()) >= 30
            and (
                score >= 20
                or links
                or credential_hits
                or otp_hits
                or payment_hits
            )
        ):

            result = await gemini_service.generate_structured(
                task_prompt=(
                    "Analyze this email for phishing, "
                    "credential theft, OTP theft, financial fraud, "
                    "sender spoofing and social engineering. "
                    "Use only evidence present in the email. "
                    "Do not assume that an email is malicious only "
                    "because it contains urgency or links. "
                    "Return a conservative risk boost."
                ),
                untrusted_content=content,
                response_schema_hint="""
{
    "risk_boost_0_to_20": number,
    "reasoning": string
}
""",
            )

            if not result.get(
                "_fallback"
            ):

                try:

                    ai_boost = float(
                        result.get(
                            "risk_boost_0_to_20",
                            0,
                        )
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    ai_boost = 0.0

                ai_boost = min(
                    max(
                        ai_boost,
                        0,
                    ),
                    20,
                )

                score = min(
                    round(
                        score + ai_boost,
                        2,
                    ),
                    100,
                )

                ai_reasoning = (
                    result.get(
                        "reasoning"
                    )
                )

                confidence = max(
                    confidence,
                    0.80,
                )

        # ====================================================
        # EVIDENCE
        # ====================================================

        evidence.update(
            {
                "from": from_header,
                "from_domain": from_domain,
                "reply_to": reply_to,
                "reply_to_domain": reply_domain,
                "return_path": return_path,
                "return_path_domain": return_path_domain,
                "display_name": display_name,
                "subject": subject,
                "headers_present": headers_present,

                "authentication": {
                    "spf": (
                        "fail"
                        if spf_fail
                        else "pass"
                        if spf_pass
                        else "not_found"
                    ),
                    "dkim": (
                        "fail"
                        if dkim_fail
                        else "pass"
                        if dkim_pass
                        else "not_found"
                    ),
                    "dmarc": (
                        "fail"
                        if dmarc_fail
                        else "pass"
                        if dmarc_pass
                        else "not_found"
                    ),
                },

                "embedded_links": links,
                "analyzed_urls": analyzed_urls,
                "shortened_urls": shortened_urls,
                "suspicious_url_structure": (
                    suspicious_structure_urls
                ),

                "urgency_phrases_found": (
                    urgency_hits
                ),
                "credential_indicators": (
                    credential_hits
                ),
                "otp_indicators": otp_hits,
                "payment_indicators": (
                    payment_hits
                ),
                "phishing_indicators": (
                    phishing_hits
                ),

                "suspicious_attachments": (
                    suspicious_attachments
                ),

                "ai_boost": ai_boost,
                "ai_reasoning": ai_reasoning,

                "signal_count": signal_count,
            }
        )

        # Remove duplicate signatures
        signatures = list(
            dict.fromkeys(signatures)
        )

        # ====================================================
        # FINAL RESULT
        # ====================================================

        return AgentFinding(
            agent_name=self.name,
            raw_score=score,
            confidence=confidence,
            evidence=evidence,
            matched_signatures=signatures,
        )