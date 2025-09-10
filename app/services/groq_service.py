import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    logger.warning("groq-sdk not installed. Falling back to Hugging Face.")
    GROQ_AVAILABLE = False
except AttributeError:
    logger.warning("Groq import error. Falling back to Hugging Face.")
    GROQ_AVAILABLE = False

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        if not GROQ_AVAILABLE:
            raise ImportError("groq-sdk is not properly installed")
        
        try:
            self.client = Groq(api_key=self.api_key)
            logger.info("Groq client initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize Groq client: {str(e)}")
        
        # Available Groq models
        self.available_models = [
            "llama3-8b-8192",
            "llama3-70b-8192", 
            "mixtral-8x7b-32768",
            "gemma-7b-it",
            "claude-3-haiku-20240307"
        ]

    def generate_text(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """Generate text using Groq API"""
        try:
            logger.info(f"Generating text with Groq model: {self.model}")
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=False
            )
            
            generated_text = chat_completion.choices[0].message.content
            logger.info(f"Successfully generated text: {generated_text[:50]}...")
            
            return generated_text
            
        except Exception as e:
            error_msg = f"Groq API error: {str(e)}"
            logger.error(error_msg)
            
            # Provide specific error messages
            if "rate limit" in str(e).lower():
                return "Error: Rate limit exceeded. Please try again in a moment."
            elif "authentication" in str(e).lower():
                return "Error: Invalid API key. Please check your GROQ_API_KEY."
            elif "connection" in str(e).lower():
                return "Error: Connection failed. Please check your internet connection."
            else:
                return f"Error: {str(e)}"

    def get_available_models(self) -> list:
        """Get list of available Groq models"""
        return self.available_models

# Create service instance only if Groq is available
groq_service = None
if GROQ_AVAILABLE:
    try:
        groq_service = GroqService()
    except Exception as e:
        logger.warning(f"Failed to initialize Groq service: {e}")
        groq_service = None

def generate_text_groq(prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
    if groq_service is None:
        return "Error: Groq service is not available. Please check installation and API key."
    return groq_service.generate_text(prompt, max_tokens, temperature)