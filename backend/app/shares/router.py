import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import get_user_by_username
from app.files.constants import FILE_PATH
from app.files.models import File
from app.files.service import create_file
from app.webhooks.schemas import SendWebhook

from ..database import get_async_session
from .models import Share
from .schemas import CreateShare
from .service import create_share, delete_share

router = APIRouter(tags=["shares"])


@router.get("/create-test-share", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    print("Creating file")
    path = Path(FILE_PATH) / "example.txt"
    binary = Path.open(path, "wb")
    binary.write(b"This is a new file.")
    binary.close()
    binary = Path.open(path, "rb")
    print("created file")
    file = UploadFile(file=binary)
    file_db = File(
        ame=file.filename,
        path="example.txt",
        encrypted=False,
        size=file.size,
        timestamp=datetime.now(),
        expiration=datetime.now() + timedelta(days=14),
        user=get_user_by_username("a", session),
    )
    try:
        print("adding file to db")
        await create_file(session, file_db)
    except Exception:
        print("Error creating file maybe it already exists")

    return "Created an example file share with a"


@router.post("/create", response_model=SendWebhook)
async def create_webhook_route(
    share: CreateShare,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Share:
    user = await get_user_by_username(share.username, session)
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
