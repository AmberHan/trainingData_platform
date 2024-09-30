from sqlmodel import SQLModel, Field, Session, select
from typing import Optional

class ProjectWorkParam(SQLModel, table=True):
    __tablename__ = "t_project_work_param"
    Id: str = Field(default=None, primary_key=True)
    ProjectId: Optional[str] = Field(default=None)
    ProjectWorkId: Optional[str] = Field(default=None)
    Evaluation: Optional[str] = Field(default=None)
    LearningRate: Optional[str] = Field(default=None)
    Impulse: Optional[str] = Field(default=None)
    Optimizer: Optional[str] = Field(default=None)
    IsUseDataExtend: Optional[bool] = Field(default=None)
    TrainDataCount: Optional[str] = Field(default=None)
    ScallDataCount: Optional[str] = Field(default=None)
    TestGap: Optional[str] = Field(default=None)
    MaxIteration: Optional[str] = Field(default=None)
    WeightSaveGap: Optional[str] = Field(default=None)
    InitSuperParam: Optional[str] = Field(default=None)

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["ProjectWorkParam"]:
        # 通过主键 ID 查找记录
        return session.get(cls, id)

    @classmethod
    def select_by_project_work_id(cls, session: Session, project_work_id: str) -> Optional["ProjectWorkParam"]:
        # 根据 ProjectWorkId 查找记录
        statement = select(cls).where(cls.ProjectWorkId == project_work_id)
        return session.exec(statement).first()

    def save(self, session: Session):
        # 保存记录
        session.add(self)
        session.commit()
