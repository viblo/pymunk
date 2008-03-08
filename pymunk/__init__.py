"""
pymunk is a python wrapper for the 2d physics library Chipmunk

IRC: #pymunk on irc.freenode.net

Homepage: http://pymunk.googlecode.com/

Forum: http://www.slembcke.net/forums/viewforum.php?f=6
"""
__version__ = "$Id$"

#: The release version of this pymunk installation
#:
#: Valid only if pymunk was installed from a source or binary 
#: distribution (i.e. not in a checked-out copy from svn).
version = "0.7"

from pymunk import *
from vec2d import *
from util import *
