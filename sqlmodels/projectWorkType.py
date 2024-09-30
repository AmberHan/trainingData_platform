from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List

class ProjectWorkType(SQLModel, table=True):
    __tablename__ = "t_project_work_type"
    Id: str = Field(default=None, primary_key=True)
    TypeName: Optional[str] = Field(default=None)
    Icon: Optional[str] = Field(default=None)

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["ProjectWorkType"]:
        # 通过主键 ID 查找记录
        return session.get(cls, id)

    @classmethod
    def find_all(cls, session: Session) -> List["ProjectWorkType"]:
        # 查找所有 ProjectWorkType 记录
        statement = select(cls)
        return session.exec(statement).all()

    def save(self, session: Session):
        # 保存记录
        session.add(self)
        session.commit()
