from typing import Optional, List

from fastapi import APIRouter

from ..controllers import orgs_controller as oc
from ..schemas import org_schema as os

router = APIRouter(prefix="/orgs", tags=["Orgs"])


@router.get("", response_model=List[os.Org])
async def list_orgs(id: Optional[int] = None):
    return await oc.list_orgs(id=id)


@router.get("/types", response_model=List[os.OrgType])
async def list_orgs():
    return await oc.list_types_of_orgs()


__all__ = ["router"]
