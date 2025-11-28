#!/bin/bash
# scripts/deploy-local.sh

set -e

echo "🚀 Deploying GENESIS AI to Local Kubernetes..."

# Step 1: Build images using Minikube's Docker
echo "📦 Building Docker images..."
eval $(minikube docker-env)
docker build -t genesis-ai/backend:latest ./backend
docker build -t genesis-ai/frontend:latest ./frontend

# Step 2: Apply Kubernetes manifests
echo "📁 Creating namespace..."
kubectl apply -f k8s/namespace.yaml

echo "💾 Setting up storage..."
kubectl apply -f k8s/storage/

echo "⚙️  Applying configuration..."
kubectl apply -f k8s/config/configmap.yaml
# Saltar secrets por ahora o usar stringData
# kubectl apply -f k8s/config/secrets.yaml

echo "🔧 Deploying backend..."
kubectl apply -f k8s/backend/

echo "🎨 Deploying frontend..."
kubectl apply -f k8s/frontend/

# Step 3: Wait for deployment
echo "⏳ Waiting for deployment to complete..."
kubectl rollout status deployment/genesis-backend -n genesis-ai --timeout=180s
kubectl rollout status deployment/genesis-frontend -n genesis-ai --timeout=180s

echo "✅ Deployment completed!"

# Step 4: Expose services
echo "🌐 Exposing services..."
kubectl port-forward -n genesis-ai service/genesis-frontend 3000:3000 &
kubectl port-forward -n genesis-ai service/genesis-backend 8002:8002 &

echo ""
echo "🎉 GENESIS AI is now running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8002"
echo "   API Docs: http://localhost:8002/docs"
echo ""
echo "💡 Press Ctrl+C to stop port forwarding"
wait