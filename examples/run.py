"""Use to run examples using pymunk located one folder level up.
Useful if you have the whole pymunk source tree and want to run the examples 
in a quick and dirty way. (a poor man's virtualenv if you like)

For example, to run the breakout demo::

    > cd examples
    > python run.py breakout.py
"""

import sys
sys.path.insert(1,'..')
# some extra things for pyglet
sys.path.insert(1,'../../../pyglet')
sys.path.insert(1,'../../../../pyglet')

if len(sys.argv) > 1:
    name = sys.argv[1]
    sys.argv = sys.argv[1:]
    del sys
    
    execfile(name)
    
else:
    print(__doc__)
