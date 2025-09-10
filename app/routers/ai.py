from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

# Import our Hugging Face service
from app.services.huggingface_service import generate_text_hf

# Create the router
router = APIRouter()

# Request model for text generation
class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 50
    temperature: Optional[float] = 0.7

# Response model
class TextGenerationResponse(BaseModel):
    generated_text: str
    model: str
    success: bool
    error: Optional[str] = None

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest):
    """
    Generate text based on the given prompt using Hugging Face API
    """
    try:
        # Call our Hugging Face service
        generated_text = generate_text_hf(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Check if the response contains an error message
        if generated_text.startswith("Error:"):
            return TextGenerationResponse(
                generated_text="",
                model=os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-small"),
                success=False,
                error=generated_text
            )
        
        return TextGenerationResponse(
            generated_text=generated_text,
            model=os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-small"),
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating text: {str(e)}"
        )

@router.get("/models")
async def get_available_models():
    """
    Return information about the currently configured model
    """
    return {
        "available_models": ["google/flan-t5-small", "google/flan-t5-base", "distilgpt2"],
        "current_model": os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-small"),
        "provider": "Hugging Face Inference API",
        "api_key_configured": bool(os.getenv("HUGGINGFACE_API_KEY")),
        "status": "active"
    }
@router.get("/debug")
async def debug_info():
    """Debug information about the current configuration"""
    from app.services.huggingface_service import huggingface_service
    
    return {
        "model": os.getenv("HUGGINGFACE_MODEL"),
        "api_key_configured": bool(os.getenv("HUGGINGFACE_API_KEY")),
        "api_url": huggingface_service.api_url,
        "model_config": huggingface_service.model_configs.get(
            os.getenv("HUGGINGFACE_MODEL", "distilgpt2"), 
            "default"
        ),
        "status": "active"
    }