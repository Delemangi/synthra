from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Code2FA(BaseModel):
    code: str


class UserMetadata(BaseModel):
    username: str
    role: str
    files_quota: int
    size_quota: int
    is_2fa_enabled: bool


class RoleMetadata(BaseModel):
    id: str
    name: str
    quota_size: int
    quota_files: int


class UpdateRole(BaseModel):
    role_id: str
    size: int
    files: int


class UpdateUser(BaseModel):
    username: str
    role_name: str
