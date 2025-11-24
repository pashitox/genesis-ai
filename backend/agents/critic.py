from typing import Dict, Any

class CriticAgent:
    async def critique(self, reasoner_text: str, user_message: str, rag_context: Dict = None) -> Dict[str, Any]:
        """
        Revisa la respuesta del reasoner con análisis de relevancia mejorado
        """
        issues = []
        score = 0.7  # Puntuación base más alta
        
        user_lower = user_message.lower()
        response_lower = reasoner_text.lower()
        
        # 1. Análisis de preguntas sobre capacidades
        capability_queries = ["hola", "ayuda", "quién eres", "qué puedes hacer"]
        is_capability_query = any(query in user_lower for query in capability_queries)
        
        if is_capability_query:
            # Para preguntas sobre capacidades, puntuar más alto si la respuesta es útil
            if len(reasoner_text) > 50 and "👋" in reasoner_text:
                score += 0.2
            return {
                "score": min(0.9, score),
                "issues": [],
                "advice": "Buena respuesta para pregunta sobre capacidades",
                "context_match_ratio": 1.0
            }
        
        # 2. Análisis de relevancia del RAG
        if rag_context and not rag_context.get("is_relevant", False):
            if "fuera de mi ámbito" in response_lower or "🔍" in reasoner_text:
                score += 0.3  # Premiar reconocer límites
                issues.append("reconoció límites correctamente")
            else:
                score -= 0.2
                issues.append("no reconoció falta de relevancia")
        
        # 3. Análisis de longitud y calidad
        if len(reasoner_text.strip()) < 30:
            issues.append("respuesta muy corta")
            score -= 0.3
        elif len(reasoner_text) > 50 and len(reasoner_text) < 300:
            score += 0.1  # Premiar respuestas de longitud adecuada
        
        # 4. Análisis de contenido técnico
        tech_keywords = ["docker", "kubernetes", "fastapi", "python", "api", "container"]
        technical_count = sum(1 for term in tech_keywords if term in response_lower)
        
        if technical_count >= 2:
            score += 0.15
        elif technical_count == 0 and any(term in user_lower for term in tech_keywords):
            issues.append("falta contenido técnico específico")
            score -= 0.1
        
        # 5. Estructura y formato
        if any(marker in reasoner_text for marker in ["**", "•", "🎯", "💡"]):
            score += 0.1  # Premiar buen formato
        
        # 6. Coincidencia de contexto
        important_words = [word for word in user_lower.split() if len(word) > 3]
        context_matches = sum(1 for word in important_words if word in response_lower)
        context_ratio = context_matches / len(important_words) if important_words else 0
        
        if context_ratio > 0.5:
            score += 0.2
        elif context_ratio < 0.2:
            issues.append("baja coincidencia con la pregunta")
            score -= 0.1
        
        # Ajustar score basado en similitud RAG
        if rag_context and rag_context.get("max_similarity", 0) > 0.6:
            score += 0.15
        
        # Consejo específico
        advice = "Respuesta adecuada."
        if score > 0.8:
            advice = "Excelente respuesta, relevante y bien estructurada."
        elif score < 0.5:
            advice = "Podría mejorar la relevancia y especificidad."
        
        score = max(0.1, min(0.95, round(score, 2)))
        
        return {
            "score": score,
            "issues": issues,
            "advice": advice,
            "context_match_ratio": round(context_ratio, 2)
        }

# Instancia global
critic_agent = CriticAgent()