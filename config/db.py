from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from sqlmodel import create_engine

from config.config import config_path
from sqlmodels.user import User

engine = create_engine(f"sqlite:///{config_path['SysConf']['DbPath']}", connect_args={"check_same_thread": False},
                       echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


def init_data_db():
    try:
        with Session(engine) as session:
            # 检查用户是否存在
            num = User.exist_username(session, "basic")
            if num == 0:
                user = User(
                    id="25f0f097-71e7-4bb9-890b-32c42bd607bd",
                    username="basic",
                    password="EJvZ7rYJvtG/",
                    create_time=datetime.now()
                )
                if not user.insert(session):
                    raise Exception("没有插入basic成功")

    except Exception as e:
        raise Exception(f"fail to open sqlite: {e}")
