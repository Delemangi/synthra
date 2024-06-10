import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.webhooks.service import (
    create_webhook,
    delete_webhook,
    get_all_webhooks_for_user,
    get_webhook_by_id,
    send_webhook_file,
)

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..auth.service import get_user_by_username
from ..database import get_async_session
from ..files.service import get_all_files_user, get_file_by_id
from ..webhooks.models import Webhook
from ..webhooks.schemas import CreateWebhook, SendWebhook

router = APIRouter(tags=["webhooks"])

WEBHOOK_URL = os.getenv(
    "WEBHOOK_EXAMPLE_URL", "Enter the webhook url here to test the webhook functionality."
)


@router.get("/test", response_model=str)
async def simple_test() -> str:
    return "Hello! The webhooks router is working."


@router.post("/create-test-webhook", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    user = await get_user_by_username("a", session)
    webhook = CreateWebhook(url=WEBHOOK_URL, platform="Test")

    if user is None:
        return "Please create a test user first"

    await create_webhook(webhook, session, user.id)  # type: ignore[arg-type]

    return "Created a test webhook"


@router.post("/send-test-webhook", response_model=str)
async def send_webhook(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    async with session:
        user = await get_user_by_username("a", session)

        if user is None:
            return "Please create a test user first"

        user_files = await get_all_files_user(user, session)
        file = user_files[0]
        user_webhook = user.webhooks[0]

        await send_webhook_file(user_webhook, file)

    return "Sent the test file to the test webhook"


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
