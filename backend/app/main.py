"""
Spam Shield AI — FastAPI application entrypoint.

Run:
    python -m uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.middleware.request_context import RequestContextMiddleware


# ---------------------------------------------------
# Logging
# ---------------------------------------------------

configure_logging()
logger = get_logger(__name__)


# ---------------------------------------------------
# FastAPI Application
# ---------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description="Spam Shield AI - Multi-Agent Cyber Threat Detection Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


# ---------------------------------------------------
# Debug Middleware
# ---------------------------------------------------

@app.middleware("http")
async def debug_requests(request: Request, call_next):
    print("\n" + "=" * 80)
    print("REQUEST :", request.method, request.url)

    try:
        response = await call_next(request)

        print("RESPONSE:", response.status_code)
        print("=" * 80)

        return response

    except Exception:
        import traceback

        print("\nUNHANDLED ERROR")
        traceback.print_exc()
        print("=" * 80)

        raise


# ---------------------------------------------------
# Middleware
# ---------------------------------------------------

app.add_middleware(RequestContextMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# Exception Handlers
# ---------------------------------------------------

register_exception_handlers(app)


# ---------------------------------------------------
# API Routes
# ---------------------------------------------------

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------

@app.get("/", tags=["System"])
async def root():
    return {
        "name": settings.APP_NAME,
        "status": "running",
        "docs": "/api/docs",
        "health": "/api/health",
    }


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@app.get(
    "/api/health",
    tags=["System"],
)
async def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.ENV,
    }


# ---------------------------------------------------
# Startup
# ---------------------------------------------------

@app.on_event("startup")
async def startup():
    logger.info(
        "application_started",
        environment=settings.ENV,
    )

    print("\n")
    print("=" * 80)
    print("Spam Shield AI Backend Started")
    print("Swagger :", "/api/docs")
    print("Health  :", "/api/health")