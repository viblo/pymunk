import os
from distutils.core import setup
import py2exe
import pymunk

pymunk_dir = os.path.dirname(pymunk.__file__)

setup(console=['basic_test.py'],
    data_files = [os.path.join(pymunk_dir, 'chipmunk.dll')]
    )
    

