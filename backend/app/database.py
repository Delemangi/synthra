import os

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)


from app.auth.models import Role  # noqa: F401
from app.file_transfer.models import File, Webhook  # noqa: F401
from app.models import Base

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://synthra:synthra@database:5432/synthra",
)


class DatabaseEngine:
    _instance: AsyncEngine | None = None

    @classmethod
    def get_engine(cls: type["DatabaseEngine"]) -> AsyncEngine:
        if cls._instance is None:
            cls._instance = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
        return cls._instance


class AsyncSessionMaker:
    _instance: None | async_sessionmaker = None

    @classmethod
    def get_sessionmaker(cls: type["AsyncSessionMaker"]) -> async_sessionmaker:
        if cls._instance is None:
            cls._instance = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=DatabaseEngine.get_engine(),
                expire_on_commit=False,
            )
        return cls._instance


async def initialize_database() -> None:
    async with DatabaseEngine.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker.get_sessionmaker()() as session:
        yield session
