import sys
import os
# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(__file__))

from agents.reasoner import ReasonerAgent
from agents.critic import CriticAgent  
from agents.improver import ImproverAgent
from agents.rag_agent import rag_agent
from memory.store import MemoryStore
import logging
import uuid
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar componentes
memory_store = MemoryStore()
reasoner = ReasonerAgent()
critic = CriticAgent()
improver = ImproverAgent()

def ensure_logs_directory():
    """Asegurar que el directorio de logs existe"""
    logs_dir = "backend/logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    events_file = os.path.join(logs_dir, "events.json")
    if not os.path.exists(events_file):
        with open(events_file, 'w') as f:
            json.dump([], f)

def append_log(event: dict):
    """Agregar evento al log estructurado"""
    try:
        ensure_logs_directory()
        events_file = "backend/logs/events.json"
        
        # Leer logs existentes
        if os.path.exists(events_file):
            with open(events_file, 'r') as f:
                data = json.load(f)
        else:
            data = []
        
        # Agregar nuevo evento
        data.append(event)
        
        # Escribir de vuelta
        with open(events_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error writing to log: {e}")

async def run_pipeline(user_message: str, context: dict = None) -> dict:
    """
    Orquesta el pipeline completo: RAG → Reasoner → Critic → Improver
    """
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Starting pipeline for: {user_message}")
    
    try:
        # 1. RAG Context Search
        rag_context = rag_agent.search(user_message)
        logger.info(f"[{request_id}] RAG found {rag_context.get('results_count', 0)} results")
        
        # 2. Reasoner Agent
        initial_response = await reasoner.generate_response(
            user_message, 
            rag_context,
            "default_user"
        )
        logger.info(f"[{request_id}] Reasoner completed")
        
        # 3. Critic Agent
        critic_review = critic.evaluate_response(
            initial_response, 
            user_message,
            rag_context
        )
        logger.info(f"[{request_id}] Critic score: {critic_review.get('score', 0)}")
        
        # 4. Improver Agent
        final_response = improver.improve_response(
            initial_response,
            critic_review,
            rag_context
        )
        logger.info(f"[{request_id}] Improver completed")
        
        # 5. Store in memory
        memory_entry = {
            "request_id": request_id,
            "user_id": "default_user",
            "message": user_message,
            "rag_context": rag_context,
            "initial_response": initial_response,
            "critic_review": critic_review,
            "final_response": final_response,
            "timestamp": datetime.now().isoformat()
        }
        memory_store.add_entry(memory_entry)
        
        # 6. Log events
        append_log({
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id,
            "agent": "orchestrator",
            "message_length": len(user_message),
            "rag_similarity": rag_context.get("max_similarity", 0),
            "critic_score": critic_review.get("score", 0)
        })
        
        return {
            "request_id": request_id,
            "reasoner": {"text": initial_response, "rag_context": rag_context},
            "critic": critic_review,
            "improver": {"text": final_response},
            "memory_entry": memory_entry
        }
        
    except Exception as e:
        logger.error(f"[{request_id}] Pipeline error: {e}")
        raise e
