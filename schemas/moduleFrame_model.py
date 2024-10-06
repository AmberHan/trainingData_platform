from typing import List

from pydantic import BaseModel

from sqlmodels.moduleFrame import ModuleFrame as ModuleFrameSql


class GetModuleFrameReply(BaseModel):
    id: str
    frameName: str

    @classmethod
    def from_orm(cls, frame: ModuleFrameSql) -> 'GetModuleFrameReply':
        return GetModuleFrameReply(
            id=frame.Id,
            frameName=frame.FrameName
        )


class GetModuleFrameListReply(BaseModel):
    list: List[GetModuleFrameReply] = []
