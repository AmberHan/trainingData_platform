from dataclasses import Field
from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.project import Project
from sqlmodels.user import User
from schemas.project_model import GetProjectListByPageReq
from sqlalchemy.orm import Session
from services.module import moudle_service

class SaveProjectReq(BaseModel):
    id: Optional[str] = None
    project_name: Optional[str] = None
    module_type_id: Optional[str] = None
    module_type_name: Optional[str] = None
    create_way: Optional[str] = None
    icon: Optional[str] = None
    work_total_num: Optional[int] = None
    working_num: Optional[int] = None
    complete_num: Optional[int] = None
    create_uid: Optional[str] = None
    create_time: Optional[str] = None
    user_name: Optional[str] = None
    detail: Optional[str] = None

class GetProjectListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveProjectReq] = []

def project_to_save_project_req(project: Project) -> SaveProjectReq:
    return SaveProjectReq(
        id=project.Id,
        project_name=project.ProjectName,
        module_type_id=project.ModuleTypeId,
        work_total_num=project.WorkTotalNum,
        working_num=project.WorkingNum,
        complete_num=project.CompleteNum,
        create_uid=project.CreateUid,
        detail=project.Detail,
        create_time=project.CreateTime
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
        module_type_reply = moudle_service.get_module_type_by_id(moudle_service.StringIdReq(Id=p.ModuleTypeId), db)

        if module_type_reply:
            saveProjectReq.icon = module_type_reply.Icon
            saveProjectReq.module_type_name = module_type_reply.ModuleTypeName
            saveProjectReq.create_way = module_type_reply.CreateWay
        user = User.select_by_id(p.CreateUid, db)
        if user:
            saveProjectReq.user_name = user.username
        reply.list.append(saveProjectReq)
    return reply
