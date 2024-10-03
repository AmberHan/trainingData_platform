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
    module_type = ModuleType.select_by_id(db, req.Id)
    if not module_type:
        return None
    return GetModuleTypeReply.from_orm(module_type)



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
                saveModuleReq.FrameName = ModuleFrame.select_by_id(db, p.FrameId).FrameName
                moduleTypeUse = ModuleType.select_by_id(db, p.ModuleTypeId)
                saveModuleReq.ModuleTypeName = moduleTypeUse.ModuleTypeName
                saveModuleReq.Icon = moduleTypeUse.Icon
                saveModuleReq.CreateWay = moduleTypeUse.CreateWay
            except:
                saveModuleReq.FrameName = "none"
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
    moduleF = ModuleFrame.select_by_id(db, moduleR.FrameId)
    if not moduleF:
        return
    moduleR.FrameName = moduleF.FrameName
    # 查询类型
    moduleT = ModuleType.select_by_id(db, moduleR.FrameId)
    if not moduleT:
        return None
    moduleR.ModuleTypeName = moduleF.ModuleTypeName
    return moduleR
