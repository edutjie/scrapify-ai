from typing import Optional
from pydantic import BaseModel, Field


class PersonLookupRequest(BaseModel):
    company_url: str = Field(
        ...,
        description="The LinkedIn company URL to scrape for employee information",
    )
    role: str = Field(
        ...,
        description="The role or job title of the employee to search for",
    )
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
    search_instructions: Optional[str] = Field(
        None,
        description="Optional specific instructions for the web search (e.g., time range, site restrictions)",
    )


class PersonLookupResponse(BaseModel):
    response: str = Field(..., description="The LLM's response to the query")
