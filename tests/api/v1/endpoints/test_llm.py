"""
LLM/OpenAI機能のテスト

このモジュールはOpenAI APIを使用したAIチャットエンドポイントのテストを提供します。
"""
import pytest
from fastapi.testclient import TestClient
import time
import logging
from unittest.mock import patch, MagicMock

from tests.utils.openai_mock import mock_openai_client, openai_patch

logger = logging.getLogger("test")

@pytest.fixture
def mock_openai(monkeypatch):
    """OpenAI APIをモックするフィクスチャ"""
    return mock_openai_client(monkeypatch, "これはAIからのテスト応答です。")

def test_chat_with_ai(authorized_client, mock_openai):
    """
    LLM-001: AIチャットのテスト
    
    認証済みユーザーがAIチャットエンドポイントを使用して
    OpenAI APIからレスポンスを取得できることを確認します。
    """
    logger.info("テスト開始: AIチャットのテスト")
    start_time = time.time()
    
    request_data = {
        "prompt": "こんにちは、AIさん。",
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = authorized_client.post("/api/v1/llm/chat", json=request_data)
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert "model" in response.json()
    assert "usage" in response.json()
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: AIチャットのテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "LLM-001",
        "status": "成功",
        "execution_time": execution_time,
        "details": "AIチャットエンドポイントが正常に応答しました。"
    }

def test_chat_with_ai_unauthorized(client, mock_openai):
    """
    LLM-002: AIチャット（認証エラー）のテスト
    
    未認証ユーザーがAIチャットエンドポイントにアクセスした際に
    401エラーが返されることを確認します。
    """
    logger.info("テスト開始: AIチャット（認証エラー）のテスト")
    start_time = time.time()
    
    request_data = {
        "prompt": "こんにちは、AIさん。",
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = client.post("/api/v1/llm/chat", json=request_data)
    
    assert response.status_code == 401
    assert "detail" in response.json()
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: AIチャット（認証エラー）のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "LLM-002",
        "status": "成功",
        "execution_time": execution_time,
        "details": "未認証ユーザーに対して適切な認証エラーが返されました。"
    }

def test_chat_with_ai_invalid_request(authorized_client, mock_openai):
    """
    LLM-003: AIチャット（無効なリクエスト）のテスト
    
    必須フィールドが欠けたリクエストを送信した際に
    422エラーが返されることを確認します。
    """
    logger.info("テスト開始: AIチャット（無効なリクエスト）のテスト")
    start_time = time.time()
    
    request_data = {
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = authorized_client.post("/api/v1/llm/chat", json=request_data)
    
    assert response.status_code == 422
    assert "detail" in response.json()
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: AIチャット（無効なリクエスト）のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "LLM-003",
        "status": "成功",
        "execution_time": execution_time,
        "details": "無効なリクエストに対して適切なバリデーションエラーが返されました。"
    }

def test_chat_with_ai_api_key_not_set(authorized_client, monkeypatch):
    """
    LLM-004: AIチャット（APIキー未設定）のテスト
    
    OpenAI APIキーが設定されていない場合に
    500エラーが返されることを確認します。
    """
    logger.info("テスト開始: AIチャット（APIキー未設定）のテスト")
    start_time = time.time()
    
    monkeypatch.setattr("app.core.config.settings.OPENAI_API_KEY", "")
    
    request_data = {
        "prompt": "こんにちは、AIさん。",
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = authorized_client.post("/api/v1/llm/chat", json=request_data)
    
    assert response.status_code == 500
    assert "detail" in response.json()
    assert "API configuration error" in response.json()["detail"]
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: AIチャット（APIキー未設定）のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "LLM-004",
        "status": "成功",
        "execution_time": execution_time,
        "details": "APIキー未設定時に適切なエラーが返されました。"
    }

def test_chat_with_ai_performance(authorized_client, mock_openai):
    """
    LLM-005: AIチャット（パフォーマンス）のテスト
    
    長いプロンプトを送信した際のレスポンス時間を測定します。
    """
    logger.info("テスト開始: AIチャット（パフォーマンス）のテスト")
    start_time = time.time()
    
    long_prompt = "こんにちは、AIさん。" * 100
    
    request_data = {
        "prompt": long_prompt,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = authorized_client.post("/api/v1/llm/chat", json=request_data)
    
    assert response.status_code == 200
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: AIチャット（パフォーマンス）のテスト (実行時間: {execution_time:.2f}秒)")
    
    assert execution_time < 10.0
    
    return {
        "test_id": "LLM-005",
        "status": "成功",
        "execution_time": execution_time,
        "details": f"長いプロンプトに対するレスポンス時間は {execution_time:.2f}秒でした。"
    }

def test_masui_introduction(authorized_client, mock_openai):
    """
    LLM-006: AI自己紹介のテスト
    
    認証済みユーザーがAI自己紹介エンドポイントを使用して
    OpenAI APIからレスポンスを取得できることを確認します。
    """
    logger.info("テスト開始: AI自己紹介のテスト")
    start_time = time.time()
    
    response = authorized_client.post("/api/v1/llm/masui")
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert "model" in response.json()
    assert "usage" in response.json()
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: AI自己紹介のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "LLM-006",
        "status": "成功",
        "execution_time": execution_time,
        "details": "AI自己紹介エンドポイントが正常に応答しました。"
    }
