import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.service import get_user_by_username
from ..database import get_async_session
from ..exceptions import USER_NOT_FOUND_EXCEPTION
from ..files.service import get_all_files_user
from ..webhooks.schemas import SendWebhook
from .models import Share
from .schemas import CreateShare
from .service import create_share, delete_share

router = APIRouter(tags=["shares"])


@router.get("/test", response_model=str)
async def simple_test() -> str:
    return "Hello! The shares router is working."


@router.post("/create-test-share", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    user = await get_user_by_username("a", session)

    if user is None:
        return "Please create a test user first"

    files = await get_all_files_user(user, session)
    file = files[0]

    if file is None:
        return "Please create a test file first"

    share = Share(user_id=user.id, file_id=file.id)
    await create_share(share, session)

    return "Created a test share"


@router.post("/create", response_model=SendWebhook)
async def create_webhook_route(
    share: CreateShare,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Share:
    user = await get_user_by_username(share.username, session)

    if user is None:
        raise USER_NOT_FOUND_EXCEPTION

    share_db = Share(user_id=user.id, file_id=share.file_id)
    await create_share(share_db, session)
    return share_db


@router.delete("/delete/{share_id}", response_model=str)
async def delete(
    share_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    await delete_share(share_id, session)
    return "Share deleted"
