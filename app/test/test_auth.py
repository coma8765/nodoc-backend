from . import *
from .fixtures import user_ref


class TestUser(BaseTest):
    async def test_reg(self):
        ref = user_ref()
        u = await uc.create_user(ref)
        print(ref, u)
        assert_dict(ref, u, exclude=["password"])

    async def test_reg_duplicate(self):
        ref = user_ref()
        await uc.create_user(ref)
        with pytest.raises(uc.exc.EmailAlreadyExists):
            await uc.create_user(ref)

    async def test_auth(self):
        ref = user_ref()
        await uc.create_user(ref)
        await uc.user_by_token(await uc.user_token(ref.email, ref.password))
