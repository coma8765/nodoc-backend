from fastapi import APIRouter

from . import exc
from .auth import router as auth_router

router = APIRouter()

router.include_router(auth_router)

__all__ = ["exc", "router"]
