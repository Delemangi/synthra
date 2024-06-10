import asyncio
import uuid
from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.database import get_async_session
from app.main import make_app

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()


app = make_app()


def get_mock_async_session() -> Generator[AsyncMock, None, None]:
    yield AsyncMock(spec=AsyncSession)


def get_mock_current_user() -> User:
    return User(id=uuid.uuid4(), username="a", password="test")  # noqa: S106


app.dependency_overrides[get_async_session] = get_mock_async_session
app.dependency_overrides[get_current_user] = get_mock_current_user


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac: # type: ignore[arg-type]
        yield ac
