from sqlalchemy import select
from typing import List, Any

from sqlalchemy.orm import Session

from .helpers import tr
from ..models.docs import Doc, DocType
from ..schemas import doc_schema as ds


@tr
async def list_doc_types(db: Session = None) -> List[ds.DocType]:
    """List of doc's types
    :type db: Session
    :rtype: List[DocType]
    :return: List of DocType
    """
    return list(map(ds.DocType.from_orm, db.execute(select(DocType)).scalars().all()))


@tr
async def add_doc_types(type_data: ds.BaseDocType, db: Session = None) -> ds.DocType:
    """Add doc type
    :param type_data: Data for creation type of doc
    :type type_data: BaseDocType
    :type db: Session
    :rtype: DocType
    :return: Created doc type
    """
    o = DocType(**type_data.dict())
    db.add(o)
    db.flush()
    db.refresh(o)
    return ds.DocType.from_orm(o)


@tr
async def upload_docs(docs_data: List[ds.Doc], db: Session = None) -> List[ds.Doc]:
    """Upload new docs
    :param docs_data: List of doc's data
    :type docs_data: List[ds.BaseDocType]
    :type db: Session
    :rtype: List[Doc]
    :return: List of added docs
    """

    new_docs = []
    for doc_data in docs_data:
        new_docs.append(Doc(**doc_data.dict(exclude_unset=True)))
        db.add(new_docs[-1])
        db.flush()
        db.refresh(new_docs[-1])

    db.flush()

    return [ds.Doc.from_orm(i) for i in new_docs]


@tr
async def list_docs(user_id: int, db: Session = None) -> List[ds.Doc]:
    """List user's docs
    :param user_id: User's id
    :type user_id: int
    :type db: Session
    :rtype: List[Doc]
    :return: List of org's types
    """
    res = db.execute(
        select(Doc.type_id).
        where(Doc.user_id == user_id).
        selectinload(Doc.type)
    ).scalars().all()

    return [ds.Doc.from_orm(r) for r in res]


__all__ = ["upload_docs", "list_docs", "list_doc_types", "add_doc_types"]
