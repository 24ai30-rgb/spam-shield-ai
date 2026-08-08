"""
Dummy Cache Service (No Redis)
"""

from typing import Any


class CacheService:

    async def get_json(self, key: str) -> Any:
        return None

    async def set_json(
        self,
        key: str,
        value: Any,
        ttl: int = 300,
    ):
        return

    async def incr(
        self,
        key: str,
        ttl: int,
    ) -> int:
        return 1


cache_service = CacheService()