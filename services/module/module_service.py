from fastapi.logger import logger
from sqlmodel import Session

from schemas.module_model import *
from schemas.module_model import GetModuleListByPageReply, SaveModuleReq
from schemas.req_model import StringIdReq, ListByPageReq
from sqlmodels.module import Module as ModuleSql
from sqlmodels.moduleFrame import ModuleFrame as ModuleFrameSql
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


def get_module_list_by_page_impl(id: str, req: ListByPageReq, db: Session):
    try:
        # 查询分页数据
        if req.size < 5:
            req.size = 5
        if req.page < 1:
            req.page = 1

            # 调用封装好的分页方法
        projects, total = ModuleSql.find_by_page(db, id, req.page, req.size, req.like)
        reply = GetModuleListByPageReply(total=total)
        for i, p in enumerate(projects):
            saveModuleReq = SaveModuleReq.from_module_orm(p)
            try:
                saveModuleReq.frameName = ModuleFrameSql.select_by_id(db, p.FrameId).FrameName
                moduleTypeUse = ModuleTypeSql.select_by_id(db, p.ModuleTypeId)
                saveModuleReq.moduleTypeName = moduleTypeUse.ModuleTypeName
                saveModuleReq.icon = moduleTypeUse.Icon
                saveModuleReq.createWay = moduleTypeUse.CreateWay
            except:
                saveModuleReq.frameName = "none"
            reply.list.append(saveModuleReq)
        return reply
    except Exception as e:
        logger.error(f"Failed to get data by page: {e}")
        raise Exception("Failed to fetch data")


def get_module_by_id(req: StringIdReq, db: Session) -> SaveModuleReq:
    module = ModuleSql.select_by_id(db, req.id)
    if not module:
        return None
    moduleR = SaveModuleReq.from_module_orm(module)
    if not moduleR:
        return None
    # 查询框架
    moduleF = ModuleFrameSql.select_by_id(db, moduleR.frameId)
    if moduleF:
        moduleR.frameName = moduleF.FrameName
    # 查询类型
    moduleT = ModuleTypeSql.select_by_id(db, moduleR.frameId)
    if moduleT:
        moduleR.ModuleTypeName = moduleT.ModuleTypeName
    return moduleR


def get_module_frame_list_impl(db: Session) -> GetModuleFrameListReply:
    module_types = ModuleFrameSql.find_all(db)
    if module_types:
        ret = GetModuleFrameListReply()
        for module_type in module_types:
            ret.list.append(GetModuleFrameReply.from_orm(module_type))
        return ret
