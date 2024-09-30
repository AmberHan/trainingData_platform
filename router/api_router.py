from http.client import HTTPException

from fastapi import APIRouter
from common import const
from common.code import RequestSuccess, ServiceInsideError
from services.module.device_temp_service import get_device_temp_impl
from util.response_format import response_format

# api接口
apiHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-i")
@apiHandler.post("/getId")
async def get_id():
    return {"message": "Hello World"}


@apiHandler.post("/getDeviceInfo")
async def get_device_info():
    try:
        reply = get_device_temp_impl()
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))
