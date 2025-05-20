"""
OpenAI APIクライアントユーティリティ

このモジュールはOpenAI APIとの通信を処理するためのユーティリティ関数を提供します。
設定クラスからAPIキーとエンドポイントを取得し、チャット完了APIを使用してAI応答を生成します。
"""
import logging
from openai import OpenAI
from typing import Dict, List, Any, Optional

from app.core.config import settings

logger = logging.getLogger("app")

def get_openai_client() -> OpenAI:
    """
    OpenAIクライアントのインスタンスを取得する
    
    設定クラスから取得したAPIキーとエンドポイントを使用して、
    OpenAIクライアントのインスタンスを生成します。
    
    Returns:
        OpenAI: OpenAIクライアントのインスタンス
        
    Raises:
        ValueError: APIキーが設定されていない場合
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
        logger.error("OpenAI API key not found")
        raise ValueError("OpenAI API key not configured")
    
    client_kwargs = {
        "api_key": settings.OPENAI_API_KEY,
    }
    
    if settings.OPENAI_API_BASE:
        client_kwargs["base_url"] = settings.OPENAI_API_BASE
        
    return OpenAI(**client_kwargs)

async def generate_response(
    messages: List[Dict[str, str]], 
    max_tokens: Optional[int] = 1000,
    temperature: Optional[float] = 0.7
) -> Dict[str, Any]:
    """
    OpenAI APIを使用して応答を生成する
    
    プロンプトテンプレートから生成されたメッセージリストを使用して、
    OpenAI APIにリクエストを送信し、AIからの応答を取得します。
    
    Args:
        messages: メッセージ辞書のリスト（role, contentキーを持つ）
        max_tokens: 生成する最大トークン数（オプション、デフォルト: 1000）
        temperature: 応答の多様性を制御するパラメータ（オプション、デフォルト: 0.7）
        
    Returns:
        Dict[str, Any]: OpenAI APIからのレスポンス（応答テキスト、モデル、使用量情報を含む）
        
    Raises:
        ValueError: APIキーが設定されていない場合
        Exception: API呼び出し中にエラーが発生した場合
    """
    try:
        client = get_openai_client()
            
        # OpenAI APIにリクエストを送信
        response = client.chat.completions.create(
            model=settings.OPENAI_API_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return {
            "response": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        logger.error(f"Error generating OpenAI response: {str(e)}")
        raise
