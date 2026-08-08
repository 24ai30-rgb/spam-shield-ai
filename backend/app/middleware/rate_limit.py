"""
Rate limiting (Disabled for development / hackathon)
"""

from fastapi import Request


async def enforce_rate_limit(
    request: Request,
    identity: str,
    plan_tier: str = "free",
):
    # Redis disabled
    return