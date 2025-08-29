# -*- mode: python ; coding: utf-8 -*-

# PyInstaller spec file for rxiv-install-deps binary

import sys
import os
from pathlib import Path

# Add src to path to ensure imports work
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

block_cipher = None

# Define hidden imports for the dependency installer
hidden_imports = [
    # Core rxiv-maker modules
    'rxiv_maker.install',
    'rxiv_maker.install.manager',
    'rxiv_maker.core',
    'rxiv_maker.utils',
    'rxiv_maker.config',
    'rxiv_maker.security',
    'rxiv_maker.cache',
    
    # Rich CLI libraries for nice output
    'rich',
    'rich.console',
    'rich.progress',
    'rich.table',
    'rich_click',
    
    # Click CLI framework
    'click',
    
    # HTTP requests for downloading
    'requests',
    'requests.packages.urllib3',
    
    # Environment and config
    'dotenv',
    'platformdirs',
    'packaging',
    'tomli_w',
    
    # System utilities
    'psutil',
    
    # YAML processing
    'yaml',
    
    # Type extensions
    'typing_extensions',
]

# Data files
datas = []

# Binary files
binaries = []

a = Analysis(
    ['rxiv_install_deps_entry.py'],  # Entry point script for install deps
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy modules not needed for dependency installation
        'matplotlib',
        'seaborn',
        'numpy',
        'pandas',
        'PIL',
        'pypdf',
        'playwright',
        'tkinter',
        'test',
        'unittest',
        'pydoc',
        'doctest',
        'argparse',
        'difflib',
        'inspect',
        'pdb',
        'pstats',
        'profile',
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
    name='rxiv-install-deps',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress the binary to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)