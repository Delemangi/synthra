from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.role import Role
from app.models.file import File
from app.models.webhook import Webhook

from .base import Base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@db:5432/mydatabase"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


