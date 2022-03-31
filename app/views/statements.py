from typing import List

from fastapi import APIRouter, Depends

from .auth import auth
from ..controllers import statement_controller as sc
from ..schemas import statement_schema as ss

router = APIRouter(prefix="/statements", tags=["Statements"])


@router.get("", response_model=List[ss.Statement])
async def list_statements(user=Depends(auth)):
    return await sc.list_statements(user.id)


@router.post("", response_model=ss.Statement)
async def send_request(req_data: ss.StatementBase, user=Depends(auth)):
    req_data.user_id = user.id
    return await sc.request_statement(req_data)


@router.get("/types", response_model=List[ss.StatementType])
async def list_types():
    return await sc.list_statement_types()
