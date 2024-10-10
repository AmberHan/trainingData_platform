from schemas.data_model import DataReply
from schemas.moduleType_model import ModuleType
from schemas.module_model import Module
from schemas.project_model import *
from schemas.user_model import UserInfo
from sqlmodels.projectWorkType import ProjectWorkType as ProjectWorkTypeSql


class GetProjectWorkTypeListReply(BaseModel):
    list: List["ProjectWorkTypeReply"] = []


class ProjectWorkTypeReply(BaseModel):
    id: Optional[str] = None
    typeName: Optional[str] = None
    icon: Optional[str] = None

    @classmethod
    def from_orm(cls, work_type: ProjectWorkTypeSql) -> 'ProjectWorkTypeReply':
        return ProjectWorkTypeReply(
            id=work_type.Id,
            typeName=work_type.TypeName,
            icon=work_type.Icon
        )

class LossReply(BaseModel):
    box_loss: Optional[str] = None
    cls_loss: Optional[str] = None
    dfl_loss: Optional[str] = None
    loss: Optional[float] = None
    time: Optional[str] = None

class StageReply(BaseModel):
    stage: Optional[float] = None

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
    def from_orm(cls, project_work: ProjectWorkSql) -> 'SaveProjectWorkReq':
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


class GetProjectWorkListByPageReply(BaseModel):
    total: Optional[int] = None
    list: List[SaveProjectWorkReq] = []


