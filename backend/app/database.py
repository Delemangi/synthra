import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine

from app.auth.models import Role  # noqa: F401
from app.file_transfer.models import File, Webhook  # noqa: F401
from app.models import Base

engine: AsyncEngine | None = None
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine() -> AsyncEngine:
    global engine

    if SQLALCHEMY_DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set")

    if engine is None:
        engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    return engine


async_session_maker: None | async_sessionmaker = None
def get_session_maker():
    global async_session_maker
    if async_session_maker is None:
        async_session_maker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine(), expire_on_commit=False
        )
    return async_session_maker

async def initialize_database() -> None:
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_session_maker() as session: # type: ignore
        yield session
