from typing import Annotated

from fastapi import Depends, File, UploadFile

from app.auth.dependencies import get_current_user
from app.auth.models import User
from .models import File
from .constants import FILE_PATH
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from .schemas import MetadataFileResponse

quota_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Quota exausted",
)
no_access_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access file",
)


async def upload_file_unencrypted(
    current_user: User, session: AsyncSession, file: UploadFile
):
    if current_user.quota == 0:
        raise quota_exception
    file_path = str(uuid.uuid4()) + file.filename
    path = FILE_PATH + file_path
    try:
        contents = file.file.read()
        with open(path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise e
    finally:
        file.file.close()
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
    current_user.quota -= 1
    await session.commit()


async def get_all_files_user(current_user: User, session: AsyncSession):
    files = await session.execute(select(File).filter(File.user_id == current_user.id))

    file_responses = []
    for file in files.scalars():
        file_response = MetadataFileResponse(
            name=file.name,
            path=file.path,
            size=file.size,
            encrypted=file.encrypted,
        )
        file_responses.append(file_response)

    return file_responses


async def verify_file(path: str, current_user: User, session: AsyncSession):
    file = await session.execute(select(File).filter(File.path == path))
    file = file.scalar_one_or_none()
    if file.user.id == current_user.id:
        return file.name
    else:
        raise no_access_exception
