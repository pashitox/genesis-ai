import os
import httpx
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

async def call_free_llm(messages: List[Dict[str, str]], provider: str = "huggingface") -> str:
    if provider == "huggingface":
        return await call_huggingface_llm(messages)
    else:
        return await call_huggingface_llm(messages)

async def call_huggingface_llm(messages: List[Dict[str, str]]) -> str:
    user_message = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_message = msg["content"]
            break
    
    if not user_message:
        return get_fallback_response("")
    
    # Modelo 1: DialoGPT
    try:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
        
        prompt = user_message
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 200,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    if generated_text:
                        return f"�� {generated_text}"
    except Exception:
        pass
    
    return get_fallback_response(user_message)

def get_fallback_response(user_message: str) -> str:
    user_lower = user_message.lower()
    
    tech_responses = {
        "docker": "🐳 **Docker - Contenedores:**\n• Crea entornos aislados para aplicaciones\n• Dockerfile define la configuración\n• Comandos: docker build -t myapp ., docker run -p 8000:8000 myapp\n• Usa Docker Compose para múltiples servicios",
        
        "kubernetes": "🚀 **Kubernetes - Orquestación:**\n• Gestiona contenedores a escala\n• Conceptos: Pods, Deployments, Services\n• Comandos: kubectl get pods, kubectl apply -f app.yaml\n• Minikube para desarrollo local",
        
        "diferencia entre docker y kubernetes": "🔍 **Docker vs Kubernetes:**\n\n**Docker:** Crea contenedores individuales\n• Ejemplo: docker run nginx\n\n**Kubernetes:** Orquesta múltiples contenedores\n• Ejemplo: kubectl create deployment nginx --image=nginx\n\nDocker empaqueta, Kubernetes despliega y escala.",
        
        "fastapi": "⚡ **FastAPI - APIs modernas:**\n• Framework Python rápido\n• Documentación automática en /docs\n• Instalación: pip install fastapi uvicorn\n• Ejemplo: @app.get(\"/\") def root(): return {\"message\": \"Hello World\"}",
        
        "python": "🐍 **Python - Desarrollo:**\n• Lenguaje versátil y legible\n• Ideal para backend, data science, IA\n• Librerías: FastAPI, Django, Pandas, TensorFlow\n• Practica con proyectos reales"
    }
    
    for keyword, response in tech_responses.items():
        if keyword in user_lower:
            return response
    
    if any(word in user_lower for word in ["docker", "contenedor"]):
        return tech_responses["docker"]
    elif any(word in user_lower for word in ["kubernetes", "k8s", "orquest"]):
        return tech_responses["kubernetes"]
    elif any(word in user_lower for word in ["fastapi", "api", "endpoint"]):
        return tech_responses["fastapi"]
    elif any(word in user_lower for word in ["python", "program"]):
        return tech_responses["python"]
    
    return f"💡 **Sobre:** \"{user_message}\"\n\nPuedo ayudarte con Docker, Kubernetes, FastAPI y Python. ¿En qué necesitas ayuda específicamente?"
