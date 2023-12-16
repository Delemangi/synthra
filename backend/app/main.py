from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
import os
import glob

from app.database import initialize_database

from .auth.router import router as auth_router
from .file_transfer.router import router as file_router

from .file_transfer.constants import FILE_PATH

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("Application is starting up")
    await initialize_database()
    os.mkdir(FILE_PATH)
    yield
    print("Application is shutting down")
    files = glob.glob(FILE_PATH)
    for f in files:
        os.remove(f)


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
app.include_router(file_router, prefix="/files")


@app.get("/")
async def root() -> str:
    return "Hello World"
