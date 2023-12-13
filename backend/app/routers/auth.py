from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login():
    pass


@router.post("/logout")
def logout():

    pass


@router.post("/register")
def register():
    return {"message": "Register"}
