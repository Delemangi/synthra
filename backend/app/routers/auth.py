from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .models.auth.token import Token
from .models.auth.user import User, UserInDB

from .helpers.auth_helpers import authenticate_user, create_access_token

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/logout")
def logout() -> None:
    ...


@router.post("/register")
def register() -> dict[str, str]:
    return {"message": "Register"}


