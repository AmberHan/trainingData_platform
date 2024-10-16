from sqlmodel import Session

import util.util
from schemas.module_model import GetModuleListByPageReply, SaveModuleReq
from schemas.req_model import StringIdReq, ListByPageReq
from sqlmodels.module import Module as ModuleSql
from sqlmodels.moduleFrame import ModuleFrame as ModuleFrameSql
from sqlmodels.moduleType import ModuleType as ModuleTypeSql


def get_module_list_by_page_impl(id: str, req: ListByPageReq, db: Session) -> GetModuleListByPageReply:
    a = ModuleTypeSql.select_by_id("basic-model-type-id")
    a.id = 1
    a.save(db)
    try:
        # 查询分页数据
        if req.size < 15:
            req.size = 15
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
        raise Exception(f"Failed to get data by page: {e}")


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


def save_module_impl(uid: str, req: SaveModuleReq, db: Session):
    if not req.moduleName:
        raise Exception("模型名称不能为空")
    if not req.moduleTypeId:
        raise Exception("请选择模型用途")
    if not req.frameId:
        raise Exception("请选择模型框架")
    if not req.moduleFile:
        raise Exception("请上传模型文件")
    save_module(uid, req, db)


def save_module(uid: str, req: SaveModuleReq, db: Session):
    module = ModuleSql()
    if req.id is not None:
        module = ModuleSql.select_by_id(db, req.id)
        if not module and module.CreateUid != uid:
            raise Exception("操作失败，无权修改")
    else:
        module.Id = util.util.NewId()
        module.CreateUid = uid
        module.CreateTime = util.util.TimeNow()
    module.ModuleName = req.moduleName
    module.FrameId = req.frameId
    module.ModuleTypeId = req.moduleTypeId
    module.Detail = req.detail
    module.ModuleFile = req.moduleFile
    module.save(db)
