# -*- mode: python ; coding: utf-8 -*-

added_files = [
    ('D:\\Python310\\Lib\\site-packages\\ultralytics\\cfg', 'ultralytics/cfg'),  # 包含 ultralytics 配置文件的文件夹
    ('D:\\Python310\Lib\\site-packages\\ultralytics\\data\\base.py', 'ultralytics/data'),  # 包含 ultralytics 基础文件的文件
    ('weights\\yolov8n.pt', 'weights')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico',
)
