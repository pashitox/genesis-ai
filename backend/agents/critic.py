# backend/agents/critic.py
from typing import Dict, Any
from ..llm import call_openai_chat

async def critique(reasoner_text: str, user_message: str) -> Dict[str, Any]:
    """
    Revisa la respuesta del reasoner y devuelve análisis mejorado
    """
    # Análisis heurístico mejorado - sin depender de JSON parsing
    issues = []
    score = 0.7  # Puntuación base
    
    # 1. Análisis de longitud
    if len(reasoner_text) < 100:
        issues.append("respuesta muy corta")
        score -= 0.2
    elif len(reasoner_text) > 300:
        issues.append("respuesta podría ser más concisa")
        score -= 0.1
    else:
        score += 0.1
    
    # 2. Análisis de contenido técnico
    technical_terms = ["kubernetes", "fastapi", "docker", "python", "api", "deployment", "container"]
    technical_count = sum(1 for term in technical_terms if term in reasoner_text.lower())
    
    if technical_count >= 2:
        score += 0.15
    elif technical_count == 0 and any(term in user_message.lower() for term in technical_terms):
        issues.append("falta contenido técnico específico")
        score -= 0.15
    
    # 3. Análisis de estructura
    if "\n" in reasoner_text or "•" in reasoner_text or "1." in reasoner_text:
        score += 0.1  # Bonus por estructura organizada
    else:
        issues.append("podría mejorar la estructura con listas o puntos")
    
    # 4. Análisis de contexto
    user_lower = user_message.lower()
    response_lower = reasoner_text.lower()
    
    context_matches = 0
    important_words = [word for word in user_lower.split() if len(word) > 3]
    for word in important_words:
        if word in response_lower:
            context_matches += 1
    
    if context_matches < len(important_words) / 2:
        issues.append("no aborda completamente la pregunta")
        score -= 0.1
    
    # 5. Consejo específico basado en el análisis
    advice = "Buena respuesta base."
    if issues:
        if "técnico" in str(issues):
            advice = "Añade ejemplos técnicos específicos y comandos."
        elif "estructura" in str(issues):
            advice = "Organiza la respuesta con puntos o listas numeradas."
        elif "corta" in str(issues):
            advice = "Expande con más detalles y ejemplos prácticos."
        else:
            advice = "Mejora el enfoque en los puntos clave de la pregunta."
    else:
        advice = "Excelente respuesta, bien estructurada y completa."
    
    # Asegurar score entre 0.3 y 0.95
    score = max(0.3, min(0.95, round(score, 2)))
    
    return {
        "score": score,
        "issues": issues,
        "advice": advice
    }
