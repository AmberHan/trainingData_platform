from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.module import Module


class GetModuleListByPageReq(BaseModel):
    page: Optional[int] = 1  # 默认值为 1
    size: Optional[int] = 5  # 默认值为 5
    like: Optional[str] = None  # 可选字符串，默认为 None



# data 返回实体
class SaveModuleReq(BaseModel):
    Id: Optional[str] = None
    ModuleName: Optional[str] = None
    ModuleTypeId: Optional[str] = None
    FrameId: Optional[str] = None
    Detail: Optional[str] = None
    ModuleFile: Optional[str] = None
    IsDelete: Optional[bool] = False
    CreateUid: Optional[str] = None
    CreateTime: Optional[str] = None
    Sort: Optional[str] = None

    # 附加 ModuleFrame
    FrameName: Optional[str] = None
    # 附加 ModuleType
    ModuleTypeName: Optional[str] = None
    Icon: Optional[str] = None
    CreateWay: Optional[str] = None

    @classmethod
    def from_module_orm(self, module: Module) -> 'SaveModuleReq':
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



