from __future__ import annotations

from typing import Optional, Dict, Union, Any

from pydantic import BaseModel

from .user_schema import User


class BaseDocType(BaseModel):
    title: str
    description: str


class DocType(BaseDocType):
    id: int


class BaseDoc(BaseModel):
    user_id: int
    type_id: int
    data: Union[str, Dict[str, Any]]


class Doc(BaseDoc):
    user: Optional[User]
    type: Optional[BaseDocType]
