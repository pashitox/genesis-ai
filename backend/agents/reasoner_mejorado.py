import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ReasonerAgent:
    def __init__(self):
        logger.info("ReasonerAgent inicializado")
    
    async def reason(self, user_message: str, rag_context: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"Reasoner procesando: {user_message}")
        
        # USAR EL CONTEXTO RAG SI ESTÁ DISPONIBLE
        if rag_context and rag_context.get('results'):
            logger.info(f"RAG proporcionó {len(rag_context['results'])} resultados")
            
            # Tomar el mejor resultado del RAG
            best_match = rag_context['results'][0]
            category = best_match.get('category', 'general')
            content = best_match.get('content', '')
            similarity = best_match.get('similarity', 0)
            
            # Construir respuesta basada en el RAG
            if 'docker' in category.lower():
                response = f"Para crear un contenedor Docker: {content}"
            elif 'python' in category.lower():
                response = f"En Python: {content}"  
            elif 'linux' in category.lower():
                response = f"Comandos Linux: {content}"
            else:
                response = f"Basado en la documentación: {content}"
                
            logger.info(f"Reasoner generó respuesta con contexto RAG (sim: {similarity:.2f})")
            return {"text": response, "rag_context": rag_context}
        
        # Fallback si no hay contexto RAG
        logger.warning("Reasoner usando fallback (sin contexto RAG)")
        return {"text": f"Respuesta para: {user_message}", "rag_context": rag_context or {"results": []}}

# Instancia global
reasoner_agent = ReasonerAgent()
