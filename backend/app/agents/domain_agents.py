"""
Domain-specific scam agents: Job Shield, Banking Shield, Shopping Shield,
Investment Shield.

Grouped in one module since each follows the same Tier-0-regex +
Tier-2-Gemini-escalation shape as the other agents, just with different
signal sets. Kept as separate classes (not one parametrized agent) so
each can evolve independent scoring logic without cross-impact — matches
the "specialist agent per category" principle from the architecture doc.
"""
import re
from typing import Any

from app.agents.base import AgentFinding, BaseAgent
from app.services.gemini_service import gemini_service


class JobScamAgent(BaseAgent):
    name = "job_scam_agent"

    PATTERNS = [
        (r"no experience.{0,20}(required|needed)", 10),
        (r"(pay|send).{0,15}(registration|processing|training) fee", 35),
        (r"work from home.{0,20}\$\d{3,}.{0,10}(day|week)", 20),
        (r"whatsapp (only|interview)", 15),
        (r"immediate (hiring|start).{0,20}no interview", 20),
        (r"deposit.{0,15}(equipment|starter kit)", 30),
    ]

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:
        text = context.get("text_value", "") or ""
        if not text:
            return AgentFinding(self.name, 0, 0, {"reason": "no_job_text_provided"})

        score, signatures = 0.0, []
        for pattern, weight in self.PATTERNS:
            if re.search(pattern, text, re.I):
                score += weight
                signatures.append(pattern.split(".")[0])

        # Legitimate-sounding but unverifiable company name + generic email domain combo
        if re.search(r"@(gmail|yahoo|outlook|hotmail)\.com", text, re.I) and re.search(
            r"(inc\.|corp|company|ltd)", text, re.I
        ):
            score += 15
            signatures.append("corporate_claim_with_free_email_domain")

        score = min(score, 100)
        ai_reasoning = None
        if 25 <= score <= 70:
            result = await gemini_service.generate_structured(
                "Analyze this job posting/offer for advance-fee fraud or fake-recruiter scam signals.",
                text,
                '{"risk_boost_0_to_25": number, "reasoning": string}',
            )
            if not result.get("_fallback"):
                score = min(score + min(max(result.get("risk_boost_0_to_25", 0), 0), 25), 100)
                ai_reasoning = result.get("reasoning")

        confidence = 0.75 if signatures else 0.5
        return AgentFinding(self.name, score, confidence, {"ai_reasoning": ai_reasoning}, signatures)


class BankingFraudAgent(BaseAgent):
    name = "banking_fraud_agent"

    PATTERNS = [
        (r"your (account|card) (has been|will be) (blocked|suspended)", 30),
        (r"share your (otp|pin|cvv)", 45),
        (r"click to (unblock|reactivate|verify) your account", 30),
        (r"kyc (update|verification) required.{0,20}(immediately|urgent)", 25),
        (r"unauthorized (transaction|debit) of", 20),
    ]

    # Illustrative — production deployment loads real sender-ID whitelist from DB
    LEGITIMATE_SENDER_HINTS = ["-BOFA", "-CHASE", "-WELLS", "VM-HDFCBK", "AD-ICICIB"]

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:
        text = context.get("text_value", "") or ""
        if not text:
            return AgentFinding(self.name, 0, 0, {"reason": "no_banking_text_provided"})

        score, signatures = 0.0, []
        for pattern, weight in self.PATTERNS:
            if re.search(pattern, text, re.I):
                score += weight
                signatures.append(pattern.split(".")[0])

        # Requesting OTP/PIN is the single strongest banking-fraud tell — no bank ever does this
        if re.search(r"(otp|pin|cvv).{0,10}(is|:)\s*\d{3,6}.{0,20}(share|send|provide)", text, re.I):
            score += 40
            signatures.append("explicit_otp_pin_solicitation")

        looks_like_sender_id = any(hint in text for hint in self.LEGITIMATE_SENDER_HINTS)
        if looks_like_sender_id and score > 0:
            # Spoofed-sender-ID pattern: legit-looking header + scam body
            score += 10
            signatures.append("legit_looking_sender_id_with_scam_body")

        score = min(score, 100)
        confidence = 0.85 if signatures else 0.5
        return AgentFinding(self.name, score, confidence, {}, signatures)


class ShoppingScamAgent(BaseAgent):
    name = "shopping_scam_agent"

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:
        text = context.get("text_value", "") or ""
        if not text:
            return AgentFinding(self.name, 0, 0, {"reason": "no_shopping_input_provided"})

        score, signatures = 0.0, []

        if re.search(r"\b(70|80|90)%\s?off\b", text, re.I):
            score += 20
            signatures.append("extreme_discount_claim")

        if re.search(r"(pay only via|no returns|no refunds|cash.?on.?delivery not available)", text, re.I):
            score += 25
            signatures.append("restrictive_no_recourse_payment_terms")

        if not re.search(r"(privacy policy|terms of service|return policy|contact us)", text, re.I):
            score += 15
            signatures.append("missing_legal_pages")

        if re.search(r"(stock ending|only \d+ left|offer ends in \d+ (minutes|hours))", text, re.I):
            score += 10
            signatures.append("artificial_urgency_scarcity")

        score = min(score, 100)
        confidence = 0.65 if signatures else 0.4
        return AgentFinding(self.name, score, confidence, {}, signatures)


class InvestmentFraudAgent(BaseAgent):
    name = "investment_fraud_agent"

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:
        text = context.get("text_value", "") or ""
        if not text:
            return AgentFinding(self.name, 0, 0, {"reason": "no_investment_text_provided"})

        score, signatures = 0.0, []

        roi_match = re.search(r"(guaranteed|assured).{0,15}(\d{2,4})%\s?(return|profit|roi)", text, re.I)
        if roi_match:
            pct = int(roi_match.group(2))
            score += 50 if pct >= 50 else 30
            signatures.append(f"unrealistic_guaranteed_return_{pct}pct")

        if re.search(r"(risk.?free|zero risk|100% safe).{0,20}(investment|return)", text, re.I):
            score += 25
            signatures.append("risk_free_claim")

        if re.search(r"refer (a friend|and earn)|recruit.{0,15}(bonus|commission)", text, re.I):
            score += 30
            signatures.append("pyramid_referral_structure")

        if re.search(r"(sebi|sec|fca|asic).{0,20}registered", text, re.I) is None and re.search(
            r"(investment|fund|trading) (scheme|platform|opportunity)", text, re.I
        ):
            score += 10
            signatures.append("no_regulator_registration_claim_found")

        score = min(score, 100)
        ai_reasoning = None
        if 30 <= score <= 75:
            result = await gemini_service.generate_structured(
                "Analyze this investment offer for Ponzi/pyramid-scheme linguistic markers and "
                "unrealistic-return claims.",
                text,
                '{"risk_boost_0_to_25": number, "reasoning": string}',
            )
            if not result.get("_fallback"):
                score = min(score + min(max(result.get("risk_boost_0_to_25", 0), 0), 25), 100)
                ai_reasoning = result.get("reasoning")

        confidence = 0.8 if signatures else 0.5
        return AgentFinding(self.name, score, confidence, {"ai_reasoning": ai_reasoning}, signatures)
