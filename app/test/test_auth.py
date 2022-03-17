import datetime
import random
import unittest
from typing import List, Dict, Any, Union
from unittest import IsolatedAsyncioTestCase

import pytest
from pydantic import BaseModel
from sqlalchemy import create_engine

from app import dependencies
from app.controllers import auth_controller as uc
from app.models import Base
from app.schemas import user_schema as us


class TestUser(IsolatedAsyncioTestCase):
    @staticmethod
    def user_ref():
        r = f"test-{random.randint(1000000, 9999999)}"
        return us.UserReg(
            email=f"{r}@mail",
            firstname=f"{r}-name",
            lastname=f"{r}-lastname",
            patronymic=f"{r}-patro",
            birthday=datetime.datetime.now(),
            password=f"{r}-password",
        )

    async def asyncSetUp(self) -> None:
        setattr(dependencies, "engine", create_engine("sqlite://"))
        Base.metadata.create_all(dependencies.engine)
        await dependencies.startup()

    async def asyncTearDown(self) -> None:
        await dependencies.shutdown()

    async def test_reg(self):
        ref = self.user_ref()
        u = await uc.create_user(ref)
        assert_dict(ref.dict(), u, exclude=["password"])

    async def test_reg_duplicate(self):
        ref = self.user_ref()
        await uc.create_user(ref)
        with pytest.raises(uc.exc.EmailAlreadyExists):
            await uc.create_user(ref)

    async def test_auth(self):
        ref = self.user_ref()
        await uc.create_user(ref)
        await uc.user_by_token(await uc.user_token(ref.email, ref.password))


def assert_dict(
    d1: Dict[str, Any], d2: Union[Dict[str, Any], BaseModel], exclude: List[str] = None
):
    for k, v in d1.items():
        if k in exclude:
            continue
        assert d1[k] == isinstance(d2, Dict) and d2[k] or getattr(d2, k)


if __name__ == "__main__":
    unittest.main()
