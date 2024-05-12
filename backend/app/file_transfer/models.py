import uuid
from typing import Self

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..models import Base


class File(Base):
    __tablename__ = "file"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    encrypted = Column(Boolean, nullable=False)

    expiration = Column(DateTime(timezone=True), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="files", lazy="selectin")

    def full_path(self: Self) -> str:
        return f"/assets/{self.path!s}"
