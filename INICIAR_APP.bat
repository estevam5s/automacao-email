@echo off
chcp 65001 > nul
title Sistema de Salários — Pedacinho do Céu

echo ==========================================
echo   Sistema de Automação de Salários
echo   Pedacinho do Céu — Bar e Restaurante
echo ==========================================
echo.

REM Tenta executável compilado primeiro
if exist "ui\desktop\dist\SistemaSalariosGarcons.exe" (
    echo Iniciando aplicativo...
    start "" "ui\desktop\dist\SistemaSalariosGarcons.exe"
    exit /b 0
)

REM Fallback: roda direto com Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    where python3 >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERRO] Python nao encontrado. Instale em https://python.org
        pause
        exit /b 1
    )
    set PYTHON=python3
) else (
    set PYTHON=python
)

echo Verificando dependencias...
%PYTHON% -m pip install -r requirements.txt --quiet 2>nul

echo Iniciando interface grafica...
cd /d "%~dp0"
%PYTHON% ui\desktop\app_tkinter.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao iniciar o aplicativo.
    echo Verifique se o arquivo .env existe e as credenciais estao corretas.
    pause
)
