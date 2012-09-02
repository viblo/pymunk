****
News 
****

pymunk 3.0.0
-------------
*Victor - 2012-09-02*

**I'm happy to announce pymunk 3!**

This release is a definite improvement over the 2.x release line of pymunk. 
It features a much improved documentation, an updated Chipmunk version with 
accompanying API adjustments, more and cooler examples. Also, to help to do
quick prototyping pymunk now includes a new module pymunk.pygame_util that 
can draw most physics objects on a pygame surface. Check out the new 
pygame_util_demo.py example to get an understanding of how it works. 

Another new feature is improved support to run in non-debug mode. Its now 
possible to pass a compile flag to setup.py to build Chipmunk in release mode
and there's a new module, pymunkoptions that can be used to turn pymunk debug 
prints off.

This release has been tested and runs on CPython 2.6, 2.7, 3.2.
At least one run of the unit tests have been made on the following 
platforms: 32 bit Python on Windows, 32 and 64 bit Python on Linux, and 32 
and 64 bit Python on OSX.

This release has also been tested on Pypy 1.9, with all tests passed!

Changes

- Several new and interesting examples added
- New draw module to help with pygame prototyping
- New pymunkoptions module to allow disable of debug
- Tested on OSX, includes a compiled dylib file
- Much extended and reworked documentation and homepage
- Update of Chipmunk
- Smaller API changes
- General polish and cleanup
- Shining new domain: www.pymunk.org

I hope you will like it!


pymunk 2.1.0
-------------
*Victor - 2011-12-03*

**A bugfix release of pymunk is here!**

The most visible change in this release is that now the source release 
contains all of it including examples and chipmunk source. :) Other fixes 
are a new velocity limit property of the body, and some removed methods 
(Reasoning behind removing them and still on same version: You would get an 
exception calling them anyway. The removal should not affect code that works). 
Note, all users should create static bodies by setting the input parameters 
to None, not using infinity. inf will be removed in an upcoming release.

Changes

- Marked pymunk.inf as deprecated
- Added velocity limit property to the body
- Fixed bug on 64bit python
- Recompiled chipmunk.dll with python 2.5
- Updated chipmunk source.
- New method in Vec2d to get int tuple
- Removed slew and resize hash methods
- Removed pymunk.init calls from examples/tests
- Updated examples/tests to create static bodies the good way 

Have fun with it!


pymunk 2.0.0
-------------
*Victor - 2012-09-04*
    
**Today I'm happy to announce the new pymunk 2 release!**

New goodies in this release comes mainly form the updated chipmunk library. Its 
now possible for bodies to sleep, there is a new data structure holding the 
objects and other smaller improvements. The updated version number comes mainly 
from the new sleep methods.

Another new item in the release is some simplification, you now don't need to 
initialize pymunk on your own, thats done automatically on import. Another cool 
feature is that pymunk passes all its unit tests on the latest pypy source 
which I think is a great thing! Have not had time to do any performance tests, 
but pypy claims improvements of the ctypes library over cpython.

Note, this release is not completely backwards compatible with pymunk 1.0, 
some minor adjustments will be necessary (one of the reasons the major version 
number were increased).

Changes from the last release:

- Removed init pymunk method, its done automatically on import
- Support for sleeping bodies.
- Updated to latest version of Chipmunk
- More API docs, more unit tests.
- Only dependent on msvcrt.dll on windows now.
- Removed dependency on setuptools
- Minor updates on other API, added some missing properties and methods. 

Enjoy! 

Older news
----------

Older news items have been archived.
