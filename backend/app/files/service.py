import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import Depends, UploadFile
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..auth.models import User
from .constants import FILE_PATH
from .exceptions import NO_ACCESS_EXCEPTION, NOT_FOUND_EXCEPTION, QUOTA_EXCEPTION
from .models import File
from .schemas import MetadataFileResponse, ShareResponse


async def upload_file_unencrypted(
    session: AsyncSession,
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
    is_shared: bool = False,
) -> str:
    if not current_user.has_remaining_quota():
        raise QUOTA_EXCEPTION

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
            user_id=current_user.id,
            shared=is_shared,
        )

        session.add(file_db)
        update_statement = (
            update(User).where(User.id == current_user.id).values(quota=User.quota - 1)
        )

        await session.execute(update_statement)

    return str(path)


async def create_file(session: AsyncSession, file: File) -> None:
    async with session:
        session.add(file)
        await session.commit()


async def get_all_files_user(
    current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession
) -> list[MetadataFileResponse]:
    async with session:
        result = await session.execute(select(File).filter(File.user_id == current_user.id))
        files = result.scalars().all()

        return [
            MetadataFileResponse(
                id=file.id,  # type: ignore[arg-type]
                name=str(file.name),
                path=str(file.path),
                size=file.size,  # type: ignore[arg-type]
                encrypted=bool(file.encrypted),
                shared=bool(file.shared),
                shared_people=[
                    ShareResponse(id=str(el.id), username=el.user.username)
                    for el in file.shared_with
                ],
                timestamp=file.timestamp,  # type: ignore[arg-type]
                expiration=file.expiration,  # type: ignore[arg-type]
            )
            for file in files
        ]


async def get_metadata_path(path: str, session: AsyncSession) -> MetadataFileResponse:
    async with session:
        files = await session.execute(select(File).filter(File.path == path))
        file = files.scalar_one_or_none()

        if file is None:
            raise NOT_FOUND_EXCEPTION

        return MetadataFileResponse(
            id=file.id,  # type: ignore[arg-type]
            name=str(file.name),
            path=str(file.path),
            size=file.size,  # type: ignore[arg-type]
            encrypted=bool(file.encrypted),
            shared=bool(file.shared),
            shared_people=[],
            timestamp=file.timestamp,  # type: ignore[arg-type]
            expiration=file.expiration,  # type: ignore[arg-type]
        )


async def verify_file(
    path: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession,
) -> str:
    async with session:
        files = await session.execute(select(File).filter(File.path == path))
        file = files.scalar_one_or_none()

        if file is None:
            raise NOT_FOUND_EXCEPTION

        if file.user.id == current_user.id:
            return str(file.name)

        if (
            bool(file.shared)
            and current_user is not None
            and str(current_user.id) not in [str(share.user_id) for share in file.shared_with]
        ):
            raise NO_ACCESS_EXCEPTION

        return str(file.name)


async def verify_file_link(
    path: str, session: AsyncSession, current_user: User | None = None
) -> str:
    async with session:
        files = await session.execute(select(File).filter(File.path == path))
        file = files.scalar_one_or_none()

        if file is None:
            raise NOT_FOUND_EXCEPTION

        if (
            bool(file.shared)
            and current_user is not None
            and str(current_user.id) not in [str(share.user_id) for share in file.shared_with]
        ):
            raise NO_ACCESS_EXCEPTION

        return str(file.name)


async def delete_file(
    path: str,
    session: AsyncSession,
) -> None:
    async with session.begin():
        await session.execute(delete(File).where(File.path == path))

    path_to_delete = Path(FILE_PATH) / path
    if path_to_delete.exists():
        path_to_delete.unlink()
    else:
        raise NOT_FOUND_EXCEPTION


async def get_file_by_id(file_id: uuid.UUID, session: AsyncSession) -> File | None:
    async with session:
        file = await session.execute(select(File).filter(File.id == file_id))
        return file.scalar_one_or_none()
