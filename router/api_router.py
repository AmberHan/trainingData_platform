from fastapi import APIRouter
from common import const
# api接口
apiHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-i")
@apiHandler.post("/getId")
async def get_id():
    return {"message": "Hello World"}


@apiHandler.post("/getDeviceInfo")
async def get_device_info():
    return {"message": "Hello World"}
