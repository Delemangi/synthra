from pydantic import BaseModel

class FileUploaded(BaseModel):
    filename: str
    username: str

class MetadataFileResponse(BaseModel):
    name: str
    path: str
    size: int
    encrypted: bool

    class Config:
        from_attributes = True