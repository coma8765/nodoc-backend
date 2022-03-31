from __future__ import annotations

from typing import Optional, Dict, Union, Any

from pydantic import BaseModel

from .user_schema import User


class BaseDocType(BaseModel):
    title: str
    description: str


class DocType(BaseDocType):
    id: int


class Doc(BaseModel):
    user_id: int
    type_id: int
    user: Optional[User] = None
    type: Optional[BaseDocType] = None
    data: Union[str, Dict[str, Any]]
