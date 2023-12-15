from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from fastapi.security import OAuth2PasswordBearer

from ..repos.users import get_user_by_filter, add_user
from ..models.user import User
from ..schemas.auth.user import User as SchemaUser

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_
import os

SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def create_user(username: str, plain_password: str,
                      quota: int, session: AsyncSession) -> User:
    password = pwd_context.hash(plain_password)
    user = User(username = username, password = password, quota = quota)
    await add_user(user, session)
    return user


def verify_password(plain_password: str, password: str) -> bool:
    return pwd_context.verify(plain_password, password)


async def authenticate_user(username:str, password: str,
                            session: AsyncSession) -> User | None:
    user = await get_user_by_filter(lambda u: and_(u.username==username,
                                    verify_password(password,str(u.password)))
                              ,session)
    if not user:
        return None
    return user


def create_access_token(data: dict,
                        expires_delta: timedelta | None =
                        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

