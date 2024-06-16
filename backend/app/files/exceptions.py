from http.client import BAD_REQUEST

from fastapi import HTTPException, status

QUOTA_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Quota exausted",
)

NO_ACCESS_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access file",
)

NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="File not found",
)

BAD_REQUEST_EXCEPTION = HTTPException(
    status_code=BAD_REQUEST,
    detail="Bad request",
)
