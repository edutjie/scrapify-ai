from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's query to process")
    model: Optional[str] = Field(
        default="gpt-4o",
        description="The OpenAI model to use (defaults to gpt-4o if not specified)",
    )
    temperature: Optional[float] = Field(
        0.5,
        description="Sampling temperature for the LLM response (default is 0.5)",
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="The LLM's response to the query")
