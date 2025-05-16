"""
AI問い合わせのためのPydanticスキーマ

このモジュールはOpenAI APIとの連携のためのPydanticモデルを定義します。
リクエストとレスポンスのデータ構造を定義し、APIとの通信を行います。
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    """
    AI問い合わせリクエストスキーマ
    
    OpenAI APIへのリクエストパラメータを定義します。
    ユーザーの入力プロンプトと生成設定を含みます。
    """
    prompt: str = Field(..., description="ユーザーの入力または質問")
    max_tokens: Optional[int] = Field(1000, description="生成する最大トークン数")
    temperature: Optional[float] = Field(0.7, description="応答の多様性を制御するパラメータ（0.0〜1.0）")

class LLMResponse(BaseModel):
    """
    AI問い合わせレスポンススキーマ
    
    OpenAI APIからのレスポンスデータを定義します。
    生成されたテキスト、使用されたモデル、トークン使用量を含みます。
    """
    response: str = Field(..., description="AIから生成された応答テキスト")
    model: Optional[str] = Field(None, description="使用されたAIモデル")
    usage: Optional[Dict[str, Any]] = Field(None, description="トークン使用量情報")
