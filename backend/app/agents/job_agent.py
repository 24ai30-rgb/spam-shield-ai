"""
Job Scam Detection Agent

Analyzes job offers for:
- Fake recruitment
- Unrealistic salary
- Upfront fees
- OTP / PIN / banking requests
- Personal document requests
- Fake company / recruiter indicators
- WhatsApp / Telegram recruitment
- Urgency and social engineering
- Suspicious URLs
- Suspicious attachments
- Work-from-home / task / recharge scams
- Money mule recruitment
- Investment-linked jobs
- AI-assisted secondary analysis
"""

import re
from typing import Any
from urllib.parse import urlparse

from app.agents.base import AgentFinding, BaseAgent
from app.services.gemini_service import gemini_service


# ============================================================
# SIGNAL DATABASE
# ============================================================

PAYMENT_PATTERNS = {
    "registration_fee": [
        r"registration\s+fee",
        r"register.*fee",
        r"registration.*payment",
    ],
    "application_fee": [
        r"application\s+fee",
        r"apply.*fee",
    ],
    "training_fee": [
        r"training\s+fee",
        r"pay.*training",
    ],
    "security_deposit": [
        r"security\s+deposit",
        r"refundable\s+deposit",
        r"deposit.*job",
    ],
    "processing_fee": [
        r"processing\s+fee",
        r"processing.*payment",
    ],
    "interview_fee": [
        r"interview\s+fee",
        r"pay.*interview",
    ],
    "joining_fee": [
        r"joining\s+fee",
        r"joining.*payment",
    ],
}

CREDENTIAL_PATTERNS = {
    "otp_request": [
        r"\botp\b",
        r"one[- ]time\s+password",
        r"verification\s+code",
        r"security\s+code",
    ],
    "upi_pin_request": [
        r"upi\s+pin",
        r"upi.*pin",
    ],
    "password_request": [
        r"send.*password",
        r"share.*password",
        r"login.*password",
    ],
    "cvv_request": [
        r"\bcvv\b",
        r"card.*cvv",
    ],
    "card_request": [
        r"card\s+number",
        r"debit\s+card",
        r"credit\s+card",
    ],
    "bank_request": [
        r"bank\s+account",
        r"account\s+number",
        r"bank\s+details",
    ],
}

DOCUMENT_PATTERNS = {
    "aadhaar_request": [
        r"\baadhaar\b",
        r"aadhar",
    ],
    "pan_request": [
        r"\bpan\s+card\b",
        r"\bpan\s+number\b",
    ],
    "passport_request": [
        r"\bpassport\b",
    ],
    "selfie_request": [
        r"send.*selfie",
        r"selfie.*verification",
        r"photo.*verification",
    ],
}

URGENCY_PATTERNS = [
    r"\burgent\b",
    r"\bimmediately\b",
    r"\bact\s+now\b",
    r"\bapply\s+now\b",
    r"\blimited\s+slots?\b",
    r"\blimited\s+seats?\b",
    r"\boffer\s+expires?\b",
    r"\bwithin\s+\d+\s+(minutes?|hours?)\b",
    r"\blast\s+chance\b",
    r"\btoday\s+only\b",
    r"\bjoin\s+immediately\b",
]

GUARANTEED_PATTERNS = [
    r"guaranteed\s+(job|income|salary|selection)",
    r"100%\s+(job|selection)",
    r"guaranteed\s+selection",
    r"no\s+interview",
    r"no\s+experience\s+required",
    r"easy\s+money",
    r"earn\s+\₹?\s*[\d,]+\s*(per|a)\s*(day|week|month)",
]

SOCIAL_ENGINEERING_PATTERNS = [
    r"do\s+not\s+tell\s+anyone",
    r"keep\s+this\s+confidential",
    r"secret\s+job",
    r"only\s+selected\s+people",
    r"you\s+have\s+been\s+selected",
    r"congratulations.*selected",
    r"hr\s+manager",
    r"senior\s+hr",
]

WORK_FROM_HOME_PATTERNS = [
    r"work\s+from\s+home",
    r"work\s+from\s+anywhere",
    r"part[- ]time\s+work",
    r"online\s+job",
    r"data\s+entry",
    r"captcha\s+typing",
    r"form\s+filling",
    r"typing\s+job",
]

TASK_SCAM_PATTERNS = [
    r"recharge",
    r"complete\s+tasks?",
    r"unlock\s+tasks?",
    r"deposit.*withdraw",
    r"withdraw.*deposit",
    r"commission.*task",
    r"prepaid\s+task",
]

MONEY_MULE_PATTERNS = [
    r"receive\s+money.*transfer",
    r"transfer\s+money.*account",
    r"use\s+your\s+bank\s+account",
    r"receive.*payment.*on\s+behalf",
    r"money\s+transfer\s+job",
]

INVESTMENT_JOB_PATTERNS = [
    r"investment.*job",
    r"invest.*earn.*salary",
    r"crypto.*job",
    r"trading.*job",
    r"investment.*commission",
]

LINK_PATTERN = re.compile(
    r"https?://[^\s<>\]\)\"']+",
    re.I,
)

EMAIL_PATTERN = re.compile(
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    re.I,
)

SUSPICIOUS_URL_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "rb.gy",
    "cutt.ly",
    "is.gd",
    "ow.ly",
}

SUSPICIOUS_EXTENSIONS = {
    ".exe",
    ".scr",
    ".bat",
    ".cmd",
    ".js",
    ".vbs",
    ".ps1",
    ".msi",
    ".jar",
    ".hta",
}


# ============================================================
# HELPERS
# ============================================================

def find_matches(
    text: str,
    patterns: list[str],
) -> list[str]:

    return [
        pattern
        for pattern in patterns
        if re.search(pattern, text, re.I)
    ]


def find_group_matches(
    text: str,
    groups: dict[str, list[str]],
) -> dict[str, list[str]]:

    result: dict[str, list[str]] = {}

    for name, patterns in groups.items():

        matches = find_matches(
            text,
            patterns,
        )

        if matches:
            result[name] = matches

    return result


def extract_urls(
    text: str,
) -> list[str]:

    return list(
        dict.fromkeys(
            LINK_PATTERN.findall(text)
        )
    )[:20]


def analyze_url(
    url: str,
) -> dict[str, Any]:

    try:

        parsed = urlparse(url)

        domain = (
            parsed.hostname or ""
        ).lower()

        suspicious = False
        reasons = []

        if domain in SUSPICIOUS_URL_DOMAINS:

            suspicious = True
            reasons.append(
                "shortened_url"
            )

        if "xn--" in domain:

            suspicious = True
            reasons.append(
                "punycode_domain"
            )

        if re.fullmatch(
            r"\d{1,3}(?:\.\d{1,3}){3}",
            domain,
        ):

            suspicious = True
            reasons.append(
                "ip_address_url"
            )

        if domain.count(".") >= 4:

            suspicious = True
            reasons.append(
                "multiple_subdomains"
            )

        return {
            "url": url,
            "domain": domain,
            "https": parsed.scheme.lower() == "https",
            "suspicious": suspicious,
            "reasons": reasons,
        }

    except Exception:

        return {
            "url": url,
            "domain": None,
            "https": False,
            "suspicious": True,
            "reasons": [
                "invalid_url"
            ],
        }


def extract_emails(
    text: str,
) -> list[str]:

    return list(
        dict.fromkeys(
            EMAIL_PATTERN.findall(text)
        )
    )[:20]


# ============================================================
# JOB AGENT
# ============================================================

class JobScamAgent(BaseAgent):

    name = "job_scam_agent"

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
                    "reason": "no_job_content",
                },
                matched_signatures=[],
            )

        text = content.strip()

        score = 0.0
        signatures: list[str] = []

        # ====================================================
        # PAYMENT
        # ====================================================

        payment_signals = find_group_matches(
            text,
            PAYMENT_PATTERNS,
        )

        payment_count = len(
            payment_signals
        )

        if payment_count:

            score += min(
                payment_count * 18,
                45,
            )

            signatures.extend(
                f"payment:{key}"
                for key in payment_signals
            )

        # ====================================================
        # CREDENTIALS
        # ====================================================

        credential_signals = find_group_matches(
            text,
            CREDENTIAL_PATTERNS,
        )

        credential_count = len(
            credential_signals
        )

        if credential_count:

            score += min(
                credential_count * 20,
                50,
            )

            signatures.extend(
                f"credential:{key}"
                for key in credential_signals
            )

        # ====================================================
        # PERSONAL DOCUMENTS
        # ====================================================

        document_signals = find_group_matches(
            text,
            DOCUMENT_PATTERNS,
        )

        document_count = len(
            document_signals
        )

        if document_count:

            score += min(
                document_count * 10,
                25,
            )

            signatures.extend(
                f"document:{key}"
                for key in document_signals
            )

        # ====================================================
        # URGENCY
        # ====================================================

        urgency_hits = find_matches(
            text,
            URGENCY_PATTERNS,
        )

        if urgency_hits:

            score += min(
                len(urgency_hits) * 6,
                18,
            )

            signatures.append(
                "urgent_recruitment_language"
            )

        # ====================================================
        # GUARANTEED JOB
        # ====================================================

        guaranteed_hits = find_matches(
            text,
            GUARANTEED_PATTERNS,
        )

        if guaranteed_hits:

            score += min(
                len(guaranteed_hits) * 10,
                25,
            )

            signatures.append(
                "unrealistic_job_promise"
            )

        # ====================================================
        # SOCIAL ENGINEERING
        # ====================================================

        social_hits = find_matches(
            text,
            SOCIAL_ENGINEERING_PATTERNS,
        )

        if social_hits:

            score += min(
                len(social_hits) * 7,
                20,
            )

            signatures.append(
                "recruitment_social_engineering"
            )

        # ====================================================
        # WORK FROM HOME
        # ====================================================

        wfh_hits = find_matches(
            text,
            WORK_FROM_HOME_PATTERNS,
        )

        if wfh_hits:

            # WFH itself is NOT a scam.
            # It only becomes risky when combined
            # with other indicators.
            signatures.append(
                "work_from_home_context"
            )

        # ====================================================
        # TASK / RECHARGE
        # ====================================================

        task_hits = find_matches(
            text,
            TASK_SCAM_PATTERNS,
        )

        if task_hits:

            score += min(
                len(task_hits) * 15,
                40,
            )

            signatures.append(
                "task_recharge_scam_pattern"
            )

        # ====================================================
        # MONEY MULE
        # ====================================================

        mule_hits = find_matches(
            text,
            MONEY_MULE_PATTERNS,
        )

        if mule_hits:

            score += min(
                len(mule_hits) * 20,
                40,
            )

            signatures.append(
                "money_mule_recruitment"
            )

        # ====================================================
        # INVESTMENT JOB
        # ====================================================

        investment_hits = find_matches(
            text,
            INVESTMENT_JOB_PATTERNS,
        )

        if investment_hits:

            score += min(
                len(investment_hits) * 12,
                30,
            )

            signatures.append(
                "investment_linked_job"
            )

        # ====================================================
        # SALARY ANALYSIS
        # ====================================================

        salary_matches = re.findall(
            r"(?:₹|rs\.?|inr)\s*[\d,]+",
            text,
            re.I,
        )

        numeric_salaries = []

        for value in salary_matches:

            digits = re.sub(
                r"[^\d]",
                "",
                value,
            )

            if digits:

                numeric_salaries.append(
                    int(digits)
                )

        unrealistic_salary = False

        for salary in numeric_salaries:

            if salary >= 100000:

                unrealistic_salary = True

            elif salary >= 50000:

                unrealistic_salary = True

        if unrealistic_salary:

            score += 15

            signatures.append(
                "potentially_unrealistic_salary"
            )

        # ====================================================
        # CONTACT METHODS
        # ====================================================

        whatsapp_only = bool(
            re.search(
                r"whatsapp.*only|only.*whatsapp",
                text,
                re.I,
            )
        )

        telegram_only = bool(
            re.search(
                r"telegram.*only|only.*telegram",
                text,
                re.I,
            )
        )

        if whatsapp_only:

            score += 8

            signatures.append(
                "whatsapp_only_recruitment"
            )

        if telegram_only:

            score += 8

            signatures.append(
                "telegram_only_recruitment"
            )

        # ====================================================
        # EMAIL ANALYSIS
        # ====================================================

        emails = extract_emails(
            text
        )

        free_email_addresses = []

        for email in emails:

            domain = email.split("@")[-1].lower()

            if domain in {
                "gmail.com",
                "yahoo.com",
                "hotmail.com",
                "outlook.com",
                "proton.me",
                "protonmail.com",
            }:

                free_email_addresses.append(
                    email
                )

        if free_email_addresses:

            # Free email is NOT automatically scam.
            # Give only a small signal.
            score += 4

            signatures.append(
                "free_email_recruiter_address"
            )

        # ====================================================
        # URL ANALYSIS
        # ====================================================

        urls = extract_urls(
            text
        )

        analyzed_urls = [
            analyze_url(url)
            for url in urls
        ]

        suspicious_urls = [
            item
            for item in analyzed_urls
            if item["suspicious"]
        ]

        if suspicious_urls:

            score += min(
                len(suspicious_urls) * 15,
                30,
            )

            signatures.append(
                "suspicious_application_url"
            )

        # ====================================================
        # ATTACHMENTS
        # ====================================================

        filenames = re.findall(
            r"(?:filename|attachment|file)\s*[:=]\s*[\"']?([^\s\"']+)",
            text,
            re.I,
        )

        suspicious_attachments = []

        for filename in filenames:

            lower = filename.lower()

            if any(
                lower.endswith(ext)
                for ext in SUSPICIOUS_EXTENSIONS
            ):

                suspicious_attachments.append(
                    filename
                )

        if suspicious_attachments:

            score += 20

            signatures.append(
                "suspicious_job_attachment"
            )

        # ====================================================
        # COMBINATION SIGNALS
        # ====================================================

        # Payment + urgency
        if (
            payment_count
            and urgency_hits
        ):

            score += 12

            signatures.append(
                "payment_plus_urgency"
            )

        # Payment + WFH
        if (
            payment_count
            and wfh_hits
        ):

            score += 12

            signatures.append(
                "work_from_home_payment_scam"
            )

        # OTP + payment
        if (
            "otp_request" in credential_signals
            and payment_count
        ):

            score += 15

            signatures.append(
                "otp_payment_combination"
            )

        # Fake selection + no interview
        if (
            social_hits
            and guaranteed_hits
        ):

            score += 10

            signatures.append(
                "fake_selection_pattern"
            )

        # ====================================================
        # FINAL SCORE BEFORE AI
        # ====================================================

        score = min(
            round(score, 2),
            100,
        )

        # ====================================================
        # CONFIDENCE
        # ====================================================

        independent_signal_count = len(
            set(signatures)
        )

        if independent_signal_count >= 8:

            confidence = 0.90

        elif independent_signal_count >= 5:

            confidence = 0.82

        elif independent_signal_count >= 3:

            confidence = 0.72

        elif independent_signal_count >= 1:

            confidence = 0.60

        else:

            confidence = 0.45

        # ====================================================
        # AI SECONDARY ANALYSIS
        # ====================================================

        ai_reasoning = None
        ai_boost = 0.0

        if len(text) >= 40:

            result = await gemini_service.generate_structured(
                task_prompt=(
                    "Analyze this job offer for employment fraud. "
                    "Look for fake recruitment, upfront payment, "
                    "credential theft, OTP requests, banking fraud, "
                    "unrealistic salary, impersonation, task/recharge "
                    "scams, money mule recruitment and social engineering. "
                    "Do not classify a job as a scam only because it is "
                    "work-from-home, uses WhatsApp, or has a high salary. "
                    "Only use evidence present in the supplied content."
                ),
                untrusted_content=text,
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

                    ai_boost = 0

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

                ai_reasoning = result.get(
                    "reasoning"
                )

                confidence = max(
                    confidence,
                    0.80,
                )

        # ====================================================
        # DEDUPLICATE SIGNATURES
        # ====================================================

        signatures = list(
            dict.fromkeys(
                signatures
            )
        )

        # ====================================================
        # EVIDENCE
        # ====================================================

        evidence = {

            "payment_signals":
                payment_signals,

            "credential_signals":
                credential_signals,

            "document_signals":
                document_signals,

            "urgency_phrases":
                urgency_hits,

            "unrealistic_job_promises":
                guaranteed_hits,

            "social_engineering":
                social_hits,

            "work_from_home_signals":
                wfh_hits,

            "task_scam_signals":
                task_hits,

            "money_mule_signals":
                mule_hits,

            "investment_job_signals":
                investment_hits,

            "salary_values":
                numeric_salaries,

            "unrealistic_salary":
                unrealistic_salary,

            "whatsapp_only":
                whatsapp_only,

            "telegram_only":
                telegram_only,

            "email_addresses":
                emails,

            "free_email_addresses":
                free_email_addresses,

            "embedded_urls":
                urls,

            "analyzed_urls":
                analyzed_urls,

            "suspicious_urls":
                suspicious_urls,

            "attachments":
                filenames,

            "suspicious_attachments":
                suspicious_attachments,

            "ai_boost":
                ai_boost,

            "ai_reasoning":
                ai_reasoning,

            "signal_count":
                independent_signal_count,
        }

        # ====================================================
        # RESULT
        # ====================================================

        return AgentFinding(
            agent_name=self.name,
            raw_score=score,
            confidence=confidence,
            evidence=evidence,
            matched_signatures=signatures,
        )