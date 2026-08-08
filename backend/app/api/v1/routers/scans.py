import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Request, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import orchestrator
from app.api.deps import get_current_user
from app.core.config import settings
from app.core.exceptions import NotFoundError, ValidationAppError
from app.core.logging import get_logger
from app.db.session import get_db
from app.middleware.rate_limit import enforce_rate_limit
from app.models.platform import AuditLog
from app.models.scan import (
    AgentResult,
    FinalVerdict,
    InputType,
    ScanRequest,
    ScanStatus,
)
from app.models.user import User
from app.schemas.scan import ScanCreateRequest, ScanHistoryItem, ScanOut
from app.services.notification_service import (
    NOTIFY_THRESHOLD_LABELS,
    notification_service,
)
from fastapi.responses import FileResponse
from app.services.pdf_service import pdf_report_service
import os

print("========== CREATE SCAN CALLED ==========")
router = APIRouter(prefix="/scans", tags=["Scans"])
logger = get_logger(__name__)


async def _persist_and_score(
    db: AsyncSession,
    scan: ScanRequest,
    context: dict,
    background_tasks: BackgroundTasks,
) -> FinalVerdict:
    scan.status = ScanStatus.PROCESSING
    await db.commit()

    from app.services.analysis_service import analysis_service

    result = await analysis_service.analyze(
    input_type=scan.input_type,
    text_value=context.get("text_value"),
    file_bytes=context.get("file_bytes"),
    extra_context=context,
)

    for f in result.findings:
        db.add(
            AgentResult(
                scan_id=scan.id,
                agent_name=f.agent_name,
                raw_score=f.raw_score,
                confidence=f.confidence,
                evidence=f.evidence,
                matched_signatures=f.matched_signatures,
                latency_ms=f.latency_ms,
            )
        )

    verdict = FinalVerdict(
        scan_id=scan.id,
        risk_score=result.risk_score,
        verdict_label=result.verdict_label,
        scam_category=result.scam_category,
        confidence_score=result.confidence_score,
        explanation_text=result.explanation_summary,
        reasoning_chain=result.reasoning_chain,
        recommended_actions=result.recommended_actions,
        evidence_summary={"key_evidence": result.key_evidence},
        model_versions_used=result.model_versions_used,
    )

    db.add(verdict)

    scan.status = ScanStatus.COMPLETED

    db.add(
        AuditLog(
            actor_id=scan.user_id,
            action="scan_completed",
            resource_type="scan",
            resource_id=str(scan.id),
            meta={"verdict": result.verdict_label},
        )
    )

    await db.commit()
    await db.refresh(verdict)

    if verdict.verdict_label in NOTIFY_THRESHOLD_LABELS:
        background_tasks.add_task(
            notification_service.notify_high_risk_verdict,
            str(scan.user_id),
            str(scan.id),
            verdict.risk_score,
            verdict.scam_category,
        )

    return verdict


@router.post("", response_model=ScanOut, status_code=201)
async def create_scan(
    request: Request,
    payload: ScanCreateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await enforce_rate_limit(
        request,
        str(current_user.id),
        current_user.plan_tier.value,
    )

    if not payload.text_value:
        raise ValidationAppError(
            "text_value is required for this input type."
        )

    scan = ScanRequest(
        user_id=current_user.id,
        input_type=payload.input_type,
        raw_text=payload.text_value,
    )

    db.add(scan)
    await db.commit()
    await db.refresh(scan)

    await _persist_and_score(
        db,
        scan,
        {"text_value": payload.text_value},
        background_tasks,
    )

    return await get_scan(scan.id, db, current_user)


@router.post("/upload", response_model=ScanOut, status_code=201)
async def create_scan_from_file(
    request: Request,
    background_tasks: BackgroundTasks,
    input_type: InputType = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await enforce_rate_limit(
        request,
        str(current_user.id),
        current_user.plan_tier.value,
    )

    contents = await file.read()

    if len(contents) > settings.MAX_UPLOAD_MB * 1024 * 1024:
        raise ValidationAppError(
            f"File exceeds {settings.MAX_UPLOAD_MB}MB limit."
        )

    scan = ScanRequest(
        user_id=current_user.id,
        input_type=input_type,
        raw_artifact_ref=file.filename,
    )

    db.add(scan)
    await db.commit()
    await db.refresh(scan)

    await _persist_and_score(
        db,
        scan,
        {"file_bytes": contents},
        background_tasks,
    )

    return await get_scan(scan.id, db, current_user)


@router.get("/{scan_id}", response_model=ScanOut)
async def get_scan(
    scan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ScanRequest).where(ScanRequest.id == scan_id)
    )

    scan = result.scalar_one_or_none()

    if (
        not scan
        or (
            scan.user_id != current_user.id
            and current_user.role.value not in ("admin", "analyst")
        )
    ):
        raise NotFoundError("Scan not found.")

    verdict_result = await db.execute(
        select(FinalVerdict).where(
            FinalVerdict.scan_id == scan_id
        )
    )

    verdict = verdict_result.scalar_one_or_none()

    results_result = await db.execute(
        select(AgentResult).where(
            AgentResult.scan_id == scan_id
        )
    )

    agent_results = results_result.scalars().all()

    return ScanOut(
        id=scan.id,
        input_type=scan.input_type,
        status=scan.status,
        created_at=scan.created_at,
        verdict=verdict,
        agent_results=agent_results,
    )


@router.get("", response_model=list[ScanHistoryItem])
async def list_scan_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 50,
):
    stmt = (
        select(ScanRequest, FinalVerdict)
        .outerjoin(
            FinalVerdict,
            FinalVerdict.scan_id == ScanRequest.id,
        )
        .where(ScanRequest.user_id == current_user.id)
        .order_by(ScanRequest.created_at.desc())
        .limit(limit)
    )

    rows = (await db.execute(stmt)).all()

    return [
        ScanHistoryItem(
            id=scan.id,
            input_type=scan.input_type,
            status=scan.status,
            risk_score=verdict.risk_score if verdict else None,
            verdict_label=verdict.verdict_label if verdict else None,
            created_at=scan.created_at,
        )
        for scan, verdict in rows
    ]

@router.get("/{scan_id}/report")
async def download_pdf_report(
    scan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Scan check
    result = await db.execute(
        select(ScanRequest).where(
            ScanRequest.id == scan_id
        )
    )

    scan = result.scalar_one_or_none()

    if not scan:
        raise NotFoundError("Scan not found.")

    verdict_result = await db.execute(
        select(FinalVerdict).where(
            FinalVerdict.scan_id == scan_id
        )
    )

    verdict = verdict_result.scalar_one_or_none()

    if not verdict:
        raise NotFoundError("Verdict not found.")

    agent_result = await db.execute(
        select(AgentResult).where(
            AgentResult.scan_id == scan_id
        )
    )

    agents = agent_result.scalars().all()

    verdict_data = {
        "risk_score": verdict.risk_score,
        "verdict_label": verdict.verdict_label.value,
        "scam_category": verdict.scam_category,
        "confidence_score": verdict.confidence_score,
        "explanation_summary": verdict.explanation_text,
        "reasoning_chain": verdict.reasoning_chain,
        "recommended_actions": verdict.recommended_actions,
        "key_evidence": verdict.evidence_summary.get(
            "key_evidence",
            [],
        ),
        "contributing_agents": [
            {
                "agent": a.agent_name,
                "raw_score": a.raw_score,
                "confidence": a.confidence,
                "weight": 1,
                "contribution": a.raw_score,
            }
            for a in agents
        ],
    }

    pdf_path = pdf_report_service.generate(
        str(scan.id),
        verdict_data,
    )

    return FileResponse(
        path=pdf_path,
        filename=f"SpamShield_Report_{scan.id}.pdf",
        media_type="application/pdf",
    )