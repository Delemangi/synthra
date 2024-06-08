from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.router import router as auth_router
from .database import run_migrations
from .files.constants import FILE_PATH
from .files.router import router as file_router
from .jobs import schedule_jobs
from .middleware import SlashNormalizerMiddleware
from .settings import APISettings
from .shares.router import router as share_router
from .webhooks.router import router as webhook_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("Starting...")

    print("Creating file storage directory...")
    Path.mkdir(Path(FILE_PATH), exist_ok=True)

    print("Running migrations...")
    run_migrations()

    print("Scheduling jobs...")
    scheduler = schedule_jobs()

    print("Server started")

    yield

    print("Shutting down...")
    scheduler.shutdown(wait=False)

    print("Server stopped")


def make_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    app.add_middleware(SlashNormalizerMiddleware)

    app.include_router(auth_router, prefix="/auth")
    app.include_router(file_router, prefix="/files")
    app.include_router(webhook_router, prefix="/webhooks")
    app.include_router(share_router, prefix="/shares")

    @app.get("/")
    async def root() -> str:
        return "Hello World"

    return app


def run() -> None:
    app = make_app()
    settings = APISettings()

    uvicorn.run(
        app, host=settings.host, port=settings.port, log_level="info", forwarded_allow_ips="*"
    )


if __name__ == "__main__":
    run()
