"""
Groq API Client & Helper Service for TCS Food Formulator Backend
Manages Groq LLM API connectivity, authentication, and completion requests
using OpenAI-compatible endpoints.
"""
import os
import json
import logging
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Ensure environmental variables are loaded from backend or project root
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))
load_dotenv()

logger = logging.getLogger("GroqClient")

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def get_groq_key() -> str:
    """Retrieves GROQ_API_KEY from environment, raising ValueError if missing."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key or key == "your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY is not configured in the environment. "
            "Please set GROQ_API_KEY in .env."
        )
    return key


def get_groq_health() -> Dict[str, Any]:
    """Diagnostic check for Groq API connectivity."""
    try:
        key = get_groq_key()
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        res = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
        if res.status_code == 200:
            models_data = res.json().get("data", [])
            model_ids = [m.get("id") for m in models_data if m.get("id")]
            return {
                "connected": True,
                "status": "ONLINE",
                "default_model": DEFAULT_MODEL,
                "available_models": model_ids[:10]
            }
        else:
            return {
                "connected": False,
                "status": "ERROR",
                "code": res.status_code,
                "message": res.text
            }
    except Exception as e:
        return {
            "connected": False,
            "status": "OFFLINE",
            "message": str(e)
        }


def generate_chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 2048,
    timeout: float = 15.0
) -> Optional[str]:
    """
    Executes a chat completion via Groq REST API.
    Returns the message content string, or None if failed.
    """
    try:
        key = get_groq_key()
    except ValueError as e:
        logger.warning(f"[GroqClient] {e}")
        return None

    target_model = model or DEFAULT_MODEL
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": target_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
        else:
            logger.warning(f"[GroqClient] API call returned {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.warning(f"[GroqClient] Request failed: {e}")
        return None
