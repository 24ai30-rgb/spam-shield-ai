"""
Message Analysis Agent ("Message Shield") — SMS / WhatsApp smishing detection.

Any URL found inside the message is delegated to the URL Analysis Agent
(agent composition) so link risk isn't re-implemented here.
"""
import re
from typing import Any

from app.agents.base import AgentFinding, BaseAgent
from app.agents.url_agent import URLAnalysisAgent

SHORTENERS = ["bit.ly", "tinyurl", "t.co", "goo.gl", "is.gd", "cutt.ly"]

SMISHING_PATTERNS = [
    r"you('ve| have) won", r"claim your (prize|reward)", r"delivery (failed|pending).{0,20}(fee|reschedule)",
    r"verify your (otp|pin|bank)", r"your (parcel|package) is on hold",
    r"congratulations", r"urgent.{0,15}action required", r"tap (here|the link)",
]

URL_RE = re.compile(r"https?://[^\s]+")


class MessageAnalysisAgent(BaseAgent):
    name = "message_analysis_agent"

    def __init__(self):
        self._url_agent = URLAnalysisAgent()

    async def analyze(self, context: dict[str, Any]) -> AgentFinding:
        text = context.get("text_value", "") or ""
        if not text:
            return AgentFinding(self.name, 0, 0, {"reason": "no_message_provided"})

        score = 0.0
        signatures: list[str] = []

        pattern_hits = [p for p in SMISHING_PATTERNS if re.search(p, text, re.I)]
        if pattern_hits:
            score += min(len(pattern_hits) * 15, 55)
            signatures.append("smishing_language_patterns")

        urls = URL_RE.findall(text)
        embedded_url_findings = []
        for url in urls[:3]:  # cap fan-out
            shortened = any(s in url for s in SHORTENERS)
            if shortened:
                score += 15
                signatures.append("shortened_url_present")
            sub_finding = await self._url_agent.run({"text_value": url})
            embedded_url_findings.append(
                {"url": url, "score": sub_finding.raw_score, "signatures": sub_finding.matched_signatures}
            )
            score = max(score, sub_finding.raw_score * 0.9)  # inherit most of the link's risk

        score = min(score, 100)
        confidence = 0.75 if pattern_hits or urls else 0.45

        evidence = {
            "matched_phrases": pattern_hits,
            "embedded_urls": embedded_url_findings,
        }
        return AgentFinding(self.name, score, confidence, evidence, signatures)
