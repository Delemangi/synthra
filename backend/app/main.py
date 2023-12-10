from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("Application is starting up")
    await initialize_database()
    yield
    print("Application is shutting down")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> str:
    return "Hello World"
