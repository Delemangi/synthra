from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateWebhook(BaseModel):
    url: str
    platform: str = "Discord"


class SendWebhook(BaseModel):
    user_id: UUID
    id: UUID
    url: str
    platform: str
    active: bool
    timestamp: datetime


class RequestStatus(BaseModel):
    message: str
