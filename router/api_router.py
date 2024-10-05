from fastapi import APIRouter

from common import const
from services.module.device_temp_service import get_device_temp_impl
# api接口
from util.util import ret_format

apiHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-i")


@apiHandler.post("/getId")
async def get_id():
    return {"message": "Hello World"}


@apiHandler.post("/getDeviceInfo")
async def get_device_info():
    reply = get_device_temp_impl()
    return ret_format(reply)
