"""
OCR Agent ("Screenshot Shield")

Extracts text from an uploaded screenshot and looks for fake bank/login
UI language and embedded scam indicators. Any URLs/phone numbers found
are handed off to the URL and Phone agents (recursive fan-out per the
orchestrator design, capped at depth 3).
"""
import re
from typing import Any

from app.agents.base import AgentFinding, BaseAgent
from app.agents.phone_agent import PhoneReputationAgent
from app.agents.url_agent import URLAnalysisAgent
from app.services.ocr_service import ocr_service

FAKE_UI_PATTERNS = [
    r"enter your (pin|otp|password|cvv)", r"account (suspended|locked|frozen)",
    r"verify to (unlock|continue|avoid closure)", r"security alert",
    r"unauthorized (login|access) detected",
]


class OCRAgent(BaseAgent):
    name = "ocr_agent"

    def __init__(self):
        self._url_agent = URLAnalysisAgent()
        self._phone_agent = PhoneReputationAgent()

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:
        image_bytes = context.get("file_bytes")
        if not image_bytes:
            return AgentFinding(self.name, 0, 0, {"reason": "no_image_provided"})

        extraction = ocr_service.extract(image_bytes)
        text = extraction["raw_text"]
        score = 0.0
        signatures: list[str] = []

        ui_hits = [p for p in FAKE_UI_PATTERNS if re.search(p, text, re.I)]
        if ui_hits:
            score += min(len(ui_hits) * 18, 55)
            signatures.append("fake_bank_or_login_ui_language")

        if extraction["word_count"] < 3:
            # Low-text screenshots are inconclusive, not automatically suspicious
            score = max(score, 0)
            signatures.append("low_extractable_text")

        sub_findings = []
        for url in extraction["extracted_urls"][:2]:
            f = await self._url_agent.run({"text_value": url})
            sub_findings.append({"type": "url", "value": url, "score": f.raw_score})
            score = max(score, f.raw_score * 0.85)

        for phone in extraction["extracted_phones"][:2]:
            f = await self._phone_agent.run({"text_value": phone})
            sub_findings.append({"type": "phone", "value": phone, "score": f.raw_score})
            score = max(score, f.raw_score * 0.7)

        score = min(score, 100)
        confidence = 0.7 if extraction["word_count"] > 5 else 0.35

        evidence = {
            "extracted_text_preview": text[:500],
            "extracted_amounts": extraction["extracted_amounts"],
            "fake_ui_phrases_found": ui_hits,
            "embedded_artifact_findings": sub_findings,
        }
        return AgentFinding(self.name, score, confidence, evidence, signatures)
