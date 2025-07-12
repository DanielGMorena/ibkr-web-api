# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

# Absolute path to config file for clarity
config_file = Path("..") / "app" / "config.yml"

a = Analysis(
    ['..\\app\\run_server.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files("tzdata") + [(str(config_file), 'app')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries + a.zipfiles + a.datas,
    exclude_binaries=False,  # ensure everything goes into one file
    name='ibkr-web-api',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
