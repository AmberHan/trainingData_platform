from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common import const
from common.const import CURRENT_USER_ID_KEY
from schemas.req_model import ListByPageReq
from config.db import get_db
from services.module import module_service
from util.util import ret_format

moduleHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-m")


@moduleHandler.post("/getModuleListByPage")
async def get_module_list_by_page(req: ListByPageReq, db: Session = Depends(get_db)):
    return ret_format(lambda: module_service.get_module_list_by_page_impl(CURRENT_USER_ID_KEY, req, db))


@moduleHandler.post("/getModuleFrameList")
async def get_module_frame_list(db: Session = Depends(get_db)):
    return ret_format(lambda: module_service.get_module_frame_list_impl(db))


@moduleHandler.post("/getModuleTypeList")
async def get_module_type_list(db: Session = Depends(get_db)):
    return ret_format(lambda: module_service.get_module_type_list_impl(db))


@moduleHandler.post("/saveModule")
async def saveModule():
    return {"message": "Hello World"}


@moduleHandler.post("/deleteModule")
async def delete_module():
    return {"message": "Hello World"}


@moduleHandler.post("/deleteAllModule")
async def delete_all_module():
    return {"message": "Hello World"}
