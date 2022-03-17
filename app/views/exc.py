import builtins
import os
import traceback
from dataclasses import dataclass
from typing import Optional, Type, List

from starlette.responses import JSONResponse

from ..controllers import exc


@dataclass
class Exc:
    exc: Type[Exception]
    code: int
    message: Optional[str] = None


exceptions = [
    Exc(exc.AuthError, 403, "Token or login's ref bad"),
    Exc(exc.EmailAlreadyExists, 403, "This email already exists"),
    Exc(AssertionError, 432, "Assertion error"),
]
exc_types = [i.exc for i in exceptions]


async def exception_handler(rq, call_next):
    # noinspection PyBroadException
    try:
        return await call_next(rq)
    except Exception as e:
        r: List[Exc] = list(filter(lambda x: isinstance(e, x.exc), exceptions))
        if r:
            return JSONResponse(
                content={"detail": r[0].message or e.__str__()}, status_code=r[0].code
            )

        return JSONResponse(
            content={
                "detail": e.__str__(),
                "traceback": os.getenv("DEBUG")
                and traceback.format_stack()
                or "Mode no debug",
            },
            status_code=500,
        )
