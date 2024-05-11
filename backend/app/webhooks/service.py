import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.webhooks.schemas import CreateWebhook
from app.webhooks.models import Webhook

from sqlalchemy import select, delete


async def create_webhook(
    webhook: CreateWebhook,
    session: AsyncSession,
) -> Webhook:
    async with session:
        webhook = Webhook(**webhook.dict())

        session.add(webhook)
        await session.commit()
        return webhook


async def get_user_webhooks(
    user_id: uuid.UUID,
    session: AsyncSession,
) -> list[Webhook]:
    async with session:
        webhooks = await session.execute(
            select(Webhook).filter(Webhook.user_id == user_id)
        )
        return webhooks.scalars().all()


async def get_webhook_by_id(
    webhook_id: uuid.UUID, session: AsyncSession
) -> Webhook | None:
    async with session:
        webhook = await session.execute(
            select(Webhook).filter(Webhook.id == webhook_id)
        )
        return webhook.scalar_one_or_none()


async def add_webhook(webhook: Webhook, session: AsyncSession) -> None:
    async with session:
        session.add(webhook)
        await session.commit()


async def delete_webhook(webhook_id: uuid.UUID, session: AsyncSession) -> None:
    async with session:
        await session.execute(delete(Webhook).where(Webhook.id == webhook_id))
        await session.commit()
