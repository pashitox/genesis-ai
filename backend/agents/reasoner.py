# backend/agents/reasoner.py
from typing import Dict
from ..llm import call_openai_chat
import uuid
from .rag_agent import get_rag_context

class ReasonerAgent:
    async def reason(self, user_message: str, context: Dict = None) -> Dict:
        """
        Genera una respuesta inicial usando RAG para contexto adicional.
        """
        request_id = str(uuid.uuid4())
        
        # 1. Obtener contexto relevante con RAG
        rag_context = await get_rag_context(user_message)
        
        # 2. Preparar mensajes con contexto RAG
        messages = [
            {"role": "system", "content": "Eres Reasoner: genera respuestas claras, precisas y basadas en el contexto proporcionado. Usa la información de RAG cuando sea relevante."},
        ]
        
        # Agregar contexto RAG si hay información relevante
        if rag_context and "No se encontró" not in rag_context:
            messages.append({"role": "system", "content": f"Contexto de documentación técnica:\n\n{rag_context}"})
        
        # Agregar contexto adicional si existe
        if context:
            messages.append({"role": "system", "content": f"Contexto adicional: {context}"})
        
        # Agregar mensaje del usuario
        messages.append({"role": "user", "content": user_message})
        
        # 3. Llamar al LLM
        text = await call_openai_chat(messages, temperature=0.2)
        
        return {"request_id": request_id, "text": text, "rag_context": rag_context}
