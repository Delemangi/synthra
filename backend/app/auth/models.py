import uuid
from typing import Self

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    quota = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=True)

    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"), nullable=True)
    role = relationship("Role", back_populates="users")

    files = relationship("File", back_populates="user", lazy="selectin")
    webhooks = relationship(
        "Webhook", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    def has_remaining_quota(self: Self) -> bool:
        return bool(self.quota != 0)


class Role(Base):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    quota_size = Column(Integer, nullable=False)
    quota_files = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=False)

    users = relationship("User", back_populates="role")


class LoggedInTokens(Base):
    __tablename__ = "logged_in_tokens"

    token = Column(String, primary_key=True, nullable=False)
    expiration = Column(DateTime, nullable=False)
