from typing import Dict, Any

from . import us, uc, ds, os, oc, dc, ss, sc
from datetime import datetime
from random import randint

from ..schemas.doc_schema import BaseDocType


def user_ref():
    r = f"test-{randint(1000000, 9999999)}"
    return us.UserReg(
        email=f"{r}@mail",
        firstname=f"{r}-name",
        lastname=f"{r}-lastname",
        patronymic=f"{r}-patro",
        birthday=datetime.now(),
        password=f"{r}-password",
    )


async def user_obj() -> us.User:
    return await uc.create_user(user_ref())


def doc_type_ref() -> ds.BaseDocType:
    r = f"test-{randint(100000, 999999)}"
    return ds.BaseDocType(title=r, description=f"description-{r}")


async def doc_type_obj() -> ds.DocType:
    return await dc.add_doc_types(doc_type_ref())


async def doc_ref() -> ds.Doc:
    r = f"test-{randint(100000, 999999)}"

    return ds.Doc(
        user_id=(await user_obj()).id,
        type_id=(await doc_type_obj()).id,
        data=f"data-{r}"
    )


async def doc_obj() -> ds.Doc:
    return (await dc.upload_docs([await doc_ref()]))[0]


def org_ref() -> str:
    return f"org-type-{randint(1000, 9999)}"


async def org_obj() -> os.Org:
    return await oc.create_org(org_ref(), (await types_of_org_obj()).id)


def types_of_org_ref() -> str:
    return f"org-type-{randint(1000, 9999)}"


async def types_of_org_obj() -> os.OrgType:
    return await oc.create_type_of_orgs(types_of_org_ref())


def statement_type_ref() -> ss.StatementTypeBase:
    r = f"test-{randint(100000, 999999)}"
    return ss.StatementTypeBase(
        title=r,
        description=f"desc-{r}",
        structure=f"structure-{r}",
        icon_id=f"icon-{r}"
    )


async def statement_type_obj() -> ss.StatementType:
    return await sc.create_statement_type(statement_type_ref())


async def statement_ref(user_id=None, org_id=None, type_id=None) -> ss.StatementBase:
    return ss.StatementBase(
        user_id=user_id or (await user_obj()).id,
        org_id=org_id or (await org_obj()).id,
        type_id=type_id or (await statement_type_obj()).id
    )


async def statement_obj(user_id=None, org_id=None, type_id=None) -> ss.Statement:
    return await sc.request_statement(await statement_ref(user_id, org_id, type_id))
