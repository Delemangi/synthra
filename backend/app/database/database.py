import os
import uuid
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import file, role, user, webhook  # noqa: F401
from app.models.base import Base

load_dotenv("../.env")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

print(SQLALCHEMY_DATABASE_URL)

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def initialize_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
) -> AsyncGenerator[SQLAlchemyUserDatabase[user.User, uuid.UUID], None]:
    yield SQLAlchemyUserDatabase(session, user.User)
