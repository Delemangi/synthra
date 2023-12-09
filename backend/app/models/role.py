# app/models/user.py
from app.database.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    quota_size = Column(Integer, nullable=False)
    quota_files = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=False)
