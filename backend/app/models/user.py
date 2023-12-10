from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    quota = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"), nullable=False)
    role = relationship("Role", back_populates="users")
