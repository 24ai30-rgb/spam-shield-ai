"""
Multi-Agent Orchestrator

Spam Shield AI currently supports:

1. URL / Website
2. Email
3. SMS / Text
4. Job Offer

Removed scan types:

- Phone Number
- WhatsApp
- QR Code
- Screenshot
- Document
- Banking
- Shopping
- Investment

The orchestrator:
    1. Receives the scan request
    2. Routes it to the correct specialist agent
    3. Runs the agent
    4. Sends findings to the Risk Aggregator
    5. Generates an explanation
    6. Generates recommended actions
    7. Returns one unified result
"""

import asyncio

from dataclasses import dataclass

from typing import Any


from app.agents.base import AgentFinding

from app.agents.email_agent import (
    EmailAnalysisAgent,
)

from app.agents.explainability_agent import (
    explainability_agent,
)

from app.agents.job_agent import (
    JobScamAgent,
)

from app.agents.message_agent import (
    MessageAnalysisAgent,
)

from app.agents.recommendation_agent import (
    recommendation_agent,
)

from app.agents.risk_aggregator_agent import (
    risk_aggregator_agent,
)

from app.agents.url_agent import (
    URLAnalysisAgent,
)

from app.core.logging import (
    get_logger,
)

from app.models.scan import (
    InputType,
)


# ============================================================
# LOGGER
# ============================================================

logger = get_logger(__name__)


# ============================================================
# AGENT INSTANCES
# ============================================================

_url_agent = URLAnalysisAgent()

_email_agent = EmailAnalysisAgent()

_message_agent = MessageAnalysisAgent()

_job_agent = JobScamAgent()


# ============================================================
# ROUTING TABLE
# ============================================================

ROUTING_TABLE: dict[InputType, list] = {

    InputType.URL: [
        _url_agent
    ],

    InputType.EMAIL: [
        _email_agent
    ],

    InputType.SMS: [
        _message_agent
    ],

    InputType.JOB: [
        _job_agent
    ],
}


# ============================================================
# CATEGORY LABELS
# ============================================================

CATEGORY_LABELS = {

    "url_analysis_agent":
        "Phishing Link",

    "email_analysis_agent":
        "Email Phishing",

    "message_analysis_agent":
        "SMS Scam",

    "job_scam_agent":
        "Employment Scam",
}


# ============================================================
# ORCHESTRATION RESULT
# ============================================================

@dataclass
class OrchestrationResult:

    findings: list[AgentFinding]

    risk_score: float

    verdict_label: str

    scam_category: str | None

    confidence_score: float

    explanation_summary: str

    key_evidence: list[dict]

    reasoning_chain: list[str]

    recommended_actions: list[str]

    model_versions_used: dict[str, str]


# ============================================================
# ORCHESTRATOR
# ============================================================

class Orchestrator:

    async def run_scan(
        self,
        input_type: InputType,
        context: dict[str, Any],
    ) -> OrchestrationResult:

        # ----------------------------------------------------
        # START LOG
        # ----------------------------------------------------

        print("\n" + "=" * 80)

        print(
            "SPAM SHIELD AI - ORCHESTRATOR"
        )

        print("=" * 80)

        print(
            "Input Type:",
            input_type.value,
        )

        print(
            "Context:",
            context,
        )

        print("=" * 80)


        # ----------------------------------------------------
        # GET SPECIALIST AGENT
        # ----------------------------------------------------

        agents = ROUTING_TABLE.get(
            input_type,
            [],
        )


        if not agents:

            raise ValueError(
                f"No agents registered for input type: "
                f"{input_type}"
            )


        logger.info(
            "orchestrator_dispatch",
            input_type=input_type.value,
            agent_count=len(agents),
        )


        # ----------------------------------------------------
        # RUN AGENTS
        # ----------------------------------------------------

        findings: list[AgentFinding] = (
            await asyncio.gather(
                *(
                    agent.run(context)
                    for agent in agents
                )
            )
        )


        # ----------------------------------------------------
        # PRINT AGENT FINDINGS
        # ----------------------------------------------------

        print("\n")

        print("=" * 80)

        print(
            "AGENT FINDINGS"
        )

        print("=" * 80)


        for finding in findings:

            print(
                "\nAgent:",
                finding.agent_name,
            )

            print(
                "Raw Score:",
                finding.raw_score,
            )

            print(
                "Confidence:",
                finding.confidence,
            )

            print(
                "Evidence:",
                finding.evidence,
            )

            print(
                "Signatures:",
                finding.matched_signatures,
            )


        # ----------------------------------------------------
        # THREAT INTELLIGENCE
        # ----------------------------------------------------

        threat_intel_override = any(

            finding.evidence.get(
                "threat_intel_match"
            )

            for finding in findings

            if isinstance(
                finding.evidence,
                dict,
            )
        )


        # ----------------------------------------------------
        # COMMUNITY SIGNAL
        # ----------------------------------------------------

        community_corroboration_count = (
            context.get(
                "community_corroboration_count",
                0,
            )
        )


        # ----------------------------------------------------
        # TRUST SIGNALS
        # ----------------------------------------------------

        trust_signals = context.get(
            "trust_signals",
            {},
        )


        # ----------------------------------------------------
        # RISK AGGREGATION
        # ----------------------------------------------------

        aggregated = (
            risk_aggregator_agent.aggregate(

                findings,

                threat_intel_override=(
                    threat_intel_override
                ),

                community_corroboration_count=(
                    community_corroboration_count
                ),

                trust_signals=(
                    trust_signals
                ),
            )
        )


        # ----------------------------------------------------
        # AGGREGATED RESULT
        # ----------------------------------------------------

        print("\n")

        print("=" * 80)

        print(
            "AGGREGATED RESULT"
        )

        print("=" * 80)

        print(
            "Risk Score:",
            aggregated.risk_score,
        )

        print(
            "Verdict:",
            aggregated.verdict_label,
        )


        # ----------------------------------------------------
        # FIND DOMINANT AGENT
        # ----------------------------------------------------

        dominant = max(

            aggregated.contributing_agents,

            key=lambda x: x.get(
                "contribution",
                0,
            ),

            default=None,
        )


        # ----------------------------------------------------
        # SCAM CATEGORY
        # ----------------------------------------------------

        scam_category = None


        if dominant:

            contribution = dominant.get(
                "contribution",
                0,
            )

            agent_name = dominant.get(
                "agent",
            )


            if contribution > 10:

                scam_category = (
                    CATEGORY_LABELS.get(
                        agent_name,
                    )
                )


        # ----------------------------------------------------
        # EXPLAINABILITY AGENT
        # ----------------------------------------------------

        explanation = (
            await explainability_agent.explain(

                findings,

                aggregated,

                scam_category,
            )
        )


        # ----------------------------------------------------
        # RECOMMENDATION AGENT
        # ----------------------------------------------------

        actions = (
            recommendation_agent.recommend(
                aggregated
            )
        )


        # ----------------------------------------------------
        # CONFIDENCE CALCULATION
        # ----------------------------------------------------

        total_contribution = (

            sum(

                c.get(
                    "contribution",
                    0,
                )

                for c
                in aggregated.contributing_agents

            )

            or 1
        )


        weighted_confidence = 0.0


        for finding in findings:

            contribution = next(

                (

                    c.get(
                        "contribution",
                        0,
                    )

                    for c
                    in aggregated.contributing_agents

                    if c.get("agent")
                    == finding.agent_name

                ),

                0,
            )


            weighted_confidence += (
                finding.confidence
                * contribution
            )


        confidence_score = (
            weighted_confidence
            / total_contribution
        )


        # ----------------------------------------------------
        # KEEP CONFIDENCE BETWEEN 0 AND 1
        # ----------------------------------------------------

        confidence_score = min(
            max(
                confidence_score,
                0.0,
            ),
            1.0,
        )


        # ----------------------------------------------------
        # DEBUG
        # ----------------------------------------------------

        print(
            "Confidence:",
            round(
                confidence_score,
                2,
            ),
        )

        print("=" * 80)


        # ----------------------------------------------------
        # RETURN FINAL RESULT
        # ----------------------------------------------------

        return OrchestrationResult(

            findings=findings,

            risk_score=(
                aggregated.risk_score
            ),

            verdict_label=(
                aggregated.verdict_label
            ),

            scam_category=(
                scam_category
            ),

            confidence_score=round(
                confidence_score,
                2,
            ),

            explanation_summary=(
                explanation.summary
            ),

            key_evidence=(
                explanation.key_evidence
            ),

            reasoning_chain=(
                explanation.reasoning_chain
            ),

            recommended_actions=(
                actions
            ),

            model_versions_used={

                "scoring_engine":
                    "risk_aggregator_v1",

                "llm":
                    "gemini-2.0-flash",
            },
        )


# ============================================================
# SINGLE ORCHESTRATOR INSTANCE
# ============================================================

orchestrator = Orchestrator()