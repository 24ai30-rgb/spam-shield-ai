"""
WHOIS Service

Provides domain registration intelligence.

Returns:
- Domain age
- Registrar
- Creation date
- Expiry date
- Country
- Risk score
"""

from datetime import datetime

import whois

from app.core.logging import get_logger

logger = get_logger(__name__)


class WhoisService:

    async def lookup(self, domain: str):

        try:

            data = whois.whois(domain)

            creation = data.creation_date
            expiry = data.expiration_date

            if isinstance(creation, list):
                creation = creation[0]

            if isinstance(expiry, list):
                expiry = expiry[0]

            age_days = None

            if creation:
                age_days = (datetime.now(creation.tzinfo) - creation).days

            risk = None

            if age_days is not None:

                if age_days < 7:
                    risk = "very_new_domain"

                elif age_days < 30:
                    risk = "new_domain"

                elif age_days < 180:
                    risk = "young_domain"

                else:
                    risk = "aged_domain"

            return {
    "domain": domain,
    "registrar": data.registrar,
    "country": data.country,

    "created": creation.isoformat() if creation else None,
    "expires": expiry.isoformat() if expiry else None,

    "age_days": age_days,
    "risk": risk,
}

        except Exception as e:

            logger.warning(
                "whois_lookup_failed",
                error=str(e),
            )

            return None


whois_service = WhoisService()