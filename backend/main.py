from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import sys
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar directorio agents al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

app = FastAPI(title="Genesis AI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    final_response: str
    rag_context: dict
    critic_review: dict

# Importar y inicializar agentes
try:
    from rag_agent import rag_agent
    logger.info("✅ RAG agent cargado")
except ImportError as e:
    logger.error(f"❌ Error cargando RAG: {e}")
    rag_agent = None

try:
    from reasoner_mejorado import ReasonerAgent
    logger.info("✅ ReasonerAgent importado")
    # Inicializar reasoner con RAG
    if rag_agent:
        reasoner_agent = ReasonerAgent(rag_agent)
        logger.info("✅ ReasonerAgent inicializado")
    else:
        reasoner_agent = None
        logger.error("❌ No se pudo inicializar ReasonerAgent")
except ImportError as e:
    logger.error(f"❌ Error cargando Reasoner: {e}")
    reasoner_agent = None

try:
    from critic import critic_agent
    logger.info("✅ Critic agent cargado")
except ImportError as e:
    logger.error(f"❌ Error cargando Critic: {e}")
    critic_agent = None

@app.get("/")
async def root():
    return {"message": "Genesis AI API - Funcionando", "status": "active"}

@app.get("/health")
async def health_check():
    return {
        "rag_loaded": rag_agent is not None,
        "reasoner_loaded": reasoner_agent is not None,
        "critic_loaded": critic_agent is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Procesando: {request.message}")
    
    # Verificar que todos los agentes estén cargados
    if not rag_agent:
        raise HTTPException(status_code=500, detail="RAG agent no disponible")
    if not reasoner_agent:
        raise HTTPException(status_code=500, detail="Reasoner agent no disponible")
    if not critic_agent:
        raise HTTPException(status_code=500, detail="Critic agent no disponible")
    
    try:
        # 1. RAG
        rag_context = rag_agent.search(request.message)
        logger.info(f"RAG encontró {rag_context['results_count']} resultados")
        
        # 2. Reasoner - SOLO pasar user_message, NO rag_context
        reasoner_result = await reasoner_agent.reason(request.message)
        
        # 3. Critic
        critic_review = await critic_agent.critique(
            reasoner_result["final_response"], 
            request.message,
            rag_context  # Pasar rag_context al crítico para análisis de relevancia
        )
        
        return ChatResponse(
            final_response=reasoner_result["final_response"],
            rag_context=reasoner_result["rag_context"],  # Usar el contexto del reasoner
            critic_review=critic_review
        )
        
    except Exception as e:
        logger.error(f"Error en pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=False)