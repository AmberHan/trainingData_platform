from typing import Optional, Sequence

from sqlmodel import Field, SQLModel, Session, select


class ModuleType(SQLModel, table=True):
    __tablename__ = "t_module_type"
    id: str = Field(primary_key=True, max_length=50, nullable=False)
    ModuleTypeName: str = Field(..., alias="moduleTypeName")
    CreateWay: str = Field(..., alias="createWay")
    Icon: str = Field(...)
    CreateTime: str = Field(..., alias="createTime")

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["ModuleType"]:
        return session.exec(select(cls).where(cls.id == id)).first()

    @classmethod
    def find_all(cls, session: Session) -> Sequence["ModuleType"]:
        return session.exec(select(cls)).all()

    def save(self, session: Session):
        session.merge(self)
        session.commit()