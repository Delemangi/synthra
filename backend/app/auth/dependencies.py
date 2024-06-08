import datetime
from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from .constants import ALGORITHM
from .exceptions import CREDENTIALS_EXCEPTION
from .models import User
from .service import (
    SECRET_KEY,
    get_user_by_username,
    oauth2_scheme,
    validate_token,
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if not (await validate_token(token, session)):
            raise CREDENTIALS_EXCEPTION

        if username is None:
            raise CREDENTIALS_EXCEPTION

        date_expir: int | None = payload.get("exp")
        if date_expir is None or date_expir < datetime.datetime.now().timestamp():
            raise CREDENTIALS_EXCEPTION

    except JWTError as err:
        raise CREDENTIALS_EXCEPTION from err

    user = await get_user_by_username(username=username, session=session)

    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user
