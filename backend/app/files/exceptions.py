from fastapi import HTTPException, status

quota_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Quota exausted",
)

no_access_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access file",
)

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="File not found",
)
