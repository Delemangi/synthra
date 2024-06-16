import io
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Header, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.files.service import delete_file

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..auth.service import get_user_by_username
from ..database import get_async_session
from ..files.models import File
from ..schemas import RequestStatus
from .constants import FILE_PATH
from .schemas import FileUploaded, MetadataFileResponse
from .service import (
    create_file,
    get_all_files_user,
    get_metadata_path,
    map_mimetype,
    upload_file,
    verify_and_decrypt_file,
    verify_file,
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
        user_id=user.id,
    )

    await create_file(session, file_db)

    return "Created a test file"


# isShared is false by default (which means that everyone can see it)
@router.post("/", response_model=FileUploaded)
async def create_upload_file(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    file: UploadFile,
    password: str = Form(""),
    is_shared: bool = Form(False),
) -> FileUploaded:
    new_file = await upload_file(session, file, current_user, is_shared, password)
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
    password: str = Header(None),
) -> StreamingResponse:
    print(path)
    file: bytes = await verify_and_decrypt_file(path, current_user, session, password)
    file_object = io.BytesIO(file)

    filename = urllib.parse.quote(path)

    return StreamingResponse(
        file_object,
        media_type=map_mimetype("." + path.split(".")[-1]),
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{filename}"},
    )


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
