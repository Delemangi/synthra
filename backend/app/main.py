from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.database import initialize_database

from .auth.router import router as auth_router
from .file_transfer.constants import FILE_PATH
from .file_transfer.router import router as file_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("Application is starting up")
    await initialize_database()
    Path.mkdir(Path(FILE_PATH), exist_ok=True)

    yield

    print("Application is shutting down")
    files = Path.rglob(Path(FILE_PATH), "*")
    for f in files:
        Path.unlink(f)


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
app.include_router(file_router, prefix="/files")


@app.get("/")
async def root() -> str:
    return "Hello World"
