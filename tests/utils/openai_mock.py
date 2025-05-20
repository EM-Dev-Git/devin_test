"""
OpenAI APIのモック機能を提供するモジュール

このモジュールはOpenAI APIのレスポンスをモックするための関数やクラスを提供します。
単体テスト時に外部APIに依存せずにテストを実行するために使用します。
"""
from typing import Dict, List, Any, Optional
import json
import pytest
from unittest.mock import MagicMock, patch

class MockOpenAIResponse:
    """OpenAI APIのレスポンスをモックするクラス"""
    def __init__(self, content: str, model: str = "gpt-3.5-turbo", 
                 prompt_tokens: int = 50, completion_tokens: int = 30):
        self.choices = [
            MagicMock(
                message=MagicMock(
                    content=content
                )
            )
        ]
        self.model = model
        self.usage = MagicMock(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )

class MockOpenAIClient:
    """OpenAIクライアントをモックするクラス"""
    def __init__(self, response_content: str = "これはモックレスポンスです。"):
        self.chat = MagicMock()
        self.chat.completions = MagicMock()
        self.chat.completions.create = MagicMock(
            return_value=MockOpenAIResponse(response_content)
        )

def mock_openai_client(monkeypatch, response_content: str = "これはモックレスポンスです。"):
    """
    OpenAIクライアントをモックする
    
    Args:
        monkeypatch: pytestのmonkeypatchフィクスチャ
        response_content: モックレスポンスの内容
    """
    mock_client = MockOpenAIClient(response_content)
    
    def mock_get_openai_client():
        return mock_client
    
    from app.utils.openai_client import get_openai_client
    monkeypatch.setattr("app.utils.openai_client.get_openai_client", mock_get_openai_client)
    
    return mock_client

openai_patch = patch("app.utils.openai_client.get_openai_client")
