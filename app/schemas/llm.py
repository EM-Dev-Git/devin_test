from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    """Schema for LLM API request."""
    prompt: str = Field(..., description="User input or question")
    max_tokens: Optional[int] = Field(1000, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Temperature for response generation")

class LLMResponse(BaseModel):
    """Schema for LLM API response."""
    response: str = Field(..., description="Generated response from AI")
    model: Optional[str] = Field(None, description="Model used for generation")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage information")
