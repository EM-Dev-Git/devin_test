"""
OpenAI APIクライアントユーティリティ

このモジュールはOpenAI APIとの通信を処理するためのユーティリティ関数を提供します。
環境変数からAPIキーを取得し、チャット完了APIを使用してAI応答を生成します。
"""
import os
import logging
from openai import OpenAI
from typing import Dict, List, Any, Optional

logger = logging.getLogger("app")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

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
        if not client.api_key or client.api_key == "":
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key not configured")
            
        # OpenAI APIにリクエストを送信
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
