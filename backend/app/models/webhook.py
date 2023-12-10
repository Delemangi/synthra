import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Webhook(Base):
    __tablename__ = "webhook"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # noqa: A003

    url = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    active = Column(Boolean, nullable=True)
    timestamp = Column(DateTime, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="webhooks")
