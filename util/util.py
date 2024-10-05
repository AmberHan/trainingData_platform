import uuid
from datetime import datetime

# 获取当前时间，格式为 'YYYY-MM-DD HH:MM:SS'
from fastapi import HTTPException

from common.code import RequestSuccess, ServiceInsideError
from util.response_format import response_format


def TimeNow() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 生成新的 UUID
def NewId() -> str:
    return str(uuid.uuid4())


def ret_format(reply):
    try:
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))
