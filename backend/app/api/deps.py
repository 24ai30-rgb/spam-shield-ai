from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthError
from app.core.security import TokenPayload, get_current_token
from app.db.session import get_db
from app.models.user import User


async def get_current_user(
    token: TokenPayload = Depends(get_current_token), db: AsyncSession = Depends(get_db)
) -> User:
    result = await db.execute(select(User).where(User.id == token.user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise AuthError("User not found or inactive")
    return user


async def get_optional_user(
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """Allows anonymous scanning at a lower rate limit — see middleware/rate_limit.py."""
    return None
