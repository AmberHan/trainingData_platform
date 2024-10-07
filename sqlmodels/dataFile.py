from typing import Optional, List

from sqlalchemy import func
from sqlmodel import SQLModel, Field, select, Session


class DataFile(SQLModel, table=True):
    __tablename__ = "t_data_file"
    Id: Optional[int] = Field(default=None, primary_key=True)
    DataId: Optional[str] = Field(default=None)
    FilePath: Optional[str] = Field(default=None)
    Url: Optional[str] = Field(default=None)
    FileType: Optional[int] = Field(default=None)
    DirPath: Optional[str] = Field(default=None)

    @classmethod
    def find_by_page(cls, session: Session, data_id: str, file_type: int, page: int, size: int) -> (
            List["DataFile"], int):
        query = select(cls).where(cls.DataId == data_id)
        if file_type != 0:
            query = query.where(cls.FileType == file_type)

        # 计算总数
        count_query = select(func.count()).select_from(query.subquery())
        count = session.exec(count_query).first()

        # 分页查询
        offset = (page - 1) * size
        result = session.exec(query.offset(offset).limit(size)).all()

        return result, count

    @classmethod
    def find_all_by_data_id(cls, session: Session, data_id: str) -> List["DataFile"]:
        # 根据 data_id 查找所有文件
        statement = select(cls).where(cls.DataId == data_id)
        return session.exec(statement).all()

    @classmethod
    def select_by_id(cls, session: Session, id: int) -> Optional["DataFile"]:
        # 根据 ID 查找记录
        return session.get(cls, id)

    @classmethod
    def find_by_data_id(cls, session: Session, data_id: str) -> List["DataFile"]:
        # 根据 data_id 查找文件记录
        statement = select(cls).where(cls.DataId == data_id)
        return session.exec(statement).all()

    @classmethod
    def find_by_data_id_and_type(cls, session: Session, data_id: str, file_type: int) -> List["DataFile"]:
        # 根据 data_id 和 file_type 查找文件记录
        statement = select(cls).where(cls.DataId == data_id, cls.FileType == file_type)
        return session.exec(statement).all()

    def save(self, session: Session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            raise Exception("save failed")

    def delete(self, session: Session):
        try:
            statement = select(self.__class__).where(self.__class__.Id == self.Id)
            result = session.exec(statement).first()
            if result:
                session.delete(result)
                session.commit()
        except Exception as e:
            raise Exception("delete failed")

    @classmethod
    def delete_by_data_id(cls, session: Session, data_id: str):
        # 根据 data_id 删除 fileType = 0 的记录
        statement = select(cls).where(cls.DataId == data_id, cls.FileType == 0)
        results = session.exec(statement).all()
        for result in results:
            session.delete(result)
        session.commit()

    @classmethod
    def delete_by_type_and_data_id(cls, session: Session, type_id: int, data_id: str):
        # 根据 data_id 和 file_type 删除记录
        statement = select(cls).where(cls.DataId == data_id, cls.FileType == type_id)
        results = session.exec(statement).all()
        for result in results:
            session.delete(result)
        session.commit()
