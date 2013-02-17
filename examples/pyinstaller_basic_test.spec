# -*- mode: python -*-



import os
"""
This little trickery is required to be able to include pymunk in case this 
script is run directly in an unpacked source distribution of pymunk when 
pymunk is not installed.
"""
import sys
sys.path.insert(0,'..')
import pymunk
pymunk_dir = os.path.dirname(pymunk.__file__)

chipmunk_libs = [
    ('chipmunk.dll', os.path.join(pymunk_dir, 'chipmunk.dll'), 'DATA'),
    ('libchipmunk.dylib', os.path.join(pymunk_dir, 'chipmunk.dll'), 'DATA'),
    ('libchipmunk.so', os.path.join(pymunk_dir, 'chipmunk.dll'), 'DATA'),
    ('libchipmunk64.so', os.path.join(pymunk_dir, 'chipmunk.dll'), 'DATA'),
]

a = Analysis(['basic_test.py'],
             pathex=[], 
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\basic_test', 'basic_test.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries + chipmunk_libs,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'basic_test'))
