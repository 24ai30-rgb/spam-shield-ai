"""
Import every model module here so Alembic's `target_metadata = Base.metadata`
autogeneration sees the full schema.
"""
from app.models.user import Organization, User  # noqa: F401
from app.models.scan import AgentResult, FinalVerdict, ScanRequest  # noqa: F401
from app.models.platform import (  # noqa: F401
    AuditLog,
    CommunityReport,
    Notification,
    PDFReport,
    ThreatIntelIOC,
)
