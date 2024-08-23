from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# 从环境变量中获取数据库连接信息
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:123456@localhost/student_management")

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建数据库基类
Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# 提供数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
