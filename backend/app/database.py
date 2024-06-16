import os
from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from alembic import command
from alembic.config import Config

from .auth.models import Role

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://synthra:synthra@database:5432/synthra",
)


class DatabaseEngine:
    _instance: AsyncEngine | None = None

    @classmethod
    def get_engine(cls: type["DatabaseEngine"]) -> AsyncEngine:
        if cls._instance is None:
            # set echo=True to enable verbose logging
            cls._instance = create_async_engine(SQLALCHEMY_DATABASE_URL)
        return cls._instance


class AsyncSessionMaker:
    _instance: async_sessionmaker[AsyncSession] | None = None

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


async def initialize_database() -> None:
    async with AsyncSessionMaker.get_sessionmaker()() as session:
        await initialize_roles(session)


async def initialize_roles(session: AsyncSession) -> None:
    existing_roles = await session.execute(select(Role).limit(1))
    if existing_roles.scalars().first() is not None:
        return

    roles = [
        Role(name="admin", quota_size=1000000000, quota_files=50, timestamp=datetime.now()),
        Role(name="user", quota_size=100000000, quota_files=10, timestamp=datetime.now()),
    ]

    session.add_all(roles)
    await session.commit()
