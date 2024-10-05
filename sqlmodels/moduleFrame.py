from typing import Optional, List

from sqlmodel import SQLModel, Field, select, Session


class ModuleFrame(SQLModel, table=True):
    __tablename__ = "t_module_frame"
    Id: str = Field(default=None, primary_key=True, nullable=False)
    FrameName: Optional[str] = Field(default=None)

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["ModuleFrame"]:
        # 通过主键 ID 查找 ModuleFrame 记录
        return session.get(cls, id)

    @classmethod
    def find_all(cls, session: Session) -> List["ModuleFrame"]:
        # 查找所有 ModuleFrame 记录
        return session.exec(select(cls)).all()
