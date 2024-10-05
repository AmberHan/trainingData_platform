from typing import Optional, List
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from schemas.module_model import SaveModuleReq
from services.data import data_service
from services.module.module_service import get_module_type_by_id, get_module_by_id, GetModuleTypeReply
from sqlmodels.data import Data
from sqlmodels.project import Project
from sqlmodels.projectWork import ProjectWork as ProjectWorkM
from sqlmodels.projectWorkType import ProjectWorkType
from sqlmodels.user import User
from sqlmodels.projectWorkParam import ProjectWorkParam as ProjectWorkParamM
from schemas.project_model import GetProjectListByPageReq, GetProjectByIdReq, GetProjectWorkListByPageReq
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
    def from_project_orm(cls, project: Project) -> 'SaveProjectReq':
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

    @classmethod
    def from_orm(cls, project_work: ProjectWorkM) -> 'ProjectWork':
        return ProjectWork(
            id=project_work.Id,
            projectId=project_work.ProjectId,
            moduleTypeId=project_work.ModuleTypeId,
            moduleFrameId=project_work.ModuleFrameId,
            projectWorkTypeId=project_work.ProjectWorkTypeId,
            workName=project_work.WorkName,
            detail=project_work.Detail,
            dataId=project_work.DataId,
            moduleId=project_work.ModuleId,
            createUid=project_work.CreateUid,
            createTime=project_work.CreateTime,
            isDelete=project_work.IsDelete,
            workStatus=project_work.WorkStatus,
            workStage=project_work.WorkStage,
            startTime=project_work.StartTime,
            updateTime=project_work.UpdateTime
            )

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

    @classmethod
    def from_orm(cls, param: ProjectWorkParamM) -> 'ProjectWorkParam':
        return ProjectWorkParam(
            id=param.Id,
            projectId=param.ProjectId,
            projectWorkId=param.ProjectWorkId,
            evaluation=param.Evaluation,
            learningRate=param.LearningRate,
            impulse=param.Impulse,
            optimizer=param.Optimizer,
            isUseDataExtend=param.IsUseDataExtend,
            trainDataCount=param.TrainDataCount,
            scallDataCount=param.ScallDataCount,
            testGap=param.TestGap,
            maxIteration=param.MaxIteration,
            weightSaveGap=param.WeightSaveGap,
            initSuperParam=param.InitSuperParam
            )


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

    @classmethod
    def from_orm(cls, type: SaveModuleReq) -> 'Module':
        return Module(
            id=type.id,
            moduleTypeName=type.ModuleTypeName,
            createWay=type.CreateWay,
            icon=type.Icon,
            createTime=type.CreateTime
            )



class ModuleType(BaseModel):
    id: Optional[str] = None
    moduleTypeName: Optional[str] = None
    createWay: Optional[str] = None
    icon: Optional[str] = None
    createTime: Optional[str] = None

    # @classmethod
    # def from_orm(cls, user: User) -> 'ModuleType':
    #     return Module(
    #         id=user.id,
    #         userName=user.username
    #         )

class UserInfo(BaseModel):
    id: Optional[str] = None
    userName: Optional[str] = None

    @classmethod
    def from_orm(cls, user: User) -> 'UserInfo':
        return UserInfo(
            id=user.id,
            userName=user.username
            )


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

    @classmethod
    def from_orm(cls, data: Data) -> 'DataReply':
        return DataReply(
            id=data.Id,
            dataName=data.DataName,
            moduleTypeId=data.ModuleTypeId,
            moduleTypeName=data.ModuleTypeName,
            detail=data.Detail,
            isTest=data.IsTest,
            dataStatus=data.DataStatus,
            uploadPath=data.UploadPath,
            exportPath=data.ExportPath,
            exportTime=data.ExportTime,
            fileSize=data.FileSize,
            createUid=data.CreateUid,
            createTime=data.CreateTime,
            updateTime=data.UpdateTime,
            isDelete=data.IsDelete,
            classNum=data.ClassNum
            )

class GetProjectWorkTypeListReply(BaseModel):
    list: List["ProjectWorkTypeReply"] = []

class ProjectWorkTypeReply(BaseModel):
    id: Optional[str] = None
    typeName: Optional[str] = None
    icon: Optional[str] = None
    @classmethod
    def from_orm(cls, projectWorkType: ProjectWorkType) -> 'ProjectWorkTypeReply':
        return ProjectWorkTypeReply(
            id=projectWorkType.Id,
            typeName=projectWorkType.TypeName,
            icon=projectWorkType.Icon
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

    @classmethod
    def from_orm(cls, project_work: ProjectWorkM) -> 'SaveProjectWorkReq':
        return SaveProjectWorkReq(
            id=project_work.Id,
            projectId=project_work.ProjectId,
            moduleTypeId=project_work.ModuleTypeId,
            moduleFrameId=project_work.ModuleFrameId,
            projectWorkTypeId=project_work.ProjectWorkTypeId,
            workName=project_work.WorkName,
            detail=project_work.Detail,
            dataId=project_work.DataId,
            moduleId=project_work.ModuleId,
            createUid=project_work.CreateUid,
            createTime=project_work.CreateTime,
            isDelete=project_work.IsDelete,
            workStatus=project_work.WorkStatus,
            workStage=project_work.WorkStage,
            startTime=project_work.StartTime,
            updateTime=project_work.UpdateTime
            )


class GetProjectListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveProjectReq] = []


class GetProjectWorkListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveProjectWorkReq] = []



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
    req: GetProjectByIdReq,
    db: Session
) -> SaveProjectWorkReq:
    work = ProjectWorkM.select_by_id(db, req.id)
    projectWork = ProjectWork.from_orm(work)
    ret = get_project_info(projectWork, db)
    if ret is None:
        return None
    return ret

def get_project_work_type_by_id(
    req: GetProjectByIdReq,
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
    work = ProjectWorkM.select_by_id(db, req.id)
    if work is None:
        raise HTTPException(status_code=404, detail="id不存在")
    saveProjectWorkReq.work = ProjectWork.from_orm(work)

    # 查询参数
    param = ProjectWorkParamM.select_by_project_work_id(db, work.Id)
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
    projectWorks, total = ProjectWorkM.find_by_page(db, uid, req.projectId, req.page, req.size, req.like)
    reply = GetProjectWorkListByPageReply(total=total)
    for i, p in enumerate(projectWorks):
        pw = ProjectWork.from_orm(p)
        saveProjectWorkReq = get_project_info(pw, db)
        reply.list.append(saveProjectWorkReq)

    return reply
