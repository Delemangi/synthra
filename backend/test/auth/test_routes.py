import json
from unittest.mock import AsyncMock, patch, ANY

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_simple_test(async_client):
    response = await async_client.get("/auth/test")
    assert response.status_code == 200
    assert response.json() == "Hello! The auth router is working."


@pytest.mark.anyio
async def test_logout(async_client: AsyncClient):
    with patch("app.auth.service.remove_token", new_callable=AsyncMock):
        headers = {"Authorization": f"Bearer test-token"}
        response = await async_client.post("/auth/logout", headers=headers)

        assert response.status_code == 200  # Check that the response status is 200
        assert response.json() == {"message": "Logged out"}


@pytest.mark.anyio
async def test_register_wrong_data(async_client: AsyncClient):
    with patch("app.auth.service.create_user", new_callable=AsyncMock) as mock_create_user:
        mock_create_user.return_value = {"username": "test-user"}

        form_data = {"username": "test-user", "password": "test-pass"}
        headers = {"Content-Type": "application/json"}

        response = await async_client.post("/auth/register", json=json.dumps(form_data), headers=headers)
        assert response.status_code == 422
