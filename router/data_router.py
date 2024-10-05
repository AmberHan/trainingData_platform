from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common import const
from common.const import CURRENT_USER_ID_KEY
from schemas.data_model import GetDataListByPageReq, DataStrong
from services.db import get_db
from services.data import data_service

# api接口
from util.util import ret_format

dataHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-d")
@dataHandler.post("/getDataListByPage")
async def get_data_list_by_page(req: GetDataListByPageReq, db: Session = Depends(get_db)):
    reply = data_service.get_data_list_by_page_impl(CURRENT_USER_ID_KEY, req, db)
    return ret_format(reply)

@dataHandler.post("/getDataStrong")
async def get_data_strong(req: DataStrong, db: Session = Depends(get_db)):
    reply = data_service.get_data_strong(req, db)
    return ret_format(reply)


