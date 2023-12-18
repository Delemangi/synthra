from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..database import get_async_session
from .constants import FILE_PATH
from .schemas import FileUploaded, MetadataFileResponse
from .service import get_all_files_user, upload_file_unencrypted, verify_file

router = APIRouter(tags=["file_transfer"])


@router.post("/", response_model=FileUploaded)
async def create_upload_file(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    file: UploadFile,
) -> dict:
    await upload_file_unencrypted(session, file, current_user)
    return {"filename": file.filename, "username": current_user.username}


@router.get("/", response_model=list[MetadataFileResponse])
async def get_all_files(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list:
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


@router.get("/test")
async def test() -> str:
    return "Endpoint works"
