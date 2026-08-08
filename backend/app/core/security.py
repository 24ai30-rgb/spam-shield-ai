"""
Authentication & authorization primitives.
"""

from datetime import datetime, timedelta, timezone
from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/swagger-login"

)


class Role(str, Enum):
    ANONYMOUS = "anonymous"
    USER = "user"
    PREMIUM = "premium"
    BUSINESS = "business"
    MODERATOR = "moderator"
    ANALYST = "analyst"
    ADMIN = "admin"


# ------------------------------------------------------------------
# PASSWORD HASHING
# ------------------------------------------------------------------

def hash_password(plain_password: str) -> str:
    print("\n" + "=" * 80)
    print("DEBUG hash_password()")
    print("VALUE :", repr(plain_password))
    print("TYPE  :", type(plain_password))

    if not isinstance(plain_password, str):
        raise ValueError(
            f"Password must be str, got {type(plain_password)}"
        )

    password_bytes = plain_password.encode("utf-8")

    print("CHARS :", len(plain_password))
    print("BYTES :", len(password_bytes))

    if len(password_bytes) > 72:
        raise ValueError(
            f"Password is {len(password_bytes)} bytes. bcrypt only supports 72 bytes."
        )

    hashed = pwd_context.hash(plain_password)

    print("HASH CREATED")
    print("=" * 80 + "\n")

    return hashed


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ------------------------------------------------------------------
# JWT
# ------------------------------------------------------------------

def _create_token(
    subject: str,
    role: str,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "role": role,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(
    user_id: str,
    role: str,
) -> str:
    return _create_token(
        user_id,
        role,
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "access",
    )


def create_refresh_token(
    user_id: str,
    role: str,
) -> str:
    return _create_token(
        user_id,
        role,
        timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
        "refresh",
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc


# ------------------------------------------------------------------
# CURRENT TOKEN
# ------------------------------------------------------------------

class TokenPayload:
    def __init__(
        self,
        user_id: str,
        role: str,
    ):
        self.user_id = user_id
        self.role = role


def get_current_token(
    token: str = Depends(oauth2_scheme),
) -> TokenPayload:

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Expected an access token",
        )

    return TokenPayload(
        user_id=payload["sub"],
        role=payload.get("role", Role.USER.value),
    )


# ------------------------------------------------------------------
# RBAC
# ------------------------------------------------------------------

_ROLE_ORDER = [
    Role.ANONYMOUS,
    Role.USER,
    Role.PREMIUM,
    Role.BUSINESS,
    Role.MODERATOR,
    Role.ANALYST,
    Role.ADMIN,
]


def require_role(minimum_role: Role):
    def dependency(
        token: TokenPayload = Depends(get_current_token),
    ):
        try:
            user_rank = _ROLE_ORDER.index(
                Role(token.role)
            )
        except ValueError:
            user_rank = -1

        if user_rank < _ROLE_ORDER.index(minimum_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role >= {minimum_role.value}",
            )

        return token

    return dependency