from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Include API routes
# app.include_router(api_main.router)

# # Include FastAPI-Users routes
# app.include_router(fastapi_users.get_auth_router(models.Token, name="token"), prefix="/auth", tags=["auth"])
# app.include_router(fastapi_users.get_register_router(name="register"), prefix="/auth", tags=["auth"])
