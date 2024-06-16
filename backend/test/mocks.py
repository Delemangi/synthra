import uuid
from datetime import UTC, datetime

from app.auth.models import User
from app.files.models import File
from app.webhooks.models import Webhook

test_user = User(id=uuid.uuid4(), username="a", password="test")  # noqa: S106

test_file = File(
    id=uuid.uuid4(),
    name="test_file.txt",
    path="test/path",
    size=1024,
    encrypted=True,
    shared=False,
    expiration=datetime(2024, 12, 31, tzinfo=UTC),
    timestamp=datetime.now(UTC),
    user_id=test_user.id,
)

test_webhook = Webhook(
    id=uuid.uuid4(),
    url="http://example.com",
    platform="Test",
    active=True,
    timestamp=datetime.now(UTC),
    user_id=test_user.id,
)
