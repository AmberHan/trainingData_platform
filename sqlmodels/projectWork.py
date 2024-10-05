from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List
from sqlalchemy import func


class ProjectWork(SQLModel, table=True):
    __tablename__ = "t_project_work"
    Id: str = Field(default=None, primary_key=True, nullable=False)
    ProjectId: Optional[str] = Field(default=None)
    ModuleTypeId: Optional[str] = Field(default=None)
    ModuleFrameId: Optional[str] = Field(default=None)
    ProjectWorkTypeId: Optional[str] = Field(default=None)
    WorkName: Optional[str] = Field(default=None)
    Detail: Optional[str] = Field(default=None)
    DataId: Optional[str] = Field(default=None)
    ModuleId: Optional[str] = Field(default=None)
    CreateUid: Optional[str] = Field(default=None)
    CreateTime: Optional[str] = Field(default=None)
    IsDelete: Optional[bool] = Field(default=False)
    WorkStatus: Optional[int] = Field(default=None)
    WorkStage: Optional[str] = Field(default=None)
    StartTime: Optional[str] = Field(default=None)
    UpdateTime: Optional[str] = Field(default=None)

    @classmethod
    def find_by_page(cls, session: Session, uid: str, project_id: str, page: int, size: int,
                     like: Optional[str] = None) -> (List["ProjectWork"], int):
        query = select(cls).where(cls.CreateUid == uid, cls.ProjectId == project_id, cls.IsDelete == False)

        if like:
            query = query.where(
                (cls.WorkName.ilike(f"%{like}%")) |
                (cls.Detail.ilike(f"%{like}%"))
            )

        # 计算总数
        count_query = select(func.count()).select_from(query.subquery())
        count = session.exec(count_query).first()

        # 分页查询
        offset = (page - 1) * size
        result = session.exec(query.offset(offset).limit(size)).all()

        return result, count

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["ProjectWork"]:
        return session.get(cls, id)


    @classmethod
    def name_exists(cls, session: Session, uid: str, work_name: str) -> bool:
        return session.exec(
            select(cls).where(cls.CreateUid == uid, cls.WorkName == work_name, cls.IsDelete == False)
        ).first() is not None


    def save(self, session: Session):
        session.add(self)
        session.commit()


    def delete(self, session: Session):
        project_work = self.select_by_id(session, self.Id)
        if project_work:
            project_work.IsDelete = True
            session.commit()
        else:
            raise Exception("ProjectWork not found")
