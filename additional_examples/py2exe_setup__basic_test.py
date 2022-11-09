"""Simple example of py2exe to create a exe of the basic_test example.

Tested on py2exe 0.13.0.0 on python 3.11
"""

import py2exe

py2exe.freeze(console=["basic_test.py"], options={"includes": ["pymunk"]})
