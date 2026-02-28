@echo off
chcp 65001 > nul

echo ==========================================
echo   Build Sistema Salarios - Windows
echo ==========================================
echo.

REM Verifica se está na pasta correta
if not exist "app_tkinter.py" (
    echo [ERRO] Execute este script dentro da pasta ui\desktop
    pause
    exit /b 1
)

if not exist "app_windows.spec" (
    echo [ERRO] Arquivo app_windows.spec nao encontrado!
    pause
    exit /b 1
)

REM Localiza o pyinstaller (venv local tem prioridade)
set PYINSTALLER=
if exist "..\..\venv\Scripts\pyinstaller.exe" (
    set PYINSTALLER=..\..\venv\Scripts\pyinstaller.exe
) else if exist "%APPDATA%\Python\Python311\Scripts\pyinstaller.exe" (
    set PYINSTALLER=%APPDATA%\Python\Python311\Scripts\pyinstaller.exe
) else (
    where pyinstaller >nul 2>&1
    if %errorlevel% == 0 (
        set PYINSTALLER=pyinstaller
    ) else (
        echo [ERRO] pyinstaller nao encontrado.
        echo        Instale com: pip install pyinstaller
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller: %PYINSTALLER%

REM Garante que appdirs esta instalado (necessario para pkg_resources)
echo [1/4] Verificando dependencias...
if exist "..\..\venv\Scripts\pip.exe" (
    ..\..\venv\Scripts\pip.exe install appdirs --quiet
) else (
    pip install appdirs --quiet
)

echo [2/4] Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist"  rmdir /s /q "dist"

echo [3/4] Compilando executavel...
echo       Isto pode levar alguns minutos...
echo.

"%PYINSTALLER%" --clean app_windows.spec

echo.
if exist "dist\SistemaSalariosGarcons.exe" (
    echo [4/4] Verificando tamanho do executavel...
    for %%A in ("dist\SistemaSalariosGarcons.exe") do echo        Tamanho: %%~zA bytes
    echo.
    echo ==========================================
    echo   [SUCESSO] Build concluido!
    echo   Executavel: dist\SistemaSalariosGarcons.exe
    echo ==========================================
) else (
    echo [ERRO] Build falhou - executavel nao gerado.
    echo        Verifique os erros acima.
    pause
    exit /b 1
)

echo.
pause
