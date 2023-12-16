from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    # email: str | None = None
    # full_name: str | None = None
    # disabled: bool | None = None


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
