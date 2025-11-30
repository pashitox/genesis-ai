#!/bin/bash
echo "🚀 DEPLOY DEFINITIVO - SIN DEPENDENCIAS EXTERNAS"
rm -f requirements.txt
vercel --prod
