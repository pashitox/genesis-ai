# backend/free_llm.py
import os
import httpx
import json
from typing import List, Dict, Any

# Tu token de Hugging Face
HF_TOKEN = "HUGGINGFACE_TOKEN_PLACEHOLDER"

async def call_free_llm(messages: List[Dict[str, str]], provider: str = "huggingface") -> str:
    """
    LLM gratuito alternativo - No modifica tu código existente
    """
    if provider == "huggingface":
        return await call_huggingface_chat(messages)
    else:
        return await call_huggingface_chat(messages)

async def call_huggingface_chat(messages: List[Dict[str, str]]) -> str:
    """
    Hugging Face Inference API - Modelo activo y gratuito
    """
    # MODELO ACTUALIZADO: Google Flan-T5 (siempre disponible)
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Extraer el último mensaje del usuario
    user_message = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_message = msg["content"]
            break
    
    if not user_message:
        return get_contextual_response("")
    
    # Preparar prompt para el modelo
    prompt = f"Responde como experto en desarrollo: {user_message}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 300,
            "temperature": 0.7,
            "do_sample": True
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Procesar respuesta de Flan-T5
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    if generated_text and len(generated_text) > 10:
                        return f"🤖 [HF] {generated_text}"
                
                # Si no hay buena respuesta, usar contextual
                return get_contextual_response(user_message)
                    
            else:
                # Si hay error de API, usar respuestas contextuales inteligentes
                return get_contextual_response(user_message)

    except Exception as e:
        # En caso de cualquier error, usar respuestas predefinidas
        return get_contextual_response(user_message)

def get_contextual_response(user_message: str) -> str:
    """Respuestas inteligentes y específicas cuando la API falla"""
    user_lower = user_message.lower()
    
    # Respuestas detalladas y específicas por contexto
    responses = {
        "kubernetes": "🚀 **Para aprender Kubernetes desde cero:**\n\n1. **Conceptos básicos:** Comprende Pods, Deployments, Services\n2. **Instalación:** Usa minikube para entorno local\n3. **Práctica:** Ejecuta `kubectl get pods`, `kubectl apply -f deployment.yaml`\n4. **Recursos:** Kubernetes.io documentation y Katacoda labs\n\nRecomiendo empezar con minikube y practicar con ejemplos simples.",
        
        "fastapi": "⚡ **FastAPI para principiantes:**\n\n1. **Instalación:** `pip install fastapi uvicorn`\n2. **Primer API:** Crea app con `@app.get('/')`\n3. **Características:** Tipado con Pydantic, documentación automática\n4. **Ejecución:** `uvicorn main:app --reload`\n\nFastAPI es rápido y tiene documentación interactiva en /docs.",
        
        "python": "🐍 **Python desarrollo:**\n\n• **Fundamentos:** Variables, funciones, clases\n• **Estructuras:** Listas, diccionarios, comprehensions\n• **Avanzado:** Decoradores, context managers, async/await\n• **Librerías:** Requests, Pandas, FastAPI, Django\n\nPractica con proyectos pequeños primero.",
        
        "docker": "🐳 **Docker desde cero:**\n\n1. **Instalar Docker** en tu sistema\n2. **Dockerfile:** Define tu aplicación\n3. **Comandos:** `docker build -t myapp .`, `docker run -p 8000:8000 myapp`\n4. **Docker Compose** para múltiples servicios\n\nComienza con contenedores simples y luego redes.",
        
        "hola": "👋 **¡Hola! Soy tu asistente de desarrollo.**\n\nPuedo ayudarte con:\n• 🐍 Python programming\n• ⚡ FastAPI y desarrollo web\n• 🚀 Kubernetes y DevOps\n• 🐳 Docker y contenedores\n• 🗄️ Bases de datos y APIs\n\n¿En qué tema te puedo asistir hoy?",
        
        "qué puedes hacer": "🛠️ **Mis áreas de especialización:**\n\n• **Backend Development:** FastAPI, Django, Flask\n• **DevOps:** Kubernetes, Docker, CI/CD\n• **Python:** Programación, librerías, best practices\n• **APIs:** Diseño, documentación, seguridad\n• **Bases de datos:** SQL, ORMs, optimización\n\n¿Qué te interesa aprender o mejorar?",
        
        "gracias": "😊 **¡De nada! Estoy aquí para ayudarte.**\n\nSi tienes más preguntas sobre desarrollo, DevOps, o cualquier tema técnico, no dudes en preguntar. ¿Hay algo específico en lo que te pueda ayudar ahora?"
    }
    
    # Buscar por palabras clave
    for keyword, response in responses.items():
        if keyword in user_lower:
            return response
    
    # Detectar contexto técnico
    tech_keywords = {
        "program": "💻 **Desarrollo de software:** Practica con proyectos reales, estudia patrones de diseño, y contribuye a código abierto.",
        "code": "📝 **Escribir buen código:** Enfócate en código limpio, testing, y documentación. Practica daily.",
        "develop": "👨‍💻 **Desarrollo profesional:** Aprende Git, metodologías ágiles, y trabaja en equipo.",
        "api": "🌐 **APIs:** Diseña RESTful APIs, documenta con OpenAPI, implementa autenticación y versionado.",
        "backend": "⚙️ **Backend development:** Domina bases de datos, caching, seguridad, y escalabilidad.",
        "database": "🗄️ **Bases de datos:** Aprende SQL, normalización, índices, y ORMs.",
        "server": "🖥️ **Servidores:** Estudia Linux, Nginx, administración, y monitoreo."
    }
    
    for keyword, response in tech_keywords.items():
        if keyword in user_lower:
            return response
    
    # Respuesta por defecto contextual
    if "?" in user_message or "cómo" in user_lower or "qué" in user_lower:
        return f"🤔 **Sobre tu pregunta:** '{user_message}'\n\nTe recomiendo:\n1. Documentación oficial del tema\n2. Tutoriales prácticos paso a paso\n3. Proyectos hands-on para aprender haciendo\n4. Comunidades como Stack Overflow para dudas específicas\n\n¿Quieres que profundice en algún aspecto en particular?"
    
    return f"💡 **Sobre:** '{user_message}'\n\nEn desarrollo, la práctica constante y proyectos reales son clave para el aprendizaje. ¿Te interesa algún tema específico como Python, Kubernetes, FastAPI o Docker?"
