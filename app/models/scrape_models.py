from typing import Optional
from pydantic import BaseModel, Field


class ScrapeRequest(BaseModel):
    web_url: str = Field(
        ...,
        description="The URL of the web page to scrape",
    )
    query: str = Field(..., description="The user's query to process")
    model: Optional[str] = Field(
        default="gpt-4o",
        description="The OpenAI model to use (defaults to gpt-4o if not specified)",
    )
    temperature: Optional[float] = Field(
        0,
        description="Sampling temperature for the LLM response (default is 0)",
        ge=0,
        le=1,
    )


class ScrapeResponse(BaseModel):
    response: str = Field(..., description="The LLM's response to the query")
