#!/bin/bash
# scripts/stop-k8s.sh

echo "🛑 Stopping all GENESIS AI services in Kubernetes..."

NAMESPACE="genesis-ai"

echo "🔎 Checking if namespace exists..."
if ! kubectl get namespace $NAMESPACE >/dev/null 2>&1; then
  echo "❌ Namespace '$NAMESPACE' not found. Nothing to stop."
  exit 0
fi

echo "🗑 Deleting deployments..."
kubectl delete deployment --all -n $NAMESPACE

echo "🗑 Deleting services..."
kubectl delete svc --all -n $NAMESPACE

echo "🗑 Deleting ingresses..."
kubectl delete ingress --all -n $NAMESPACE

echo "🗑 Deleting HPA..."
kubectl delete hpa --all -n $NAMESPACE

echo "🗑 Deleting configmaps..."
kubectl delete configmap --all -n $NAMESPACE

echo "🗑 Deleting secrets..."
kubectl delete secret --all -n $NAMESPACE

echo "🗑 Deleting PVCs..."
kubectl delete pvc --all -n $NAMESPACE

echo "🗑 Deleting pods..."
kubectl delete pod --all -n $NAMESPACE

echo "💥 Deleting namespace completely..."
kubectl delete namespace $NAMESPACE

echo "⏳ Waiting for namespace deletion..."
while kubectl get namespace $NAMESPACE >/dev/null 2>&1; do
  sleep 1
done

echo "✅ All GENESIS AI services stopped and namespace deleted!"
