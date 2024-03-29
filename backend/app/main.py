from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import initialize_database
import uvicorn
import time
import sys

from .auth.router import router as auth_router
from .file_transfer.constants import FILE_PATH
from .file_transfer.router import router as file_router
from app.settings import APISettings

from .constants import MAX_DB_CONNECTION_ATTEMPTS

from .jobs import schedule_jobs


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("Application is starting up")
    for i in range(10):
        try:
            await initialize_database()
            print("Database initialized...")
            break
        except Exception as ex:
            print(ex)
            time.sleep(1)
        if i == MAX_DB_CONNECTION_ATTEMPTS - 1:
            sys.exit()
    Path.mkdir(Path(FILE_PATH), exist_ok=True)

    scheduler = schedule_jobs()

    yield

    print("Application is shutting down")
    files = Path.rglob(Path(FILE_PATH), "*")
    for f in files:
        Path.unlink(f)
    scheduler.shutdown(wait=False)


def make_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
