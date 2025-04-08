from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's query to process")
    model: Optional[str] = Field(
        None,
        description="The OpenAI model to use (defaults to gpt-4o if not specified)",
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="The LLM's response to the query")
