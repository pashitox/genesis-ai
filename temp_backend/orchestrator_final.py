import sys
import os
import logging
import uuid
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator_final")

# Agregar el directorio agents al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Importar componentes MEJORADOS - NOMBRES CORREGIDOS
try:
    from rag_agent import rag_agent  # Desde agents/rag_agent.py
    from reasoner_agent import ReasonerAgent  # Desde agents/reasoner_agent.py  
    from critic_agent import CriticAgent  # Desde agents/critic_agent.py
    logger.info("✅ Módulos principales cargados")
except ImportError as e:
    logger.error(f"Error cargando módulos: {e}")
    logger.error("Verifica que los archivos existan en el directorio agents/")
    # Fallback para desarrollo
    rag_agent = None

app = FastAPI(title="Genesis AI Orchestrator - Mejorado")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    final_response: str
    rag_context: Dict[str, Any]
    critic_review: Dict[str, Any]
    request_id: str
    timestamp: str

class SimpleMemory:
    async def add_interaction(self, **kwargs):
        return {"timestamp": datetime.now().isoformat()}

memory_store = SimpleMemory()

# Inicializar agentes MEJORADOS
try:
    reasoner_agent = ReasonerAgent(rag_agent)  # Se pasa rag_agent al constructor
    critic_agent = CriticAgent()
    logger.info("✅ Todos los agentes inicializados")
except Exception as e:
    logger.error(f"Error inicializando agentes: {e}")
    reasoner_agent = None
    critic_agent = None

@app.get("/")
async def root():
    return {"message": "Genesis AI Orchestrator - Mejorado con detección de relevancia"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents_loaded": all([rag_agent, reasoner_agent, critic_agent]),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not rag_agent or not reasoner_agent:
        raise HTTPException(status_code=500, detail="Agentes no inicializados correctamente")
    
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Procesando: {request.message}")
    
    try:
        user_message = request.message
        
        # 1. Obtener respuesta del reasoner MEJORADO
        reasoner_result = await reasoner_agent.reason(user_message)
        
        # 2. Obtener crítica MEJORADA con contexto RAG
        critic_review = await critic_agent.critique(
            reasoner_result["final_response"], 
            user_message,
            reasoner_result["rag_context"]  # Pasar contexto RAG para análisis de relevancia
        )
        
        # 3. Guardar en memoria (opcional)
        await memory_store.add_interaction(
            request_id=request_id,
            user_message=user_message,
            response=reasoner_result["final_response"],
            rag_context=reasoner_result["rag_context"],
            critic_review=critic_review
        )
        
        return ChatResponse(
            final_response=reasoner_result["final_response"],
            rag_context=reasoner_result["rag_context"],
            critic_review=critic_review,
            request_id=request_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"[{request_id}] Error en chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

async def run_pipeline(user_message: str, context=None) -> dict:
    """Función de pipeline para compatibilidad"""
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Iniciando pipeline para: {user_message}")
    
    try:
        # 1. RAG MEJORADO
        rag_context = rag_agent.search(user_message)
        logger.info(f"[{request_id}] RAG: {rag_context['results_count']} resultados, Relevante: {rag_context.get('is_relevant', 'N/A')}")
        
        # 2. Reasoner MEJORADO
        reasoner_output = await reasoner_agent.reason(user_message)
        
        # 3. Critic MEJORADO
        critic_review = await critic_agent.critique(
            reasoner_output["final_response"], 
            user_message,
            rag_context
        )
        
        return {
            "request_id": request_id,
            "final_response": reasoner_output["final_response"],
            "rag_context": rag_context,
            "critic_review": critic_review,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"[{request_id}] Error: {e}")
        return {
            "request_id": request_id,
            "final_response": f"Error: {str(e)}",
            "rag_context": {"results": [], "results_count": 0, "is_relevant": False},
            "critic_review": {"score": 0.0, "issues": ["error"]},
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)