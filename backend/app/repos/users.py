
from ..models.user import User

from uuid import UUID
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def add_user(user: User,
                   session: AsyncSession) -> None:
    session.add(user)
    await session.commit()

async def get_user_by_filter(user_filter: Callable,
                   session: AsyncSession) -> User:
    users = await session.execute(select(User)
                                    .filter(lambda: user_filter(User)))

    return users.first()

async def get_user_by_id(user_id: UUID,
                   session: AsyncSession) -> User:
    users = await session.execute(select(User)
                                    .filter(User.id == user_id))

    return users.first()


async def get_user_by_username(username: str,
                   session: AsyncSession) -> User:
    users = await session.execute(select(User)
        .filter(User.username == username and User.password))

    return users.first()
