"""Simple example of py2exe to create a exe of the basic_test example.

Tested on py2exe 0.9.2.2 on python 3.4
"""

import os
from distutils.core import setup

import py2exe

import pymunk

setup(console=["basic_test.py"], data_files=[("", [pymunk.chipmunk_path])])
