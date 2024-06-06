import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from alembic import command
from alembic.config import Config

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
    _instance: None | async_sessionmaker[AsyncSession] = None

    @classmethod
    def get_sessionmaker(cls: type["AsyncSessionMaker"]) -> async_sessionmaker[AsyncSession]:
        if cls._instance is None:
            cls._instance = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=DatabaseEngine.get_engine(),
                expire_on_commit=False,
            )
        return cls._instance


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker.get_sessionmaker()() as session:
        yield session


def run_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
