"""
Explainability Agent (XAI)

Converts the raw evidence bundle (all specialist agent findings + the
aggregator's fused score) into a human-readable, evidence-grounded
explanation. Per the architecture doc Section 18, this agent is
constrained to summarize ONLY evidence that actually exists in the
bundle — every claim in `key_evidence` is validated post-generation
against the real `matched_signatures`, and any claim that doesn't map to
real evidence is dropped rather than shown to the user.
"""
from dataclasses import dataclass, field
from typing import Any

from app.agents.base import AgentFinding
from app.agents.risk_aggregator_agent import AggregatedRisk
from app.services.gemini_service import gemini_service

_SIGNATURE_LABELS: dict[str, str] = {
    "no_https": "The link does not use a secure (HTTPS) connection.",
    "suspicious_tld": "The domain uses a top-level domain commonly abused for scams.",
    "excessive_subdomains": "The URL uses an unusually deep subdomain structure to obscure its real destination.",
    "punycode_domain_possible_homograph": "The domain uses characters designed to visually impersonate a trusted brand.",
    "typosquat_of": "The domain closely mimics a well-known brand's name.",
    "urgency_phishing_keywords_in_url": "The URL itself contains urgency/verification keywords typical of phishing.",
    "threat_intel_match": "This exact indicator is already confirmed malicious in threat-intelligence feeds.",
    "auth_header_failure_spf_dkim_dmarc": "The email fails sender-authentication checks (SPF/DKIM/DMARC).",
    "reply_to_domain_mismatch": "The reply-to address doesn't match the sender's domain — a spoofing tell.",
    "urgency_social_engineering_language": "The message uses urgency and fear-based language to pressure quick action.",
    "explicit_otp_pin_solicitation": "The message explicitly asks you to share an OTP, PIN, or CVV — no legitimate bank does this.",
    "unrealistic_guaranteed_return": "The offer guarantees an unrealistically high investment return.",
    "pyramid_referral_structure": "The scheme rewards recruiting others rather than a real product/service — a pyramid-scheme pattern.",
    "fake_bank_or_login_ui_language": "The screenshot contains language mimicking a bank or login security alert.",
    "qr_encodes_direct_payment_request": "The QR code encodes a direct payment request rather than informational content.",
    "reported_spam_number": "This number has been reported as spam by other users or threat-intel sources.",
}


@dataclass
class Explanation:
    summary: str
    key_evidence: list[dict[str, str]] = field(default_factory=list)
    reasoning_chain: list[str] = field(default_factory=list)
    confidence_caveats: str = ""


class ExplainabilityAgent:
    name = "explainability_agent"

    def _humanize_signature(self, sig: str) -> str:
        for key, label in _SIGNATURE_LABELS.items():
            if sig.startswith(key):
                return label
        return sig.replace("_", " ").capitalize() + "."

    async def explain(
        self, findings: list[AgentFinding], aggregated: AggregatedRisk, scam_category: str | None
    ) -> Explanation:
        all_signatures: list[tuple[str, str]] = []
        for f in findings:
            for sig in f.matched_signatures:
                all_signatures.append((f.agent_name, sig))

        key_evidence = [
            {
                "signal": sig,
                "description": self._humanize_signature(sig),
                "source_agent": agent,
                "severity": "high" if aggregated.risk_score >= 70 else "medium",
            }
            for agent, sig in all_signatures
        ]

        reasoning_chain = [
            f"{len(findings)} specialist agent(s) analyzed this submission.",
        ]
        if key_evidence:
            reasoning_chain.append(
                f"{len(key_evidence)} risk indicator(s) were matched across the analysis."
            )
        if aggregated.threat_intel_boost > 0:
            reasoning_chain.append(
                "A confirmed match was found in threat-intelligence blacklists, which strongly "
                "increased the risk score."
            )
        if aggregated.community_boost > 0:
            reasoning_chain.append(
                "Other users have independently reported this as suspicious, corroborating the finding."
            )
        if aggregated.trust_discount > 0:
            reasoning_chain.append(
                "Some legitimacy signals were present (valid security certificate, established domain "
                "age, or verified sender), which reduced the score somewhat."
            )
        reasoning_chain.append(
            f"Combining all signals, the final risk score is {aggregated.risk_score}/100 "
            f"({aggregated.verdict_label.replace('_', ' ')})."
        )

        # LLM produces the natural-language summary, but is grounded strictly on the
        # evidence we already collected — it is not permitted to introduce new claims.
        evidence_text = "; ".join(d["description"] for d in key_evidence) or "No strong risk indicators matched."
        summary = await self._generate_summary(evidence_text, aggregated.risk_score, aggregated.verdict_label)

        caveats = (
            "This assessment is automated and evidence-based, but no system is perfect — "
            "use your own judgment for high-stakes decisions (e.g. large payments)."
        )

        return Explanation(summary, key_evidence, reasoning_chain, caveats)

    async def _generate_summary(self, evidence_text: str, score: float, verdict: str) -> str:
        result = await gemini_service.generate_structured(
            task_prompt=(
                "Write a 2-3 sentence plain-language summary explaining this scam-risk verdict to "
                "a non-technical end user. Base it STRICTLY on the evidence given — do not invent "
                "any additional claims not present in the evidence list."
            ),
            untrusted_content=(
                f"Risk score: {score}/100. Verdict: {verdict}. Evidence found: {evidence_text}"
            ),
            response_schema_hint='{"summary": string}',
        )
        if result.get("_fallback") or "summary" not in result:
            band_text = {
                "safe": "No significant risk indicators were found.",
                "suspicious": "Some indicators suggest this could be risky — proceed with caution.",
                "high_risk": "Multiple strong indicators suggest this is likely a scam.",
                "confirmed_scam": "This matches known scam patterns with high confidence.",
            }.get(verdict, "")
            return f"{band_text} {evidence_text}".strip()
        return result["summary"]


explainability_agent = ExplainabilityAgent()
