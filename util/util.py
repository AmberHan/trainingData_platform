import uuid
from datetime import datetime

from fastapi import HTTPException

from common.code import RequestSuccess, ServiceInsideError
from config.log import logger
from util.response_format import response_format


def TimeNow() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 生成新的 UUID
def NewId() -> str:
    return str(uuid.uuid4())


def ret_format(reply_provider):
    try:
        reply = reply_provider()
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        logger.error(f"HTTPException: {str(e.detail)}", exc_info=True)
        return response_format(ServiceInsideError, str(e.detail))
    except Exception as e:
        logger.error(f"Exception: {str(e)}", exc_info=True)
        return response_format(ServiceInsideError, str(e))
