#!/bin/bash

# 🚀 Script para subir Dashboard no GitHub
# Execute: bash upload_to_github.sh <seu-usuario-github>

if [ -z "$1" ]; then
    echo "❌ Uso: bash upload_to_github.sh <seu-usuario-github>"
    echo ""
    echo "Exemplo: bash upload_to_github.sh dhcgof"
    exit 1
fi

GITHUB_USER="$1"
REPO_NAME="dashboard-auth"
REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo "📍 Configurando repositório para: $GITHUB_USER/$REPO_NAME"
echo ""

# Adicionar remote
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# Renomear branch para main
git branch -M main

# Push para GitHub
echo "🚀 Fazendo push para GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCESSO! Repositório criado e sincronizado:"
    echo "   URL: $REPO_URL"
    echo ""
    echo "📊 Dashboard disponível em:"
    echo "   https://$GITHUB_USER.github.io/$REPO_NAME/dashboard_login.html"
else
    echo ""
    echo "❌ Erro ao fazer push. Verifique:"
    echo "   1. Seu usuário GitHub ($GITHUB_USER)"
    echo "   2. Se o repositório já existe"
    echo "   3. Suas credenciais Git"
fi
