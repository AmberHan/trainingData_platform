from pydantic import BaseModel


class FileReply(BaseModel):
    path: str
    url: str
    fileSize: str

class ChunkUploadResult(BaseModel):
    path: str
    isComplete: bool