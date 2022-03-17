from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

    firstname: str
    lastname: str
    patronymic: Optional[str]
    birthday: date


class User(UserBase):
    id: int
    is_confirmed: bool


class UserReg(UserBase):
    password: str


class AccessRef(BaseModel):
    type: str = "bearer"
    token: str
