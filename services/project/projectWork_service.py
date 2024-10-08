import multiprocessing
import time

from sqlalchemy.orm import Session

import config.config
from schemas.projectWork_model import SaveProjectWorkReq, ProjectWork, ProjectWorkTypeReply, \
    GetProjectWorkTypeListReply, ProjectWorkParam, GetProjectWorkListByPageReply
from schemas.project_model import SaveProjectReq
from schemas.req_model import StringIdReq, ListByPageReq
from schemas.user_model import UserInfo
from services.data import data_service
from services.module import module_service
from services.module.moduleType_service import get_module_type_by_id_impl
from services.module.module_service import get_module_by_id
from sqlmodels.module import Module as ModuleSql
from sqlmodels.project import Project
from sqlmodels.projectWork import ProjectWork as ProjectWorkSql
from sqlmodels.projectWorkParam import ProjectWorkParam as ProjectWorkParamSql
from sqlmodels.projectWorkType import ProjectWorkType
from sqlmodels.user import User
from util import util
from util.commd import exec_work, exec_work2
from util.file import get_last_row_log_stage, get_last_row_loss


def delete_project_work_impl(
        id: str,
        db: Session,
):
    delete_project_work(id, db)


def delete_all_project_work_impl(
        ids: list,
        db: Session,
):
    if len(ids) == 0:
        raise Exception("id不能为空")
    for id in ids:
        delete_project_work(id, db)


def delete_project_work(
        id: str,
        db: Session,
):
    project_work_sql = ProjectWorkSql()
    project_work_sql.Id = id
    project_work_sql.delete(db)

    # 更新项目工作流数量
    Project.flush_project_work_num(db, id)


def save_project_work_impl(
        uid: str,
        req: SaveProjectWorkReq,
        db: Session,
        # current_user_id: str = Depends(get_current_user_id)
):
    if not req.work.projectId:
        raise Exception("未选择任何项目")

    if not req.work.projectWorkTypeId:
        raise Exception("请选择工作流类型")

    if not req.work.moduleTypeId:
        raise Exception("项目类型不能为空")

    if not req.work.moduleFrameId:
        raise Exception("请选择训练框架")

    if not req.work.workName:
        raise Exception("请填写工作流名称")

    if not req.work.dataId:
        raise Exception("请选择数据")

    if not req.work.moduleId:
        raise Exception("请选择模型")

    if not req.param.evaluation:
        raise Exception("请选择评估指标")

    if not req.param.learningRate:
        raise Exception("请填写学习率")

    if not req.param.optimizer:
        raise Exception("请选择优化器")

    if not req.param.trainDataCount:
        raise Exception("请填写训练数据批处理数据量")

    if not req.param.scallDataCount:
        req.work.ScallDataCount = req.work.TrainDataCount

    if not req.param.testGap:
        raise Exception("请填写测试周期间隔")

    if not req.param.maxIteration:
        raise Exception("请填写最大迭代次数")

    if not req.param.weightSaveGap:
        raise Exception("请填写权重保存周期")

    if not req.param.initSuperParam:
        req.param.initSuperParam = "1"

    save_project_work(uid, req, db)

    # 更新项目工作流数量
    Project.flush_project_work_num(db, req.work.projectId)


def save_project_work(
        uid: str,
        req: SaveProjectWorkReq,
        db: Session
):
    restart = True
    projectWork = ProjectWorkSql()
    if req.work.id is not None:
        r = ProjectWorkSql.select_by_id(db, req.work.id)
        if r is not None:
            restart = False
    else:
        if ProjectWorkSql.name_exists(db, uid, req.work.workName):
            raise Exception("工作流名称已存在")
        projectWork.Id = util.NewId()
        projectWork.CreateUid = uid
        projectWork.CreateTime = util.TimeNow()
        projectWork.CreateTime = projectWork.CreateTime
    projectWork.ProjectId = req.work.projectId
    projectWork.ModuleTypeId = req.work.moduleTypeId
    projectWork.ModuleFrameId = req.work.moduleFrameId
    projectWork.ProjectWorkTypeId = req.work.projectWorkTypeId
    projectWork.WorkName = req.work.workName
    projectWork.Detail = req.work.detail
    projectWork.DataId = req.work.dataId
    projectWork.ModuleId = req.work.moduleId
    projectWork.UpdateTime = projectWork.CreateTime
    projectWork.save(db)

    # param
    paramMod = ProjectWorkParamSql.select_by_project_work_id(db, projectWork.Id)
    paramMod.Id = util.NewId()
    paramMod.ProjectWorkId = projectWork.Id
    if req.work.projectId is not None:
        paramMod.ProjectId = req.work.projectId
    if req.param.projectId is not None:
        paramMod.ProjectId = req.param.projectId

    paramMod.Evaluation = req.param.evaluation
    paramMod.LearningRate = req.param.learningRate
    paramMod.Impulse = req.param.impulse
    paramMod.Optimizer = req.param.optimizer
    paramMod.IsUseDataExtend = req.param.isUseDataExtend
    paramMod.TrainDataCount = req.param.trainDataCount
    paramMod.ScallDataCount = req.param.scallDataCount
    paramMod.TestGap = req.param.testGap
    paramMod.MaxIteration = req.param.maxIteration
    paramMod.WeightSaveGap = req.param.weightSaveGap
    paramMod.InitSuperParam = req.param.initSuperParam
    paramMod.save(db)

    if restart:
        # startWork(StringIdReq(id=projectWork.Id))
        res_value = StringIdReq(id=projectWork.Id)
        start_work(res_value, db)


def get_project_work_by_id_impl(
        req: StringIdReq,
        db: Session
) -> SaveProjectWorkReq:
    work = ProjectWorkSql.select_by_id(db, req.id)
    ret = get_project_info(ProjectWork.from_orm(work), db)
    if ret is None:
        return None
    return ret


# 进度
def get_project_work_stage_by_id(req: StringIdReq, db: Session):
    loss_exec = config.config.exec_into(req.id)
    res_exec = exec_work2(loss_exec)
    res = get_last_row_log_stage(res_exec)
    return res


# loss获取， 目前从日志获取
def get_project_work_inter_by_id(req: StringIdReq, db: Session):
    loss_exec = config.config.exec_into(req.id)
    res_exec = exec_work2(loss_exec)
    res = get_last_row_loss(res_exec)
    return res


def get_project_work_type_by_id(
        req: StringIdReq,
        db: Session
) -> ProjectWorkTypeReply:
    work_type = ProjectWorkType.select_by_id(db, req.id)
    if work_type is None:
        return None
    ret = ProjectWorkTypeReply.from_orm(work_type)
    return ret


def get_project_work_type_list_impl(
        db: Session
) -> GetProjectWorkTypeListReply:
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
        raise Exception("id不存在")
    saveProjectWorkReq.work = ProjectWork.from_orm(work)

    # 查询参数
    param = ProjectWorkParamSql.select_by_project_work_id(db, work.Id)
    if param is not None:
        saveProjectWorkReq.param = ProjectWorkParam.from_orm(param)

    # 模型类型
    type = get_module_type_by_id_impl(StringIdReq(id=work.ModuleTypeId), db)
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
        req: ListByPageReq,
        db: Session,
        # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectWorkListByPageReply:
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
        reply.list.append(get_project_info(pw, db))

    return reply


def run_work(command: str):
    # 检查进程是否已启动
    exec_work(command)


# 开始任务
def start_work(req: StringIdReq, db: Session):
    # TODO 开始运行完后的结果获取
    res_work = ProjectWorkSql.select_by_id(db, req.id)
    module = ModuleSql.select_by_id(db, res_work.ModuleId)
    res_work.WorkStatus = 0
    res_work.save(db)
    # 启动一个新的线程执行工作
    # work_process = multiprocessing.Process(target=run_work, args=(req.id, config.config.start_into(res_work.DataId)))
    command = config.config.start_into(res_work.DataId, req.id, module.ModuleName)
    work_process = multiprocessing.Process(target=run_work, args=(command,))
    work_process.start()


# 停止任务
def stop_work(req: StringIdReq, db: Session):
    work = ProjectWorkSql.select_by_id(db, req.id)
    if work.WorkStatus == 2:
        raise Exception("任务暂未开启！")
    else:
        work.WorkStatus = 2
        work.save(db)
    # 关闭pid
    # 设置配置文件路径 TODO 设置动态从前端获取
    conf_path = "/data/disk2/yolov8/app/"
    # 等待 500 毫秒
    time.sleep(0.5)
    # 构建 shell 命令
    command = f"ps -ef | grep {conf_path}config.py | grep -v grep | awk '{{print $2}}' | xargs kill -9"
    exec_work(command)
    # work获取
    Project.flush_project_work_num(db, work.ProjectId)
