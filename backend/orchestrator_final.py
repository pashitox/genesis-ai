import sys
import os
import logging
import uuid
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar componentes
try:
    from agents.rag_agent import rag_agent
    from agents.reasoner_mejorado import reasoner_agent
    logger.info("✅ Módulos principales cargados")
except Exception as e:
    logger.error(f"Error cargando módulos: {e}")
    exit(1)

# Componentes simples integrados
class SimpleCritic:
    async def critique(self, text, user_message):
        score = 0.8
        issues = []
        if len(text) < 50 or "Respuesta para:" in text:
            score = 0.3
            issues.append("Respuesta genérica o muy corta")
        return {"score": score, "issues": issues}

class SimpleImprover:
    async def improve(self, text, critic, user_message):
        return f"✅ {text}" if critic.get("score", 0) > 0.5 else f"💡 {text} [Revisado]"

class SimpleMemory:
    async def add_interaction(self, **kwargs):
        return {"timestamp": datetime.now().isoformat()}

# Inicializar
critic_agent = SimpleCritic()
improver_agent = SimpleImprover()
memory_store = SimpleMemory()

async def run_pipeline(user_message: str, context=None) -> dict:
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Iniciando pipeline para: {user_message}")
    
    try:
        # 1. RAG
        rag_context = rag_agent.search(user_message)
        logger.info(f"[{request_id}] RAG: {len(rag_context.get('results', []))} resultados")
        
        # 2. Reasoner
        reasoner_output = await reasoner_agent.reason(user_message, rag_context)
        
        # 3. Critic
        critic_review = await critic_agent.critique(reasoner_output["text"], user_message)
        
        # 4. Improver
        final_response = await improver_agent.improve(reasoner_output["text"], critic_review, user_message)
        
        return {
            "request_id": request_id,
            "final_response": final_response,
            "rag_context": rag_context,
            "critic_review": critic_review,
            "improvement": {
                "original": reasoner_output["text"],
                "improved": final_response
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"[{request_id}] Error: {e}")
        return {
            "request_id": request_id,
            "final_response": f"Error: {str(e)}",
            "rag_context": {"results": []},
            "critic_review": {"score": 0.0, "issues": ["error"]},
            "improvement": {"original": "Error", "improved": "Error"},
            "timestamp": datetime.now().isoformat()
        }
