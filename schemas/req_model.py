from pydantic import BaseModel


class StringIdReq(BaseModel):
    Id: str

class StringidReq(BaseModel):
    id: str