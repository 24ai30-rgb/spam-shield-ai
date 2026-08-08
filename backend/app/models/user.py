import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.scan import ScanRequest


class PlanTier(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    BUSINESS = "business"


class UserRole(str, enum.Enum):
    USER = "user"
    PREMIUM = "premium"
    BUSINESS = "business"
    MODERATOR = "moderator"
    ANALYST = "analyst"
    ADMIN = "admin"


class Organization(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan_type: Mapped[str] = mapped_column(String(50), default="business")
    api_key_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    webhook_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rate_limit_tier: Mapped[str] = mapped_column(String(50), default="standard")

    users: Mapped[list["User"]] = relationship(
        back_populates="organization"
    )


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
    )

    plan_tier: Mapped[PlanTier] = mapped_column(
        Enum(PlanTier),
        default=PlanTier.FREE,
    )

    org_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=True,
    )

    mfa_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    reputation_score: Mapped[float] = mapped_column(
        Float,
        default=50.0,
    )

    cyber_safety_score: Mapped[float] = mapped_column(
        Float,
        default=70.0,
    )

    organization: Mapped["Organization | None"] = relationship(
        back_populates="users"
    )

    scans: Mapped[list["ScanRequest"]] = relationship(
        "ScanRequest",
        back_populates="user",
        cascade="all, delete-orphan",
    )