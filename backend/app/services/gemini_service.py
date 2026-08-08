"""
Shared AI service for Spam Shield AI.

Uses Groq LLM instead of Gemini.

All agents (Explainability, Chatbot, etc.) call this service.
"""

import json
import traceback
from typing import Any

from groq import AsyncGroq

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


SYSTEM_GUARDRAIL = """
You are Spam Shield AI.

You are a cybersecurity assistant.

Rules:
- Return ONLY valid JSON.
- Never use markdown.
- Never wrap JSON inside ``` blocks.
- Never explain outside JSON.
- Follow the exact JSON schema requested.
- Do not invent extra fields.
"""


class GeminiService:
    """
    Shared AI service (Groq backend).

    The class name is kept as GeminiService so the rest of the project
    doesn't need any changes.
    """

    def __init__(self):

        if settings.GROQ_API_KEY:
            self.client = AsyncGroq(
                api_key=settings.GROQ_API_KEY
            )
        else:
            self.client = None

        self.model = settings.GROQ_MODEL

    async def generate_structured(
        self,
        task_prompt: str,
        untrusted_content: str,
        response_schema_hint: str,
    ) -> dict[str, Any]:

        if self.client is None:
            return {
                "_fallback": True,
                "reasoning": "Groq API key not configured."
            }

        prompt = f"""
{task_prompt}

Expected JSON schema:

{response_schema_hint}

<data>

{untrusted_content}

</data>

Return ONLY valid JSON.
"""

        try:

            response = await self.client.chat.completions.create(

                model=self.model,

                temperature=0.2,

                response_format={
                    "type": "json_object"
                },

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_GUARDRAIL,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            print("\n" + "=" * 80)
            print("RAW GROQ RESPONSE")
            print(response)
            print("=" * 80)

            raw = response.choices[0].message.content

            print("\nRAW CONTENT:")
            print(raw)
            print("=" * 80)

            if raw is None or raw.strip() == "":
                return {
                    "_fallback": True,
                    "reasoning": "Groq returned an empty response."
                }

            try:
                parsed = json.loads(raw)

                print("\nPARSED JSON:")
                print(parsed)
                print("=" * 80)

                return parsed

            except json.JSONDecodeError:

                logger.exception("Invalid JSON returned by Groq")

                print("\nINVALID JSON:")
                print(raw)

                return {
                    "_fallback": True,
                    "reasoning": raw,
                }

        except Exception as e:

            print("\n" + "=" * 80)
            print("GROQ ERROR")
            traceback.print_exc()
            print("=" * 80)

            logger.exception("Groq request failed")

            return {
                "_fallback": True,
                "reasoning": str(e),
            }


gemini_service = GeminiService()