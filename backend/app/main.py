from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.database import initialize_database
import uvicorn
import time
import sys
from .auth.router import router as auth_router
from .file_transfer.constants import FILE_PATH
from .file_transfer.router import router as file_router

from app.settings import APISettings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("Application is starting up")
    for i in range(10):
        try:
            await initialize_database()
            break
        except Exception as ex:
            print(ex)
            time.sleep(1)
        if i == 9:
            sys.exit()

    Path.mkdir(Path(FILE_PATH), exist_ok=True)

    yield

    print("Application is shutting down")
    files = Path.rglob(Path(FILE_PATH), "*")
    for f in files:
        Path.unlink(f)


def make_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(auth_router, prefix="/auth")
    app.include_router(file_router, prefix="/files")

    @app.get("/")
    async def root() -> str:
        return "Hello World"

    return app


def run() -> None:
    app = make_app()
    settings = APISettings()
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")


if __name__ == "__main__":
    run()
