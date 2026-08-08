"""
Phone Reputation Agent ("Phone Shield")

Combines threat-intel/community-report density with structural heuristics
(premium-rate prefixes, spoof-prone patterns) to score a phone number.
"""
import re
from typing import Any

from app.agents.base import AgentFinding, BaseAgent
from app.services.threat_intel_service import threat_intel_service

# Illustrative premium-rate / high-risk prefixes (extend per region in production)
PREMIUM_RATE_PREFIXES = ["+1900", "+44909", "+2348", "+234"]


class PhoneReputationAgent(BaseAgent):
    name = "phone_reputation_agent"

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:
        raw = context.get("text_value", "").strip()
        if not raw:
            return AgentFinding(self.name, 0, 0, {"reason": "no_phone_provided"})

        normalized = re.sub(r"[^\d+]", "", raw)
        score = 0.0
        signatures: list[str] = []

        if not normalized.startswith("+"):
            score += 5
            signatures.append("missing_country_code")

        for prefix in PREMIUM_RATE_PREFIXES:
            if normalized.startswith(prefix):
                score += 30
                signatures.append(f"premium_rate_prefix_{prefix}")
                break

        ioc_hit = await threat_intel_service.lookup("phone", normalized)
        if ioc_hit:
            # Confirmed community/threat-intel spam number → strong signal
            base = {"low": 40, "medium": 65, "high": 90}.get(ioc_hit.get("severity", "medium"), 60)
            score = max(score, base)
            signatures.append(f"reported_spam_number:{ioc_hit['source']}")

        # Sequential/repeating digit patterns often indicate burner/spoofed numbers
        digits = re.sub(r"\D", "", normalized)
        if re.search(r"(\d)\1{4,}", digits) or digits in ("1234567890",):
            score += 15
            signatures.append("suspicious_digit_pattern")

        score = min(score, 100)
        confidence = 0.85 if ioc_hit else 0.5

        evidence = {
            "normalized_number": normalized,
            "threat_intel_match": ioc_hit,
        }
        return AgentFinding(self.name, score, confidence, evidence, signatures)
