from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..database import get_async_session
from ..schemas import RequestStatus
from .constants import FILE_PATH
from .schemas import FileUploaded, MetadataFileResponse
from .service import (
    delete_file,
    get_all_files_user,
    upload_file_unencrypted,
    verify_file,
)

router = APIRouter(tags=["file_transfer"])


# /files/..
@router.post("/", response_model=FileUploaded)
async def create_upload_file(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    file: UploadFile,
) -> FileUploaded:
    await upload_file_unencrypted(session, file, current_user)
    return FileUploaded(filename=file.filename, username=str(current_user.username))


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
    # Return the file using FileResponse
    return FileResponse(FILE_PATH + path, filename=filename)


@router.delete("/{path}", response_model=RequestStatus)
async def verify_and_delete_file(
    path: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> RequestStatus:
    filename = await verify_file(path, current_user, session)
    # Return the file using FileResponse
    await delete_file(path, session)

    return RequestStatus(message=f"File {filename} deleted")


@router.get("/test")
async def test() -> str:
    return "Endpoint works"
