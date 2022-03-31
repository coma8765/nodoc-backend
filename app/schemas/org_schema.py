from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel


class MemberStatus(IntEnum):
    """Statuses for users in orgs"""
    PENDING = 0
    ACCEPTED = 1
    DECLINED = 2


class OrgType(BaseModel):
    id: int
    title: str


class Org(OrgType):
    type_id: int
    type: OrgType


__all__ = ["MemberStatus", "OrgType", "Org"]
