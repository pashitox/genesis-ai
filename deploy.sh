#!/bin/bash
echo "�� DEPLOY GENESIS AI - VERSIÓN LIGERA"

# Verificar login
echo "🔐 Verificando autenticación..."
if ! vercel whoami &> /dev/null; then
    echo "⚠️  Haciendo login..."
    vercel login
fi

# Hacer deploy
echo "📦 Desplegando..."
vercel --prod --yes

echo ""
echo "✅ ¡DEPLOY COMPLETADO!"
echo "🌐 Tu aplicación estará disponible en unos minutos"
