import json

from pydantic import BaseModel


def model_to_string(model: BaseModel, indent: int = 4, ensure_ascii: bool = False) -> str:
    data_dict = model.dict()
    json_str = json.dumps(data_dict, ensure_ascii=ensure_ascii, indent=indent)
    return json_str
