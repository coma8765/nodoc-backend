from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from .helpers import tr
from ..models.orgs import OrgType
from ..models.statements import Statement, StatementType
from ..schemas import statement_schema as ss


@tr
async def list_statements(user_id: int, db: Session = None) -> List[ss.Statement]:
    """List of statements
    :param user_id: User id
    :type user_id: int
    :type db: Session
    :return: List of statements
    :rtype: List[Statement]
    """
    return list(map(
        ss.Statement.from_orm,
        db.execute(
            select(Statement).
            where(Statement.user_id == user_id)
        ).scalars().all()
    ))


@tr
async def list_statement_types(db: Session = None) -> List[ss.Statement]:
    """List of statement types
    :type db: Session
    :return: List of statement types
    :rtype: List[StatementType]
    """
    return list(map(
        ss.StatementType.from_orm,
        db.execute(select(StatementType)).scalars().all()
    ))


@tr
async def create_statement_type(type_data: ss.StatementTypeBase, db: Session = None) -> ss.StatementType:
    """List of statement types
    :param type_data: Ref for create type
    :type type_data: StatementTypeBase
    :type db: Session
    :return: Created type
    :rtype: StatementType
    """
    o = StatementType(**type_data.dict())
    db.add(o)
    db.flush()
    db.refresh(o)
    return ss.StatementType.from_orm(o)


@tr
async def add_orgs_to_statement_type(statement_type_id: int, org_types_ids: List[int], db: Session = None) \
        -> ss.StatementType:
    """List of statement types
    :param statement_type_id: Statement type id
    :param org_types_ids: List of org_types ids
    :type statement_type_id: int
    :type org_types_ids: List[int]
    :type db: Session
    :return: Created statement type
    :rtype: StatementType
    """
    st: StatementType = db.execute(
        select(StatementType).where(StatementType.id == statement_type_id)
    ).scalar_one_or_none()

    if not st:
        raise

    orgs = db.execute(
        select(OrgType).
        where(OrgType.id.in_(org_types_ids))
    ).scalars().all()

    if len(orgs) != len(org_types_ids):
        map(lambda x: x not in [i.id for i in orgs], org_types_ids)
        raise

    list(map(st.org_types.append, orgs))
    db.flush()
    db.refresh(st)

    return ss.StatementType.from_orm(st)


@tr
async def request_statement(req_data: ss.StatementBase, db: Session = None) -> ss.Statement:
    """Send request statement
    :param req_data: Ref for request statement
    :type req_data: Statement
    :type db: Session
    :return: Sent statement
    :rtype: Statement
    """

    o = Statement(**req_data.dict())
    db.add(o)
    db.flush()

    return ss.Statement.from_orm(o)


@tr
async def review_statement(statement_id: int, db: Session = None) -> ss.Statement:
    """Review statement
    :param statement_id: Statement id
    :type statement_id: int
    :type db: Session
    :return: List of org types
    :rtype: List[OrgType]
    """
    pass
