from sqlmodel import Session

from schemas.moduleType_model import GetModuleTypeReply, GetModuleTypeListReply
from schemas.req_model import StringIdReq
from sqlmodels.moduleType import ModuleType as ModuleTypeSql


def get_module_type_by_id_impl(req: StringIdReq, db: Session) -> GetModuleTypeReply:
    module_type = ModuleTypeSql.select_by_id(db, req.id)
    if not module_type:
        return None
    return GetModuleTypeReply.from_orm(module_type)


def get_module_type_list_impl(db: Session) -> GetModuleTypeListReply:
    module_types = ModuleTypeSql.find_all(db)
    ret = GetModuleTypeListReply()
    if module_types:
        for module_type in module_types:
            ret.list.append(GetModuleTypeReply.from_orm(module_type))
        return ret
