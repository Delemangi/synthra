from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreateWebhook(BaseModel):
    user_id: UUID
    url: str
    platform: str


class SendWebhook(BaseModel):
    user_id: UUID
    url: str
    platform: str
    active: bool
    timestamp: datetime
