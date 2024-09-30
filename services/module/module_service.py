from fastapi.logger import logger

from schemas.module_model import GetModuleListByPageReply, GetModuleListByPageReq, SaveModuleReq
from sqlmodels.data import Data
from sqlmodels.module import Module
from sqlmodels.moduleFrame import ModuleFrame
from sqlmodels.user import User

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Session
from sqlmodels.moduleType import ModuleType

class GetModuleTypeReply(SQLModel):
    id: str
    ModuleTypeName: str
    CreateWay: str
    Icon: str
    CreateTime: str


class StringIdReq(BaseModel):
    Id: str


def get_module_type_by_id(req: StringIdReq, db: Session) -> GetModuleTypeReply:
    module_type = ModuleType.select_by_id(req.Id, db)
    if not module_type:
        return None
    return GetModuleTypeReply.from_orm(module_type)


def module_to_save_project_req(module: Module) -> SaveModuleReq:
    return SaveModuleReq(
        id=module.Id,
        moduleName=module.ModuleName,
        moduleTypeId=module.ModuleTypeId,

        frameId=module.FrameId,
        detail=module.Detail,
        moduleFile=module.ModuleFile,
        isDelete=module.IsDelete,
        createUid=module.CreateUid,
        createTime=module.CreateTime,
        sort=module.Sort
    )



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
            saveModuleReq = module_to_save_project_req(p)
            try:
                saveModuleReq.frameName = ModuleFrame.select_by_id(db, p.FrameId).FrameName
                moduleTypeUse = ModuleType.select_by_id(p.ModuleTypeId, db)
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