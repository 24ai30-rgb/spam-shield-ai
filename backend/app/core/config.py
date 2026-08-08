"""
Central application configuration.

All runtime configuration is sourced from environment variables (12-factor
style). Nothing sensitive is hard-coded.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # --------------------------------------------------
    # App
    # --------------------------------------------------

    APP_NAME: str = "Spam Shield AI"
    ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --------------------------------------------------
    # Security
    # --------------------------------------------------

    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    DATABASE_URL: str = (
        "postgresql+asyncpg://spamshield:spamshield@localhost:5432/spamshield"
    )

    SYNC_DATABASE_URL: str = (
        "postgresql://spamshield:spamshield@localhost:5432/spamshield"
    )

    # --------------------------------------------------
    # Redis
    # --------------------------------------------------

    REDIS_URL: str = "redis://localhost:6379/0"

    # --------------------------------------------------
    # AI Providers
    # --------------------------------------------------

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    AI_TIMEOUT_SECONDS: int = 20

    # --------------------------------------------------
    # OCR
    # --------------------------------------------------

    TESSERACT_CMD: str = "/usr/bin/tesseract"

    # --------------------------------------------------
    # Threat Intelligence APIs
    # --------------------------------------------------

    VIRUSTOTAL_API_KEY: str = ""

    SAFE_BROWSING_API_KEY: str = ""

    ABUSEIPDB_API_KEY: str = ""

    PHISHTANK_API_KEY: str = ""

    # --------------------------------------------------
    # Storage
    # --------------------------------------------------

    UPLOAD_DIR: str = "./uploads"

    REPORT_DIR: str = "./reports"

    MAX_UPLOAD_MB: int = 15

    # --------------------------------------------------
    # CORS
    # --------------------------------------------------

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # --------------------------------------------------
    # Rate Limit
    # --------------------------------------------------

    RATE_LIMIT_FREE: str = "20/hour"

    RATE_LIMIT_PREMIUM: str = "1000/hour"

    # --------------------------------------------------
    # Pydantic Settings
    # --------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()