from fastapi import APIRouter
from .utils import LoggingRoute
from .users import router as users_router

master_router = APIRouter()
master_router.include_router(users_router, prefix="/users", tags=["Users"])
