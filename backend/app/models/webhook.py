# app/models/user.py
from app.database.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .user import User

class Webhook(Base):
    __tablename__ = "webhook"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    active = Column(Boolean, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='webhooks')
    timestamp = Column(DateTime, nullable=False)
