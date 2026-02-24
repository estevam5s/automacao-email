#!/bin/bash

# Script para construir o executável do Sistema de Salários de Garçons
# Uso: ./build_exe.sh

echo "=========================================="
echo "  BUILD EXECUTÁVEL - Sistema de Salários"
echo "=========================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "ui/desktop/app_tkinter.py" ]; then
    echo "Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt
pip install pyinstaller

echo ""
echo "🔨 Construindo executável..."
echo ""

# Construir com PyInstaller
pyinstaller build.spec --clean --noconfirm

echo ""
echo "=========================================="
echo "  BUILD CONCLUÍDO!"
echo "=========================================="
echo ""
echo "O executável está em:"
echo "  dist/SistemaSalariosGarcons/SistemaSalariosGarcons"
echo ""
echo "Para criar um .app (macOS) ou .exe (Windows):"
echo "  - macOS: O arquivo já funciona, arraste para Applications"
echo "  - Windows: Execute no Windows com Wine ou PyInstaller"
echo ""

# Listar arquivos gerados
echo "Arquivos gerados:"
ls -la dist/SistemaSalariosGarcons/ 2>/dev/null || echo "Pasta dist não encontrada"
