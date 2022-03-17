from pydantic import BaseModel


class GetUserToken(BaseModel):
    email: str
    password: str
