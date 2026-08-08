from fastapi import APIRouter

from app.api.v1.routers import auth, chatbot, community, dashboard, notifications, scans

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(scans.router)
api_router.include_router(community.router)
api_router.include_router(dashboard.router)
api_router.include_router(chatbot.router)
api_router.include_router(notifications.router)
