# PyInstaller build configuration for the File Utility Suite desktop app.

from PyInstaller.utils.hooks import collect_data_files


hiddenimports = ["pymupdf"]
datas = collect_data_files("PIL") + collect_data_files("yaml")


a = Analysis(
    ["file_utility_suite.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name="file-utility-suite",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
