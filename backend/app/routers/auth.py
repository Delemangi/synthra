from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.auth.token import Token
from ..schemas.auth.user import User

from ..database.database import get_async_session

from ..services.auth import authenticate_user, create_access_token, create_user

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})  # type: ignore
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
