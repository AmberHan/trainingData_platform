from fastapi import HTTPException
from sqlmodel import Session

from schemas.module_model import GetModuleListByPageReply, SaveModuleReq
from schemas.req_model import StringIdReq, ListByPageReq
from sqlmodels.module import Module as ModuleSql
from sqlmodels.moduleFrame import ModuleFrame as ModuleFrameSql
from sqlmodels.moduleType import ModuleType as ModuleTypeSql


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
        raise HTTPException(status_code=400, detail=f"Failed to get data by page: {e}")


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
