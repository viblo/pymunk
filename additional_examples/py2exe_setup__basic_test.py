"""Simple example of py2exe to create a exe of the no_dependencies example.

Tested on py2exe 0.13.0.0 on python 3.11
"""

import py2exe

py2exe.freeze(console=["no_dependencies.py"], options={"includes": ["pymunk"]})
