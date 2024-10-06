from sqlmodel import Session

from schemas.moduleFrame_model import GetModuleFrameListReply, GetModuleFrameReply
from sqlmodels.moduleFrame import ModuleFrame as ModuleFrameSql


def get_module_frame_list_impl(db: Session) -> GetModuleFrameListReply:
    module_types = ModuleFrameSql.find_all(db)
    if module_types:
        ret = GetModuleFrameListReply()
        for module_type in module_types:
            ret.list.append(GetModuleFrameReply.from_orm(module_type))
        return ret
