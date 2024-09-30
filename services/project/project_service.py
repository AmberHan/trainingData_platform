from dataclasses import Field
from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.project import Project
from sqlmodels.user import User
from schemas.project_model import GetProjectListByPageReq
from sqlalchemy.orm import Session
from services.module import module_service

class SaveProjectReq(BaseModel):
    id: Optional[str] = None
    projectName: Optional[str] = None
    moduleTypeId: Optional[str] = None
    moduleTypeName: Optional[str] = None
    createWay: Optional[str] = None
    icon: Optional[str] = None
    workTotalNum: Optional[int] = None
    workingNum: Optional[int] = None
    completeNum: Optional[int] = None
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    userName: Optional[str] = None
    detail: Optional[str] = None

class GetProjectListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveProjectReq] = []

def project_to_save_project_req(project: Project) -> SaveProjectReq:
    return SaveProjectReq(
        id=project.Id,
        projectName=project.ProjectName,
        moduleTypeId=project.ModuleTypeId,
        workTotalNum=project.WorkTotalNum,
        workingNum=project.WorkingNum,
        completeNum=project.CompleteNum,
        createUid=project.CreateUid,
        detail=project.Detail,
        createTime=project.CreateTime
    )

def get_project_list_by_page_impl(
    uid: str,
    req: GetProjectListByPageReq,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectListByPageReply:
    # 处理分页参数，确保 page 和 size 有效
    if req.size < 5:
        req.size = 5
    if req.page < 1:
        req.page = 1

    # 调用封装好的分页方法
    projects, total = Project.find_by_page(uid, req.page, req.size, req.like, db)
    reply = GetProjectListByPageReply(total=total)
    for i, p in enumerate(projects):
        saveProjectReq = project_to_save_project_req(p)
        module_type_reply = module_service.get_module_type_by_id(module_service.StringIdReq(Id=p.ModuleTypeId), db)

        if module_type_reply:
            saveProjectReq.icon = module_type_reply.Icon
            saveProjectReq.moduleTypeName = module_type_reply.ModuleTypeName
            saveProjectReq.createWay = module_type_reply.CreateWay
        user = User.select_by_id(p.CreateUid, db)
        if user:
            saveProjectReq.userName = user.username
        reply.list.append(saveProjectReq)
    return reply
