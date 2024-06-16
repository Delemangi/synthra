from fastapi import HTTPException, status

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

EXPIRED_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expired credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

USERNAME_TAKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username already taken."
)

AUTHENTICATION_2FA_EXCEPTION = HTTPException(
    status_code=status.HTTP_302_FOUND, detail="User found. 2FA authentication required."
)

NO_PERMISSION_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="You don't have enough permissions."
)
