from typing import Optional, List

from sqlalchemy import func
from sqlmodel import SQLModel, Field, select, Session


class Data(SQLModel, table=True):
    __tablename__ = "t_data"
    Id: str = Field(default=None, primary_key=True)
    DataName: Optional[str] = Field(default=None)
    ModuleTypeId: Optional[str] = Field(default=None)
    Detail: Optional[str] = Field(default=None)
    IsTest: Optional[bool] = Field(default=False)
    DataStatus: Optional[int] = Field(default=None)
    UploadPath: Optional[str] = Field(default=None)
    ExportPath: Optional[str] = Field(default=None)
    ExportTime: Optional[str] = Field(default=None)
    FileSize: Optional[str] = Field(default=None)
    CreateUid: Optional[str] = Field(default=None)
    CreateTime: Optional[str] = Field(default=None)
    UpdateTime: Optional[str] = Field(default=None)
    IsDelete: Optional[bool] = Field(default=False)
    ClassNum: Optional[int] = Field(default=None)

    @classmethod
    def find_by_page(cls, uid: str, page: int, size: int, like: str, session: Session) -> (List["Data"], int):
        query = select(cls).where(cls.CreateUid == uid, cls.IsDelete == False)
        if like:
            query = query.where(
                (cls.DataName.ilike(f"%{like}%")) |
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
    def select_by_id(cls, session: Session, id: str) -> Optional["Data"]:
        # 根据 ID 查找记录
        return session.get(cls, id)

    def save(self, session: Session):
        # 保存记录
        session.add(self)
        session.commit()

    def delete(self, session: Session):
        # 软删除记录，将 IsDelete 设为 True
        data_record = self.select_by_id(session, self.Id)
        if data_record:
            data_record.IsDelete = True
            session.commit()
        else:
            raise Exception("Data not found")
