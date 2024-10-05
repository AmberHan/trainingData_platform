from fastapi.logger import logger
from pydantic import parse_raw_as
from sqlalchemy.orm import Session

from schemas.data_model import GetDataListByPageReq, SaveDataReq, GetDataListByPageReply, DataStrong, DataStrongParam
from services.module import module_service
from services.module.module_service import StringIdReq, get_module_type_by_id
from sqlmodels.data import Data
from sqlmodels.dataStrong import DataStrong as DataStrongSql
from sqlmodels.moduleType import ModuleType
from sqlmodels.user import User


def get_data_list_by_page_impl(id: str, req: GetDataListByPageReq, db: Session):
    try:
        # 查询分页数据
        if req.size < 5:
            req.size = 5
        if req.page < 1:
            req.page = 1

            # 调用封装好的分页方法
        projects, total = Data.find_by_page(id, req.page, req.size, req.like, db)
        reply = GetDataListByPageReply(total=total)
        for i, p in enumerate(projects):
            saveDataReq = SaveDataReq.from_orm(p)
            saveDataReq.userName = User.select_by_id(db, p.CreateUid).username
            try:
                saveDataReq.moduleTypeName = ModuleType.select_by_id(db, p.ModuleTypeId).ModuleTypeName
            except:
                saveDataReq.moduleTypeName = "none"
            reply.list.append(saveDataReq)
        return reply
    except Exception as e:
        logger.error(f"Failed to get data by page: {e}")
        raise Exception("Failed to fetch data")


def get_data_by_id(req: StringIdReq, db: Session) -> SaveDataReq:
    data = Data.select_by_id(db, req.id)
    if data is None:
        return None
    saveData = SaveDataReq.from_orm(data)
    m = get_module_type_by_id(module_service.StringIdReq(id=data.ModuleTypeId), db)
    if m is not None:
        saveData.moduleTypeName = m.moduleTypeName
    user = User.select_by_id(db, data.CreateUid)
    saveData.userName = user.username
    return saveData


def get_data_strong_impl(req: DataStrong, db: Session) -> DataStrongParam:
    data = get_data_strong(req, db)
    if data is not None:
        data_strong_param = parse_raw_as(DataStrongParam, data.StrongParam)
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


def delete_data_impl(
        id: str,
        db: Session,
        ):
    delete_data(id, db)


def delete_all_data_impl(
        ids: list,
        db: Session,
        ):
    for id in ids:
        delete_data(id, db)


def delete_data(
        id: str,
        db: Session,
        ):
    pass
