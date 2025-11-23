import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json

class RAGAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self._load_knowledge_base()
        self.embeddings = self._compute_embeddings()
    
    def _load_knowledge_base(self) -> List[Dict[str, Any]]:
        base = [
            {
                "id": "docker_basics",
                "content": "Docker permite crear contenedores. Dockerfile básico: FROM python:3.9, WORKDIR /app, COPY . ., RUN pip install, CMD python app.py. Comandos: docker build -t myapp ., docker run -p 8000:8000 myapp, docker ps, docker images",
                "category": "docker",
                "tags": ["containers", "deployment", "devops"]
            },
            {
                "id": "kubernetes_basics", 
                "content": "Kubernetes gestiona contenedores. Conceptos: Pods (mínima unidad), Deployments (gestión estado), Services (red). Comandos: kubectl get pods, kubectl apply -f deployment.yaml, kubectl get services, minikube start para local.",
                "category": "kubernetes",
                "tags": ["orchestration", "containers", "devops"]
            },
            {
                "id": "fastapi_basics",
                "content": "FastAPI: framework Python moderno. Instalación: pip install fastapi uvicorn. App básica: from fastapi import FastAPI, app = FastAPI(), @app.get('/'). Ejecutar: uvicorn main:app --reload. Documentación automática en /docs.",
                "category": "fastapi", 
                "tags": ["python", "api", "backend"]
            },
            {
                "id": "python_fundamentals",
                "content": "Python: lenguaje interpretado. Fundamentos: variables, funciones def, clases class, estructuras list, dict, tuple. Características: tipado dinámico, indentación, comprehensions [x for x in range(10)], decoradores @.",
                "category": "python",
                "tags": ["programming", "fundamentals", "syntax"]
            },
            {
                "id": "api_design",
                "content": "APIs REST: representational state transfer. Principios: endpoints resource-oriented, HTTP methods GET/POST/PUT/DELETE, status codes 200/201/400/404/500. Mejores prácticas: versionado, documentación, autenticación, rate limiting.",
                "category": "api",
                "tags": ["backend", "design", "rest"]
            }
        ]
        return base
    
    def _compute_embeddings(self):
        texts = [item["content"] for item in self.knowledge_base]
        return self.model.encode(texts)
    
    def search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        try:
            query_embedding = self.model.encode([query])
            similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        
            top_indices = np.argsort(similarities)[-top_k:][::-1]
        
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.3:
                    results.append({
                        "content": self.knowledge_base[idx]["content"],
                        "category": self.knowledge_base[idx]["category"],
                        "similarity": float(similarities[idx]),
                        "tags": self.knowledge_base[idx]["tags"]
                    })
        
            max_similarity = max([r["similarity"] for r in results]) if results else 0
        
            return {
                "query": query,
                "results": results,
                "max_similarity": max_similarity,
                "results_count": len(results)
            }
        
        except Exception as e:
            return {
                "query": query,
                "results": [],
                "max_similarity": 0,
                "results_count": 0,
                "error": str(e)
            }

# === Crear instancia global ===
rag_agent = RAGAgent()

# === FUNCIÓN COMPATIBLE CON REASONER ===
async def get_rag_context(query: str) -> str:
    results = rag_agent.search(query)

    if results["results_count"] == 0:
        return "No se encontró información relevante en la base de conocimiento."

    final_text = "📚 Información relevante encontrada:\n\n"

    for item in results["results"]:
        final_text += f"- {item['content']} (Similitud: {item['similarity']:.2f})\n\n"

    return final_text
