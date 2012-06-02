import os
from distutils.core import setup
import py2exe
import pymunk

# Fix to make py2exe include some dlls it needs but doesnt include by default.
origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"):
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one

pymunk_dir = os.path.dirname(pymunk.__file__)

setup(
    console=['breakout.py']
    , data_files = [os.path.join(pymunk_dir, 'chipmunk.dll')]
    
    , zipfile = None
    , options = {"py2exe":{"bundle_files":1}}
    )
    

