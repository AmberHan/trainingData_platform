from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common import const
from common.const import CURRENT_USER_ID_KEY
from schemas.data_model import GetDataListByPageReq, DataStrong
from schemas.req_model import DeleteListReq, StringIdReq
from services.data import data_service
from services.db import get_db
# api接口
from util.util import ret_format

dataHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-d")


@dataHandler.post("/getDataListByPage")
async def get_data_list_by_page(req: GetDataListByPageReq, db: Session = Depends(get_db)):
    reply = data_service.get_data_list_by_page_impl(CURRENT_USER_ID_KEY, req, db)
    return ret_format(reply)


@dataHandler.post("/getDataStrong")
async def get_data_strong(req: DataStrong, db: Session = Depends(get_db)):
    reply = data_service.get_data_strong_impl(req, db)
    return ret_format(reply)


@dataHandler.post("/deleteData")
def delete_project(project_req: StringIdReq, db: Session = Depends(get_db)):
    reply = data_service.delete_data_impl(project_req.id, db)
    return ret_format(reply)


@dataHandler.post("/deleteAllData")
def delete_all_projects(ids: DeleteListReq, db: Session = Depends(get_db)):
    reply = data_service.delete_all_data_impl(ids.id, db)
    return ret_format(reply)
