from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Session
from sqlmodels.moudleType import ModuleType

class GetModuleTypeReply(SQLModel):
    id: str
    ModuleTypeName: str
    CreateWay: str
    Icon: str
    CreateTime: str


class StringIdReq(BaseModel):
    Id: str


def get_module_type_by_id(req: StringIdReq, db: Session) -> GetModuleTypeReply:
    module_type = ModuleType.select_by_id(db, req.Id)
    if not module_type:
        return None
    return GetModuleTypeReply.from_orm(module_type)
