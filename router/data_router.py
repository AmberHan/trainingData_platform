from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common import const
from common.code import RequestSuccess, ServiceInsideError
from common.const import CURRENT_USER_ID_KEY
from schemas.data_model import GetDataListByPageReq
from services.db import get_db
from services.data import data_service
from util.response_format import response_format

# api接口
dataHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-d")
@dataHandler.post("/getDataListByPage")
async def get_data_list_by_page(req: GetDataListByPageReq, db: Session = Depends(get_db)):
    try:
        reply = data_service.get_data_list_by_page_impl(CURRENT_USER_ID_KEY, req, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))


