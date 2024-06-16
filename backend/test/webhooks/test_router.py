from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from ..constants import HTTP_SUCCESS
from ..mocks import test_webhook

# @pytest.mark.anyio
# async def test_create_webhook_route(async_client: AsyncClient):
#     with patch("app.webhooks.service.create_webhook", return_value=test_webhook) as mock_create_webhook:
#         headers = {
#             "authorization": "Bearer test_token",
#             "Accept": "application/json",
#             "Content-Type": "application/json"
#         }
#         json_content = {"url": "test", "platform": "Test"}
#
#         response = await async_client.post("/webhooks/create", json=json_content, headers=headers)
#         assert response.status_code == 200
#         response_json = response.json()
#         assert response_json["url"] == "http://example.com"
#         assert response_json["platform"] == "Test"
#         assert response_json["active"] == True
#         assert "id" in response_json
#         assert "timestamp" in response_json


# @pytest.mark.anyio
# async def test_send_webhook_route(async_client: AsyncClient, mocker: ...) -> None:
#     test_webhook = {}
#     test_file = {}

#     mock_get_webhook = mocker.patch(
#         "app.webhooks.service.get_webhook_by_id", new_callable=AsyncMock
#     )
#     mock_get_file = mocker.patch("app.files.service.get_file_by_id", new_callable=AsyncMock)
#     mock_send_webhook = mocker.patch(
#         "app.webhooks.service.send_webhook_file", new_callable=AsyncMock
#     )

#     mock_get_webhook.return_value = test_webhook
#     mock_get_file.return_value = test_file
#     mock_send_webhook.return_value = None

#     response = await async_client.post(
#         "/webhooks/send", params={"webhook_id": str(uuid.uuid4()), "file_id": str(uuid.uuid4())}
#     )

#     assert response.status_code == HTTP_SUCCESS
#     assert response.json() == "Sent webhook with file"


@pytest.mark.anyio
async def test_delete_webhook(async_client: AsyncClient) -> None:
    with patch("app.webhooks.service.delete_webhook", new_callable=AsyncMock) as _:
        response = await async_client.delete(f"/webhooks/delete/{test_webhook.id}")

        assert response.status_code == HTTP_SUCCESS
        assert response.json() == "Webhook deleted"


@pytest.mark.anyio
async def test_simple_test(async_client: AsyncClient) -> None:
    response = await async_client.get("/webhooks/test")

    assert response.status_code == HTTP_SUCCESS
    assert response.json() == "Hello! The webhooks router is working."
