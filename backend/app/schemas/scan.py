import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.scan import (
    InputType,
    ScanStatus,
    VerdictLabel,
)


# ---------------------------------------------------------
# Request
# ---------------------------------------------------------

class ScanCreateRequest(BaseModel):
    input_type: InputType
    text_value: str | None = None


# ---------------------------------------------------------
# Agent Result
# ---------------------------------------------------------

class AgentResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    agent_name: str
    raw_score: float
    confidence: float
    evidence: dict[str, Any]
    matched_signatures: list[str]
    latency_ms: int


# ---------------------------------------------------------
# Final Verdict
# ---------------------------------------------------------

class FinalVerdictOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    risk_score: float
    verdict_label: VerdictLabel
    scam_category: str | None
    confidence_score: float
    explanation_text: str
    reasoning_chain: list[str]
    recommended_actions: list[str]
    evidence_summary: dict[str, Any]
    model_versions_used: dict[str, Any]


# ---------------------------------------------------------
# Scan Output
# ---------------------------------------------------------

class ScanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    input_type: InputType
    status: ScanStatus
    created_at: datetime

    verdict: FinalVerdictOut | None = None
    agent_results: list[AgentResultOut] = []


# ---------------------------------------------------------
# History Item
# ---------------------------------------------------------

class ScanHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    input_type: InputType
    status: ScanStatus

    risk_score: float | None = None
    verdict_label: VerdictLabel | None = None

    created_at: datetime