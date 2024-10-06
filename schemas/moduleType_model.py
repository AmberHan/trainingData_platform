from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.moduleType import ModuleType as ModuleTypeSql


class ModuleType(BaseModel):
    id: Optional[str] = None
    moduleTypeName: Optional[str] = None
    createWay: Optional[str] = None
    icon: Optional[str] = None
    createTime: Optional[str] = None


class GetModuleTypeListReply(BaseModel):
    list: List["GetModuleTypeReply"] = []


class GetModuleTypeReply(BaseModel):
    id: str
    moduleTypeName: str
    createWay: str
    icon: str
    createTime: str

    @classmethod
    def from_orm(cls, type: ModuleTypeSql) -> 'GetModuleTypeReply':
        return GetModuleTypeReply(
            id=type.id,
            moduleTypeName=type.ModuleTypeName,
            createWay=type.CreateWay,
            icon=type.Icon,
            createTime=type.CreateTime
        )
