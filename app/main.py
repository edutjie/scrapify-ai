from typing import Annotated
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field

from app.models.chat_models import ChatRequest, ChatResponse
from app.models.scrape_models import ScrapeRequest, ScrapeResponse
from app.models.websearch_models import WebSearchRequest, WebSearchResponse
from app.services.llm_service import LLMService
from app.services.agent_service import AgentService

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


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
