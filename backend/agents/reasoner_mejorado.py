from typing import Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agents.reasoner")

class ReasonerAgent:
    def __init__(self, rag_agent):
        self.rag_agent = rag_agent
        logger.info("ReasonerAgent inicializado con RAG mejorado")
    
    async def reason(self, user_message: str) -> Dict[str, Any]:
        # Primero obtener contexto RAG
        rag_results = self.rag_agent.search(user_message)
        logger.info(f"RAG encontró {rag_results['results_count']} resultados, similitud: {rag_results.get('max_similarity', 0):.2f}, relevante: {rag_results.get('is_relevant', False)}")
        
        # Determinar si debemos responder o no
        should_respond = self._should_respond_to_query(rag_results, user_message)
        logger.info(f"Should respond: {should_respond}")
        
        if not should_respond:
            # Respuesta para consultas fuera de contexto
            final_response = self._get_out_of_scope_response(user_message)
        else:
            # Lógica normal de respuesta
            final_response = self._generate_response(user_message, rag_results)
        
        return {
            "final_response": final_response,
            "rag_context": rag_results,
            "should_respond": should_respond
        }
    
    def _should_respond_to_query(self, rag_results: Dict, user_message: str) -> bool:
        """Determina si debemos intentar responder o no"""
        user_lower = user_message.lower().strip()
        
        # 1. Preguntas sobre capacidades - SIEMPRE responder
        capability_queries = [
            "hola", "hi", "hello", 
            "ayuda", "help", 
            "quién eres", "who are you",
            "qué puedes hacer", "what can you do",
            "qué sabes", "what do you know"
        ]
        if user_lower in capability_queries:
            return True
        
        # 2. Si RAG no tiene resultados, no responder
        if rag_results["results_count"] == 0:
            return False
        
        # 3. Consultas claramente fuera de contexto - NO responder
        non_tech_keywords = [
            "pizza", "marvel", "roma", "automóvil", "fútbol", "japón", 
            "soñar", "guitarra", "pan", "espacio", "película", "cocinar",
            "receta", "viajar", "equipo", "reparar", "historia", "deporte",
            "música", "cine", "comida", "restaurante", "hotel", "viaje",
            "netflix", "spotify", "facebook", "instagram", "twitter"
        ]
        if any(keyword in user_lower for keyword in non_tech_keywords):
            return False
        
        # 4. Para preguntas técnicas, usar umbral de relevancia del RAG
        if rag_results.get("is_relevant", False):
            return True
        
        # 5. Si tiene baja similitud pero es pregunta técnica, intentar responder
        tech_keywords = ["docker", "kubernetes", "fastapi", "python", "api", "container", "program"]
        if any(keyword in user_lower for keyword in tech_keywords):
            return rag_results.get("max_similarity", 0) > 0.3
        
        return False
    
    def _generate_response(self, user_message: str, rag_results: Dict) -> str:
        """Genera respuesta basada en el contexto RAG"""
        user_lower = user_message.lower().strip()
        
        # Respuestas para preguntas sobre capacidades
        if user_lower in ["hola", "hi", "hello"]:
            return "¡Hola! 👋 Soy un asistente especializado en desarrollo de software. Puedo ayudarte con Docker, Kubernetes, FastAPI, Python y temas relacionados. ¿En qué puedo asistirte?"
        
        elif user_lower in ["ayuda", "help"]:
            return "🤖 **Mi especialidad**: Desarrollo de software\n\n**Temas que domino**:\n• Docker y contenedores\n• Kubernetes y orquestación\n• FastAPI y desarrollo de APIs\n• Python y programación\n• Diseño de APIs REST\n\nPregúntame sobre estos temas y te ayudo con información específica."
        
        elif user_lower in ["quién eres", "who are you"]:
            return "Soy Genesis AI, un asistente especializado en tecnologías de desarrollo y DevOps. Mi conocimiento incluye Docker, Kubernetes, FastAPI, Python y mejores prácticas de desarrollo."
        
        elif user_lower in ["qué puedes hacer", "what can you do", "qué sabes"]:
            return "🎯 **Mis capacidades**:\n\n• Explicar conceptos de Docker y contenedores\n• Ayudar con Kubernetes y orquestación\n• Asistir con desarrollo en FastAPI\n• Explicar fundamentos de Python\n• Diseño de APIs REST\n• Mejores prácticas de DevOps\n\n¿Sobre qué tema te gustaría consultar?"
        
        # Para preguntas técnicas con contexto RAG
        if rag_results["results_count"] > 0:
            best_result = rag_results["results"][0]
            
            # Personalizar respuesta basada en la categoría
            if best_result['similarity'] > 0.6:
                # Alta similitud - respuesta completa
                content_preview = best_result['content']
                return f"🎯 **{best_result['category'].title()}**: {content_preview}"
            else:
                # Media/baja similitud - respuesta más cuidadosa
                content_preview = best_result['content'][:150] + "..." if len(best_result['content']) > 150 else best_result['content']
                return f"💡 Basado en mi conocimiento de {best_result['category']}: {content_preview}\n\n*Nota: Esta información puede no ser exactamente lo que buscas.*"
        else:
            return f"🤔 No tengo información específica sobre '{user_message}' en mi base de conocimiento actual. ¿Podrías reformular la pregunta o consultar sobre Docker, Kubernetes, FastAPI o Python?"
    
    def _get_out_of_scope_response(self, user_message: str) -> str:
        """Respuesta para consultas fuera del ámbito"""
        return f"""🔍 **Fuera de mi ámbito especializado**

Me concentro en **tecnologías de desarrollo**: Docker, Kubernetes, FastAPI, Python y DevOps.

Tu pregunta sobre *"{user_message}"* está fuera de estos temas. 

¿Te puedo ayudar con algo relacionado con desarrollo de software?"""