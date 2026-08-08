"""
Shared Analysis Service
"""

from typing import Any

from app.agents.orchestrator import orchestrator
from app.models.scan import InputType


class AnalysisService:

    async def analyze(
        self,
        input_type: InputType,
        text_value: str | None = None,
        file_bytes: bytes | None = None,
        extra_context: dict[str, Any] | None = None,
    ):

        context: dict[str, Any] = {}

        if extra_context:
            context.update(extra_context)

        if text_value is not None:
            context["text_value"] = text_value

        if file_bytes is not None:
            context["file_bytes"] = file_bytes

        print("\n" + "=" * 80)
        print("ANALYSIS SERVICE")
        print("Input Type :", input_type)
        print("Context    :", context)
        print("=" * 80)

        result = await orchestrator.run_scan(
            input_type=input_type,
            context=context,
        )

        print("\nPIPELINE RESULT")
        print("Risk Score :", result.risk_score)
        print("Confidence :", result.confidence_score)
        print("Verdict    :", result.verdict_label)
        print("=" * 80)

        return result

    async def analyze_url(self, url: str):
        return await self.analyze(
            InputType.URL,
            text_value=url,
        )

    async def analyze_email(self, email: str):
        return await self.analyze(
            InputType.EMAIL,
            text_value=email,
        )

    async def analyze_phone(self, phone: str):
        return await self.analyze(
            InputType.PHONE,
            text_value=phone,
        )

    async def analyze_sms(self, message: str):
        return await self.analyze(
            InputType.SMS,
            text_value=message,
        )

    async def analyze_whatsapp(self, message: str):
        return await self.analyze(
            InputType.WHATSAPP,
            text_value=message,
        )

    async def analyze_qr(self, file_bytes: bytes):
        return await self.analyze(
            InputType.QR,
            file_bytes=file_bytes,
        )

    async def analyze_document(self, file_bytes: bytes):
        return await self.analyze(
            InputType.DOCUMENT,
            file_bytes=file_bytes,
        )

    async def analyze_screenshot(self, file_bytes: bytes):
        return await self.analyze(
            InputType.SCREENSHOT,
            file_bytes=file_bytes,
        )


analysis_service = AnalysisService()