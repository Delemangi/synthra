from app.models.user import User
from fastapi import APIRouter, Depends

from app.auth.users import current_active_user

router = APIRouter(prefix="/file", tags=["file"])


@router.post("/upload")
def upload(user: User = Depends(current_active_user)) -> str:  # noqa: B008
    return str(user.id)
