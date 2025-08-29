# -*- mode: python ; coding: utf-8 -*-

# PyInstaller spec file for rxiv-maker main binary

import sys
import os
from pathlib import Path

# Add src to path to ensure imports work
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

block_cipher = None

# Define hidden imports for all the dependencies that PyInstaller might miss
hidden_imports = [
    # Core rxiv-maker modules
    'rxiv_maker.cli',
    'rxiv_maker.core',
    'rxiv_maker.services',
    'rxiv_maker.processors',
    'rxiv_maker.converters',
    'rxiv_maker.validators',
    'rxiv_maker.utils',
    'rxiv_maker.config',
    'rxiv_maker.engines',
    'rxiv_maker.docker',
    'rxiv_maker.security',
    'rxiv_maker.cache',
    'rxiv_maker.validate',
    'rxiv_maker.scripts',
    
    # Scientific libraries
    'matplotlib',
    'matplotlib.pyplot',
    'matplotlib.backends',
    'matplotlib.backends.backend_agg',
    'seaborn',
    'numpy',
    'pandas',
    
    # Image processing
    'PIL',
    'PIL._tkinter_finder',
    
    # PDF processing
    'pypdf',
    
    # YAML processing
    'yaml',
    
    # Rich CLI libraries
    'rich',
    'rich.console',
    'rich.progress',
    'rich.table',
    'rich_click',
    
    # Click CLI framework
    'click',
    
    # HTTP requests
    'requests',
    'requests.packages.urllib3',
    
    # Environment and config
    'dotenv',
    'platformdirs',
    'packaging',
    'tomli_w',
    
    # System utilities
    'psutil',
    
    # Web automation (Playwright)
    'playwright',
    'playwright._impl',
    
    # Cross-reference utilities
    'crossref_commons',
    
    # Type extensions
    'typing_extensions',
]

# Data files that might be needed (templates, configs, etc.)
datas = [
    # Add any data files from the rxiv-maker package
    # ('src/rxiv_maker/templates', 'rxiv_maker/templates'),
    # ('src/rxiv_maker/configs', 'rxiv_maker/configs'),
]

# Binary files that need to be included
binaries = []

a = Analysis(
    ['src/rxiv_maker/cli/__main__.py'],  # Entry point for the CLI
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce binary size
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
    name='rxiv',
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