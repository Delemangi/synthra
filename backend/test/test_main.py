import pytest
from httpx import AsyncClient

from .constants import HTTP_SUCCESS


@pytest.mark.anyio
async def test_root(async_client: AsyncClient) -> None:
    response = await async_client.get("/")

    assert response.status_code == HTTP_SUCCESS
