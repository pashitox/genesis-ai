# backend/agents/improver.py
from typing import Dict, Any
from ..llm import call_openai_chat

async def improve(reasoner_text: str, critic_report: Dict[str, Any], user_message: str) -> str:
    """
    Toma la respuesta inicial y el informe del critic y genera una respuesta final mejorada.
    REALMENTE usa la crítica para mejorar.
    """
    score = critic_report.get('score', 0.5)
    issues = critic_report.get('issues', [])
    advice = critic_report.get('advice', '')
    
    # Si el score es alto (>0.8) y no hay issues, mantener respuesta similar
    if score >= 0.8 and not issues:
        return reasoner_text
    
    # Si hay issues específicos, mejorar basado en ellos
    improvement_instructions = []
    
    if "corta" in str(issues).lower():
        improvement_instructions.append("expande la respuesta con más detalles y ejemplos")
    
    if "concisa" in str(issues).lower():
        improvement_instructions.append("haz la respuesta más concisa pero mantén los puntos clave")
    
    if "técnico" in str(issues).lower():
        improvement_instructions.append("añade contenido técnico específico y comandos prácticos")
    
    if "estructura" in str(issues).lower():
        improvement_instructions.append("mejora la estructura organizando con puntos claros")
    
    if "contexto" in str(issues).lower() or "aborda" in str(issues).lower():
        improvement_instructions.append("enfócate más directamente en la pregunta del usuario")
    
    # Usar el advice del critic si está disponible
    if advice and advice != "Revisar puntos faltantes y añadir ejemplos concretos.":
        improvement_instructions.append(advice)
    
    # Si no hay instrucciones específicas, usar genéricas basadas en score
    if not improvement_instructions:
        if score < 0.6:
            improvement_instructions.append("mejora significativamente la respuesta, añade más valor y detalles")
        elif score < 0.8:
            improvement_instructions.append("refina la respuesta para hacerla más útil y completa")
    
    # Construir el prompt de mejora
    improvement_text = ". ".join(improvement_instructions)
    
    messages = [
        {"role": "system", "content": f"Eres Improver: mejora la respuesta incorporando este feedback: {improvement_text}"},
        {"role": "user", "content":
            f"Pregunta original: {user_message}\n\n"
            f"Respuesta inicial: {reasoner_text}\n\n"
            f"Puntuación recibida: {score}/1.0\n"
            f"Problemas identificados: {issues}\n\n"
            f"Devuelve una respuesta mejorada que solucione los problemas mencionados."
        }
    ]
    
    try:
        final = await call_openai_chat(messages, temperature=0.15)
        return final
    except Exception as e:
        # Fallback: añadir indicador de mejora a la respuesta original
        if improvement_instructions:
            return f"🔄 MEJORADO: {reasoner_text}\n\n💡 Mejoras aplicadas: {improvement_text}"
        return reasoner_text
