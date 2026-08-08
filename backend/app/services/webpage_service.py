"""
Webpage Service

Fetches webpage HTML for AI and heuristic analysis.
"""

import httpx

from app.core.logging import get_logger

logger = get_logger(__name__)


class WebpageService:

    async def fetch(self, url: str):

        try:

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/126 Safari/537.36"
                )
            }

            async with httpx.AsyncClient(
                timeout=10,
                follow_redirects=True,
            ) as client:

                response = await client.get(
                    url,
                    headers=headers,
                )

            return {
                "success": True,
                "status_code": response.status_code,
                "html": response.text,
                "headers": dict(response.headers),
                "final_url": str(response.url),
            }

        except Exception as e:

            logger.warning(
                "webpage_fetch_failed",
                error=str(e),
            )

            return {
                "success": False,
                "status_code": None,
                "html": "",
                "headers": {},
                "final_url": url,
                "error": str(e),
            }


webpage_service = WebpageService()