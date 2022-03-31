from . import *
from .fixtures import org_ref, types_of_org_ref, types_of_org_obj, org_obj


class TestUser(BaseTest):
    async def test_types_of_orgs(self):
        r1 = await types_of_org_obj()
        r2 = await oc.get_types_of_orgs()

        assert getattr(next(filter(lambda x: x.id == r1.id, r2)), "title") == r1.title

        for i in r2:
            assert isinstance(i.id, int)
            assert isinstance(i.title, str)

    async def test_create_orgs(self):
        ref = {
            "title": org_ref(),
            "type_id": (await types_of_org_obj()).id
        }

        r = await oc.create_org(**ref)
        assert_dict(ref, r)

    async def test_list_orgs(self):
        orgs = [await org_obj() for i in range(5)]
        res = await oc.list_orgs()

        for r in filter(lambda x: x.id in [i.id for i in orgs], res):
            assert r.dict() == next(filter(lambda i: i.id == r.id, orgs)).dict()
