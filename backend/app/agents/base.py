"""
Base contract every specialist agent implements.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any
import traceback


@dataclass
class AgentFinding:
    agent_name: str
    raw_score: float
    confidence: float
    evidence: dict[str, Any] = field(default_factory=dict)
    matched_signatures: list[str] = field(default_factory=list)
    latency_ms: int = 0


class BaseAgent(ABC):
    """
    Base class for every AI Agent.
    """

    name: str = "base_agent"

    async def run(
        self,
        context: dict[str, Any],
    ) -> AgentFinding:

        start = perf_counter()

        print("\n" + "=" * 80)
        print(f"STARTING AGENT : {self.name}")
        print("=" * 80)

        try:

            finding = await self.analyze(context)

            print(f"{self.name} SUCCESS")
            print(f"Score      : {finding.raw_score}")
            print(f"Confidence : {finding.confidence}")

        except Exception as exc:

            print("\n" + "=" * 80)
            print("AGENT FAILED")
            print("Agent :", self.name)
            print("Error :", repr(exc))
            traceback.print_exc()
            print("=" * 80 + "\n")

            # IMPORTANT:
            # Re-raise while debugging so the real traceback
            # appears in the terminal.
            raise

        finally:

            latency = int(
                (perf_counter() - start) * 1000
            )

        finding.latency_ms = latency
        finding.agent_name = self.name

        print(f"Latency : {latency} ms")

        return finding

    @abstractmethod
    async def analyze(
        self,
        context: dict[str, Any],
    ) -> AgentFinding:
        """
        Implemented by every specialist agent.
        """
        raise NotImplementedError