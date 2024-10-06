from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas.data_model import SaveDataReq, GetDataListByPageReply
from schemas.req_model import ListByPageReq
from services.module import module_service
from services.module.moduleType_service import get_module_type_by_id_impl
from services.module.module_service import StringIdReq
from sqlmodels.data import Data as DataSql
from sqlmodels.moduleType import ModuleType
from sqlmodels.user import User


def get_data_list_by_page_impl(id: str, req: ListByPageReq, db: Session):
    try:
        # 查询分页数据
        if req.size < 5:
            req.size = 5
        if req.page < 1:
            req.page = 1

            # 调用封装好的分页方法
        projects, total = DataSql.find_by_page(id, req.page, req.size, req.like, db)
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
        raise HTTPException(status_code=400, detail=f"Failed to get data by page: {e}")


def get_data_by_id(req: StringIdReq, db: Session) -> SaveDataReq:
    data = DataSql.select_by_id(db, req.id)
    if data is None:
        return None
    saveData = SaveDataReq.from_orm(data)
    m = get_module_type_by_id_impl(module_service.StringIdReq(id=data.ModuleTypeId), db)
    if m is not None:
        saveData.moduleTypeName = m.moduleTypeName
    user = User.select_by_id(db, data.CreateUid)
    saveData.userName = user.username
    return saveData


def delete_data_impl(
        id: str,
        db: Session,
        ):
    delete_data(id, db)


def delete_all_data_impl(
        ids: list,
        db: Session,
        ):
    if len(ids) == 0:
        raise HTTPException(status_code=400, detail="id不能为空")
    for id in ids:
        delete_data(id, db)


def delete_data(
        id: str,
        db: Session,
        ):
    data_sql = DataSql()
    data_sql.Id = id
    data_sql.delete(db)
