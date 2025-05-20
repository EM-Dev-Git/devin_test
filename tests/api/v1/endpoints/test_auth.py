"""
認証機能のテスト

このモジュールはユーザー登録とトークン取得のAPIエンドポイントのテストを提供します。
"""
import pytest
from fastapi.testclient import TestClient
import time
import logging

logger = logging.getLogger("test")

def test_register_user(client):
    """
    AUTH-001: ユーザー登録のテスト
    
    有効なユーザーデータでユーザー登録エンドポイントにリクエストを送信し、
    正常に登録されることを確認します。
    """
    logger.info("テスト開始: ユーザー登録のテスト")
    start_time = time.time()
    
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "Password123!"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 201
    assert "message" in response.json()
    assert "successfully" in response.json()["message"]
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: ユーザー登録のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "AUTH-001",
        "status": "成功",
        "execution_time": execution_time,
        "details": "新規ユーザーが正常に登録されました。"
    }

def test_register_duplicate_user(client, test_user):
    """
    AUTH-002: 重複ユーザー登録のテスト
    
    既に存在するユーザー名でユーザー登録エンドポイントにリクエストを送信し、
    エラーが返されることを確認します。
    """
    logger.info("テスト開始: 重複ユーザー登録のテスト")
    start_time = time.time()
    
    user_data = {
        "username": "testuser",  # 既存のユーザー名
        "email": "another@example.com",
        "password": "Password123!"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 400
    assert "detail" in response.json()
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: 重複ユーザー登録のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "AUTH-002",
        "status": "成功",
        "execution_time": execution_time,
        "details": "既存のユーザー名で登録を試みた際に適切なエラーが返されました。"
    }

def test_login_for_access_token(client, test_user):
    """
    AUTH-003: トークン取得のテスト
    
    有効な認証情報でトークン取得エンドポイントにリクエストを送信し、
    JWTトークンが返されることを確認します。
    """
    logger.info("テスト開始: トークン取得のテスト")
    start_time = time.time()
    
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/auth/token", data=login_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: トークン取得のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "AUTH-003",
        "status": "成功",
        "execution_time": execution_time,
        "details": "有効な認証情報でJWTトークンが正常に取得できました。"
    }

def test_login_with_invalid_credentials(client):
    """
    AUTH-004: 無効な認証情報でのログインテスト
    
    無効なパスワードでトークン取得エンドポイントにリクエストを送信し、
    認証エラーが返されることを確認します。
    """
    logger.info("テスト開始: 無効な認証情報でのログインテスト")
    start_time = time.time()
    
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/token", data=login_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == "Bearer"
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: 無効な認証情報でのログインテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "AUTH-004",
        "status": "成功",
        "execution_time": execution_time,
        "details": "無効なパスワードで適切な認証エラーが返されました。"
    }
