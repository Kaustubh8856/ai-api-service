from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Import routers (we'll create these next)
from app.routers.ai import router as ai_router

# Create FastAPI application
app = FastAPI(
    title="AI API Service",
    description="Production-ready AI-powered REST API using Hugging Face",
    version="1.0.0",
    docs_url="/docs",  # Enables Swagger UI at /docs
    redoc_url="/redoc"  # Enables ReDoc at /redoc
)

# Add CORS middleware to allow frontend applications to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - change in production!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the AI router
app.include_router(ai_router, prefix="/ai", tags=["AI"])

@app.get("/")
async def root():
    """Root endpoint that returns basic API information"""
    return {
        "message": "Welcome to AI API Service!",
        "status": "healthy",
        "version": "1.0.0",
        "provider": "Hugging Face",
        "model": os.getenv("HUGGINGFACE_MODEL", "Not configured"),
        "docs": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "ai-api-service",
        "environment": os.getenv("APP_ENV", "development")
    }

@app.get("/info")
async def api_info():
    """Returns API configuration information"""
    return {
        "api_name": "AI API Service",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "development"),
        "ai_provider": "Hugging Face",
        "model": os.getenv("HUGGINGFACE_MODEL"),
        "api_key_configured": bool(os.getenv("HUGGINGFACE_API_KEY"))
    }

# This allows running the app directly: python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0",  # Allows access from other devices on network
        port=8000,       # Default FastAPI port
        reload=True      # Auto-reload on code changes (development only)
    )