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
    from agents.reasoner import ReasonerAgent
    from agents.critic import CriticAgent  
    from agents.improver import ImproverAgent
    from agents.rag_agent import rag_agent
    from memory.store import MemoryStore
except ImportError as e:
    logger.error(f"Import error: {e}")
    # Fallbacks simples
    class ReasonerAgent:
        async def reason(self, user_message, rag_context):
            # ¡AHORA USA EL CONTEXTO RAG!
            if rag_context and rag_context.get('results'):
                best_result = rag_context['results'][0]
                content = best_result.get('content', '')
                return {"text": f"Basado en la documentación: {content}", "rag_context": rag_context}
            return {"text": f"Respuesta para: {user_message}", "rag_context": rag_context}
    
    class CriticAgent:
        async def critique(self, text, user_message):
            return {"score": 0.8, "issues": []}
    
    class ImproverAgent:
        async def improve(self, text, critic, user_message):
            return f"{text} [Mejorado]"
    
    class MemoryStore:
        async def add_interaction(self, **kwargs):
            return {"timestamp": datetime.now().isoformat()}
    
    rag_agent = type('RAG', (), {'search': lambda self, x: {"results": []}})()

# Inicializar componentes
memory_store = MemoryStore()
reasoner = ReasonerAgent()
critic = CriticAgent()
improver = ImproverAgent()

async def run_pipeline(user_message: str, context=None) -> dict:
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Start pipeline")
    
    try:
        # 1. RAG - Buscar contexto PRIMERO
        rag_context = rag_agent.search(user_message)
        logger.info(f"[{request_id}] RAG found {len(rag_context.get('results', []))} results")
        
        # 2. Reasoner - Usar el contexto RAG
        reasoner_output = await reasoner.reason(user_message, rag_context)
        
        # 3. Critic - Evaluar
        critic_review = await critic.critique(reasoner_output["text"], user_message)
        
        # 4. Improver - Mejorar
        final_response = await improver.improve(reasoner_output["text"], critic_review, user_message)
        
        # Memory
        memory_entry = await memory_store.add_interaction(
            request_id=request_id,
            user_message=user_message,
            reasoner_resp=reasoner_output["text"],
            critic_report=critic_review,
            improver_resp=final_response,
            rag_context=rag_context
        )
        
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
        logger.error(f"[{request_id}] Pipeline error: {e}")
        # Fallback garantizado
        return {
            "request_id": request_id,
            "final_response": f"Error: {str(e)}",
            "rag_context": {"results": []},
            "critic_review": {"score": 0.0, "issues": ["error"]},
            "improvement": {
                "original": "Error",
                "improved": f"Fallback: {user_message}"
            },
            "timestamp": datetime.now().isoformat()
        }
