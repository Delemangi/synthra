from fastapi import HTTPException, status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

username_taken_exception = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username already taken."
)
