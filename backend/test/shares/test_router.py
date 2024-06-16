import uuid
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from ..constants import HTTP_SUCCESS


@pytest.mark.anyio
async def test_simple_test(async_client: AsyncClient) -> None:
    response = await async_client.get("/shares/test")

    assert response.status_code == HTTP_SUCCESS
    assert response.json() ==  "Hello! The shares router is working."


@pytest.mark.anyio
async def test_delete_nonexistant_file(async_client: AsyncClient) -> None:
    with patch("app.shares.service.delete_share", new_callable=AsyncMock):
        response = await async_client.delete(f"/shares/delete/{uuid.UUID('00000000-0000-0000-0000-000000000000')}")

        assert response.status_code == 200
