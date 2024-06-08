from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..auth.service import get_user_by_username
from ..database import get_async_session
from ..files.models import File
from ..schemas import RequestStatus
from .constants import FILE_PATH
from .schemas import FileUploaded, IsShared, MetadataFileResponse
from .service import (
    create_file,
    delete_file,
    get_all_files_user,
    get_metadata_path,
    upload_file_unencrypted,
    verify_file,
    verify_file_link,
)

router = APIRouter(tags=["files"])


@router.get("/test", response_model=str)
async def simple_test() -> str:
    return "Hello! The files router is working."


@router.post("/create-test-file", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    file_name = "a.txt"

    path = Path(FILE_PATH) / file_name

    binary = Path.open(path, "wb")
    binary.write(b"a")
    binary.close()

    user = await get_user_by_username("a", session)

    if user is None:
        return "Please create a test user first"

    file_db = File(
        name=file_name,
        path=file_name,
        encrypted=False,
        size=1,
        timestamp=datetime.now(),
        expiration=datetime.now() + timedelta(days=14),
        user=user,
    )

    await create_file(session, file_db)

    return "Created a test file"


@router.post("/", response_model=FileUploaded)
async def create_upload_file(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    file: UploadFile,
    is_shared: IsShared,
) -> FileUploaded:
    new_file = await upload_file_unencrypted(session, file, current_user, is_shared.is_shared)
    return FileUploaded(filename=new_file, username=str(current_user.username))


@router.get("/", response_model=list[MetadataFileResponse])
async def get_all_files(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[MetadataFileResponse]:
    return await get_all_files_user(current_user, session)


@router.get("/download/{path}")
async def get_file(
    path: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> FileResponse:
    filename = await verify_file(path, current_user, session)
    return FileResponse(FILE_PATH + path, filename=filename)


@router.get("/download-link/{path}")
async def get_file_link(
    path: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> FileResponse:
    filename = await verify_file_link(path, session, current_user)
    return FileResponse(FILE_PATH + path, filename=filename)


@router.get("/metadata/{path}", response_model=MetadataFileResponse)
async def get_file_metadata(
    path: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> MetadataFileResponse:
    return await get_metadata_path(path, session)


@router.delete("/{path}", response_model=RequestStatus)
async def verify_and_delete_file(
    path: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> RequestStatus:
    filename = await verify_file(path, current_user, session)
    await delete_file(path, session)
    return RequestStatus(message=f"File {filename} deleted")
