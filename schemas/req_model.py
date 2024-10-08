from typing import List, Optional

from pydantic import BaseModel


class ListByPageReq(BaseModel):
    page: Optional[int] = 1  # 默认值为 1
    size: Optional[int] = 5  # 默认值为 5
    like: Optional[str] = None  # 可选字符串，默认为 None
    projectId: Optional[str] = None


class StringIdReq(BaseModel):
    id: str


class DeleteListReq(BaseModel):
    id: List[str]
