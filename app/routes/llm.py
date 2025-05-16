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
    tags=["llm"],
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "OpenAI API Error"}
    },
)

@router.post("/chat", response_model=LLMResponse, status_code=status.HTTP_200_OK)
async def chat_with_ai(
    request: LLMRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Chat with AI using OpenAI API.
    Requires authentication.
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
