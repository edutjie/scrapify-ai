from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.models.chat_models import ChatRequest, ChatResponse
from app.services.llm_service import LLMService

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
            query=request.query, api_key=api_key, model=request.model
        )
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
