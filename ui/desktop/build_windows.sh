#!/bin/bash
# Build executável para Windows usando PyInstaller

echo "🏗️ Build Sistema de Salários - Windows"
echo "========================================"

cd "$(dirname "$0")"

echo ""
echo "📦 Criando executável para Windows..."

pyinstaller --clean --onedir --windowed --name SistemaSalariosGarcons \
    --add-data "config:config" \
    --add-data ".env:." \
    --hidden-import=supabase \
    --hidden-import=tkinter \
    --hidden-import=pandas \
    --hidden-import=openpyxl \
    --hidden-import=python_docx \
    --hidden-import=jinja2 \
    --hidden-import=email \
    --hidden-import=smtplib \
    app_tkinter.py

echo ""
echo "✅ Build concluído!"
echo "📂 Executável disponível em: dist/SistemaSalariosGarcons.exe"
