from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

# Determine which AI provider to use
AI_PROVIDER = "none"
generate_text_ai = None

# Try to import Groq service first
try:
    from app.services.groq_service import generate_text_groq, groq_service
    if groq_service is not None and os.getenv("GROQ_API_KEY"):
        generate_text_ai = generate_text_groq
        AI_PROVIDER = "groq"
        print("✅ Using Groq API provider")
except ImportError as e:
    print(f"❌ Groq import failed: {e}")
except Exception as e:
    print(f"❌ Groq initialization failed: {e}")

# Fallback to Hugging Face if Groq fails
if AI_PROVIDER == "none":
    try:
        from app.services.huggingface_service import generate_text_hf
        generate_text_ai = generate_text_hf
        AI_PROVIDER = "huggingface"
        print("✅ Using Hugging Face API provider (fallback)")
    except ImportError as e:
        print(f"❌ Hugging Face import failed: {e}")
    except Exception as e:
        print(f"❌ Hugging Face initialization failed: {e}")

# Final fallback - mock service
if AI_PROVIDER == "none":
    print("⚠️  No AI provider available, using mock service")
    
    def generate_text_mock(prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        return f"[Mock Response] I received your prompt: '{prompt[:50]}...'. Please configure an AI provider."
    
    generate_text_ai = generate_text_mock
    AI_PROVIDER = "mock"

router = APIRouter()

class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7

class TextGenerationResponse(BaseModel):
    generated_text: str
    model: str
    provider: str
    success: bool
    error: Optional[str] = None

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest):
    """Generate text using AI API"""
    try:
        if generate_text_ai is None:
            raise HTTPException(status_code=503, detail="AI service not configured")
        
        generated_text = generate_text_ai(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Check for error messages
        if generated_text.startswith("Error:"):
            return TextGenerationResponse(
                generated_text="",
                model=os.getenv("GROQ_MODEL", os.getenv("HUGGINGFACE_MODEL", "unknown")),
                provider=AI_PROVIDER,
                success=False,
                error=generated_text
            )
        
        return TextGenerationResponse(
            generated_text=generated_text,
            model=os.getenv("GROQ_MODEL", os.getenv("HUGGINGFACE_MODEL", "unknown")),
            provider=AI_PROVIDER,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating text: {str(e)}"
        )

@router.get("/provider")
async def get_current_provider():
    """Get the current AI provider information"""
    return {
        "provider": AI_PROVIDER,
        "status": "active" if AI_PROVIDER != "none" else "inactive",
        "message": f"Using {AI_PROVIDER} API",
        "configured": bool(os.getenv("GROQ_API_KEY") or os.getenv("HUGGINGFACE_API_KEY"))
    }
class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "auto"

class SummarizationRequest(BaseModel):
    text: str
    max_length: int = 100

class CodeGenerationRequest(BaseModel):
    instruction: str
    language: str = "python"
    max_tokens: int = 150

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    """Translate text to another language"""
    prompt = f"Translate the following text from {request.source_language} to {request.target_language}: {request.text}"
    
    result = generate_text_ai(
        prompt=prompt,
        max_tokens=100,
        temperature=0.3
    )
    
    return {
        "original_text": request.text,
        "translated_text": result,
        "source_language": request.source_language,
        "target_language": request.target_language,
        "model": os.getenv("GROQ_MODEL")
    }

@router.post("/summarize")
async def summarize_text(request: SummarizationRequest):
    """Summarize longer text"""
    prompt = f"Please summarize the following text concisely: {request.text}"
    
    result = generate_text_ai(
        prompt=prompt,
        max_tokens=request.max_length,
        temperature=0.2
    )
    
    return {
        "original_length": len(request.text),
        "summary": result,
        "summary_length": len(result),
        "model": os.getenv("GROQ_MODEL")
    }

@router.post("/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on instructions"""
    prompt = f"Write {request.language} code that: {request.instruction}. Provide only the code with comments."
    
    result = generate_text_ai(
        prompt=prompt,
        max_tokens=request.max_tokens,
        temperature=0.1  # Low temperature for deterministic code
    )
    
    return {
        "instruction": request.instruction,
        "language": request.language,
        "code": result,
        "model": os.getenv("GROQ_MODEL")
    }

@router.post("/chat")
async def chat_completion(message: str, max_tokens: int = 100):
    """Have a conversation with the AI"""
    result = generate_text_ai(
        prompt=message,
        max_tokens=max_tokens,
        temperature=0.7
    )
    
    return {
        "user_message": message,
        "ai_response": result,
        "model": os.getenv("GROQ_MODEL")
    }