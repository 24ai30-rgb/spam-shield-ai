"""
Centralized error handling.

Development Mode:
- Prints full traceback in terminal
- Returns actual exception message in response for debugging

Production:
- Replace the generic exception handler with a generic message before deployment.
"""

import traceback

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "APP_ERROR"

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "NOT_FOUND"


class ValidationAppError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "VALIDATION_ERROR"


class AuthError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_ERROR"


class PermissionError_(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "PERMISSION_DENIED"


class RateLimitError(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "RATE_LIMITED"


class AgentExecutionError(AppError):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "AGENT_EXECUTION_FAILED"


class UpstreamServiceError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "UPSTREAM_UNAVAILABLE"


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        logger.warning(
            "app_error",
            code=exc.code,
            message=exc.message,
            path=str(request.url),
            details=exc.details,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(Exception)
    async def handle_unhandled(request: Request, exc: Exception):
        # Print complete traceback
        print("\n" + "=" * 80)
        print("UNHANDLED EXCEPTION")
        print("=" * 80)
        traceback.print_exc()
        print("=" * 80 + "\n")

        logger.exception(
            "Unhandled exception occurred",
            extra={
                "path": str(request.url),
                "exception": str(exc),
            },
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(exc),
                    "details": {
                        "exception_type": type(exc).__name__,
                        "path": str(request.url),
                    },
                }
            },
        )