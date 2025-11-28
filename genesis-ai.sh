#!/bin/bash

case "$1" in
    "start")
        echo "🚀 Iniciando Genesis AI..."
        docker-compose up -d
        echo "⏳ Esperando inicialización..."
        sleep 10
        echo "✅ Genesis AI iniciado"
        echo "🌐 Aplicación: http://localhost:3000"
        echo "📚 API Docs: http://localhost:8002/docs"
        ;;
    "stop")
        echo "🛑 Deteniendo Genesis AI..."
        docker-compose down
        echo "✅ Genesis AI detenido"
        ;;
    "restart")
        echo "🔃 Reiniciando Genesis AI..."
        docker-compose restart
        echo "✅ Genesis AI reiniciado"
        ;;
    "status")
        echo "📊 Estado de Genesis AI:"
        docker-compose ps
        echo ""
        echo "🔍 Health check:"
        curl -s http://localhost:8002/health || echo "❌ Backend no disponible"
        ;;
    "logs")
        echo "📋 Logs de Genesis AI:"
        docker-compose logs -f
        ;;
    "test")
        echo "🧪 Probando Genesis AI..."
        curl -s http://localhost:8002/health && echo "✅ Backend OK" || echo "❌ Backend Error"
        ;;
    *)
        echo "🎯 Genesis AI - Comandos:"
        echo "  ./genesis-ai.sh start    # Iniciar"
        echo "  ./genesis-ai.sh stop     # Detener"
        echo "  ./genesis-ai.sh restart  # Reiniciar"
        echo "  ./genesis-ai.sh status   # Ver estado"
        echo "  ./genesis-ai.sh logs     # Ver logs"
        echo "  ./genesis-ai.sh test     # Probar"
        echo ""
        echo "📁 Archivos: docker-compose.yml, requirements.txt, main.py"
        echo "🌐 URL: http://localhost:3000"
        ;;
esac
