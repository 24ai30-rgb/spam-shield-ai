"""
Threat Intelligence Service

Priority:

1. Redis Cache
2. Local IOC Database
3. VirusTotal
4. Google Safe Browsing
5. AbuseIPDB
"""

from typing import Any, Optional

import httpx
from sqlalchemy import select

from app.core.config import settings
from app.core.logging import get_logger
from app.services.cache_service import cache_service

logger = get_logger(__name__)


class ThreatIntelService:

    CACHE_PREFIX = "ioc:"
    CACHE_TTL_SECONDS = 900

    # ---------------------------------------------------------
    # VirusTotal
    # ---------------------------------------------------------

    async def _check_virustotal(
        self,
        ioc_type: str,
        value: str,
    ) -> Optional[dict[str, Any]]:

        if not settings.VIRUSTOTAL_API_KEY:
            return None

        if ioc_type != "domain":
            return None

        url = (
            f"https://www.virustotal.com/api/v3/domains/{value}"
        )

        headers = {
            "x-apikey": settings.VIRUSTOTAL_API_KEY
        }

        try:

            async with httpx.AsyncClient(
                timeout=10
            ) as client:

                response = await client.get(
                    url,
                    headers=headers,
                )

            if response.status_code != 200:
                return None

            data = response.json()

            stats = (
                data.get("data", {})
                .get("attributes", {})
                .get("last_analysis_stats", {})
            )

            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)

            if malicious == 0 and suspicious == 0:
                return None

            return {
                "source": "VirusTotal",
                "severity": min(
                    100,
                    malicious * 10 + suspicious * 5,
                ),
                "confidence": 0.98,
            }

        except Exception as e:

            logger.warning(
                "virustotal_failed",
                error=str(e),
            )

            return None

    # ---------------------------------------------------------
    # Google Safe Browsing
    # ---------------------------------------------------------

    async def _check_safe_browsing(
        self,
        ioc_type: str,
        value: str,
    ) -> Optional[dict[str, Any]]:

        if not settings.SAFE_BROWSING_API_KEY:
            return None

        if ioc_type != "domain":
            return None

        url = (
            "https://safebrowsing.googleapis.com/v4/"
            f"threatMatches:find?key={settings.SAFE_BROWSING_API_KEY}"
        )

        payload = {
            "client": {
                "clientId": "spamshield-ai",
                "clientVersion": "1.0",
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION",
                ],
                "platformTypes": [
                    "ANY_PLATFORM",
                ],
                "threatEntryTypes": [
                    "URL",
                ],
                "threatEntries": [
                    {
                        "url": value,
                    }
                ],
            },
        }

        try:

            async with httpx.AsyncClient(
                timeout=10
            ) as client:

                response = await client.post(
                    url,
                    json=payload,
                )

            if response.status_code != 200:
                return None

            data = response.json()

            if not data.get("matches"):
                return None

            return {
                "source": "Google Safe Browsing",
                "severity": 95,
                "confidence": 0.99,
            }

        except Exception as e:

            logger.warning(
                "safe_browsing_failed",
                error=str(e),
            )

            return None

    # ---------------------------------------------------------
    # Local IOC Database
    # ---------------------------------------------------------

    async def _lookup_database(
        self,
        ioc_type: str,
        value: str,
    ) -> Optional[dict[str, Any]]:

        from app.db.session import AsyncSessionLocal
        from app.models.platform import ThreatIntelIOC

        async with AsyncSessionLocal() as session:

            stmt = select(
                ThreatIntelIOC
            ).where(
                ThreatIntelIOC.ioc_type == ioc_type,
                ThreatIntelIOC.value == value.lower(),
            )

            result = await session.execute(stmt)

            ioc = result.scalar_one_or_none()

        if not ioc:
            return None

        return {
            "source": ioc.source,
            "severity": ioc.severity,
            "confidence": ioc.confidence,
        }        

    # ---------------------------------------------------------
    # AbuseIPDB
    # ---------------------------------------------------------

    async def _check_abuseipdb(
        self,
        ioc_type: str,
        value: str,
    ) -> Optional[dict[str, Any]]:

        if not settings.ABUSEIPDB_API_KEY:
            return None

        if ioc_type != "ip":
            return None

        try:

            async with httpx.AsyncClient(
                timeout=10
            ) as client:

                response = await client.get(
                    "https://api.abuseipdb.com/api/v2/check",
                    headers={
                        "Key": settings.ABUSEIPDB_API_KEY,
                        "Accept": "application/json",
                    },
                    params={
                        "ipAddress": value,
                        "maxAgeInDays": 90,
                    },
                )

            if response.status_code != 200:
                return None

            data = response.json().get("data", {})

            score = data.get("abuseConfidenceScore", 0)

            if score == 0:
                return None

            return {
                "source": "AbuseIPDB",
                "severity": score,
                "confidence": 0.98,
            }

        except Exception as e:

            logger.warning(
                "abuseipdb_failed",
                error=str(e),
            )

            return None

    # ---------------------------------------------------------
    # Main Lookup
    # ---------------------------------------------------------

    async def lookup(
        self,
        ioc_type: str,
        value: str,
    ) -> Optional[dict[str, Any]]:

        value = value.lower()

        cache_key = (
            f"{self.CACHE_PREFIX}{ioc_type}:{value}"
        )

        # -----------------------------
        # Cache
        # -----------------------------

        cached = await cache_service.get_json(
            cache_key
        )

        if cached is not None:
            return cached or None

        # -----------------------------
        # Local Database
        # -----------------------------

        result = await self._lookup_database(
            ioc_type,
            value,
        )

        if result:

            await cache_service.set_json(
                cache_key,
                result,
                ttl=self.CACHE_TTL_SECONDS,
            )

            return result

        # -----------------------------
        # VirusTotal
        # -----------------------------

        result = await self._check_virustotal(
            ioc_type,
            value,
        )

        if result:

            await cache_service.set_json(
                cache_key,
                result,
                ttl=self.CACHE_TTL_SECONDS,
            )

            return result

        # -----------------------------
        # Google Safe Browsing
        # -----------------------------

        result = await self._check_safe_browsing(
            ioc_type,
            value,
        )

        if result:

            await cache_service.set_json(
                cache_key,
                result,
                ttl=self.CACHE_TTL_SECONDS,
            )

            return result

        # -----------------------------
        # AbuseIPDB
        # -----------------------------

        result = await self._check_abuseipdb(
            ioc_type,
            value,
        )

        if result:

            await cache_service.set_json(
                cache_key,
                result,
                ttl=self.CACHE_TTL_SECONDS,
            )

            return result

        # -----------------------------
        # Cache Miss
        # -----------------------------

        await cache_service.set_json(
            cache_key,
            {},
            ttl=self.CACHE_TTL_SECONDS,
        )

        return None    

        # ---------------------------------------------------------
    # Clear Cache (Admin Utility)
    # ---------------------------------------------------------

    async def clear_cache(
        self,
        ioc_type: str,
        value: str,
    ) -> None:
        """
        Placeholder for future Redis delete support.
        """

        logger.info(
            "cache_clear_requested",
            ioc_type=ioc_type,
            value=value,
        )

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    async def health(self) -> dict[str, Any]:

        providers = {
            "database": True,
            "cache": True,
            "virustotal": bool(
                settings.VIRUSTOTAL_API_KEY
            ),
            "safe_browsing": bool(
                settings.SAFE_BROWSING_API_KEY
            ),
            "abuseipdb": bool(
                settings.ABUSEIPDB_API_KEY
            ),
        }

        return {
            "service": "Threat Intelligence",
            "status": "healthy",
            "providers": providers,
        }


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

threat_intel_service = ThreatIntelService()