"""
OpenAI API client utilities.
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
    Generate a response using OpenAI API.
    
    Args:
        messages (List[Dict[str, str]]): List of message dictionaries
        max_tokens (int, optional): Maximum number of tokens to generate
        temperature (float, optional): Temperature for response generation
        
    Returns:
        Dict[str, Any]: Response from OpenAI API
    """
    try:
        if not client.api_key or client.api_key == "":
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key not configured")
            
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
