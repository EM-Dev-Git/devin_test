"""
データベースセッションモジュール

このモジュールはSQLAlchemyセッションの作成と管理を行います。
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

logger = logging.getLogger("app")

os.makedirs("sqlite_db", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_db/app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    データベースセッションを取得するための依存関係関数
    
    FastAPIの依存関係注入システムで使用され、
    リクエスト処理中にデータベースセッションを提供します。
    
    Yields:
        Session: SQLAlchemyセッションオブジェクト
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
