# backend/llm.py
import os
import asyncio
import httpx
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

async def call_openai_chat(messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
    """
    Llamada simple a la API de OpenAI. Si no hay OPENAI_API_KEY, usa Hugging Face gratuito.
    """
    # Si no hay API key de OpenAI, usar Hugging Face inmediatamente
    if not OPENAI_KEY:
        from .free_llm import call_free_llm
        return await call_free_llm(messages, provider="huggingface")
    
    # Si hay API key, intentar con OpenAI primero
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 800
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            choices = data.get("choices", [])
            if not choices:
                # Si OpenAI falla, usar Hugging Face
                from .free_llm import call_free_llm
                return await call_free_llm(messages, provider="huggingface")
            content = choices[0].get("message", {}).get("content", "")
            return content
    except Exception as e:
        # Si hay error, usar Hugging Face
        from .free_llm import call_free_llm
        return await call_free_llm(messages, provider="huggingface")
