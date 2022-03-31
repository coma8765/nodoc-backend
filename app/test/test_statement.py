from . import *
from .fixtures import statement_type_ref, statement_type_obj, org_obj, statement_ref, statement_obj, user_obj


class TestUser(BaseTest):
    async def test_create_statement_type(self):
        ref = statement_type_ref()
        r = await sc.create_statement_type(ref)
        assert_dict(ref, r)

    async def test_add_orgs_to_statement_type(self):
        r1 = await statement_type_obj()
        r2 = await org_obj()

        r = await sc.add_orgs_to_statement_type(r1.id, [r2.id])
        assert r

    async def test_request_statement(self):
        ref = await statement_ref()
        r = await sc.request_statement(ref)

        assert_dict(ref, r)

    async def test_list_statement(self):
        user_ref = await user_obj()
        refs = [await statement_obj(user_id=user_ref.id) for _ in range(5)]
        res = await sc.list_statements(user_ref.id)

        assert_dict_in_list(refs, res)

    async def test_list_statement_types(self):
        refs = [await statement_type_obj() for _ in range(5)]
        res = await sc.list_statement_types()

        assert_dict_in_list(refs, res)

