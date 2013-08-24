"""Simple example of py2exe to create a exe of the basic_test example.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import os
from distutils.core import setup
import py2exe
import pymunk

pymunk_dir = os.path.dirname(pymunk.__file__)

setup(console=['basic_test.py'],
    data_files = [os.path.join(pymunk_dir, 'chipmunk.dll')]
    )
    

