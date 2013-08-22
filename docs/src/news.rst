****
News 
****

pymunk 4.0.0
-------------
*Victor - 2013-XX-XX*

**DRAFT**

**A new release of pymunk is here!**

This release is definatley a milestone, pymunk is now over 5 years old! 
(first version was released in February 2008, for the pyweek competition)


In this release a number of improvements have been made to pymunk. It 
includes debug drawing for pyglet (debug draw for pygame was introduced in 
pymunk 3), an updated Chipmunk version with the resulting API adjustments, 
more and better examples and overall polish as usual.

With the new Chipmunk version (6.2 beta), collision detection might behave a 
little bit differently as it uses a different algorithm compared to earlier 
versions. The new algorithm means that segments to segment collisions will be 
detected now. If you have some segments that you dont want to collide then 
you can use the sensor property, or a custom collision callback function.

To see the new pymunk.pyglet_util module in action check out the 
pyglet_util_demo.py example. It has an interface similar to the pygame_util, 
with a couple of changes because of differences between pyglet and pygame.

Some API additions and changes have been made. Its now legal to add and remove 
objects such as bodies and shapes during the simulation step (for example in a 
callback). The actual removal will be scheduled to occur as soon as the 
simulation step is complete. Other changes are the possibility to change 
body of a shape, to get the BB of a shape, and create a shape with empty body.
On a body you can now retrieve the shapes and constraints attached to it.

This release has been tested and runs on CPython and Pypy. At least one run 
of the unit tests have been made on the following platforms: 32 bit CPython 
on Windows, 32 and 64 bit CPython on Linux, and 64 bit CPython on OSX. 
Pypy 2.1 on one of the above platforms.



Changes

- New draw module to help with pyglet prototyping
- Updated Chipmunk verison, with new collision detected code.
- Added, improved and fixed broken examples
- Possible to switch bodies on shapes
- Made it legal do add and remove bodies during a simulation step
- Added shapes and constraints properties to Body
- Possible to get BB of a Shape, and they now allow empty body in constructor
- Added radius property to Poly shapes
- Renamed Poly.get_points to get_vertices
- Renamed the Segment.a and Segment.b properties to unsafe_set
- Added example of using pyinstaller
- Fixed a number of bugs reported
- Improved docs in various places
- General polish and cleanup

I hope you will enjoy this new release!


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
*Victor - 2011-09-04*
    
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
