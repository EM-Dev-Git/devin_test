"""
基本エンドポイントのテスト

このモジュールはルートエンドポイントとヘルスチェックエンドポイントのテストを提供します。
"""
import pytest
from fastapi.testclient import TestClient
import time
import logging

logger = logging.getLogger("test")

def test_root_endpoint(client):
    """
    BASE-001: ルートエンドポイントのテスト
    
    ルートエンドポイント（/）にアクセスして正しいレスポンスが返されることを確認します。
    """
    logger.info("テスト開始: ルートエンドポイントのテスト")
    start_time = time.time()
    
    response = client.get("/")
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome to EM_test_project API" in response.json()["message"]
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: ルートエンドポイントのテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "BASE-001",
        "status": "成功",
        "execution_time": execution_time,
        "details": "ルートエンドポイントが正常に応答しました。"
    }

def test_health_check_endpoint(client):
    """
    BASE-002: ヘルスチェックエンドポイントのテスト
    
    ヘルスチェックエンドポイント（/health）にアクセスして正しいレスポンスが返されることを確認します。
    """
    logger.info("テスト開始: ヘルスチェックエンドポイントのテスト")
    start_time = time.time()
    
    response = client.get("/health")
    
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: ヘルスチェックエンドポイントのテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "BASE-002",
        "status": "成功",
        "execution_time": execution_time,
        "details": "ヘルスチェックエンドポイントが正常に応答しました。"
    }
