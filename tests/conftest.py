"""
テスト用の共通フィクスチャとヘルパー関数を提供するモジュール

このモジュールは単体テストのためのpytestフィクスチャとヘルパー関数を定義します。
テストデータベースの設定、テストクライアントの作成、認証トークンの生成などを行います。
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import logging
from datetime import datetime, timedelta
from typing import Dict, Generator, List, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.models.item import Item
from app.utils.auth import get_password_hash, create_access_token
from app.core.config import settings

os.makedirs("tests/temp", exist_ok=True)

test_logger = logging.getLogger("test")
test_logger.setLevel(logging.INFO)
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
log_filename = f"tests/temp/test_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)
test_logger.addHandler(file_handler)

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine():
    """テスト用のSQLAlchemyエンジンを提供するフィクスチャ"""
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine

@pytest.fixture(scope="function")
def test_db(test_engine):
    """テスト用のデータベースを提供するフィクスチャ"""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    
    try:
        from app.models.user import User
        from app.models.item import Item
        from app.utils.auth import get_password_hash
        
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            is_active=True
        )
        db.add(test_user)
        db.commit()
        
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client(test_db):
    """テスト用のFastAPIクライアントを提供するフィクスチャ"""
    def _get_test_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(test_db):
    """テスト用のユーザーを提供するフィクスチャ"""
    user = test_db.query(User).filter(User.username == "testuser").first()
    if not user:
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            is_active=True
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def inactive_user(test_db):
    """非アクティブなテスト用ユーザーを提供するフィクスチャ"""
    user = test_db.query(User).filter(User.username == "inactiveuser").first()
    if not user:
        user = User(
            username="inactiveuser",
            email="inactive@example.com",
            hashed_password=get_password_hash("testpassword"),
            is_active=False
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def token(test_user):
    """テスト用のJWTトークンを提供するフィクスチャ"""
    return create_access_token(
        data={"sub": test_user.username}
    )

@pytest.fixture(scope="function")
def expired_token(test_user):
    """期限切れのJWTトークンを提供するフィクスチャ"""
    return create_access_token(
        data={"sub": test_user.username},
        expires_delta=timedelta(minutes=-30)
    )

@pytest.fixture(scope="function")
def authorized_client(client, token):
    """認証済みのテストクライアントを提供するフィクスチャ"""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture(scope="function")
def mock_openai_response():
    """OpenAI APIのモックレスポンスを提供するフィクスチャ"""
    return {
        "response": "これはOpenAI APIからのモックレスポンスです。",
        "model": "gpt-3.5-turbo",
        "usage": {
            "prompt_tokens": 50,
            "completion_tokens": 30,
            "total_tokens": 80
        }
    }
