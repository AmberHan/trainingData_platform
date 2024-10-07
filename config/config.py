from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

db_path = "./db/atp.db"
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

config_path = {
    'FileConf': {
        'SavePath': './upload_files',  # 替换为你的存储路径
        'Uri': 'http://localhost/uploads/'  # 替换为你的 URI
    }
}