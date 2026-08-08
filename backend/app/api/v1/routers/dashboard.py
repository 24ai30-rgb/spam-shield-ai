from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.platform import CommunityReport
from app.models.scan import FinalVerdict, ScanRequest, VerdictLabel
from app.models.user import User
from app.schemas.community import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_scans = (
        await db.execute(
            select(func.count(ScanRequest.id)).where(ScanRequest.user_id == current_user.id)
        )
    ).scalar_one()

    scams_blocked = (
        await db.execute(
            select(func.count(FinalVerdict.id))
            .join(ScanRequest, ScanRequest.id == FinalVerdict.scan_id)
            .where(
                ScanRequest.user_id == current_user.id,
                FinalVerdict.verdict_label.in_([VerdictLabel.HIGH_RISK, VerdictLabel.CONFIRMED_SCAM]),
            )
        )
    ).scalar_one()

    community_reports = (await db.execute(select(func.count(CommunityReport.id)))).scalar_one()

    recent = (
        await db.execute(
            select(ScanRequest, FinalVerdict)
            .outerjoin(FinalVerdict, FinalVerdict.scan_id == ScanRequest.id)
            .where(ScanRequest.user_id == current_user.id)
            .order_by(ScanRequest.created_at.desc())
            .limit(8)
        )
    ).all()
    recent_scans = [
        {
            "id": str(scan.id),
            "input_type": scan.input_type.value,
            "risk_score": verdict.risk_score if verdict else None,
            "verdict_label": verdict.verdict_label.value if verdict else None,
            "created_at": scan.created_at.isoformat(),
        }
        for scan, verdict in recent
    ]

    verdict_dist_rows = (
        await db.execute(
            select(FinalVerdict.verdict_label, func.count(FinalVerdict.id))
            .join(ScanRequest, ScanRequest.id == FinalVerdict.scan_id)
            .where(ScanRequest.user_id == current_user.id)
            .group_by(FinalVerdict.verdict_label)
        )
    ).all()
    verdict_distribution = {label.value: count for label, count in verdict_dist_rows}

    category_rows = (
        await db.execute(
            select(FinalVerdict.scam_category, func.count(FinalVerdict.id))
            .join(ScanRequest, ScanRequest.id == FinalVerdict.scan_id)
            .where(ScanRequest.user_id == current_user.id, FinalVerdict.scam_category.isnot(None))
            .group_by(FinalVerdict.scam_category)
        )
    ).all()
    scans_by_category = {cat: count for cat, count in category_rows}

    return DashboardStats(
        total_scans=total_scans,
        scams_blocked=scams_blocked,
        community_reports=community_reports,
        cyber_safety_score=current_user.cyber_safety_score,
        recent_scans=recent_scans,
        verdict_distribution=verdict_distribution,
        scans_by_category=scans_by_category,
    )
