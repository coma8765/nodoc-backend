from typing import List

from fastapi import APIRouter, Depends

from .auth import auth
from ..controllers import doc_controller as dc
from ..schemas import doc_schema as ds

router = APIRouter(prefix="/documents", tags=["Docs"])


@router.get("", response_model=List[ds.Doc])
async def list_docs(user=Depends(auth)):
    return await dc.list_docs(user.id)


@router.get("/types", response_model=List[ds.DocType])
async def list_doc_types():
    return await dc.list_doc_types()


@router.post("", response_model=List[ds.Doc])
async def upload_docs(docs_data: List[ds.BaseDoc], user=Depends(auth)):
    for i in range(len(docs_data)):
        docs_data[i].user_id = user.id

    return await dc.upload_docs(docs_data)


__all__ = ["router"]
