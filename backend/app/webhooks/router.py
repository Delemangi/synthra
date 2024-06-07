import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.service import create_user, get_user_by_username
from app.files.schemas import MetadataFileResponse
from app.files.service import get_all_files_user, get_file_by_id
from app.webhooks.models import Webhook
from app.webhooks.schemas import CreateWebhook, SendWebhook
from app.webhooks.service import (
    create_webhook,
    delete_webhook,
    get_all_webhooks_for_user,
    get_webhook_by_id,
    send_webhook_file,
)

from ..database import get_async_session

router = APIRouter(tags=["webhooks"])

WEBHOOK_URL = os.getenv(
    "WEBHOOK_EXAMPLE_URL", "Enter the webhook url here to test the webhook functionality."
)


@router.get("/create-test-webhook", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    print("creating user")
    user: User = await create_user("a", "a", 30, session)
    webhook = CreateWebhook(url=WEBHOOK_URL, platform="discord")
    try:
        await create_webhook(webhook, session, user.id)  # type: ignore[arg-type]
    except Exception:
        print("error creating webhook")

    return "Created webhook and user"


@router.get("/send-test-webhook", response_model=str)
async def send_webhook(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    async with session:
        user: User | None = await get_user_by_username("a", session)
        if user is None:
            return "User not found"

        user_files = await get_all_files_user(user, session)
        dog_image: MetadataFileResponse = user_files[0]
        user_webhook = user.webhooks[0]
        await send_webhook_file(user_webhook, dog_image)
    return "Sent webhook with file"


@router.post("/create", response_model=SendWebhook)
async def create_webhook_route(
    webhook: CreateWebhook,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Webhook:
    return await create_webhook(webhook, session, current_user.id)  # type: ignore[arg-type]


@router.post("/send", response_model=str)
async def send_webhook_route(
    webhook_id: uuid.UUID,
    file_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    webhook = await get_webhook_by_id(webhook_id, session)
    if webhook is None:
        raise HTTPException(status_code=404, detail="Webhook not found")

    file_data = await get_file_by_id(file_id, session)
    if file_data is None:
        raise HTTPException(status_code=404, detail="File not found")

    await send_webhook_file(webhook, file_data)
    return "Sent webhook with file"


@router.get("/user-webhooks", response_model=list[SendWebhook])
async def get_user_webhooks(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[Webhook]:
    return await get_all_webhooks_for_user(current_user.id, session)  # type: ignore[arg-type]


@router.delete("/delete/{webhook_id}", response_model=str)
async def delete(
    webhook_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    await delete_webhook(webhook_id, session)
    return "Webhook deleted"
