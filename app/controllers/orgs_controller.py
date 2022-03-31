from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from .helpers import tr
from ..models.orgs import *
from ..schemas import org_schema as os


@tr
async def get_types_of_orgs(db: Session = None) -> List[os.OrgType]:
    """Get list of types of orgs
    :param db: Database session
    :type db: Session
    :return: List of org's types
    :rtype: List[OrgType]
    """

    orgs_types = db.execute(
        select(OrgType)
    ).scalars().all()

    return [os.OrgType.from_orm(i) for i in orgs_types]


@tr
async def create_type_of_orgs(title: str, db: Session = None) -> os.OrgType:
    """Create of type of orgs
    :param title: Database session
    :param db: Database session
    :type title: str
    :type db: Session
    :return: Type of org
    :rtype: OrgType
    """

    ot = OrgType(title=title)

    db.add(ot)
    db.flush()
    db.refresh(ot)

    return os.OrgType.from_orm(ot)


@tr
async def list_orgs(id: int = None, db: Session = None) -> List[os.OrgType]:
    """List of organizations
    :param id: For find by id
    :param db: Database session
    :type id: Optional[int]
    :type db: Session
    :return: List of Org
    :rtype: List[Org]
    """

    s = select(Org)
    s = id and s.where(Org.id == id) or s

    orgs = db.execute(s).scalars().all()

    return [os.Org.from_orm(i) for i in orgs]


@tr
async def create_org(title: str, type_id: int, db: Session = None) -> os.Org:
    """Create of type of orgs
    :param type_id: Type's id
    :param title: Database session
    :param db: Database session
    :type type_id: int
    :type title: str
    :type db: Session
    :return: Created Org
    :rtype: Org
    """

    ot = Org(title=title, type_id=type_id)

    db.add(ot)
    db.flush()
    db.refresh(ot)

    return os.Org.from_orm(ot)


__all__ = ["get_types_of_orgs", "create_type_of_orgs", "create_org", "list_orgs"]
