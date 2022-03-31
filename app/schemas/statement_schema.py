from __future__ import annotations

import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from .user_schema import User
from .org_schema import Org, OrgType


class StatementStatus(Enum):
    PENDING = 0
    CONSIDERED = 1
    DONE = 2
    REFUSED = 3


class StatementBase(BaseModel):
    """
    Future:
        * add accepted docs
    """
    user_id: int
    type_id: int
    org_id: int


class Statement(StatementBase):
    status: StatementStatus
    send_time: datetime.datetime
    # check_time: Optional[datetime.datetime]

    user: Optional[User]
    type: Optional[StatementType]
    org: Optional[Org]


class StatementTypeBase(BaseModel):
    title: str
    description: str = ""
    structure: str
    icon_id: Optional[str]


class StatementType(StatementTypeBase):
    id: int

    # statements: Optional[List[Statement]]
    org_types: Optional[List[OrgType]]


Statement.update_forward_refs()
