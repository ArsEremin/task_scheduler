from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    login: str
    password: str
