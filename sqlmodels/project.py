from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List
from sqlalchemy import func, text


class Project(SQLModel, table=True):
    __tablename__ = "t_project"
    Id: str = Field(default=None, primary_key=True, index=True, nullable=False)
    ProjectName: Optional[str] = Field(default=None)
    ModuleTypeId: Optional[str] = Field(default=None)
    WorkTotalNum: Optional[int] = Field(default=None)
    WorkingNum: Optional[int] = Field(default=None)
    CompleteNum: Optional[int] = Field(default=None)
    CreateUid: Optional[str] = Field(default=None)
    Detail: Optional[str] = Field(default=None)
    IsDelete: Optional[bool] = Field(default=False)
    CreateTime: Optional[str] = Field(default=None)

    @classmethod
    def find_by_page(cls, uid:str, page: int, size: int, like: str, session: Session) -> (List["Project"], int):
        # 构建查询
        query = select(cls).where(cls.CreateUid == uid, cls.IsDelete == False)

        # 如果有 like 条件，添加过滤条件
        if like:
            query = query.where(
                (cls.ProjectName.ilike(f"%{like}%")) |
                (cls.Detail.ilike(f"%{like}%"))
            )

            # 计数查询：使用 func.count() 来计算总数
        count_query = select(func.count()).select_from(query.subquery())
        total_count = session.exec(count_query).first()  # 使用 first() 获取结果

        # 分页查询
        offset = (page - 1) * size
        result = session.exec(query.offset(offset).limit(size)).all()

        return result, total_count

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["Project"]:
        return session.get(cls, id)

    def save(self, session: Session):
        session.add(self)
        session.commit()

    def delete(self, session: Session):
        project = self.select_by_id(session, self.Id)
        if project:
            project.IsDelete = True
            session.commit()
        else:
            raise Exception("Project not found")

    @classmethod
    def flush_project_work_num(cls, session: Session, project_id: str):
        sql_update_work_total = text("""
            update t_project set WorkTotalNum = (
            select count(*) from t_project_work where ProjectId = :project_id and IsDelete = 0)
            where Id = :project_id
        """)
        session.execute(sql_update_work_total, {"project_id": project_id})

        sql_update_working_num = text("""
            update t_project set WorkingNum = (
            select count(*) from t_project_work where ProjectId = :project_id and WorkStatus = 0 and IsDelete = 0)
            where Id = :project_id
        """)
        session.execute(sql_update_working_num, {"project_id": project_id})

        sql_update_complete_num = text("""
            update t_project set CompleteNum = (
            select count(*) from t_project_work where ProjectId = :project_id and WorkStatus = 1 and IsDelete = 0)
            where Id = :project_id
        """)
        session.execute(sql_update_complete_num, {"project_id": project_id})

        session.commit()

    @classmethod
    def project_name_exists(cls, session: Session, uid: str, project_name: str) -> bool:
        return session.exec(
            select(cls).where(cls.CreateUid == uid, cls.ProjectName == project_name, cls.IsDelete == False)
        ).first() is not None
