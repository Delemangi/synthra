from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..schemas import RequestStatus
from .exceptions import credentials_exception
from .schemas import Token, User
from .service import (
    authenticate_user,
    create_access_token,
    create_user,
    oauth2_scheme,
    remove_token,
)

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict[str, str]:
    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise credentials_exception

    access_token = await create_access_token(session, data={"sub": str(user.username)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> RequestStatus:
    await remove_token(token, session)
    return RequestStatus(message="Logged out")


@router.post("/register")
async def register(
    user_schema: User, session: Annotated[AsyncSession, Depends(get_async_session)]
) -> RequestStatus:
    user = await create_user(user_schema.username, user_schema.password, 30, session)
    return RequestStatus(message=f"User {user.username} registered successfully")
