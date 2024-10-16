from typing import Optional, List

from sqlalchemy import func
from sqlmodel import SQLModel, Field, select, Session


class Module(SQLModel, table=True):
    __tablename__ = "t_module"
    Id: str = Field(default=None, primary_key=True, nullable=False, index=True)
    ModuleName: Optional[str] = Field(default=None, index=True)
    ModuleTypeId: Optional[str] = Field(default=None)
    FrameId: Optional[str] = Field(default=None)
    Detail: Optional[str] = Field(default=None)
    ModuleFile: Optional[str] = Field(default=None)
    IsDelete: Optional[bool] = Field(default=False)
    CreateUid: Optional[str] = Field(default=None)
    CreateTime: Optional[str] = Field(default=None)
    Sort: Optional[str] = Field(default=None)

    @classmethod
    def find_by_page(cls, session: Session, uid: str, page: int, size: int, like: Optional[str] = None) -> (
            List["Module"], int):
        query = select(cls).where(cls.CreateUid == uid, cls.IsDelete == False)

        # 如果存在 like 参数，添加筛选条件
        if like:
            query = query.where(
                (cls.ModuleName.ilike(f"%{like}%")) |
                (cls.Detail.ilike(f"%{like}%"))
            ).order_by(cls.Sort)

        # 计数查询
        # 修正后的计数查询
        count_query = select(func.count()).select_from(query.subquery())
        count = session.exec(count_query).first()

        # 分页查询
        offset = (page - 1) * size
        result = session.exec(query.offset(offset).limit(size)).all()

        return result, count

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional["Module"]:
        return session.get(cls, id)

    def save(self, session: Session):
        session.merge(self)
        session.commit()

    def delete(self, session: Session):
        module = self.select_by_id(session, self.Id)
        if module:
            module.IsDelete = True
            session.commit()
        else:
            raise Exception("Module not found")
