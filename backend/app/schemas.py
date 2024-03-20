from pydantic import BaseModel


class RequestStatus(BaseModel):
    message: str
