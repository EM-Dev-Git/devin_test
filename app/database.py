"""
データベース設定モジュール

このモジュールはSQLAlchemyを使用してSQLiteデータベースへの接続を設定します。
データベースエンジン、セッション、ベースモデルクラスを提供します。
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

os.makedirs("sqlite_db", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_db/app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    データベースセッションの依存関数
    
    FastAPIのDependencyとして使用され、リクエストごとに新しいセッションを提供します。
    リクエスト処理が完了すると、セッションは自動的に閉じられます。
    
    Yields:
        Session: SQLAlchemyデータベースセッション
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
