from unittest.mock import AsyncMock, patch, ANY

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import make_app  # Adjust the import to the correct path for your make_app function

app = make_app()


@pytest.mark.anyio
async def test_simple_test(async_client):
    response = await async_client.get("/auth/test")
    assert response.status_code == 200
    assert response.json() == "Hello! The auth router is working."


@pytest.mark.anyio
async def test_logout(async_client: AsyncClient):
    # Create a mock session with necessary methods mocked
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = None  # Mock execute to return None

    # Create a coroutine function to yield the mock session
    async def mock_get_async_session_override():
        yield mock_session

    # Patch the remove_token function and get_async_session dependency
    with patch("app.auth.service.remove_token", new_callable=AsyncMock) as mock_remove_token:
        with patch("app.database.get_async_session", mock_get_async_session_override):
            # Mock the OAuth2 password bearer scheme
            with patch("app.auth.router.oauth2_scheme", return_value="test-token"):
                # Use the token to log out
                headers = {"Authorization": f"Bearer test-token"}
                response = await async_client.post("/auth/logout", headers=headers)

                # Assert the response
                assert response.status_code == 200
                assert response.json() == {"message": "Logged out"}

                # Assert that remove_token was called once with the correct arguments
                mock_remove_token.assert_called_once_with("test-token", mock_session)
