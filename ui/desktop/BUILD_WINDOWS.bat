@echo off
REM =============================================================================
REM Script para gerar executável Windows
REM =============================================================================
REM Execute este script na pasta ui\desktop
REM =============================================================================

echo.
echo ==========================================
echo   Build Sistema Salarios - Windows
echo ==========================================
echo.

REM Verifica se está no diretório correto
if not exist "app_tkinter.py" (
    echo [ERRO] Execute este script na pasta ui\desktop
    pause
    exit /b 1
)

REM Instala PyInstaller se não estiver instalado
echo [1/4] Verificando dependencias...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo        Instalando PyInstaller...
    pip install pyinstaller
)

REM Limpa builds anteriores
echo [2/4] Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

REM Cria arquivo spec
echo [3/4] Criando arquivo de configuracao...

(
echo # -*- mode: python ; coding: utf-8 -*-
echo block_cipher = None
echo.
echo a = Analysis(
echo     ['app_tkinter.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[],
echo     hiddenimports=[
echo         'supabase',
echo         'tkinter',
echo         'pandas',
echo         'openpyxl',
echo         'python_docx',
echo         'jinja2',
echo         'email.mime',
echo         'smtplib',
echo     ],
echo     hookspath=[],
echo     hooksconfig^={},
echo     runtime_hooks=[],
echo     excludes=[],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo )
echo.
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
echo.
echo exe = EXE(
echo     pyz,
echo     a.scripts,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='SistemaSalariosGarcons',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo     icon=None,
echo )
) > app_windows.spec

REM Executa PyInstaller
echo [4/4] Compilando executavel...
echo        Isto pode levar alguns minutos...
echo.

pyinstaller --clean app_windows.spec

REM Verifica se o build foi bem sucedido
if exist "dist\SistemaSalariosGarcons.exe" (
    echo.
    echo [SUCESSO] Build concluido!
    echo.
    echo Executavel: dist\SistemaSalariosGarcons.exe
    echo.
    echo Para distribuir, compacte a pasta dist:
    echo   cd dist
    echo   powershell Compress-Archive -Path SistemaSalariosGarcons -DestinationPath SistemaSalariosGarcons-Windows.zip
) else (
    echo.
    echo [ERRO] Build falhou. Verifique os erros acima.
    pause
    exit /b 1
)

echo.
pause
