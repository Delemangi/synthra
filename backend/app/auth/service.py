import os
from collections.abc import Callable
from datetime import datetime, timedelta
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from .models import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SECRET")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def create_user(
    username: str, plain_password: str, quota: int, session: AsyncSession
) -> User:
    password = pwd_context.hash(plain_password)
    user = User(username=username, password=password, quota=quota)
    await add_user(user, session)
    return user


def verify_password(plain_password: str, password: str) -> bool:
    return pwd_context.verify(plain_password, password)


async def authenticate_user(
    username: str, password: str, session: AsyncSession
) -> User | None:
    user = await get_user_by_username(username, session)

    if not user:
        return None

    stored_password = str(user.password)
    is_password_correct = verify_password(password, stored_password)

    if not is_password_correct:
        return None

    return await get_user_by_filter(
        lambda u: and_(u.username == username, u.password == stored_password),
        session,
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def add_user(user: User, session: AsyncSession) -> None:
    session.add(user)
    await session.commit()


async def get_user_by_filter(
    user_filter: Callable, session: AsyncSession
) -> User | None:
    async with session:
        users = await session.execute(select(User).filter(lambda: user_filter(User)))
        return users.scalar_one_or_none()


async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User | None:
    async with session:
        users = await session.execute(select(User).filter(User.id == user_id))
        return users.scalar_one_or_none()


async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    async with session:
        users = await session.execute(select(User).filter(User.username == username))
        return users.scalar_one_or_none()
