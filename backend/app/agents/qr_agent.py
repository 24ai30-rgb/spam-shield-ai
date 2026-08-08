"""
QR Agent ("QR Shield")

Works even if ZBar is not installed.
"""

from typing import Any

import cv2
import numpy as np

try:
    from pyzbar.pyzbar import decode as zbar_decode
except Exception:
    zbar_decode = None

from app.agents.base import AgentFinding, BaseAgent
from app.agents.url_agent import URLAnalysisAgent


class QRAgent(BaseAgent):
    name = "qr_agent"

    def __init__(self):
        self._url_agent = URLAnalysisAgent()

    def _decode(self, image_bytes: bytes) -> list[str]:

        # If ZBar is not installed, skip QR scanning
        if zbar_decode is None:
            return []

        img_array = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        decoded_objects = zbar_decode(img)

        return [
            obj.data.decode("utf-8", errors="ignore")
            for obj in decoded_objects
        ]

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:

        image_bytes = context.get("file_bytes")

        if not image_bytes:
            return AgentFinding(
                self.name,
                0,
                0,
                {"reason": "no_qr_image_provided"},
            )

        # If ZBar is unavailable
        if zbar_decode is None:
            return AgentFinding(
                self.name,
                0,
                1.0,
                {
                    "reason": "zbar_library_not_installed",
                    "message": "QR scanning temporarily disabled."
                },
                ["qr_feature_disabled"]
            )

        payloads = self._decode(image_bytes)

        if not payloads:
            return AgentFinding(
                self.name,
                0,
                0.3,
                {"reason": "no_qr_code_detected_in_image"},
                ["no_qr_detected"],
            )

        score = 0.0
        signatures = []
        payload_findings = []

        for payload in payloads:

            if payload.startswith(("http://", "https://")):

                sub = await self._url_agent.run(
                    {"text_value": payload}
                )

                payload_findings.append({
                    "type": "url",
                    "payload": payload,
                    "score": sub.raw_score
                })

                score = max(score, sub.raw_score)

            elif payload.lower().startswith("upi://") or "pay?" in payload.lower():

                score = max(score, 45)

                signatures.append(
                    "qr_encodes_direct_payment_request"
                )

                payload_findings.append({
                    "type": "payment_link",
                    "payload": payload
                })

            else:

                payload_findings.append({
                    "type": "other",
                    "payload": payload[:200]
                })

        evidence = {
            "decoded_payloads": payload_findings,
            "payload_count": len(payloads),
        }

        return AgentFinding(
            self.name,
            min(score, 100),
            0.8,
            evidence,
            signatures,
        )