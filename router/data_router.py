from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common import const
from common.const import CURRENT_USER_ID_KEY
from schemas.dataStrong_model import DataStrong
from schemas.req_model import DeleteListReq, StringIdReq, ListByPageReq
from services.data import data_service, dataStrong_service
from config.db import get_db
# api接口
from util.util import ret_format

dataHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-d")


@dataHandler.post("/getDataListByPage")
async def get_data_list_by_page(req: ListByPageReq, db: Session = Depends(get_db)):
    return ret_format(lambda: data_service.get_data_list_by_page_impl(CURRENT_USER_ID_KEY, req, db))


@dataHandler.post("/getDataStrong")
async def get_data_strong(req: DataStrong, db: Session = Depends(get_db)):
    return ret_format(lambda: dataStrong_service.get_data_strong_impl(req, db))


@dataHandler.post("/deleteData")
def delete_project(project_req: StringIdReq, db: Session = Depends(get_db)):
    return ret_format(lambda: data_service.delete_data_impl(project_req.id, db))


@dataHandler.post("/deleteAllData")
def delete_all_projects(ids: DeleteListReq, db: Session = Depends(get_db)):
    return ret_format(lambda: data_service.delete_all_data_impl(ids.id, db))
