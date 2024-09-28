from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///./db/atp.db", connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)