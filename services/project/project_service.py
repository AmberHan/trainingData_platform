from typing import Optional, List
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from services.module.module_service import get_module_type_by_id, get_module_by_id
from sqlmodels.data import Data
from sqlmodels.project import Project
from sqlmodels.projectWork import ProjectWork
from sqlmodels.projectWorkType import ProjectWorkType
from sqlmodels.user import User
from schemas.project_model import GetProjectListByPageReq, GetProjectByIdReq
from sqlalchemy.orm import Session
from services.module import module_service
from util import util
import logging


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

    @classmethod
    def from_project_orm(self, project: Project) -> 'SaveProjectReq':
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


class ProjectWork(BaseModel):
    id: Optional[str] = None
    projectId: Optional[str] = None
    moduleTypeId: Optional[str] = None
    moduleFrameId: Optional[str] = None
    projectWorkTypeId: Optional[str] = None
    workName: Optional[str] = None
    detail: Optional[str] = None
    dataId: Optional[str] = None
    moduleId: Optional[str] = None
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    isDelete: Optional[bool] = None
    workStatus: Optional[int] = None
    workStage: Optional[str] = None
    startTime: Optional[str] = None
    updateTime: Optional[str] = None

class ProjectWorkParam(BaseModel):
    id: Optional[str] = None
    projectId: Optional[str] = None
    projectWorkId: Optional[str] = None
    evaluation: Optional[str] = None
    learningRate: Optional[str] = None
    impulse: Optional[str] = None
    optimizer: Optional[str] = None
    isUseDataExtend: Optional[bool] = None
    trainDataCount: Optional[str] = None
    scallDataCount: Optional[str] = None
    testGap: Optional[str] = None
    maxIteration: Optional[str] = None
    weightSaveGap: Optional[str] = None
    initSuperParam: Optional[str] = None

class Module(BaseModel):
    id: Optional[str] = None
    icon: Optional[str] = None
    moduleName: Optional[str] = None
    moduleTypeId: Optional[str] = None
    frameId: Optional[str] = None
    detail: Optional[str] = None
    moduleFile: Optional[str] = None
    isDelete: Optional[bool] = None
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    moduleTypeName: Optional[str] = None
    createWay: Optional[str] = None
    frameName: Optional[str] = None

class ModuleType(BaseModel):
    id: Optional[str] = None
    moduleTypeName: Optional[str] = None
    createWay: Optional[str] = None
    icon: Optional[str] = None
    createTime: Optional[str] = None

class UserInfo(BaseModel):
    id: Optional[str] = None
    userName: Optional[str] = None

class DataReply(BaseModel):
    id: Optional[str] = None
    dataName: Optional[str] = None
    moduleTypeId: Optional[str] = None
    detail: Optional[str] = None
    isTest: Optional[bool] = None
    dataStatus: Optional[int] = None
    uploadPath: Optional[str] = None
    exportPath: Optional[str] = None
    exportTime: Optional[str] = None
    fileSize: Optional[str] = None
    createUid: Optional[str] = None
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    isDelete: Optional[bool] = None
    moduleTypeName: Optional[str] = None

class ProjectWorkTypeReply(BaseModel):
    Id: Optional[str] = None
    TypeName: Optional[str] = None
    Icon: Optional[str] = None
    @classmethod
    def from_work_type_orm(self, projectWorkType: ProjectWorkType) -> 'ProjectWorkTypeReply':
        return ProjectWorkTypeReply(
            Id=projectWorkType.Id,
            TypeName=projectWorkType.TypeName,
            Icon=projectWorkType.Icon
        )

class SaveProjectWorkReq(BaseModel):
    work: Optional[ProjectWork] = None
    param: Optional[ProjectWorkParam] = None
    module: Optional[Module] = None
    moduleType: Optional[ModuleType] = None
    user: Optional[UserInfo] = None
    project: Optional['SaveProjectReq'] = None  # Define SaveProjectReq similarly
    data: Optional[DataReply] = None
    projectWorkType: Optional[ProjectWorkTypeReply] = None


class GetProjectListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveProjectReq] = []

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
            saveProjectReq.icon = module_type_reply.Icon
            saveProjectReq.moduleTypeName = module_type_reply.ModuleTypeName
            saveProjectReq.createWay = module_type_reply.CreateWay
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
    req: GetProjectByIdReq,
    db: Session
) -> SaveProjectWorkReq:
    work = ProjectWork.select_by_id(db, req.id)
    ret = get_project_info(work, db)
    if ret is None:
        return None
    return ret

def get_project_work_type_by_id(
    req: GetProjectByIdReq,
    db: Session
) -> ProjectWorkTypeReply:
    work_type = ProjectWorkType.select_by_id(db, req.id)
    ret = ProjectWorkTypeReply.from_work_type_orm(work_type)
    if ret is None:
        return None
    return ret

def get_project_info(
    req: ProjectWork,
    db: Session
) -> SaveProjectWorkReq:
    saveProjectWorkReq = SaveProjectWorkReq()
    work = ProjectWork.select_by_id(db, req.id)
    if work is None:
        raise HTTPException(status_code=404, detail="id不存在")
    saveProjectWorkReq.work = work

    # 查询参数
    param = ProjectWork.select_by_project_work_id(work.Id)
    if param is not None:
        saveProjectWorkReq.param = param

    # 模型类型
    type = get_module_type_by_id(module_service.StringIdReq(Id=work.ModuleTypeId), db)
    if type is not None:
        saveProjectWorkReq.moduleType = type

    # 模型
    module = get_module_by_id(module_service.StringIdReq(Id=work.ModuleTypeId), db)
    if module is not None:
        saveProjectWorkReq.module = module

    # 项目
    projectM = Project.select_by_id(db, req.projectId)
    if projectM is not None:
        saveProjectWorkReq.project = projectM

    # 创建者
    user = User.select_by_id(db, req.projectId)
    if user is not None:
        saveProjectWorkReq.user = user

    # 数据
    data = Data.select_by_id(db, req.projectId)
    if data is not None:
        saveProjectWorkReq.data = data

    # 数据类型
    projectWorkType = ProjectWorkType.select_by_id(db, req.projectId)
    if projectWorkType is not None:
        saveProjectWorkReq.projectWorkType = projectWorkType
    return saveProjectWorkReq