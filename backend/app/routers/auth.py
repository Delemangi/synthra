from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login() -> None:
    ...


@router.post("/logout")
def logout() -> None:
    ...


@router.post("/register")
def register() -> dict[str, str]:
    return {"message": "Register"}
