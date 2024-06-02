import uuid
from pathlib import Path

from discord_webhook import DiscordWebhook
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.file_transfer.models import File
from app.file_transfer.schemas import MetadataFileResponse
from app.webhooks.models import Webhook
from app.webhooks.schemas import CreateWebhook


async def create_webhook(
    webhook_schema: CreateWebhook, session: AsyncSession, user_id: UUID
) -> Webhook:
    async with session:
        webhook = Webhook(**webhook_schema.model_dump())
        webhook.user_id = user_id  # type: ignore[assignment]
        webhook.active = True  # type: ignore[assignment]

        session.add(webhook)
        await session.commit()

        return webhook


async def get_webhook_by_id(webhook_id: uuid.UUID, session: AsyncSession) -> Webhook | None:
    async with session:
        webhook = await session.execute(select(Webhook).filter(Webhook.id == webhook_id))
        return webhook.scalar_one_or_none()


async def add_webhook(webhook: Webhook, session: AsyncSession) -> None:
    async with session:
        session.add(webhook)
        await session.commit()


async def delete_webhook(webhook_id: uuid.UUID, session: AsyncSession) -> None:
    async with session:
        await session.execute(delete(Webhook).where(Webhook.id == webhook_id))
        await session.commit()


async def send_webhook_file(webhook: Webhook, file_data: File | MetadataFileResponse) -> None:
    discord_webhook = DiscordWebhook(url=str(webhook.url))

    with Path(file_data.full_path()).open("rb") as f:
        discord_webhook.add_file(file=f.read(), filename=str(file_data.name))

    discord_webhook.execute()


async def get_all_webhooks_for_user(user_id: uuid.UUID, session: AsyncSession) -> list[Webhook]:
    async with session:
        webhooks = await session.execute(select(Webhook).filter(Webhook.user_id == user_id))

        return list(webhooks.scalars().all())
