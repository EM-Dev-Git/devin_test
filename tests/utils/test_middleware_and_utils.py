"""
ミドルウェアとユーティリティのテスト

このモジュールはロギングミドルウェア、CORS設定、設定読み込み、JWTトークン検証のテストを提供します。
"""
import pytest
from fastapi.testclient import TestClient
import time
import logging
import os
from datetime import datetime, timedelta

from app.utils.auth import verify_password, get_password_hash, create_access_token, verify_token
from app.core.config import settings
from fastapi import HTTPException, status

logger = logging.getLogger("test")

def test_logging_middleware(client):
    """
    UTIL-001: ロギングミドルウェアのテスト
    
    リクエストがロギングミドルウェアによって正しくログに記録されることを確認します。
    """
    logger.info("テスト開始: ロギングミドルウェアのテスト")
    start_time = time.time()
    
    log_dir = "logs"
    if not os.path.exists(log_dir):
        pytest.skip("ログディレクトリが存在しません")
        
    log_files = [f for f in os.listdir(log_dir) if f.startswith("app_")]
    
    if not log_files:
        pytest.skip("ログファイルが見つかりません")
    
    latest_log = os.path.join(log_dir, sorted(log_files)[-1])
    initial_log_size = os.path.getsize(latest_log)
    
    response = client.get("/")
    
    assert os.path.getsize(latest_log) > initial_log_size
    
    with open(latest_log, "r") as f:
        log_content = f.read()
    
    assert "GET /" in log_content
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: ロギングミドルウェアのテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "UTIL-001",
        "status": "成功",
        "execution_time": execution_time,
        "details": "リクエストが正しくログに記録されました。"
    }

def test_cors_settings(client):
    """
    UTIL-002: CORS設定のテスト
    
    CORSヘッダーが正しく設定されていることを確認します。
    """
    logger.info("テスト開始: CORS設定のテスト")
    start_time = time.time()
    
    headers = {
        "Origin": "http://example.com",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = client.options("/api/v1/llm/chat", headers=headers)
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: CORS設定のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "UTIL-002",
        "status": "成功",
        "execution_time": execution_time,
        "details": "CORSヘッダーが正しく設定されています。"
    }

def test_settings_loading():
    """
    UTIL-003: 設定読み込みのテスト
    
    設定値が正しく読み込まれることを確認します。
    """
    logger.info("テスト開始: 設定読み込みのテスト")
    start_time = time.time()
    
    assert settings.APP_NAME == "EM_test_project"
    assert isinstance(settings.APP_VERSION, str)
    assert isinstance(settings.OPENAI_API_MODEL, str)
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: 設定読み込みのテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "UTIL-003",
        "status": "成功",
        "execution_time": execution_time,
        "details": "設定値が正しく読み込まれています。"
    }

def test_jwt_token_verification(client, test_user, expired_token):
    """
    UTIL-004: JWTトークン検証のテスト
    
    期限切れのJWTトークンが正しく検証されることを確認します。
    """
    logger.info("テスト開始: JWTトークン検証のテスト")
    start_time = time.time()
    
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/items/", headers=headers)
    
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "credentials" in response.json()["detail"]
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: JWTトークン検証のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "UTIL-004",
        "status": "成功",
        "execution_time": execution_time,
        "details": "期限切れトークンが正しく検証されました。"
    }
