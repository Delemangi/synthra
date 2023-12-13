import os
import uuid
from collections.abc import AsyncGenerator
from typing import Self

from app.database.database import get_user_db
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.models.user import User

SECRET = os.getenv("SECRET", "SECRET")

if SECRET == "SECRET":  # noqa: S105
    print("You should set the SECRET environment variable")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self: Self, user: User, _: Request | None = None
    ) -> None:
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self: Self, user: User, token: str, _: Request | None = None
    ) -> None:
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self: Self, user: User, token: str, _: Request | None = None
    ) -> None:
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),  # noqa: B008
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
