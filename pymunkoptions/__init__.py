# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2012 Victor Blomqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------

"""Use this module to set runtime options of pymunk.

Currently there is one option that can be changed, debug. By setting debug to 
false debug print outs will be limited. In order to remove all debug prints 
you will also need to compile chipmunk in release mode. See 
:ref:`compile-chipmunk` for details on how to compile chipmunk.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

options = {
    "debug" : True
}
"""Global dict of pymunk options.
To change make sure you import pymunk before any sub-packages and then set the 
option you want. For example::

    import pymunkoptions
    pymunkoptions.options["debug"] = False
    import pymunk
    
    #..continue to use pymunk as you normally do
    
"""
