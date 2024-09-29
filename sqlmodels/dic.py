from sqlmodel import SQLModel, Field, Session, select
from typing import Optional, List

class Dic(SQLModel, table=True):
    Id: str = Field(default=None, primary_key=True)
    Value: Optional[str] = Field(default=None)
    Name: Optional[str] = Field(default=None)
    Type: Optional[str] = Field(default=None)
    Description: Optional[str] = Field(default=None)
    Sort: Optional[int] = Field(default=1)
    ParentId: Optional[str] = Field(default='0')
    ParentIds: Optional[str] = Field(default=None)

    @classmethod
    def insert(cls, session: Session, dic: "Dic") -> bool:
        # 插入新记录
        session.add(dic)
        session.commit()
        return True

    @classmethod
    def update(cls, session: Session, dic: "Dic") -> bool:
        # 更新记录
        statement = select(cls).where(cls.Id == dic.Id)
        result = session.exec(statement).first()
        if result:
            result.Value = dic.Value
            result.Name = dic.Name
            result.Type = dic.Type
            result.Description = dic.Description
            result.Sort = dic.Sort
            result.ParentId = dic.ParentId
            result.ParentIds = dic.ParentIds
            session.commit()
            return True
        return False

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["Dic"]:
        # 根据 ID 查询记录
        statement = select(cls).where(cls.Id == id)
        return session.exec(statement).first()

    @classmethod
    def delete_by_id(cls, session: Session, id: str) -> bool:
        # 根据 ID 删除记录
        statement = select(cls).where(cls.Id == id)
        result = session.exec(statement).first()
        if result:
            session.delete(result)
            session.commit()
            return True
        return False

    @classmethod
    def find_by_type(cls, session: Session, typ: str) -> List["Dic"]:
        # 根据 Type 查找记录
        statement = select(cls).where(cls.Type == typ)
        return session.exec(statement).all()
