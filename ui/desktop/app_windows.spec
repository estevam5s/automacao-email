# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Raiz do projeto (dois níveis acima de ui/desktop)
PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))

# collect_all garante que os pacotes vendorizados do pkg_resources
# (appdirs, packaging, jaraco, etc.) sejam incluídos corretamente
pkg_res_datas, pkg_res_binaries, pkg_res_hiddenimports = collect_all('pkg_resources')

# .env junto ao executável para carregar variáveis de ambiente
env_file = os.path.join(PROJECT_ROOT, '.env')
extra_datas = [(env_file, '.')] if os.path.exists(env_file) else []

a = Analysis(
    ['app_tkinter.py'],
    pathex=[PROJECT_ROOT],
    binaries=pkg_res_binaries,
    datas=pkg_res_datas + extra_datas,
    hiddenimports=pkg_res_hiddenimports + [
        # tkinter
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        # supabase e dependências
        'supabase',
        'gotrue',
        'postgrest',
        'realtime',
        'storage3',
        'httpx',
        'anyio',
        # processamento de dados
        'pandas',
        'openpyxl',
        'docx',
        'python_docx',
        'jinja2',
        # e-mail
        'email.mime',
        'email.mime.text',
        'email.mime.multipart',
        'email.mime.image',
        'smtplib',
        'ssl',
        # utilitários
        'datetime',
        'uuid',
        'dotenv',
        # pkg_resources vendor (fix para 'appdirs' não encontrado)
        'pkg_resources',
        'pkg_resources.extern',
        'pkg_resources._vendor',
        'pkg_resources._vendor.appdirs',
        'pkg_resources._vendor.packaging',
        'pkg_resources._vendor.packaging.version',
        'pkg_resources._vendor.packaging.specifiers',
        'pkg_resources._vendor.packaging.requirements',
        'pkg_resources._vendor.packaging.markers',
        'pkg_resources._vendor.pyparsing',
        'pkg_resources._vendor.jaraco',
        'pkg_resources._vendor.jaraco.text',
        'pkg_resources._vendor.jaraco.functools',
        'pkg_resources._vendor.jaraco.context',
        'pkg_resources._vendor.more_itertools',
        'pkg_resources._vendor.zipp',
        'pkg_resources._vendor.importlib_resources',
        'setuptools',
        # módulos do projeto
        'config',
        'config.settings',
        'data',
        'data.models',
        'data.models.funcionario',
        'data.repositories',
        'data.repositories.supabase_repository',
        'services',
        'services.report_generator',
        'services.email_service',
        'services.auth_service',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch',
        'tensorflow',
        'scipy',
        'matplotlib',
        'IPython',
        'transformers',
        'cv2',
        'PIL',
        'sklearn',
        'seaborn',
        'plotly',
        'streamlit',
        'altair',
        'pydeck',
        'pytest',
        'jupyter',
    ],
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
