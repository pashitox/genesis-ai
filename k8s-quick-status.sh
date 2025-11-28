#!/bin/bash
# k8s-quick-status.sh

echo "📊 ESTADO RÁPIDO - GENESIS AI KUBERNETES"

echo ""
echo "🐳 PODS:"
kubectl get pods -n genesis-ai

echo ""
echo "🔧 SERVICIOS:"
kubectl get services -n genesis-ai

echo ""
echo "📦 DEPLOYMENTS:"
kubectl get deployments -n genesis-ai

echo ""
echo "🔍 LOGS BACKEND (últimas 3 líneas):"
kubectl logs -n genesis-ai -l app=genesis-backend --tail=3 --prefix=true 2>/dev/null || echo "No hay logs aún"

echo ""
echo "🔍 LOGS FRONTEND (últimas 3 líneas):"
kubectl logs -n genesis-ai -l app=genesis-frontend --tail=3 --prefix=true 2>/dev/null || echo "No hay logs aún"

echo ""
echo "🌐 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8002"