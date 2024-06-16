from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..schemas import RequestStatus
from .dependencies import get_current_user
from .exceptions import AUTHENTICATION_2FA_EXCEPTION, CREDENTIALS_EXCEPTION
from .models import User as DbUser
from .schemas import Code2FA, RoleMetadata, Token, UpdateRole, User, UserMetadata
from .service import (
    authenticate_user,
    create_access_token,
    create_user,
    edit_role_quotas,
    get_roles,
    oauth2_scheme,
    remove_2fa_code,
    remove_token,
    update_2fa_code,
    verify_2fa_code,
)

router = APIRouter(tags=["auth"])


@router.get("/test", response_model=str)
async def simple_test() -> str:
    return "Hello! The auth router is working."


@router.post("/create-test-user", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    await create_user("a", "a", session)

    return "Created a test user"


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    code_2fa: str = Form(None),
) -> dict[str, str]:
    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise CREDENTIALS_EXCEPTION

    if not verify_2fa_code(user, code_2fa):
        raise AUTHENTICATION_2FA_EXCEPTION

    access_token = await create_access_token(session, data={"sub": str(user.username)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/get-sharex-token", response_model=Token)
async def get_sharex_token(
    current_user: Annotated[DbUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict[str, str]:
    expires_delta = timedelta(days=365 * 10)

    access_token = await create_access_token(
        session, data={"sub": str(current_user.username)}, expires_delta=expires_delta
    )
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
    user = await create_user(user_schema.username, user_schema.password, session)
    return RequestStatus(message=f"User {user.username} registered successfully")


@router.post("/2fa")
async def get_2fa_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Code2FA:
    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise CREDENTIALS_EXCEPTION

    code_2fa = await update_2fa_code(user, session)

    return Code2FA(code=code_2fa)


@router.post("/2fa/disable")
async def disable_2fa(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> RequestStatus:
    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise CREDENTIALS_EXCEPTION

    await remove_2fa_code(user, session)

    return RequestStatus(message="2FA disabled successfully")


@router.get("/fetch_user_data", response_model=UserMetadata)
async def fetch_user_data(
    current_user: Annotated[DbUser, Depends(get_current_user)],
) -> UserMetadata:
    return UserMetadata(
        username=str(current_user.username),
        role=str(current_user.role.name),
        files_quota=int(current_user.role.quota_files),
        size_quota=int(current_user.role.quota_size),
        is_2fa_enabled=(current_user.code_2fa is not None),
    )


@router.get("/roles", response_model=list[RoleMetadata])
async def roles(
    current_user: Annotated[DbUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[RoleMetadata]:
    roles = await get_roles(current_user, session)

    return [
        RoleMetadata(
            id=str(role.id),
            name=str(role.name),
            quota_size=int(role.quota_size),  # type: ignore
            quota_files=int(role.quota_files),  # type: ignore
        )
        for role in roles
    ]


@router.post("/roles/edit")
async def edit_role(
    update_input: UpdateRole,
    current_user: Annotated[DbUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> RequestStatus:
    await edit_role_quotas(
        current_user,
        update_input.role_id,  # type: ignore
        update_input.size,
        update_input.files,
        session,
    )

    return RequestStatus(message="Role quotas updated successfully")
