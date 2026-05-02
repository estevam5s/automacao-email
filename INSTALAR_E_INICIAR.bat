@echo off
chcp 65001 > nul
title Instalação — Sistema de Salários Pedacinho do Céu

echo ==========================================
echo   Instalação do Sistema de Salários
echo   Pedacinho do Céu — Bar e Restaurante
echo ==========================================
echo.

REM Verifica Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao instalado!
    echo Baixe em: https://www.python.org/downloads/
    echo Marque "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% encontrado.

echo.
echo [1/3] Instalando dependencias...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [AVISO] Algumas dependencias podem nao ter instalado corretamente.
)
echo [OK] Dependencias instaladas.

echo.
echo [2/3] Verificando conexao com Supabase...
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
url = os.getenv('SUPABASE_URL','')
key = os.getenv('SUPABASE_KEY','')
if url and key:
    print('[OK] Credenciais Supabase encontradas.')
else:
    print('[AVISO] Arquivo .env nao encontrado ou incompleto.')
" 2>nul || echo [AVISO] Verificacao do .env falhou.

echo.
echo [3/3] Iniciando aplicativo...
python ui\desktop\app_tkinter.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] O aplicativo encerrou com erro.
    pause
)
