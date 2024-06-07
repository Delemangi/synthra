from uuid import UUID

from pydantic import BaseModel


class CreateShare(BaseModel):
    username: str
    file_id: UUID
