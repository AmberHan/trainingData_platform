# schemas/project.py
from typing import Optional, List

from pydantic import BaseModel

from sqlmodels.project import Project
from sqlmodels.projectWork import ProjectWork as ProjectWorkSql
from sqlmodels.projectWorkParam import ProjectWorkParam as ProjectWorkParamSql


# 假设你已经定义了 SaveProjectReq 模型
# class SaveProjectReq(BaseModel):
#     id: str
#     project_name: str
#     module_type_id: str
#     create_uid: str
#     detail: Optional[str] = None  # 可选字段

# 分页响应模型
# class GetProjectListByPageReply(BaseModel):
#     total: int  # 总条目数
#     list: List[SaveProjectReq]  # 项目列表

# class GetProjectListByPageReq(BaseModel):
#     page: Optional[int] = 1  # 默认值为 1
#     size: Optional[int] = 5  # 默认值为 5
#     like: Optional[str] = None  # 可选字符串，默认为 None

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
    def from_orm(cls, project_work: ProjectWorkSql) -> 'ProjectWork':
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
    def from_orm(cls, param: ProjectWorkParamSql) -> 'ProjectWorkParam':
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


class GetProjectListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveProjectReq] = []
