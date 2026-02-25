#!/bin/bash
# =============================================================================
# Script para gerar executável Windows (usando PyInstaller)
# =============================================================================
# Este script compila a aplicação Desktop para Windows.
# Execute: bash build_for_windows.sh
# =============================================================================

echo "=========================================="
echo "  Build Sistema Salários - Windows"
echo "=========================================="
echo ""

# Verifica se está no diretório correto
if [ ! -f "app_tkinter.py" ]; then
    echo "❌ Erro: Execute este script na pasta ui/desktop"
    exit 1
fi

# Instala PyInstaller se não estiver instalado
echo "📦 Verificando dependências..."
if ! command -v pyinstaller &> /dev/null; then
    echo "   Instalando PyInstaller..."
    pip install pyinstaller
fi

# Limpa builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf build dist *.spec

# Cria arquivo spec para Windows
echo "📝 Criando arquivo de configuração..."

cat > app_windows.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_tkinter.py'],
    pathex=['..'],
    binaries=[],
    datas=[
        ('../../config', 'config'),
    ],
    hiddenimports=[
        'supabase',
        'tkinter',
        'pandas',
        'openpyxl',
        'python_docx',
        'jinja2',
        'email.mime',
        'smtplib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SistemaSalariosGarcons',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
EOF

echo ""
echo "🔨 Compilando executável..."
echo "   (Isso pode levar alguns minutos)"
echo ""

# Executa PyInstaller
pyinstaller --clean app_windows.spec

# Verifica se o build foi bem sucedido
if [ -f "dist/SistemaSalariosGarcons.exe" ]; then
    echo ""
    echo "✅ Build concluído com sucesso!"
    echo "📂 Executável: dist/SistemaSalariosGarcons.exe"
    echo ""
    echo "Para distribuir, compacte a pasta dist:"
    echo "   cd dist"
    echo "   zip -r SistemaSalariosGarcons-Windows.zip SistemaSalariosGarcons"
else
    echo ""
    echo "❌ Erro no build. Verifique os erros acima."
    exit 1
fi
