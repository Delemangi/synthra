import uuid
from datetime import datetime

from pydantic import BaseModel


class ShareResponse(BaseModel):
    id: str
    username: str

    class Config:
        from_attributes = True


class FileUploaded(BaseModel):
    filename: str | None
    username: str


class MetadataFileResponse(BaseModel):
    id: uuid.UUID
    author: str
    name: str
    path: str
    size: int
    encrypted: bool
    shared: bool
    shared_people: list[ShareResponse]
    timestamp: datetime
    expiration: datetime

    class Config:
        from_attributes = True

    def full_path(self: "MetadataFileResponse") -> str:
        return "/assets/" + self.path


class FileSecurityUpdate(BaseModel):
    is_encrypted: bool
    current_password: str | None
    new_password: str | None
    is_shared: bool
