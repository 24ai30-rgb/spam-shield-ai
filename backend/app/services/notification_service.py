"""
Notification dispatch service (architecture doc Section 20).

Called from the scan pipeline (background task) when a verdict crosses
the high-risk threshold, and from the community pipeline when a
moderator verifies a report matching something in the user's history.
Channel adapters are stubbed with clear extension points — wire real
SES/Twilio/FCM credentials per deployment.
"""
from app.core.logging import get_logger
from app.models.scan import VerdictLabel

logger = get_logger(__name__)

NOTIFY_THRESHOLD_LABELS = {VerdictLabel.HIGH_RISK, VerdictLabel.CONFIRMED_SCAM}


class NotificationService:
    async def notify_high_risk_verdict(self, user_id: str, scan_id: str, risk_score: float, category: str | None):
        from app.db.session import AsyncSessionLocal
        from app.models.platform import Notification

        payload = {
            "scan_id": scan_id,
            "risk_score": risk_score,
            "category": category,
            "title": "High-risk scam detected",
            "body": f"Spam Shield flagged a scan as {risk_score}/100 risk"
            + (f" ({category})" if category else "") + ".",
        }

        async with AsyncSessionLocal() as session:
            session.add(
                Notification(user_id=user_id, type="scan.verdict.high_risk", channel="in_app", payload=payload)
            )
            await session.commit()

        # Extension points for real channel delivery:
        # await self._send_email(user, payload)
        # await self._send_push(user, payload)
        logger.info("notification_dispatched", user_id=user_id, scan_id=scan_id, channel="in_app")


notification_service = NotificationService()
