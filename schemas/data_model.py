from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.data import Data as DataSql
from sqlmodels.dataFile import DataFile as DataFileSql



# 定义 DetailItem 模型
class DetailItem(BaseModel):
    input1: str
    input2: int


# 保存data实体
class SaveDataForm(BaseModel):
    dataName: Optional[str] = None
    detail: Optional[str] = None
    fileSize: Optional[str] = None
    isTest: Optional[bool] = False
    moduleTypeId: Optional[str] = None
    uploadPath: Optional[str] = None

    details: Optional[List[DetailItem]] = None  # 可选的 details 列表



# data 表格实体
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
    def from_orm(cls, data: DataSql) -> 'SaveDataReq':
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


class DataReply(BaseModel):
    id: Optional[str] = None
    dataName: Optional[str] = None
    moduleTypeId: Optional[str] = None
    detail: Optional[str] = None
    isTest: Optional[bool] = None
    dataStatus: Optional[int] = None
    uploadPath: Optional[str] = None
    exportPath: Optional[str] = None
    exportTime: Optional[str] = None
    fileSize: Optional[str] = None
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    isDelete: Optional[bool] = None
    moduleTypeName: Optional[str] = None

    @classmethod
    def from_orm(cls, data: DataSql) -> 'DataReply':
        return DataReply(
            id=data.Id,
            dataName=data.DataName,
            moduleTypeId=data.ModuleTypeId,
            detail=data.Detail,
            isTest=data.IsTest,
            dataStatus=data.DataStatus,
            uploadPath=data.UploadPath,
            exportPath=data.ExportPath,
            exportTime=data.ExportTime,
            fileSize=data.FileSize,
            createUid=data.CreateUid,
            createTime=data.CreateTime,
            updateTime=data.UpdateTime,
            isDelete=data.IsDelete,
            classNum=data.ClassNum
        )


class DataFile(BaseModel):
    id: Optional[int] = None
    dataId: Optional[str] = None
    filePath: Optional[str] = None
    url: Optional[str] = None
    fileType: Optional[int] = -1
    dirPath: Optional[str] = None

    @classmethod
    def from_orm(cls, data: DataFileSql) -> 'DataFile':
        return DataFile(
            id=data.Id,
            dataId=data.DataId,
            filePath=data.FilePath,
            url=data.Url,
            fileType=data.FileType,
            dirPath=data.DirPath,
        )


class GetDataFileListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[DataFile] = []


class FilePresent(BaseModel):
    dir: Optional[str] = None
    number: Optional[int] = None


class GetDataFilePresentReply(BaseModel):
    total: Optional[int] = None
    list: List[FilePresent] = []
