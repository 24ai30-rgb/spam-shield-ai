"""
Risk Aggregator Agent

Implements the weighted risk-fusion formula from the architecture doc
(Section 17):

    RiskScore = clamp(0,100,
        Σ (AgentScore_i * AgentWeight_i * AgentConfidence_i)
        + ThreatIntelBoost
        + CommunityCorroborationBoost
        - TrustSignalDiscount
    )

This agent does NOT call any external service — it purely fuses the
AgentFinding objects already produced by the specialist agents that ran
for this scan, plus optional threat-intel/community context passed in.
"""
from dataclasses import dataclass
from typing import Any

from app.agents.base import AgentFinding

# Per-category weights — tunable via admin console in production, versioned
# here as the v1 baseline (see architecture doc Section 17.3 on calibration).
AGENT_WEIGHTS: dict[str, float] = {
    "url_analysis_agent": 1.0,
    "email_analysis_agent": 1.0,
    "phone_reputation_agent": 0.9,
    "message_analysis_agent": 1.0,
    "ocr_agent": 0.85,
    "qr_agent": 0.9,
    "job_scam_agent": 1.0,
    "banking_fraud_agent": 1.15,  # banking fraud weighted higher — high real-world harm
    "shopping_scam_agent": 0.8,
    "investment_fraud_agent": 1.1,
}

VERDICT_BANDS = [
    (0, 25, "safe"),
    (25, 55, "suspicious"),
    (55, 80, "high_risk"),
    (80, 101, "confirmed_scam"),
]


@dataclass
class AggregatedRisk:
    risk_score: float
    verdict_label: str
    contributing_agents: list[dict[str, Any]]
    threat_intel_boost: float
    community_boost: float
    trust_discount: float


class RiskAggregatorAgent:
    name = "risk_aggregator_agent"

    def aggregate(
        self,
        findings: list[AgentFinding],
        threat_intel_override: bool = False,
        community_corroboration_count: int = 0,
        trust_signals: dict[str, bool] | None = None,
    ) -> AggregatedRisk:
        trust_signals = trust_signals or {}

        weighted_sum = 0.0
        weight_total = 0.0
        contributing = []
        for f in findings:
            weight = AGENT_WEIGHTS.get(f.agent_name, 1.0)
            contribution = f.raw_score * weight * f.confidence
            weighted_sum += contribution
            weight_total += weight * f.confidence
            contributing.append(
                {
                    "agent": f.agent_name,
                    "raw_score": f.raw_score,
                    "confidence": f.confidence,
                    "weight": weight,
                    "contribution": round(contribution, 2),
                    "matched_signatures": f.matched_signatures,
                }
            )

        base_score = (weighted_sum / weight_total) if weight_total > 0 else 0.0

        threat_intel_boost = 0.0
        if threat_intel_override:
            threat_intel_boost = max(0.0, 85 - base_score)  # hard floor at 85

        community_boost = min(community_corroboration_count * 5, 20)

        trust_discount = 0.0
        if trust_signals.get("valid_ssl") and trust_signals.get("aged_domain"):
            trust_discount += 10
        if trust_signals.get("verified_sender"):
            trust_discount += 10

        final_score = base_score + threat_intel_boost + community_boost - trust_discount
        final_score = max(0.0, min(100.0, final_score))

        verdict = next(
            label for lo, hi, label in VERDICT_BANDS if lo <= final_score < hi
        )

        return AggregatedRisk(
            risk_score=round(final_score, 1),
            verdict_label=verdict,
            contributing_agents=contributing,
            threat_intel_boost=threat_intel_boost,
            community_boost=community_boost,
            trust_discount=trust_discount,
        )


risk_aggregator_agent = RiskAggregatorAgent()
