# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    ['login.py'],
    pathex=['C:\\Users\\geral\\OneDrive\\Desktop\\ERP'],
    binaries=[
        ('C:\\Users\\geral\\OneDrive\\Desktop\\ERP\\venv\\Lib\\site-packages\\bcrypt\\_bcrypt*.pyd', 'bcrypt'),
        ('C:\\Users\\geral\\OneDrive\\Desktop\\ERP\\venv\\Lib\\site-packages\\lz4\\block\\_block.cp313-win_amd64.pyd', 'lz4.block'),
        ('C:\\Users\\geral\\OneDrive\\Desktop\\ERP\\venv\\Lib\\site-packages\\lz4\\frame\\_frame.cp313-win_amd64.pyd', 'lz4.frame'),
    ],
    datas=[('assets', 'assets')], # <--- Añade esto para incluir la carpeta de assets
    hiddenimports=[
        'bcrypt',
        'flet_embedded_dist',
        'lz4',
        'lz4.block',
        'lz4.frame',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QUASSARERP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None ,
    icon=['assets\\iconos\\QZERP_ico.ico'] # <--- La ruta relativa ahora funciona
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QUASSARERP'
)