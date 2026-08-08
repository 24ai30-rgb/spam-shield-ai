import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.platform import ReportStatus


class CommunityReportCreate(BaseModel):
    input_type: str
    raw_value: str
    description: str = ""


class CommunityReportOut(BaseModel):
    id: uuid.UUID
    input_type: str
    raw_value: str
    description: str
    status: ReportStatus
    upvotes: int
    created_at: datetime

    class Config:
        from_attributes = True


class TrendingScamItem(BaseModel):
    raw_value: str
    input_type: str
    report_count: int
    severity: str


class DashboardStats(BaseModel):
    total_scans: int
    scams_blocked: int
    community_reports: int
    cyber_safety_score: float
    recent_scans: list
    verdict_distribution: dict
    scans_by_category: dict
