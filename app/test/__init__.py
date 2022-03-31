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
    doc_controller as dc
)
# noinspection PyUnresolvedReferences
from ..schemas import (
    org_schema as os,
    user_schema as us,
    doc_schema as ds
)


def assert_dict(
    d1: Dict[str, Any], d2: Union[Dict[str, Any], BaseModel], exclude: List[str] = None
):
    for k, v in d1.items():
        if k in (exclude or []) or not v:
            continue
        assert isinstance(d1, Dict) and d1[k] or getattr(d1, k, None) == \
               isinstance(d2, Dict) and d2[k] or getattr(d2, k, None)


def assert_dict_in_list(
    d1: List[Dict[str, Any]], d2: List[Union[Dict[str, Any], BaseModel]], exclude: List[str] = None
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
        Base.metadata.create_all(dependencies.engine)
        await dependencies.startup()

    async def asyncTearDown(self) -> None:
        await dependencies.shutdown()
