from fastapi import APIRouter

from common import const
from services.api.device_temp_service import get_device_temp_impl
from util.response_format import response_format

apiHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-i")


@apiHandler.post("/getId")
async def get_id():
    return {"message": "Hello World"}


@apiHandler.post("/getDeviceInfo")
async def get_device_info():
    return response_format(lambda: get_device_temp_impl())
