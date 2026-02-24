#!/bin/bash

# ==============================================
# Script para resetar commits de um repositório
# Uso: ./reset_commits.sh [primeiro-commit]
# ==============================================

if [ -z "$1" ]; then
    echo "Uso: $0 <primeiro-commit-hash>"
    echo "Exemplo: $0 911c43e"
    exit 1
fi

COMMIT="$1"
REPO=$(basename "$(pwd)")

echo "⚠️  ATENÇÃO: Este processo é IRREVERSÍVEL!"
echo "Repositório: $REPO"
echo "Primeiro commit: $COMMIT"
echo ""
read -p "Continuar? (s/n): " CONFIRM

if [ "$CONFIRM" != "s" ]; then
    echo "Operação cancelada."
    exit 0
fi

# Backup automático
echo "📦 Criando backup..."
cp -r . "../${REPO}-backup-$(date +%Y%m%d_%H%M%S)"

# Reset e novo commit
echo "🔄 Resetando commits..."
git reset --soft "$COMMIT"

echo "📝 Fazendo novo commit..."
git add -A
git commit -m "Initial commit - $(date +%Y-%m-%d)"

echo ""
echo "✅ Pronto! Execute para enviar ao GitHub:"
echo "   git push origin main --force"
