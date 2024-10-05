from sqlalchemy import func
from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List

class DataStrong(SQLModel, table=True):
    __tablename__ = "t_data_strong"
    Id: str = Field(default=None, primary_key=True)
    DataId: Optional[str] = Field(default=None)
    StrongParam: Optional[str] = Field(default=None)
    IsDelete: Optional[bool] = Field(default=False)

    @classmethod
    def find_by_page(cls, session: Session, uid: str, page: int, size: int, like: Optional[str] = None) -> (List["DataStrong"], int):
        query = select(cls).where(cls.IsDelete == False)
        if like:
            query = query.where(
                (cls.ProjectName.ilike(f"%{like}%")) |
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
    def select_by_id(cls, session: Session, id: str) -> Optional["DataStrong"]:
        # 根据 ID 查找记录
        return session.get(cls, id)

    @classmethod
    def select_by_data_id(cls, session: Session, data_id: str) -> Optional["DataStrong"]:
        # 根据 DataId 查找记录
        statement = select(cls).where(cls.DataId == data_id)
        return session.exec(statement).first()

    def save(self, session: Session):
        # 保存记录
        session.add(self)
        session.commit()

    def delete(self, session: Session):
        # 软删除记录，将 IsDelete 设为 True
        data_strong = self.select_by_id(session, self.Id)
        if data_strong:
            data_strong.IsDelete = True
            session.commit()
        else:
            raise Exception("DataStrong not found")
