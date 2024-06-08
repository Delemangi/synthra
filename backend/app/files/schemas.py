import uuid
from datetime import datetime

from pydantic import BaseModel


class FileUploaded(BaseModel):
    filename: str | None
    username: str


class MetadataFileResponse(BaseModel):
    id: uuid.UUID
    name: str
    path: str
    size: int
    encrypted: bool
    timestamp: datetime
    expiration: datetime

    class Config:
        from_attributes = True

    def full_path(self: "MetadataFileResponse") -> str:
        return "/assets/" + self.path
