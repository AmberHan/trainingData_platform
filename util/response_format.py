import json

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from common.code import Code, RequestSuccess
from config.log_config import logger


def ret_format(code: Code, data=None):
    response_data = code.to_dict()
    if data is not None:
        if isinstance(data, dict):
            response_data["data"] = data
        else:
            response_data["data"] = data if isinstance(data, str) else json.loads(data.json(exclude_none=True))
    return JSONResponse(content=response_data, status_code=code.status)


def response_format(reply_provider):
    try:
        reply = reply_provider()
        return ret_format(RequestSuccess, reply)
    except HTTPException as e:
        logger.error(f"HTTPException: {str(e.detail)}", exc_info=True)
        return ret_format(Code(500, False, str(e.detail)), str(e.detail))
    except Exception as e:
        logger.error(f"Exception: {str(e)}", exc_info=True)
        return ret_format(Code(500, False, str(e)), str(e))


async def response_format_async(reply_provider):
    try:
        reply = await reply_provider()
        return ret_format(RequestSuccess, reply)
    except HTTPException as e:
        logger.error(f"HTTPException: {str(e.detail)}", exc_info=True)
        return ret_format(Code(500, False, str(e.detail)), str(e.detail))
    except Exception as e:
        logger.error(f"Exception: {str(e)}", exc_info=True)
        return ret_format(Code(500, False, str(e)), str(e))
