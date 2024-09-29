from fastapi.responses import JSONResponse
import json
from common.code import Code


def response_format(code: Code, data=None):
    response_data = code.to_dict()
    if data is not None:
        response_data["data"] = data if isinstance(data, str) else json.loads(data.json())
    return JSONResponse(content=response_data, status_code=code.status)