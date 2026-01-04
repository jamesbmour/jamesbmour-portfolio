"""
FastAPI server for the RAG-powered chatbot backend.
Provides endpoints for chat interactions and health checks.
"""
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from config import config
from rag_chain import rag_chain

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio RAG Chatbot API",
    description="RAG-powered recruitment assistant for James Brendamour's portfolio",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's question or message")
    session_id: str = Field(default=None, description="Optional session ID for conversation tracking")


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="Chatbot's response")
    sources: list = Field(default_factory=list, description="Source documents used for the response")
    success: bool = Field(default=True, description="Whether the request was successful")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Health status: healthy or unhealthy")
    message: str = Field(..., description="Human-readable status message")
    vector_store: str = Field(..., description="Vector store connection status")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize RAG chain on startup"""
    logger.info("Starting Portfolio RAG Chatbot API...")
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated successfully")

        # Perform health check
        health = rag_chain.health_check()
        if health["status"] == "healthy":
            logger.info(f"RAG chain initialized successfully. Collection: {health.get('collection')}, Vectors: {health.get('vector_count')}")
        else:
            logger.warning(f"RAG chain health check failed: {health.get('message')}")

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise


# Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Portfolio RAG Chatbot API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Verifies Qdrant connection and collection status.
    """
    try:
        health = rag_chain.health_check()
        return HealthResponse(**health)

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for RAG-powered responses.

    Args:
        request: ChatRequest containing user's message

    Returns:
        ChatResponse with bot's answer and source documents
    """
    try:
        logger.info(f"Received chat request: {request.message[:100]}...")

        # Validate message
        if not request.message or request.message.strip() == "":
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Query RAG chain
        result = await rag_chain.query(request.message)

        # Check if query was successful
        if not result.get("success", False):
            logger.error(f"RAG query failed: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate response: {result.get('error', 'Unknown error')}"
            )

        logger.info(f"Generated response with {len(result.get('sources', []))} sources")

        return ChatResponse(
            response=result["response"],
            sources=result.get("sources", []),
            success=True
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "success": False,
        "error": "An unexpected error occurred. Please try again later.",
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
