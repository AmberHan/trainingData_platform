from typing import Optional

from sqlmodel import Field, SQLModel, Session, select, func


class User(SQLModel, table=True):
    __tablename__ = "t_user"
    id: Optional[str] = Field(default=None, primary_key=True, index=True)
    username: str
    password: str
    createTime: str
    isDelete: bool = Field(default=False)

    def insert(self, session: Session) -> bool:
        session.add(self)
        session.commit()
        return True

    @classmethod
    def update(cls, session: Session, user: 'User') -> bool:
        session.merge(user)
        session.commit()
        return True

    @classmethod
    def select_by_id(cls, session: Session, id: str) -> Optional['User']:
        return session.exec(select(User).where(User.id == id)).first()

    @classmethod
    def exist_username(cls, session: Session, username: str) -> int:
        result = session.exec(select(func.count()).where(cls.username == username)).one()
        return result

    @classmethod
    def get_user(cls, session: Session, username: str) -> 'User':
        result = session.exec(select(User).where(cls.username == username)).first()
        return result
