from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(__file__))

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Genesis AI API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    request_id: str
    final_response: str
    rag_context: dict
    critic_review: dict
    improvement: dict
    timestamp: str

# Importar después de definir las clases para evitar problemas circulares
from orchestrator import run_pipeline

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Processing message: {request.message}")
        result = await run_pipeline(request.message)
        
        return ChatResponse(
            request_id=result["request_id"],
            final_response=result["improver"]["text"],
            rag_context=result["reasoner"]["rag_context"],
            critic_review=result["critic"],
            improvement={
                "original": result["reasoner"]["text"],
                "improved": result["improver"]["text"]
            },
            timestamp=result["memory_entry"]["timestamp"]
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Genesis AI API"}

@app.get("/")
async def root():
    return {"message": "Genesis AI API is running", "version": "1.0.0"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
