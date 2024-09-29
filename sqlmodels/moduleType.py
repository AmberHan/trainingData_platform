from typing import List, Optional, Sequence
from sqlmodel import Field, SQLModel, Session, select, func


class ModuleType(SQLModel, table=True):
    __tablename__ = "t_module_type"
    id: str = Field(primary_key=True, max_length=50, nullable=False)
    ModuleTypeName: str = Field(..., alias="moduleTypeName")
    CreateWay: str = Field(..., alias="createWay")
    Icon: str = Field(...)
    CreateTime: str = Field(..., alias="createTime")

    @classmethod
    def select_by_id(cls, id: str, session: Session) -> Optional["ModuleType"]:
        return session.exec(select(cls).where(cls.id == id)).first()

    @classmethod
    def find_all(cls, session: Session) -> Sequence["ModuleType"]:
        return session.exec(select(cls)).all()
