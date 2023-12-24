from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session

from .models import User
from .service import ALGORITHM, SECRET_KEY, get_user_by_username, oauth2_scheme

from .exceptions import credentials_exception


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError as err:
        raise credentials_exception from err

    user = await get_user_by_username(username=username, session=session)

    if user is None:
        raise credentials_exception

    return user
