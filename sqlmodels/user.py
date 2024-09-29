from typing import Optional
from sqlmodel import Field, SQLModel, Session, select, func


class User(SQLModel, table=True):
    __tablename__ = "t_user"
    id: Optional[str] = Field(default=None, primary_key=True, index=True)
    username: str
    password: str
    createTime: str
    isDelete: bool = Field(default=False)

    @classmethod
    def insert(cls, user: 'User', session: Session) -> bool:
        session.add(user)
        session.commit()
        return True

    @classmethod
    def update(cls, user: 'User', session: Session) -> bool:
        session.merge(user)
        session.commit()
        return True

    @classmethod
    def select_by_id(cls, id: str, session: Session) -> Optional['User']:
        return session.exec(select(User).where(User.id == id)).first()

    @classmethod
    def exist_username(cls, username: str, session: Session) -> int:
        result = session.exec(select(func.count()).where(cls.username == username)).one()
        return result

    @classmethod
    def get_user(cls, username: str, session: Session) -> 'User':
        result = session.exec(select(User).where(cls.username == username)).first()
        return result
