import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class IOCType(str, enum.Enum):
    DOMAIN = "domain"
    IP = "ip"
    PHONE = "phone"
    HASH = "hash"
    EMAIL = "email"


class ThreatIntelIOC(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "threat_intel_iocs"

    ioc_type: Mapped[IOCType] = mapped_column(Enum(IOCType), nullable=False)
    value: Mapped[str] = mapped_column(String(500), index=True, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "safe_browsing", "community"
    severity: Mapped[str] = mapped_column(String(20), default="medium")  # low|medium|high
    confidence: Mapped[float] = mapped_column(Float, default=0.5)


class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class CommunityReport(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "community_reports"

    reporter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    scan_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_requests.id"), nullable=True
    )
    input_type: Mapped[str] = mapped_column(String(50))
    raw_value: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), default=ReportStatus.PENDING)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)
    moderator_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String(100))
    channel: Mapped[str] = mapped_column(String(50))  # in_app|email|push|sms
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    read: Mapped[bool] = mapped_column(default=False)


class PDFReport(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "pdf_reports"

    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_requests.id"))
    file_path: Mapped[str] = mapped_column(String(500))


class AuditLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    actor_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str] = mapped_column(String(100))
    meta: Mapped[dict] = mapped_column(JSONB, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
