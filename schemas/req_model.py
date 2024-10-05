from typing import List

from pydantic import BaseModel


class StringIdReq(BaseModel):
    id: str


class DeleteListReq(BaseModel):
    id: List[str]
