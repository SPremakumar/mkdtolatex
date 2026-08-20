# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["launcher.py"],
    pathex=[
        "backend",
    ],
    binaries=[],
    datas=[
        ("frontend/dist", "frontend/dist"),
    ],
    hiddenimports=[
        "Mkd_Interpreter",
        "Mkd_Parser",
        "Mkd_Lexer",
        "Token",
        "AST",
        "Enum_Rule",
        "convertir_link_image",
    ],
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
    a.binaries,
    a.datas,
    [],
    name="mkdtolatexEditor",
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
)