import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.exceptions import NotFoundError
from app.core.security import Role, require_role
from app.db.session import get_db
from app.models.platform import CommunityReport, ReportStatus, ThreatIntelIOC
from app.models.user import User
from app.schemas.community import CommunityReportCreate, CommunityReportOut, TrendingScamItem

router = APIRouter(prefix="/community", tags=["Community"])

MIN_CORROBORATION_FOR_AUTO_PROMOTE = 3


@router.post("/reports", response_model=CommunityReportOut, status_code=201)
async def submit_report(
    payload: CommunityReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = CommunityReport(
        reporter_id=current_user.id,
        input_type=payload.input_type,
        raw_value=payload.raw_value,
        description=payload.description,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.post("/reports/{report_id}/upvote", response_model=CommunityReportOut)
async def upvote_report(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(CommunityReport).where(CommunityReport.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError("Report not found.")
    report.upvotes += 1

    # Auto-promote to threat intel once corroboration threshold is met (anti-abuse gate,
    # see architecture doc Section 16)
    if report.upvotes >= MIN_CORROBORATION_FOR_AUTO_PROMOTE and report.status == ReportStatus.PENDING:
        db.add(
            ThreatIntelIOC(
                ioc_type=report.input_type if report.input_type in ("domain", "phone", "email") else "domain",
                value=report.raw_value.lower(),
                source="community",
                severity="medium",
                confidence=0.6,
            )
        )
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/reports", response_model=list[CommunityReportOut])
async def list_reports(
    status: ReportStatus | None = None,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(get_current_user),
):
    stmt = select(CommunityReport).order_by(CommunityReport.created_at.desc()).limit(100)
    if status:
        stmt = stmt.where(CommunityReport.status == status)
    rows = (await db.execute(stmt)).scalars().all()
    return rows


@router.post("/reports/{report_id}/verify", response_model=CommunityReportOut)
async def verify_report(
    report_id: uuid.UUID,
    approve: bool,
    db: AsyncSession = Depends(get_db),
    moderator: User = Depends(require_role(Role.MODERATOR)),
):
    result = await db.execute(select(CommunityReport).where(CommunityReport.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError("Report not found.")

    report.status = ReportStatus.VERIFIED if approve else ReportStatus.REJECTED
    report.moderator_id = moderator.user_id if hasattr(moderator, "user_id") else None

    if approve:
        db.add(
            ThreatIntelIOC(
                ioc_type=report.input_type if report.input_type in ("domain", "phone", "email") else "domain",
                value=report.raw_value.lower(),
                source="community_verified",
                severity="high",
                confidence=0.9,
            )
        )
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/trending", response_model=list[TrendingScamItem])
async def trending_scams(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(
            CommunityReport.raw_value,
            CommunityReport.input_type,
            func.count(CommunityReport.id).label("report_count"),
        )
        .group_by(CommunityReport.raw_value, CommunityReport.input_type)
        .order_by(func.count(CommunityReport.id).desc())
        .limit(20)
    )
    rows = (await db.execute(stmt)).all()
    return [
        TrendingScamItem(
            raw_value=r.raw_value,
            input_type=r.input_type,
            report_count=r.report_count,
            severity="high" if r.report_count >= MIN_CORROBORATION_FOR_AUTO_PROMOTE else "medium",
        )
        for r in rows
    ]
