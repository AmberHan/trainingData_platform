from fastapi import APIRouter
from common import const

moduleHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-m")

@moduleHandler.post("/getModuleListByPage")
async def get_module_list_by_page():
    return {"message": "Hello World"}


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

