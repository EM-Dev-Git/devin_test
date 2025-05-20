"""
LLMサービスモジュール

このモジュールはOpenAI APIを使用したLLM（大規模言語モデル）サービスを提供します。
チャット応答の生成や自己紹介プロンプトの処理を担当します。
"""
from typing import Dict, Any, Optional
import logging

from app.utils.openai_client import generate_response
from app.prompts.chat_prompt import get_chat_prompt, get_masui_prompt
from app.schemas.llm import LLMRequest

logger = logging.getLogger("app")

async def generate_chat_response(request: LLMRequest, username: str) -> Dict[str, Any]:
    """
    チャットレスポンスを生成する
    
    Args:
        request: LLMリクエスト情報
        username: リクエストを行ったユーザー名
        
    Returns:
        生成されたレスポンス情報
        
    Raises:
        ValueError: APIキーが設定されていない場合
        Exception: API呼び出し中にエラーが発生した場合
    """
    logger.info(f"Generating chat response for user {username} with prompt length {len(request.prompt)}")
    
    messages = get_chat_prompt(request.prompt)
    
    response = await generate_response(
        messages=messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    
    logger.info(f"Chat response generated for user {username}, tokens used: {response.get('usage', {}).get('total_tokens', 0)}")
    
    return response

async def generate_masui_introduction(username: Optional[str] = None) -> Dict[str, Any]:
    """
    自己紹介レスポンスを生成する
    
    Args:
        username: リクエストを行ったユーザー名（オプション）
        
    Returns:
        生成された自己紹介レスポンス情報
        
    Raises:
        ValueError: APIキーが設定されていない場合
        Exception: API呼び出し中にエラーが発生した場合
    """
    logger.info(f"Generating masui self-introduction for user {username}")
    
    messages = get_masui_prompt(username)
    
    response = await generate_response(
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )
    
    logger.info(f"Masui self-introduction generated for user {username}, tokens used: {response.get('usage', {}).get('total_tokens', 0)}")
    
    return response
