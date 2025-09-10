import os
import requests
import logging
from dotenv import load_dotenv
from typing import Dict, Any
import time

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceService:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.model = os.getenv("HUGGINGFACE_MODEL", "microsoft/DialoGPT-medium")
        
        if not self.api_key:
            logger.warning("HUGGINGFACE_API_KEY not found")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Optimized model list with purposes
        self.models = {
            "conversation": [
                "microsoft/DialoGPT-medium",
                "microsoft/DialoGPT-large"
            ],
            "text_generation": [
                "gpt2",
                "distilgpt2"
            ],
            "summarization": [
                "facebook/bart-large-cnn",
                "google/pegasus-xsum"
            ],
            "text_to_text": [
                "google/t5-v1_1-base",
                "google/flan-t5-base"
            ]
        }

    def generate_text(self, prompt: str, max_tokens: int = 50, temperature: float = 0.7) -> str:
        """Generate text with intelligent model selection"""
        try:
            # Determine the best model type based on prompt
            model_type = self._determine_model_type(prompt)
            models_to_try = self.models[model_type] + [self.model]
            
            for model in models_to_try:
                result = self._call_api(model, prompt, max_tokens, temperature)
                if not self._is_error(result):
                    if model != self.model:
                        return f"[{model_type.capitalize()} model: {model}] {result}"
                    return result
                
                time.sleep(1)  # Brief delay between tries
            
            return "Sorry, all models are currently unavailable. Please try again later."
            
        except Exception as e:
            return f"Error: {str(e)}"

    def _determine_model_type(self, prompt: str) -> str:
        """Determine the best model type based on prompt content"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["hello", "hi", "how are you", "chat", "talk"]):
            return "conversation"
        elif any(word in prompt_lower for word in ["summarize", "summary", "brief", "overview"]):
            return "summarization"
        elif any(word in prompt_lower for word in ["translate", "convert", "transform"]):
            return "text_to_text"
        else:
            return "text_generation"

    def _is_error(self, result: str) -> bool:
        """Check if the result contains an error"""
        error_indicators = ["error", "404", "503", "not found", "unavailable", "loading"]
        return any(indicator in result.lower() for indicator in error_indicators)

    def _call_api(self, model_name: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Make API call to specific model"""
        api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        try:
            # Model-specific parameters
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_tokens,
                    "temperature": max(0.1, min(temperature, 1.0)),
                }
            }
            
            # Special parameters for different model types
            if "gpt" in model_name.lower():
                payload["parameters"] = {"max_new_tokens": max_tokens}
            elif "bart" in model_name.lower() or "pegasus" in model_name.lower():
                payload["parameters"] = {"max_length": max_tokens, "min_length": 10}
            
            response = requests.post(api_url, headers=self.headers, json=payload, timeout=25)
            
            if response.status_code == 200:
                return self._parse_response(response.json(), model_name)
            else:
                return f"Error {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"

    def _parse_response(self, response_data: Any, model_name: str) -> str:
        """Parse API response based on model type"""
        try:
            if isinstance(response_data, list) and response_data:
                item = response_data[0]
                if isinstance(item, dict):
                    if 'generated_text' in item:
                        return item['generated_text'].strip()
                    elif 'summary_text' in item:
                        return item['summary_text'].strip()
                    elif 'translation_text' in item:
                        return item['translation_text'].strip()
                return str(item).strip()
            
            elif isinstance(response_data, dict):
                for key in ['generated_text', 'summary_text', 'translation_text']:
                    if key in response_data:
                        return response_data[key].strip()
                return str(response_data).strip()
            
            return str(response_data).strip()
            
        except Exception as e:
            return f"Parse error: {str(e)}"

# Create service instance
huggingface_service = HuggingFaceService()

def generate_text_hf(prompt: str, max_tokens: int = 50, temperature: float = 0.7) -> str:
    return huggingface_service.generate_text(prompt, max_tokens, temperature)