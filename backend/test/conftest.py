from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import make_app  # Adjust the import to the correct path for your make_app function
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.dependencies import get_current_user
from app.auth.models import User
import uuid
import asyncio

pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# @pytest.fixture(scope="module")
# def event_loop():
#     return asyncio.get_event_loop()

app = make_app()


def get_mock_async_session() -> AsyncGenerator[AsyncSession, None]:
    yield AsyncMock(spec=AsyncSession)


def get_mock_current_user() -> User:
    test_user = User(id=uuid.uuid4(), username="a", password="test")
    return test_user


app.dependency_overrides[get_async_session] = get_mock_async_session
app.dependency_overrides[get_current_user] = get_mock_current_user


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c




@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
