import httpx

from app.core.config import settings


class SafeBrowsingService:

    async def lookup(self, url: str):

        if not settings.SAFE_BROWSING_API_KEY:
            return None

        endpoint = (
            "https://safebrowsing.googleapis.com/v4/threatMatches:find"
            f"?key={settings.SAFE_BROWSING_API_KEY}"
        )

        payload = {
            "client": {
                "clientId": "spamshield",
                "clientVersion": "1.0",
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                ],
                "platformTypes": [
                    "ANY_PLATFORM",
                ],
                "threatEntryTypes": [
                    "URL",
                ],
                "threatEntries": [
                    {
                        "url": url,
                    }
                ],
            },
        }

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.post(
                endpoint,
                json=payload,
            )

        if response.status_code != 200:
            return None

        data = response.json()

        if "matches" in data:
            return data["matches"]

        return None


safe_browsing_service = SafeBrowsingService()