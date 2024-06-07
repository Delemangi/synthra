import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.shares.models import Share


async def create_share(share: Share, session: AsyncSession) -> None:
    async with session:
        session.add(share)
        await session.commit()


async def get_share_by_id(webhook_id: uuid.UUID, session: AsyncSession) -> Share | None:
    async with session:
        share = await session.execute(select(Share).filter(Share.id == webhook_id))
        return share.scalar_one_or_none()


async def delete_share(webhook_id: uuid.UUID, session: AsyncSession) -> None:
    async with session:
        await session.execute(delete(Share).where(Share.id == webhook_id))
        await session.commit()


async def get_user_list(file_id: uuid.UUID, session: AsyncSession) -> list[User]:
    async with session:
        users = await session.execute(select(User).join(Share).filter(Share.file_id == file_id))
        return list(users.scalars().all())
