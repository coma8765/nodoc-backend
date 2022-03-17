from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..controllers import auth_controller as uc
from ..schemas import user_schema as us

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)


async def auth_optional(
    token: Optional[str] = None, token2: str = Depends(oauth2_scheme)
) -> Optional[str]:
    return token or token2


async def auth(token: Optional[str] = Depends(auth_optional)) -> str:
    if not token:
        raise uc.exc.AuthError("Need access token")
    return token


@router.post("/signup", response_model=us.User)
async def signup(user_data: us.UserReg):
    return await uc.create_user(user_data)


@router.post("/token")
async def get_user_token(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await uc.user_token(form_data.username, form_data.password)
    return {"access_token": res.token, "token_type": res.type}


@router.get("/me", response_model=us.User)
async def get_me(token: str = Depends(auth)):
    return await uc.user_by_token(us.AccessRef(token=token, type="bearer"))


__all__ = ["auth", "auth_optional", "router"]
