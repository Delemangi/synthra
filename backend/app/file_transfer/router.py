from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from app.database import get_async_session
from app.auth.dependencies import get_current_user
from app.auth.models import User

from .schemas import FileUploaded, MetadataFileResponse
from .service import upload_file_unencrypted, get_all_files_user, verify_file
from .constants import FILE_PATH


router = APIRouter(tags=["file_transfer"])


@router.post("/", response_model=FileUploaded)
async def create_upload_file(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    file: UploadFile,
) -> dict:
    await upload_file_unencrypted(current_user, session, file)
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
