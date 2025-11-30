import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import faiss
import json

class RAGAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self._load_knowledge_base()
        self.embeddings = self._compute_embeddings()
        
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
        self.id_map = {i: doc for i, doc in enumerate(self.knowledge_base)}
    
    def _load_knowledge_base(self) -> List[Dict[str, Any]]:
        base = [
            {
                "id": "docker_basics",
                "content": "Docker permite crear contenedores. Dockerfile básico: FROM python:3.9, WORKDIR /app, COPY . ., RUN pip install, CMD python app.py. Comandos: docker build -t myapp ., docker run -p 8000:8000 myapp, docker ps, docker images, docker-compose up para múltiples contenedores.",
                "category": "docker",
                "tags": ["containers", "deployment", "devops"]
            },
            {
                "id": "kubernetes_basics", 
                "content": "Kubernetes gestiona contenedores. Conceptos: Pods (mínima unidad), Deployments (gestión estado), Services (red), ConfigMaps (configuración). Comandos: kubectl get pods, kubectl apply -f deployment.yaml, kubectl get services, minikube start para local, kubectl logs para ver logs.",
                "category": "kubernetes",
                "tags": ["orchestration", "containers", "devops"]
            },
            {
                "id": "fastapi_basics",
                "content": "FastAPI: framework Python moderno para APIs. Instalación: pip install fastapi uvicorn. App básica: from fastapi import FastAPI, app = FastAPI(), @app.get('/') def root(): return {'message': 'Hello'}. Ejecutar: uvicorn main:app --reload. Documentación automática en /docs y /redoc. Soporte para async/await.",
                "category": "fastapi", 
                "tags": ["python", "api", "backend", "web"]
            },
            {
                "id": "fastapi_advanced",
                "content": "FastAPI características avanzadas: Path parameters @app.get('/items/{item_id}'), Query parameters, Request bodies con Pydantic, Dependencias injection, Middleware, CORS, Autenticación OAuth2. Ventajas: rápido, fácil de usar, documentación automática, basado en estándares OpenAPI.",
                "category": "fastapi",
                "tags": ["python", "api", "advanced", "rest"]
            },
            {
                "id": "python_fundamentals",
                "content": "Python: lenguaje interpretado de alto nivel. Fundamentos: variables, funciones def, clases class, estructuras de datos list, dict, tuple, set. Características: tipado dinámico, indentación obligatoria, comprehensions [x for x in range(10)], decoradores @, manejo de excepciones try/except.",
                "category": "python",
                "tags": ["programming", "fundamentals", "syntax"]
            },
            {
                "id": "python_advanced",
                "content": "Python avanzado: programación orientada a objetos (herencia, polimorfismo), módulos y paquetes, manejo de archivos, expresiones regulares, threading, asyncio para programación asíncrona, generators, context managers with, metaprogramación. Librerías populares: requests, pandas, numpy, django, flask.",
                "category": "python",
                "tags": ["programming", "advanced", "libraries"]
            },
            {
                "id": "api_design",
                "content": "APIs REST: representational state transfer. Principios: endpoints resource-oriented, HTTP methods GET/POST/PUT/DELETE, status codes 200/201/400/404/500. Mejores prácticas: versionado (/api/v1/), documentación Swagger/OpenAPI, autenticación JWT, rate limiting, paginación, filtros, ordenamiento.",
                "category": "api",
                "tags": ["backend", "design", "rest", "best-practices"]
            },
            {
                "id": "container_concepts",
                "content": "Contenedores: empaquetado de aplicaciones con dependencias. Ventajas: portabilidad, consistencia entre entornos, aislamiento, eficiencia de recursos. Docker vs Kubernetes: Docker crea contenedores, Kubernetes los orquesta. Alternativas: Podman, Containerd. Imágenes vs contenedores: la imagen es el template, el contenedor es la instancia.",
                "category": "containers",
                "tags": ["docker", "kubernetes", "devops", "concepts"]
            }
        ]
        return base
    
    def _compute_embeddings(self):
        texts = [item["content"] for item in self.knowledge_base]
        return self.model.encode(texts, convert_to_numpy=True)
    
    def search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        try:
            query_embedding = self.model.encode([query], convert_to_numpy=True)
            distances, indices = self.index.search(query_embedding, top_k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                sim_score = 1 / (1 + distances[0][i])
                
                # Umbral más bajo para encontrar más resultados
                if sim_score > 0.25:  # Reducido de 0.3 para más cobertura
                    doc = self.id_map[idx]
                    results.append({
                        "content": doc["content"],
                        "category": doc["category"],
                        "similarity": float(sim_score),
                        "tags": doc["tags"]
                    })
            
            max_similarity = max([r["similarity"] for r in results]) if results else 0
            
            # Mejorar detección de relevancia
            is_relevant = max_similarity > 0.45  # Umbral más bajo
            
            return {
                "query": query,
                "results": results,
                "max_similarity": max_similarity,
                "results_count": len(results),
                "is_relevant": is_relevant,
                "relevance_level": self._get_relevance_level(max_similarity)
            }
        
        except Exception as e:
            return {
                "query": query,
                "results": [],
                "max_similarity": 0,
                "results_count": 0,
                "is_relevant": False,
                "relevance_level": "none",
                "error": str(e)
            }
    
    def _get_relevance_level(self, similarity: float) -> str:
        """Determina el nivel de relevancia basado en similitud"""
        if similarity > 0.6:
            return "high"
        elif similarity > 0.4:
            return "medium" 
        elif similarity > 0.25:
            return "low"
        else:
            return "none"

# Instancia global
rag_agent = RAGAgent()