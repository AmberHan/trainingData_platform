from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.data import Data


class GetDataListByPageReq(BaseModel):
    page: Optional[int] = 1  # 默认值为 1
    size: Optional[int] = 5  # 默认值为 5
    like: Optional[str] = None  # 可选字符串，默认为 None



# data 返回实体
class SaveDataReq(BaseModel):
    id: Optional[str] = None
    dataName: Optional[str] = None
    moduleTypeId: Optional[str] = None
    detail: Optional[str] = None
    dataStatus: Optional[int] = -1
    uploadPath: Optional[str] = None
    exportPath: Optional[str] = None
    fileSize: Optional[str] = None
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    classNum: Optional[int] = None
    # 附加
    userName: Optional[str] = None
    moduleTypeName: Optional[str] = None

    @classmethod
    def from_orm(cls, data: Data) -> 'SaveDataReq':
        return SaveDataReq(
            id=data.Id,
            dataName=data.DataName,
            moduleTypeId=data.ModuleTypeId,
            detail=data.Detail,
            dataStatus=data.DataStatus if data.DataStatus is not None else -1,
            uploadPath=data.UploadPath,
            exportPath=data.ExportPath,
            fileSize=data.FileSize,
            createUid=data.CreateUid,
            createTime=data.CreateTime,
            updateTime=data.UpdateTime,
            classNum=data.ClassNum
            )






# 返回list数据列表
class GetDataListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveDataReq] = []


