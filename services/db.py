from datetime import datetime
from sqlmodel import Session
from sqlmodels.user import User
from config.config import *

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
            num = User.exist_username("basic", session)
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
        print(f"fail to open sqlite: {e}")
