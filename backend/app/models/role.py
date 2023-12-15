import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # noqa: A003

    name = Column(String, nullable=False)
    quota_size = Column(Integer, nullable=False)
    quota_files = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=False)

    users = relationship("User", back_populates="role")
