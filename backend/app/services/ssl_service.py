import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime


class SSLService:

    async def lookup(self, url: str):

        try:

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            host = urlparse(url).hostname

            context = ssl.create_default_context()

            with socket.create_connection((host, 443), timeout=5) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=host,
                ) as ssock:

                    cert = ssock.getpeercert()

            issuer = dict(x[0] for x in cert["issuer"])

            expires = datetime.strptime(
                cert["notAfter"],
                "%b %d %H:%M:%S %Y %Z",
            )

            days_left = (expires - datetime.utcnow()).days

            return {

                "valid": True,

                "issuer": issuer.get("organizationName"),

                "expires": expires.isoformat(),

                "days_left": days_left,

                "expired": days_left < 0,

                "self_signed": False,

            }

        except Exception:

            return {

                "valid": False,

                "issuer": None,

                "expires": None,

                "days_left": None,

                "expired": True,

                "self_signed": True,

            }


ssl_service = SSLService()