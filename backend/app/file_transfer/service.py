import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import Depends, UploadFile
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..exceptions import internal_server_error
from .constants import FILE_PATH
from .exceptions import no_access_exception, quota_exception
from .models import File
from .schemas import MetadataFileResponse


async def upload_file_unencrypted(
    session: AsyncSession,
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    if not current_user.has_remaining_quota():
        raise quota_exception

    file_path = f"{uuid.uuid4()}{file.filename}"
    path = Path(FILE_PATH) / file_path

    async with session.begin():
        contents = await file.read()
        with Path.open(path, "wb") as f:
            f.write(contents)

        file_db = File(
            name=file.filename,
            path=file_path,
            encrypted=False,
            size=file.size,
            timestamp=datetime.now(),
            expiration=datetime.now() + timedelta(days=14),
            user=current_user,
        )

        session.add(file_db)
        update_statement = (
            update(User).where(User.id == current_user.id).values(quota=User.quota - 1)
        )

        await session.execute(update_statement)


async def get_all_files_user(
    current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession
) -> list[MetadataFileResponse]:
    async with session:
        files = await session.execute(
            select(File).filter(File.user_id == current_user.id)
        )

        return [
            MetadataFileResponse(
                name=str(file.name),
                path=str(file.path),
                size=int(file.size),  # type: ignore
                encrypted=bool(file.encrypted),
            )
            for file in files.scalars()
        ]


async def verify_file(
    path: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession,
) -> str:
    async with session:
        files = await session.execute(select(File).filter(File.path == path))
        file = files.scalar_one_or_none()

        if file is None:
            raise internal_server_error

        if file.user.id == current_user.id:
            return str(file.name)

        raise no_access_exception
