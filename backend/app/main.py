from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .auth.router import router as auth_router
from .database import initialize_database, run_migrations
from .files.constants import FILE_PATH
from .files.router import router as file_router
from .jobs import schedule_jobs
from .middleware import SlashNormalizerMiddleware
from .settings import APISettings
from .shares.router import router as share_router
from .webhooks.router import router as webhook_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("Starting...", flush=True)

    print("Creating file storage directory...", flush=True)
    Path(FILE_PATH).mkdir(parents=True, exist_ok=True)
    print("File storage directory created", flush=True)

    print("Running migrations...", flush=True)
    run_migrations()
    print("Migrations complete", flush=True)

    print("Initializing database...", flush=True)
    await initialize_database()
    print("Database initialized", flush=True)

    print("Scheduling jobs...", flush=True)
    scheduler = schedule_jobs()
    print("Jobs scheduled", flush=True)

    print("Server started", flush=True)

    yield

    print("Shutting down...", flush=True)

    print("Stopping jobs...", flush=True)
    scheduler.shutdown(wait=False)
    print("Jobs stopped", flush=True)

    print("Server stopped", flush=True)


def make_app() -> FastAPI:
    # set debug=True to enable verbose logging
    app = FastAPI(lifespan=lifespan)

    # URL Normalizer Middleware
    app.add_middleware(SlashNormalizerMiddleware)

    app.include_router(auth_router, prefix="/auth")
    app.include_router(file_router, prefix="/files")
    app.include_router(webhook_router, prefix="/webhooks")
    app.include_router(share_router, prefix="/shares")

    @app.get("/")
    async def root() -> str:
        return "Hello! The application is running."

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    return app


def run() -> None:
    app = make_app()
    settings = APISettings()

    uvicorn.run(
        app, host=settings.host, port=settings.port, log_level="info", forwarded_allow_ips="*"
    )


if __name__ == "__main__":
    run()
