import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # noqa: A003

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    quota = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=True)

    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"), nullable=True)
    role = relationship("Role", back_populates="users")

    files = relationship("File", back_populates="user")
    webhooks = relationship("Webhook", back_populates="user")
