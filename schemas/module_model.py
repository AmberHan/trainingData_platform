from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.module import Module as ModuleSql
from sqlmodels.moduleFrame import ModuleFrame as ModuleFrameSql
from sqlmodels.moduleType import ModuleType as ModuleTypeSql


class Module(BaseModel):
    id: Optional[str] = None
    icon: Optional[str] = None
    moduleName: Optional[str] = None
    moduleTypeId: Optional[str] = None
    frameId: Optional[str] = None
    detail: Optional[str] = None
    moduleFile: Optional[str] = None
    isDelete: Optional[bool] = None
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    moduleTypeName: Optional[str] = None
    createWay: Optional[str] = None
    frameName: Optional[str] = None

    @classmethod
    def from_orm(cls, type: ModuleSql) -> 'Module':
        return Module(
            id=type.Id,
            createTime=type.CreateTime
            )


class ModuleType(BaseModel):
    id: Optional[str] = None
    moduleTypeName: Optional[str] = None
    createWay: Optional[str] = None
    icon: Optional[str] = None
    createTime: Optional[str] = None


# data 返回实体
class SaveModuleReq(BaseModel):
    id: Optional[str] = None
    moduleName: Optional[str] = None
    moduleTypeId: Optional[str] = None
    frameId: Optional[str] = None
    detail: Optional[str] = None
    moduleFile: Optional[str] = None
    isDelete: Optional[bool] = False
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    sort: Optional[str] = None

    # 附加 ModuleFrame
    frameName: Optional[str] = None
    # 附加 ModuleType
    moduleTypeName: Optional[str] = None
    icon: Optional[str] = None
    createWay: Optional[str] = None

    @classmethod
    def from_module_orm(cls, module: ModuleSql) -> 'SaveModuleReq':
        return SaveModuleReq(
            id=module.Id,
            moduleName=module.ModuleName,
            moduleTypeId=module.ModuleTypeId,

            frameId=module.FrameId,
            detail=module.Detail,
            moduleFile=module.ModuleFile,
            isDelete=module.IsDelete,
            createUid=module.CreateUid,
            createTime=module.CreateTime,
            )


# 返回list数据列表
class GetModuleListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveModuleReq] = []


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
