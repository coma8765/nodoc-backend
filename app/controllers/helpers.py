from functools import wraps
from typing import TYPE_CHECKING, TypeVar

RT = TypeVar("RT")
PT = TypeVar("PT")


def tr(func):
    @wraps(func)
    async def w(*args, **kwargs):
        from ..dependencies import session

        with session().begin() as s:
            kwargs.get("db") or kwargs.update({"db": s.session})
            return await func(*args, **kwargs)

    return TYPE_CHECKING and func or w


__all__ = ["tr"]
