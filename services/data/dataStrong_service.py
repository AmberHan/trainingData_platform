from sqlalchemy.orm import Session

from schemas.dataStrong_model import DataStrong, DataStrongParam
from sqlmodels.dataStrong import DataStrong as DataStrongSql


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
