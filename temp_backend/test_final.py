#!/usr/bin/env python3
import requests
import time
import json

def test_sistema_optimizado():
    """Test del sistema con las optimizaciones"""
    
    print("🧪 SISTEMA OPTIMIZADO - TEST MEJORADO")
    print("=" * 60)
    
    categorias = {
        "❌ FUERA DE CONTEXTO": [
            "Cómo cocinar una pizza",
            "Qué películas de Marvel recomiendas", 
            "Dime sobre la historia de Roma antigua"
        ],
        "⚠️  PALABRAS CLAVE": [
            "Python de serpientes",
            "Docker en un barco"
        ],
        "✅ TÉCNICAS VÁLIDAS": [
            "Cómo crear un contenedor Docker",
            "Qué es Kubernetes", 
            "Cómo hacer una API con FastAPI",
            "Fundamentos de Python"
        ],
        "🤖 GENERALES": [
            "hola",
            "ayuda",
            "qué puedes hacer"
        ]
    }
    
    for categoria, preguntas in categorias.items():
        print(f"\n{categoria}")
        print("-" * 40)
        
        for pregunta in preguntas:
            print(f"\n🔍 '{pregunta}'")
            
            try:
                response = requests.post(
                    "http://localhost:8002/chat",
                    json={"message": pregunta},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    respuesta = data['final_response']
                    rag = data['rag_context']
                    critico = data['critic_review']
                    
                    print(f"   🤖 {respuesta[:70]}...")
                    print(f"   🔍 {rag['results_count']} resultados | Sim: {rag.get('max_similarity', 0):.3f} | Rel: {rag.get('is_relevant', False)}")
                    print(f"   ⭐ Calidad: {critico['score']:.2f} | Issues: {critico.get('issues', [])}")
                    
                    # Análisis rápido
                    if "fuera de mi ámbito" in respuesta.lower():
                        print("   💡 ✅ RECONOCIÓ LÍMITES")
                    elif critico['score'] > 0.7:
                        print("   💡 ✅ ALTA CALIDAD")
                    elif rag.get('is_relevant', False):
                        print("   💡 ✅ INFO RELEVANTE")
                    else:
                        print("   💡 🔍 ANALIZANDO...")
                        
                else:
                    print(f"   ❌ Error HTTP: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            time.sleep(0.3)
    
    print("\n" + "=" * 60)
    print("🎯 TEST COMPLETADO - Sistema optimizado")

if __name__ == "__main__":
    test_sistema_optimizado()