import importlib
import os

from fastapi import APIRouter

from . import exc

exclude = ["exc"]

router = APIRouter()

for f in os.listdir("./app/views"):
    if not f.startswith("__") and f not in exclude:
        lib = importlib.import_module(f".{f.split('.')[0]}", "app.views")

        if getattr(lib, "router", None):
            router.include_router(getattr(lib, "router"))

__all__ = ["exc", "router"]
