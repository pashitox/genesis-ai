#!/bin/bash
# scripts/build.sh

echo "🚀 Building GENESIS AI containers..."

# Build Backend
echo "📦 Building backend image..."
docker build -t genesis-ai/backend:latest ./backend

# Build Frontend  
echo "📦 Building frontend image..."
docker build -t genesis-ai/frontend:latest ./frontend

echo "✅ Build completed!"