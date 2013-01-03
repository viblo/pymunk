"""Use to run examples using pymunk located one folder level up.
Useful if you have the whole pymunk source tree and want to run the examples 
in a quick and dirty way.

For example, to run the breakout demo::

    > cd examples
    > python run.py breakout.py
"""

import sys
sys.path.insert(0,'..')

if len(sys.argv) > 1:
    name = sys.argv[1]
    sys.argv = sys.argv[1:]
    del sys
    exec(compile(open(name).read(), name, 'exec'))
    
else:
    print(__doc__)
