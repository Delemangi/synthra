from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session

from .schemas import Token, User
from .service import authenticate_user, create_access_token, create_user
from .exceptions import credentials_exception

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict:
    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise credentials_exception

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout() -> None:
    ...


@router.post("/register")
async def register(
    user: User, session: Annotated[AsyncSession, Depends(get_async_session)]
) -> dict[str, str]:
    user = await create_user(user.username, user.password, 30, session)
    return {"message": "Registered user"}
