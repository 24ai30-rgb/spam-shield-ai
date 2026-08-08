"""
Recommendation Agent

Translates the verdict + matched signal categories into concrete,
actionable next steps for the end user. Kept deterministic (no LLM call)
because recommended actions are safety-critical and must be predictable,
consistent, and reviewable — not subject to generation variance.
"""
from app.agents.risk_aggregator_agent import AggregatedRisk

_BASE_ACTIONS = {
    "safe": [
        "No action needed — this appears safe based on current signals.",
        "Stay cautious of unsolicited requests for personal or financial information regardless.",
    ],
    "suspicious": [
        "Do not click links or share personal/financial information until you verify independently.",
        "Contact the organization directly using a phone number or website you already trust — not one from this message.",
        "Report this to Spam Shield's community feed to help warn others.",
    ],
    "high_risk": [
        "Do not click any links, download attachments, or respond.",
        "Do not share OTPs, PINs, passwords, or payment details.",
        "Block the sender/number and report it to your email or phone provider.",
        "If you already shared sensitive information, contact your bank immediately.",
    ],
    "confirmed_scam": [
        "This matches a confirmed scam pattern — do not engage in any way.",
        "Block and report the sender immediately.",
        "If you already made a payment or shared credentials, contact your bank/card issuer now and consider a password reset.",
        "File a report with your local cybercrime authority if financial loss occurred.",
    ],
}

_CATEGORY_ADDENDA = {
    "banking_fraud_agent": "Call your bank using the number on the back of your card — never a number from the message.",
    "investment_fraud_agent": "Verify any investment platform's registration with your national financial regulator before investing.",
    "job_scam_agent": "Legitimate employers never ask candidates to pay registration or equipment fees upfront.",
    "shopping_scam_agent": "Prefer payment methods with buyer protection (credit card) over direct bank transfer for unfamiliar stores.",
}


class RecommendationAgent:
    name = "recommendation_agent"

    def recommend(self, aggregated: AggregatedRisk) -> list[str]:
        actions = list(_BASE_ACTIONS.get(aggregated.verdict_label, []))

        contributing_agent_names = {c["agent"] for c in aggregated.contributing_agents if c["raw_score"] >= 30}
        for agent_name, addendum in _CATEGORY_ADDENDA.items():
            if agent_name in contributing_agent_names:
                actions.append(addendum)

        return actions


recommendation_agent = RecommendationAgent()
