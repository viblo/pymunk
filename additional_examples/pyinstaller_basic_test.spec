# -*- mode: python ; coding: utf-8 -*-

# No special settings should be required to make Pymunk work with PyInstaller,
# running this spec file should produce the same output as if running
# > python -m PyInstaller -F basic_test.py
# in the examples folder.

block_cipher = None

import pymunk

a = Analysis(['basic_test.py'],
             pathex=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='basic_test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
