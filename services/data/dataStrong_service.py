from sqlalchemy.orm import Session

import util.util
from config.config import config_path
from schemas.dataStrong_model import DataStrong, DataStrongParam
from sqlmodels.data import Data as DataSql
from sqlmodels.dataFile import DataFile
from sqlmodels.dataStrong import DataStrong as DataStrongSql
from util.convert import model_to_string
from util.file import split_and_move_files


def save_data_strong_impl(req: DataStrongParam, db: Session):
    if req.dataId == "" or None:
        raise Exception("未选择任何数据,DataId不能为空")

    # TODO 此处可以优化
    dataStrongSql = DataStrongSql()
    dataStrongSql.DataId = req.dataId
    dataStrongSql.Id = req.id
    dataStrongSql.StrongParam = model_to_string(req)

    dataId = save_data_strong(dataStrongSql, db)

    # 文件分类迁移
    # 添加清洗文件夹的区分
    # res = DataFile.find_all_by_data_id(db, "0b7ad095-3efe-4e42-8286-448a7e631792")
    res = DataFile.find_all_by_data_id(db, dataId)
    # 保存DataSets 在路径中的位置
    images_parent_dir = config_path['FileConf']['SaveDataSetsPath']
    # 统一文件名dataId表示
    images_parent_dir += ("/" + dataId)
    split_and_move_files(res, int(req.validation_num), int(req.test_data_num), int(req.training_data_num),
                         images_parent_dir)




def save_data_strong(req: DataStrongSql, db: Session):
    data = DataSql.select_by_id(db, req.DataId)
    if data is None:
        raise Exception("fail to model.Data.SelectById")
    dataStrong = DataStrongSql.select_by_data_id(db, req.DataId)
    if dataStrong is None:
        req.Id = util.util.NewId()
    else:
        req.Id = dataStrong.Id
    req.save(db)

    # 删除文件
    # dataFileSql.DataFile.delete_by_type_and_data_id(db, 1, req.DataId)
    # dataFileSql.DataFile.delete_by_type_and_data_id(db, 2, req.DataId)
    # dataFileSql.DataFile.delete_by_type_and_data_id(db, 3, req.DataId)

    return req.DataId


def get_data_strong_impl(req: DataStrong, db: Session) -> DataStrongParam:
    data = get_data_strong(req, db)
    if data is not None:
        data_strong_param = DataStrongParam.parse_raw(data.StrongParam)
        data_strong_param.id = data.Id
        data_strong_param.dataId = data.DataId
        return data_strong_param


def get_data_strong(req: DataStrong, db: Session) -> DataStrongSql:
    if req.dataId:
        data = DataStrongSql.select_by_data_id(db, req.dataId)
        return data
    elif req.id:
        data = DataStrongSql.select_by_id(db, req.id)
        return data
