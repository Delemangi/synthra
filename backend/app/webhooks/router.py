from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from discord_webhook import DiscordWebhook

from app.auth.service import create_user, get_user_by_username
from app.database import get_async_session
from app.auth.models import User
from app.file_transfer.schemas import MetadataFileResponse
from app.file_transfer.service import get_all_files_user
from app.webhooks.schemas import CreateWebhook

router = APIRouter(tags=["webhooks"])
WEBHOOK_URL = "https://discord.com/api/webhooks/1238910641121787965/5HUf8gsJ2jLlAPxkmYAXlmsJwPTQFdfmcb0vZvqyjYU0O_Wb-wcK0kIypmBqtTpeZdkg"


@router.get("/create-test-webhook", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    webhook = DiscordWebhook(url=WEBHOOK_URL, content="Webhook Test")
    webhook.execute()
    user: User = await create_user("a", "a", 30, session)

    webhook: CreateWebhook = CreateWebhook(
        url=WEBHOOK_URL, user_id=user.id, platform="discord"
    )

    return "Created webhook and user"


@router.get("/send-webhook", response_model=str)
async def send_webhook(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    user: User | None = get_user_by_username("a", session)
    if user is None:
        return "User not found"
    user_files = get_all_files_user(user, session)
    dog_image: MetadataFileResponse = user_files[0]

    webhook = DiscordWebhook(url=WEBHOOK_URL)
    with Path(dog_image.path).open("rb") as f:
        webhook.add_file(file=f.read(), filename=dog_image.path)
    webhook.execute()
    return "Sent webhook with file"
