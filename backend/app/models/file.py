import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class File(Base):
    __tablename__ = "file"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    encrypted = Column(Boolean, nullable=False)

    expiration = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.ID"), nullable=False)
    user = relationship("User", back_populates="files")
