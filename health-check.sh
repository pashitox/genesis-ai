#!/bin/bash
# scripts/health-check.sh

echo "🏥 Running health checks..."

# Check pods
echo "📊 Pod status:"
kubectl get pods -n genesis-ai

# Check services
echo "🔌 Service status:"
kubectl get services -n genesis-ai

# Check ingress
echo "🌐 Ingress status:"
kubectl get ingress -n genesis-ai

# Check HPA
echo "📈 HPA status:"
kubectl get hpa -n genesis-ai

# Test backend health
echo "❤️  Backend health:"
kubectl run -i --rm --restart=Never test-curl --image=curlimages/curl \
  -n genesis-ai --command -- curl -s http://genesis-backend:8002/health

echo "✅ Health checks completed!"