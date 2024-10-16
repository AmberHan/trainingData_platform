from typing import List, Optional

from pydantic import BaseModel


class ListByPageReq(BaseModel):
    page: Optional[int] = 1  # 默认值为 1
    size: Optional[int] = 5  # 默认值为 5
    like: Optional[str] = None  # 可选字符串，默认为 None
    projectId: Optional[str] = None


class DataFileListByPageReq(BaseModel):
    page: Optional[int] = 1  # 默认值为 1
    size: Optional[int] = 5  # 默认值为 5
    fileType: Optional[int] = 1
    dataId: Optional[str] = None


class StringIdReq(BaseModel):
    id: str


class DeleteListReq(BaseModel):
    id: List[str]


class DownloadParams(BaseModel):
    workId: Optional[str] = None
    modelName: Optional[str] = None
    path: Optional[str] = None


class UploadParams(BaseModel):
    chunkId: Optional[int] = None
    fileName: Optional[str] = None
    fileMd5: Optional[str] = None
