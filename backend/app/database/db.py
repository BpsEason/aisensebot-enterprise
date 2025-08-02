from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 從 .env 檔案中取得資料庫 URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 建立一個 SQLAlchemy 引擎
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 建立一個 SessionLocal 類別，用於建立資料庫會話
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立一個基類 (Base)
Base = declarative_base()

def get_db():
    """
    建立並回傳一個新的資料庫會話，並在完成後關閉它。
    這個函數將被用作 FastAPI 的依賴注入 (Dependency Injection)。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()