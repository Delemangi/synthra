from fastapi import APIRouter

router = APIRouter(prefix="/file-transfer", tags=["file-transfer"])


@router.post("/upload")
def upload() -> str:
    return "Upload"
