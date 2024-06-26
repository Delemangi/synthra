import base64
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import Depends, UploadFile
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..shares.models import Share
from .constants import FILE_PATH
from .exceptions import (
    BAD_REQUEST_EXCEPTION,
    NO_ACCESS_EXCEPTION,
    NOT_FOUND_EXCEPTION,
    QUOTA_EXCEPTION,
)
from .models import File
from .schemas import FileSecurityUpdate, MetadataFileResponse, ShareResponse


async def upload_file(
    session: AsyncSession,
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
    is_shared: bool = False,
    password: str | None = None,
) -> str:
    if not current_user.has_remaining_files_quota():
        raise QUOTA_EXCEPTION

    if not current_user.has_remaining_size_quota(file.size or 0):
        raise QUOTA_EXCEPTION

    file_path = f"{uuid.uuid4()}{file.filename}"
    path = Path(FILE_PATH) / file_path

    async with session.begin():
        contents = await file.read()

        if password is not None and password != "":
            key = derive_key(password, current_user.id.bytes)
            fernet = Fernet(key)
            contents = fernet.encrypt(contents)

        with Path.open(path, "wb") as f:
            f.write(contents)

        file_db = File(
            name=file.filename,
            path=file_path,
            encrypted=password is not None and password != "",
            size=file.size,
            timestamp=datetime.now(),
            expiration=datetime.now() + timedelta(days=14),
            user_id=current_user.id,
            shared=is_shared,
        )

        session.add(file_db)

    return str(file_path)


async def create_file(session: AsyncSession, file: File) -> None:
    async with session:
        session.add(file)
        await session.commit()


async def get_all_files_user(
    current_user: User, session: AsyncSession
) -> list[MetadataFileResponse]:
    async with session:
        result = (
            await session.execute(select(File).options(joinedload(File.user)))
            if current_user.role.name == "admin"
            else await session.execute(
                select(File).options(joinedload(File.user)).filter(File.user_id == current_user.id)
            )
        )
        files = result.scalars().all()

        return [
            MetadataFileResponse(
                id=file.id,  # type: ignore[arg-type]
                author=file.user.username,
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
        files = await session.execute(
            select(File).options(joinedload(File.user)).filter(File.path == path)
        )
        file = files.scalar_one_or_none()

        if file is None:
            raise NOT_FOUND_EXCEPTION

        return MetadataFileResponse(
            id=file.id,  # type: ignore[arg-type]
            author=file.user.username,
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
) -> tuple[str, User]:
    async with session:
        files = await session.execute(
            select(File).options(joinedload(File.user)).filter(File.path == path)
        )

        file = files.scalar_one_or_none()

        if file is None:
            raise NOT_FOUND_EXCEPTION

        if current_user.role.name == "admin" or file.user.id == current_user.id:
            return str(file.name), file.user

        if (
            bool(file.shared)
            and current_user is not None
            and str(current_user.id) not in [str(share.user_id) for share in file.shared_with]
        ):
            raise NO_ACCESS_EXCEPTION

        return str(file.name), file.user


async def verify_and_decrypt_file(
    path: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession,
    password: str | None = None,
) -> bytes:
    _, author = await verify_file(path, current_user, session)
    return decrypt_file(path, password, author)


def map_mimetype(extension: str) -> str:
    return {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".mp4": "video/mp4",
        ".avi": "video/x-msvideo",
        ".mov": "video/quicktime",
        ".wmv": "video/x-ms-wmv",
        ".txt": "text/plain",
        ".html": "text/html",
        ".csv": "text/csv",
        ".json": "application/json",
        ".xml": "application/xml",
        ".svg": "image/svg+xml",
    }.get(extension, "application/octet-stream")


async def verify_file_link(
    path: str, session: AsyncSession, current_user: User | None = None, password: str | None = None
) -> str:
    async with session:
        files = await session.execute(select(File).filter(File.path == path))
        file = files.scalar_one_or_none()

        if file is None:
            raise NOT_FOUND_EXCEPTION

        if bool(file.encrypted) and password is None:
            raise NOT_FOUND_EXCEPTION

        if (
            bool(file.shared)
            and current_user is not None
            and str(current_user.id) not in [str(share.user_id) for share in file.shared_with]
        ):
            raise NO_ACCESS_EXCEPTION

        if bool(file.encrypted) and (password is None or password == ""):
            raise NO_ACCESS_EXCEPTION

        return str(file.name)


async def delete_file(
    path: str,
    session: AsyncSession,
) -> None:
    async with session.begin():
        await session.execute(delete(File).where(File.path == path))
        await session.commit()

    path_to_delete = Path(FILE_PATH) / path
    if path_to_delete.exists():
        path_to_delete.unlink()
    else:
        raise NOT_FOUND_EXCEPTION


async def get_file_by_id(file_id: uuid.UUID, session: AsyncSession) -> File | None:
    async with session:
        file = await session.execute(select(File).filter(File.id == file_id))
        return file.scalar_one_or_none()


def decrypt_file(path: str, password: str | None, author_user: User) -> bytes:
    with Path.open(Path(FILE_PATH) / path, "rb") as f:
        contents = f.read()

    if password is None or password == "":
        return contents

    key = derive_key(password, author_user.id.bytes)
    fernet = Fernet(key)

    try:
        decoded_file = fernet.decrypt(contents)
    except InvalidToken as err:
        raise NO_ACCESS_EXCEPTION from err

    return decoded_file


def encrypt_contents(contents: bytes, password: str, current_user: User) -> bytes:
    key = derive_key(password, current_user.id.bytes)
    fernet = Fernet(key)
    return fernet.encrypt(contents)


def validate_file(file: File, security_input: FileSecurityUpdate, current_user: User) -> None:
    if str(file.user_id) != str(current_user.id) and str(current_user.role.name) != "admin":
        raise NO_ACCESS_EXCEPTION

    if bool(file.encrypted) and (
        security_input.current_password is None or security_input.current_password == ""
    ):
        raise NO_ACCESS_EXCEPTION


async def update_file_security(
    file_id: uuid.UUID,
    security_input: FileSecurityUpdate,
    current_user: User,
    session: AsyncSession,
) -> None:
    file = await get_file_by_id(file_id, session)

    if file is None:
        raise NOT_FOUND_EXCEPTION

    validate_file(file, security_input, current_user)

    if bool(file.encrypted):
        contents: bytes = decrypt_file(
            str(file.path), security_input.current_password, current_user
        )
    else:
        contents = Path.open(Path(FILE_PATH) / str(file.path), "rb").read()
    path = Path(FILE_PATH) / str(file.path)

    if (
        security_input.is_encrypted
        and security_input.new_password is not None
        and security_input.new_password != ""
    ):
        contents = encrypt_contents(contents, security_input.new_password, current_user)
        Path(path).unlink()

        with Path.open(path, "wb") as f:
            f.write(contents)

    elif bool(file.encrypted) and not security_input.is_encrypted:
        with Path.open(path, "wb") as f:
            f.write(contents)

    elif (
        not bool(file.encrypted)
        and security_input.is_encrypted
        and (security_input.new_password is None or security_input.new_password == "")
    ):
        raise BAD_REQUEST_EXCEPTION

    if bool(file.shared) and not security_input.is_shared:
        await session.execute(delete(Share).where(Share.file_id == file_id))

    await session.execute(
        update(File)
        .where(File.id == file_id)
        .values(encrypted=bool(security_input.is_encrypted), shared=security_input.is_shared)
    )

    await session.commit()


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))
