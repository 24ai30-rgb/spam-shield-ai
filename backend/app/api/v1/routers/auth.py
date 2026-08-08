from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.exceptions import AuthError, ValidationAppError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserPublic,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ------------------------------------------------------------------
# Register
# ------------------------------------------------------------------

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise ValidationAppError(
            "An account with this email already exists."
        )

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(
            str(user.id),
            user.role.value,
        ),
        refresh_token=create_refresh_token(
            str(user.id),
            user.role.value,
        ),
    )


# ------------------------------------------------------------------
# Login (JSON) - Frontend
# ------------------------------------------------------------------

@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(User).where(User.email == payload.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise AuthError("Invalid email or password.")

    if not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise AuthError("Invalid email or password.")

    if not user.is_active:
        raise AuthError("Account is disabled.")

    return TokenResponse(
        access_token=create_access_token(
            str(user.id),
            user.role.value,
        ),
        refresh_token=create_refresh_token(
            str(user.id),
            user.role.value,
        ),
    )


# ------------------------------------------------------------------
# Swagger OAuth2 Login
# ------------------------------------------------------------------

@router.post("/swagger-login", response_model=TokenResponse)
async def swagger_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise AuthError("Invalid email or password.")

    if not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise AuthError("Invalid email or password.")

    if not user.is_active:
        raise AuthError("Account is disabled.")

    return TokenResponse(
        access_token=create_access_token(
            str(user.id),
            user.role.value,
        ),
        refresh_token=create_refresh_token(
            str(user.id),
            user.role.value,
        ),
    )


# ------------------------------------------------------------------
# Refresh Token
# ------------------------------------------------------------------

@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    payload: RefreshRequest,
):

    data = decode_token(payload.refresh_token)

    if data.get("type") != "refresh":
        raise AuthError("Expected refresh token.")

    return TokenResponse(
        access_token=create_access_token(
            data["sub"],
            data["role"],
        ),
        refresh_token=create_refresh_token(
            data["sub"],
            data["role"],
        ),
    )


# ------------------------------------------------------------------
# Current User
# ------------------------------------------------------------------

@router.get("/me", response_model=UserPublic)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user