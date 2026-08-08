import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class InputType(str, enum.Enum):
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    QR = "qr"
    SCREENSHOT = "screenshot"
    JOB = "job"
    BANKING = "banking"
    SHOPPING = "shopping"
    INVESTMENT = "investment"
    DOCUMENT = "document"


class ScanStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VerdictLabel(str, enum.Enum):
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    HIGH_RISK = "high_risk"
    CONFIRMED_SCAM = "confirmed_scam"


class ScanRequest(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "scan_requests"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    org_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    input_type: Mapped[InputType] = mapped_column(
        Enum(InputType),
        nullable=False,
    )

    raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    raw_artifact_ref: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status: Mapped[ScanStatus] = mapped_column(
        Enum(ScanStatus),
        default=ScanStatus.QUEUED,
    )

    # Relationship with User
    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="scans",
    )

    results: Mapped[list["AgentResult"]] = relationship(
        "AgentResult",
        back_populates="scan",
        cascade="all, delete-orphan",
    )

    verdict: Mapped["FinalVerdict | None"] = relationship(
        "FinalVerdict",
        back_populates="scan",
        uselist=False,
        cascade="all, delete-orphan",
    )


class AgentResult(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "scan_results"

    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scan_requests.id"),
    )

    agent_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    raw_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    evidence: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    matched_signatures: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )

    latency_ms: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    scan: Mapped["ScanRequest"] = relationship(
        "ScanRequest",
        back_populates="results",
    )


class FinalVerdict(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "final_verdicts"

    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scan_requests.id"),
        unique=True,
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    verdict_label: Mapped[VerdictLabel] = mapped_column(
        Enum(VerdictLabel),
        nullable=False,
    )

    scam_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    explanation_text: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    reasoning_chain: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )

    recommended_actions: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )

    evidence_summary: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    model_versions_used: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    scan: Mapped["ScanRequest"] = relationship(
        "ScanRequest",
        back_populates="verdict",
    )