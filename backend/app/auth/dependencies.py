from fastapi import Depends, HTTPException, status
from typing import Annotated
from .service import oauth2_scheme, SECRET_KEY, ALGORITHM, get_user_by_username
from app.database import get_async_session
from .schemas import TokenData
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[AsyncSession, Depends(get_async_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user