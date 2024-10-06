from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.data import Data as DataSql
from sqlmodels.dataStrong import DataStrong as DataStrongSql


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


class DataStrong(BaseModel):
    id: Optional[str] = None
    dataId: Optional[str] = None
    strongParam: Optional[str] = None

    @classmethod
    def from_orm(cls, data: DataStrongSql) -> 'DataStrong':
        return DataStrong(
            id=data.Id,
            dataId=data.DataId,
            strongParam=data.StrongParam,
            )


class DataStrongParam(DataStrong):
    open_cross_validation: bool = False
    is_test: bool = False
    training_data_num: Optional[str] = None
    validation_num: Optional[str] = None
    test_data_num: Optional[str] = None
    open_center_cut: bool = False
    center_cut_width: Optional[str] = None
    center_cut_height: Optional[str] = None
    open_regular: bool = False
    regular_mean: Optional[str] = None
    regular_std: Optional[str] = None
    open_fill: bool = False
    fill_width: Optional[str] = None
    fill_height: Optional[str] = None
    open_random_cut: bool = False
    random_cut_width: Optional[str] = None
    random_cut_height: Optional[str] = None
    open_change_size: bool = False
    change_size_width: Optional[str] = None
    change_size_height: Optional[str] = None
    open_random_delete: bool = False
    random_delete_erase_prob: Optional[str] = None
    random_delete_min_area_ratio: Optional[str] = None
    random_delete_max_area_ratio: Optional[str] = None
    open_random_flip: bool = False
    random_flip_prob: Optional[str] = None
    random_flip_direction: Optional[str] = None
    open_random_grey: bool = False
    random_grey_prob: Optional[str] = None
