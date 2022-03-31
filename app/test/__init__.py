# noinspection PyUnresolvedReferences
from random import randint
from unittest import IsolatedAsyncioTestCase
from typing import Dict, Any, Union, List

# noinspection PyUnresolvedReferences
import pytest
from pydantic import BaseModel
from sqlalchemy import create_engine

from .. import dependencies
from ..models import Base

# noinspection PyUnresolvedReferences
from ..controllers import (
    orgs_controller as oc,
    auth_controller as uc,
    doc_controller as dc,
    statement_controller as sc
)
# noinspection PyUnresolvedReferences
from ..schemas import (
    org_schema as os,
    user_schema as us,
    doc_schema as ds,
    statement_schema as ss
)


def assert_dict(
    d1: Union[Dict[str, Any], BaseModel],
    d2: Union[Dict[str, Any], BaseModel],
    exclude: List[str] = None
):
    d1 = isinstance(d1, Dict) and d1 or d1.dict()
    d2 = isinstance(d2, Dict) and d2 or d2.dict()

    print(11, d1, d2)
    for k, v in d1.items():
        if k in (exclude or []) or not v:
            continue
        if isinstance(v, BaseModel):
            assert_dict(d1[k], d2[k])
        else:
            assert d1[k] == d2[k]


def assert_dict_in_list(
    d1: List[Union[Dict[str, Any], BaseModel]],
    d2: List[Union[Dict[str, Any], BaseModel]],
    exclude: List[str] = None
):
    for i1 in d1:
        s = False
        for i2 in d2:
            try:
                assert_dict(i1, i2, exclude)
                s = True
            except AssertionError:
                pass
        if not s:
            raise AssertionError


class BaseTest(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        setattr(dependencies, "engine", create_engine("sqlite://"))
        await dependencies.startup()
        Base.metadata.create_all(dependencies.engine)

    async def asyncTearDown(self) -> None:
        await dependencies.shutdown()
