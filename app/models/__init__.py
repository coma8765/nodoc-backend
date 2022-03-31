import importlib

from .base import Base

model_files = ["users", "orgs", "docs", "statements"]

for mf in model_files:
    importlib.import_module(f"app.models.{mf}")


__all__ = []
