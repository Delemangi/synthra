# app/models/user.py
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .role import Role

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    quota = Column(Integer, nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.id'), nullable=False)
    role = relationship('Role', back_populates='users')
    timestamp = Column(DateTime, nullable=False)
