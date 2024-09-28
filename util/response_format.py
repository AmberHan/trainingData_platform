from fastapi.responses import JSONResponse

from common.code import Code


def response_format(code: Code, data=None):
    response_data = code.to_dict()
    if data is not None:
        response_data["data"] = data
    return JSONResponse(content=response_data, status_code=code.status)