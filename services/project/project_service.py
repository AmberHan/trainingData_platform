from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from schemas.project_work_model import SaveProjectWorkReq, ProjectWork, ProjectWorkTypeReply, \
    GetProjectWorkTypeListReply, ProjectWorkParam, GetProjectWorkListByPageReq, GetProjectWorkListByPageReply
from schemas.req_model import StringIdReq
from schemas.user_model import UserInfo
from services.data import data_service
from services.module.module_service import get_module_type_by_id, get_module_by_id
from sqlmodels.project import Project
from sqlmodels.projectWork import ProjectWork as ProjectWorkSql
from sqlmodels.projectWorkType import ProjectWorkType
from sqlmodels.user import User
from sqlmodels.projectWorkParam import ProjectWorkParam as ProjectWorkParamSql
from schemas.project_model import GetProjectListByPageReq, GetProjectListByPageReply, SaveProjectReq
from sqlalchemy.orm import Session
from services.module import module_service
from util import util
import logging


# 定义入参实体
class DeleteListReq(BaseModel):
    id: List[str]

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
        saveProjectReq = SaveProjectReq.from_project_orm(p)
        module_type_reply = module_service.get_module_type_by_id(module_service.StringIdReq(Id=p.ModuleTypeId), db)

        if module_type_reply:
            saveProjectReq.icon = module_type_reply.icon
            saveProjectReq.moduleTypeName = module_type_reply.moduleTypeName
            saveProjectReq.createWay = module_type_reply.createWay
        user = User.select_by_id(db, p.CreateUid)
        if user:
            saveProjectReq.userName = user.username
        reply.list.append(saveProjectReq)
    return reply




# 保存项目信息
def save_project_impl(
    uid: str,
    req: SaveProjectReq,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectListByPageReply:
    project = Project()
    # 日志配置
    logger = logging.getLogger(__name__)
    try:
        # 判断是否是更新项目
        if req.id:
            project = Project.select_by_id(db, req.id)
            if not project:
                logger.error(f"Failed to find project with ID {req.id}")
                return Exception("项目不存在")

            # 验证用户是否有权限操作
            if project.CreateUid != uid:
                return Exception("无权操作")

        # 如果是新项目，检查项目名称是否已存在
        else:
            if Project.project_name_exists(db, uid, req.projectName):
                return Exception("项目名称已存在")
            # 生成新项目 ID 和创建时间
            project.Id = util.NewId()
            project.CreateTime = util.TimeNow()

        project.ProjectName = req.projectName
        project.ModuleTypeId = req.moduleTypeId
        project.CreateUid = uid
        project.Detail = req.detail
        project.save(db)

    except SQLAlchemyError as e:
        logger.error(f"Failed to save project: {e}")
        return e  # 返回错误对象
    return None

# 删除项目信息
def delete_project_impl(
    id: str,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectListByPageReply:
    project = Project()
    # 日志配置
    logger = logging.getLogger(__name__)
    try:
        project.Id = id
        project.delete(db)
    except SQLAlchemyError as e:
        logger.error(f"Failed to save project: {e}")
        return e  # 返回错误对象
    return None

def delete_all_project_impl(
    id: list,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectListByPageReply:
    # 日志配置
    logger = logging.getLogger(__name__)
    try:
        Project.delete_all(db, id)
    except SQLAlchemyError as e:
        logger.error(f"Failed to save project: {e}")
        return e  # 返回错误对象
    return None

def get_project_work_by_id(
    req: StringIdReq,
    db: Session
) -> SaveProjectWorkReq:
    work = ProjectWorkSql.select_by_id(db, req.id)
    projectWork = ProjectWork.from_orm(work)
    ret = get_project_info(projectWork, db)
    if ret is None:
        return None
    return ret

def get_project_work_type_by_id(
    req: StringIdReq,
    db: Session
) -> ProjectWorkTypeReply:
    work_type = ProjectWorkType.select_by_id(db, req.id)
    if work_type is None:
        return None
    ret = ProjectWorkTypeReply.from_orm(work_type)
    return ret

def get_project_work_type_list(
    db: Session
) -> ProjectWorkTypeReply:
    work_types = ProjectWorkType.find_all(db)
    if work_types is None:
        return None
    l = GetProjectWorkTypeListReply()
    for work_type in work_types:
        l.list.append(ProjectWorkTypeReply.from_orm(work_type))
    return l

def get_project_info(
    req: ProjectWork,
    db: Session
) -> SaveProjectWorkReq:
    saveProjectWorkReq = SaveProjectWorkReq()
    work = ProjectWorkSql.select_by_id(db, req.id)
    if work is None:
        raise HTTPException(status_code=404, detail="id不存在")
    saveProjectWorkReq.work = ProjectWork.from_orm(work)

    # 查询参数
    param = ProjectWorkParamSql.select_by_project_work_id(db, work.Id)
    if param is not None:
        saveProjectWorkReq.param = ProjectWorkParam.from_orm(param)

    # 模型类型
    type = get_module_type_by_id(module_service.StringIdReq(Id=work.ModuleTypeId), db)
    if type is not None:
        saveProjectWorkReq.moduleType = type

    module = get_module_by_id(module_service.StringIdReq(Id=work.ModuleId), db)
    if module is not None:
        saveProjectWorkReq.module = module

    # 项目
    projectM = Project.select_by_id(db, req.projectId)
    if projectM is not None:
        saveProjectWorkReq.project = SaveProjectReq.from_project_orm(projectM)

    # 创建者
    user = User.select_by_id(db, req.createUid)
    if user is not None:
        saveProjectWorkReq.user = UserInfo.from_orm(user)

    # 数据
    data = data_service.get_data_by_id(module_service.StringIdReq(Id=req.dataId), db)
    if data is not None:
        saveProjectWorkReq.data = data

    # 数据类型
    projectWorkType = ProjectWorkType.select_by_id(db, req.projectWorkTypeId)
    if projectWorkType is not None:
        saveProjectWorkReq.projectWorkType = ProjectWorkTypeReply.from_orm(projectWorkType)
    return saveProjectWorkReq


def get_project_work_list_by_page_impl(
    uid: str,
    req: GetProjectWorkListByPageReq,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectListByPageReply:
    # 处理分页参数，确保 page 和 size 有效
    if req.size < 5:
        req.size = 5
    if req.page < 1:
        req.page = 1

    # 调用封装好的分页方法
    projectWorks, total = ProjectWorkSql.find_by_page(db, uid, req.projectId, req.page, req.size, req.like)
    reply = GetProjectWorkListByPageReply(total=total)
    for i, p in enumerate(projectWorks):
        pw = ProjectWork.from_orm(p)
        saveProjectWorkReq = get_project_info(pw, db)
        reply.list.append(saveProjectWorkReq)

    return reply
