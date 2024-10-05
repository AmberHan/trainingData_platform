from fastapi.logger import logger
from schemas.module_model import *
from schemas.module_model import GetModuleListByPageReply, GetModuleListByPageReq, SaveModuleReq
from schemas.req_model import StringIdReq
from sqlmodels.module import Module
from sqlmodels.moduleFrame import ModuleFrame
from sqlmodel import Session
from sqlmodels.moduleType import ModuleType


def get_module_type_by_id(req: StringIdReq, db: Session) -> GetModuleTypeReply:
    module_type = ModuleType.select_by_id(db, req.Id)
    if not module_type:
        return None
    return GetModuleTypeReply.from_orm(module_type)

def get_module_frame_list(db: Session) -> GetModuleTypeReply:
    module_types = ModuleType.find_all(db)
    if not module_types:
        return None
    ret = GetModuleFrameListReply()
    for module_type in module_types:
        ret.list.append(GetModuleTypeReply.from_orm(module_type))
    return ret


def get_module_list_by_page_impl(id: str, req: GetModuleListByPageReq, db: Session):
    try:
        # 查询分页数据
        if req.size < 5:
            req.size = 5
        if req.page < 1:
            req.page = 1

            # 调用封装好的分页方法
        projects, total = Module.find_by_page(db, id, req.page, req.size, req.like)
        reply = GetModuleListByPageReply(total=total)
        for i, p in enumerate(projects):
            saveModuleReq = SaveModuleReq.from_module_orm(p)
            try:
                saveModuleReq.frameName = ModuleFrame.select_by_id(db, p.FrameId).FrameName
                moduleTypeUse = ModuleType.select_by_id(db, p.ModuleTypeId)
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
    module = Module.select_by_id(db, req.Id)
    if not module:
        return None
    moduleR = SaveModuleReq.from_module_orm(module)
    if not moduleR:
        return None
    # 查询框架
    moduleF = ModuleFrame.select_by_id(db, moduleR.frameId)
    if moduleF:
        moduleR.frameName = moduleF.FrameName
    # 查询类型
    moduleT = ModuleType.select_by_id(db, moduleR.frameId)
    if moduleT:
        moduleR.ModuleTypeName = moduleT.ModuleTypeName
    return moduleR
