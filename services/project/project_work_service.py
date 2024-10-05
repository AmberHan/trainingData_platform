from fastapi import HTTPException
from schemas.project_work_model import SaveProjectWorkReq, ProjectWork, ProjectWorkTypeReply, \
    GetProjectWorkTypeListReply, ProjectWorkParam, GetProjectWorkListByPageReq, GetProjectWorkListByPageReply
from schemas.req_model import StringIdReq
from schemas.user_model import UserInfo
from services.data import data_service
from services.module.module_service import get_module_type_by_id, get_module_by_id
from sqlmodels import projectWork as projectWorkSql
from sqlmodels.project import Project
from sqlmodels.projectWork import ProjectWork as ProjectWorkSql
from sqlmodels.projectWorkType import ProjectWorkType
from sqlmodels.user import User
from sqlmodels.projectWorkParam import ProjectWorkParam as ProjectWorkParamSql
from schemas.project_model import GetProjectListByPageReply, SaveProjectReq
from sqlalchemy.orm import Session
from services.module import module_service
from util import util

# 保存项目信息
def save_project_work_impl(
    uid: str,
    req: SaveProjectWorkReq,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
):
    #todo 一堆校验
    save_project_work(uid, req, db)

    # 更新项目工作流数量
    Project.flush_project_work_num(db, req.work.ProjectId)

def delete_project_work_impl(
    id: str,
    db: Session,
):
    delete_project_work(id, db)


def delete_all_project_work_impl(
    ids: list,
    db: Session,
):
    for id in ids:
        delete_project_work(id, db)

def delete_project_work(
    id: str,
    db: Session,
):
    project_work_sql = projectWorkSql()
    project_work_sql.Id = id
    project_work_sql.delete(db)

    # 更新项目工作流数量
    Project.flush_project_work_num(db, id)

def save_project_work(
    uid: str,
    req: SaveProjectWorkReq,
    db: Session
) -> SaveProjectWorkReq:
    restart = True
    projectWork = ProjectWorkSql()
    if req.work.id != "":
        r = ProjectWorkSql.select_by_id(db, req.work.id)
        if r is not None:
            restart = False
    else:
        if ProjectWorkSql.name_exists(db, uid, req.work.workName):
            return
        projectWork.Id = util.NewId()
        projectWork.CreateUid = uid
        projectWork.CreateTime = util.TimeNow()
        projectWork.CreateTime = projectWork.CreateTime
    projectWork.ProjectId = req.work.projectId
    projectWork.ModuleTypeId = req.work.ModuleTypeId
    projectWork.ModuleFrameId = req.work.ModuleFrameId
    projectWork.ProjectWorkTypeId = req.work.ProjectWorkTypeId
    projectWork.WorkName = req.work.WorkName
    projectWork.Detail = req.work.Detail
    projectWork.DataId = req.work.DataId
    projectWork.ModuleId = req.work.ModuleId
    projectWork.UpdateTime = projectWork.CreateTime
    projectWork.save(db)

    # param
    paramMod = ProjectWorkParamSql.select_by_project_work_id(projectWork.Id)
    paramMod.Id = util.NewId()
    paramMod.ProjectWorkId = projectWork.Id
    paramMod.ProjectId = req.work.ProjectId
    paramMod.ProjectId = req.param.ProjectId
    paramMod.Evaluation = req.param.Evaluation
    paramMod.LearningRate = req.param.LearningRate
    paramMod.Impulse = req.param.Impulse
    paramMod.Optimizer = req.param.Optimizer
    paramMod.IsUseDataExtend = req.param.IsUseDataExtend
    paramMod.TrainDataCount = req.param.TrainDataCount
    paramMod.ScallDataCount = req.param.ScallDataCount
    paramMod.TestGap = req.param.TestGap
    paramMod.MaxIteration = req.param.MaxIteration
    paramMod.WeightSaveGap = req.param.WeightSaveGap
    paramMod.InitSuperParam = req.param.InitSuperParam
    paramMod.Save()

    if restart:
        #startWork(StringIdReq(id=projectWork.Id))
        pass


def get_project_work_by_id(
    req: StringIdReq,
    db: Session
) -> SaveProjectWorkReq:
    work = ProjectWorkSql.select_by_id(db, req.id)
    ret = get_project_info(ProjectWork.from_orm(work), db)
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
    type = get_module_type_by_id(StringIdReq(id=work.ModuleTypeId), db)
    if type is not None:
        saveProjectWorkReq.moduleType = type

    module = get_module_by_id(StringIdReq(id=work.ModuleId), db)
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
    data = data_service.get_data_by_id(module_service.StringIdReq(id=req.dataId), db)
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
