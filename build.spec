# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(SPEC))))

# Hidden imports for PyInstaller
hiddenimports = [
    'supabase',
    'supabase.lib',
    'postgrest',
    'gotrue',
    'storage3',
    'functions',
    'urllib3',
    'requests',
    'certifi',
    'idna',
    'charset_normalizer',
    'email_validator',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
]

# Collect all data files
datas = [
    ('README.md', '.'),
]

a = Analysis(
    ['ui/desktop/app_tkinter.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='SistemaSalariosGarcons',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon here
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SistemaSalariosGarcons',
)
