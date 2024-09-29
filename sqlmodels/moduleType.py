from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List

class ModuleType(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True, nullable=False)
    moduleTypeName: Optional[str] = Field(default=None)
    createWay: Optional[str] = Field(default=None)
    icon: Optional[str] = Field(default=None)
    createTime: Optional[str] = Field(default=None)

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["ModuleType"]:
        # 通过主键 ID 查找 ModuleType 记录
        return session.get(cls, id)

    @classmethod
    def find_all(cls, session: Session) -> List["ModuleType"]:
        # 查找所有 ModuleType 记录
        return session.exec(select(cls)).all()
