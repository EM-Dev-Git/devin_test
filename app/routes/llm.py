"""
AI問い合わせのためのAPIルーター

このモジュールはOpenAI APIを使用したAI問い合わせエンドポイントを提供します。
すべてのエンドポイントは認証が必要で、プロンプトテンプレートを使用して
OpenAI APIにリクエストを送信します。
"""
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.llm import LLMRequest, LLMResponse
from app.utils.openai_client import generate_response
from app.prompts.chat_prompt import get_chat_prompt

logger = logging.getLogger("app")

router = APIRouter(
    prefix="/llm",
    tags=["AI問い合わせ"],
    responses={
        401: {"description": "認証されていません"},
        500: {"description": "OpenAI APIエラー"}
    },
)

@router.post("/chat", response_model=LLMResponse, status_code=status.HTTP_200_OK)
async def chat_with_ai(
    request: LLMRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    AIとチャットする
    
    OpenAI APIを使用してAIとチャットします。このエンドポイントは認証が必要です。
    
    - **prompt**: ユーザーの質問やプロンプト（必須）
    - **max_tokens**: 生成する最大トークン数（オプション、デフォルト: 1000）
    - **temperature**: 応答の多様性を制御するパラメータ（オプション、デフォルト: 0.7）
    
    プロンプトはテンプレートに適用され、OpenAI APIに送信されます。
    応答には生成されたテキスト、使用されたモデル、トークン使用量が含まれます。
    
    APIキーが設定されていない場合や、OpenAI APIでエラーが発生した場合は
    500エラーが返されます。
    """
    try:
        messages = get_chat_prompt(request.prompt)
        
        logger.info(f"LLM request from user {current_user.username} with prompt length {len(request.prompt)}")
        
        response = await generate_response(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        logger.info(f"LLM response generated for user {current_user.username}, tokens used: {response.get('usage', {}).get('total_tokens', 0)}")
        
        return response
    except ValueError as ve:
        logger.error(f"Value error in LLM request: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"API configuration error: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error in LLM request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating AI response: {str(e)}"
        )
