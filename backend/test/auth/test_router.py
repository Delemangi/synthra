import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from ..constants import HTTP_SUCCESS, HTTP_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_simple_test(async_client: AsyncClient) -> None:
    response = await async_client.get("/auth/test")

    assert response.status_code == HTTP_SUCCESS
    assert response.json() == "Hello! The auth router is working."


@pytest.mark.anyio
async def test_logout(async_client: AsyncClient) -> None:
    with patch("app.auth.service.remove_token", new_callable=AsyncMock):
        headers = {"Authorization": "Bearer test-token"}
        response = await async_client.post("/auth/logout", headers=headers)

        assert response.status_code == HTTP_SUCCESS
        assert response.json() == {"message": "Logged out"}


@pytest.mark.anyio
async def test_register_wrong_data(async_client: AsyncClient) -> None:
    with patch("app.auth.service.create_user", new_callable=AsyncMock) as mock_create_user:
        mock_create_user.return_value = {"username": "test-user"}

        form_data = {"username": "test-user", "password": "test-pass"}
        headers = {"Content-Type": "application/json"}

        response = await async_client.post(
            "/auth/register", json=json.dumps(form_data), headers=headers
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY
