from typing import Annotated
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field

from app.models.chat_models import ChatRequest, ChatResponse
from app.models.person_lookup_models import PersonLookupRequest, PersonLookupResponse
from app.models.scrape_models import ScrapeRequest, ScrapeResponse
from app.models.websearch_models import WebSearchRequest, WebSearchResponse
from app.models.company_models import (
    CompanyProfile,
    CompanyScrapeRequest,
    CompanyScrapeResponse,
)
from app.services.llm_service import LLMService
from app.services.agent_service import AgentService
from app.services.linkedin_scraper_service import LinkedInScraperService

app = FastAPI(
    title="Scrapify AI",
    description="A service for scraping and processing data using LLMs",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service
llm_service = LLMService()
# Initialize agent service
agent_service = AgentService()
# Initialize linkedin scraper service
linkedin_scraper_service = LinkedInScraperService()


async def get_api_key(x_api_key: str = Header(...)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key is required")
    return x_api_key


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_llm(request: ChatRequest, api_key: str = Depends(get_api_key)):
    """
    Chat with the LLM using OpenAI.
    Requires an API key in the X-API-Key header.
    """
    try:
        response = await llm_service.generate_response(
            query=request.query,
            api_key=api_key,
            model=request.model,
            temperature=request.temperature,
            response_model=str,
        )
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/websearch", response_model=WebSearchResponse)
async def run_agent(request: WebSearchRequest, api_key: str = Depends(get_api_key)):
    """
    Run a ReAct agent with Google search and web scraping capabilities.
    Requires an API key in the X-API-Key header.
    """
    try:
        response = await agent_service.run_websearch_agent(
            query=request.query,
            api_key=api_key,
            search_instructions=request.search_instructions,
            model=request.model,
            temperature=request.temperature,
        )
        return WebSearchResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/person-lookup", response_model=PersonLookupResponse)
async def run_person_lookup_agent(
    request: PersonLookupRequest, api_key: str = Depends(get_api_key)
):
    """
    Run a ReAct agent with Google search and web scraping capabilities for person lookup.
    Requires an API key in the X-API-Key header.
    """
    try:
        response = await agent_service.run_person_lookup(
            company_url=request.company_url,
            role=request.role,
            api_key=api_key,
            model=request.model,
            temperature=request.temperature,
        )
        return PersonLookupResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_agent(request: ScrapeRequest, api_key: str = Depends(get_api_key)):
    """
    Run a web scraping agent using the provided URL and query.
    Requires an API key in the X-API-Key header.
    """
    try:
        response = await agent_service.run_scrape_agent(
            web_url=request.web_url,
            query=request.query,
            api_key=api_key,
            model=request.model,
            temperature=request.temperature,
        )
        return ScrapeResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/company", response_model=CompanyScrapeResponse)
async def scrape_company(request: CompanyScrapeRequest):
    """
    Scrapes the company LinkedIn page to pull all information found on the page
    and returns a summary of key company information.
    Requires an API key in the X-API-Key header.
    """
    try:
        # Scrape the LinkedIn page
        company_data = await linkedin_scraper_service.scrape_company(
            linkedin_url=request.linkedin_url
        )

        company_profile = CompanyProfile(
            name=company_data["name"],
            linkedin_internal_id=company_data["linkedin_internal_id"],
            website=company_data["website"],
            industry=company_data["industry"],
            company_size=" - ".join([str(cs) for cs in company_data["company_size"]]),
            company_size_on_linkedin=company_data["company_size_on_linkedin"],
            hq_location=company_data["hq"]["city"]
            + ", "
            + company_data["hq"]["state"]
            + ", "
            + company_data["hq"]["country"],
            company_type=company_data["company_type"],
            founded_year=company_data["founded_year"],
            tagline=company_data["tagline"],
        )

        return CompanyScrapeResponse(response=company_profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
