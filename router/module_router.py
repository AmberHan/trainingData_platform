from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.code import *
from services.db import get_db
from common import const
from common.const import CURRENT_USER_ID_KEY
from schemas.module_model import GetModuleListByPageReq
from services.module import module_service
from util.response_format import response_format

moduleHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-m")

@moduleHandler.post("/getModuleListByPage")
async def get_module_list_by_page(req: GetModuleListByPageReq, db: Session = Depends(get_db)):
    try:
        reply = module_service.get_module_list_by_page_impl(CURRENT_USER_ID_KEY, req, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))


@moduleHandler.post("/getModuleFrameList")
async def get_module_frame_list():
    return {"message": "Hello World"}


@moduleHandler.post("/getModuleTypeList")
async def get_module_type_list():
    return {"message": "Hello World"}


@moduleHandler.post("/saveModule")
async def saveModule():
    return {"message": "Hello World"}


@moduleHandler.post("/deleteModule")
async def delete_module():
    return {"message": "Hello World"}


@moduleHandler.post("/deleteAllModule")
async def delete_all_module():
    return {"message": "Hello World"}

