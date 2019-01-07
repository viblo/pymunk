****
News 
****

Pymunk 5.4.2
------------
*Victor - 2019-01-07*

**Fix for chipmunk.dll load troubles on windows**

This release fixes a problem on Windows that made the chipmunk.dll file depend
on libwinpthread-1.dll which happened in Pymunk 5.4.1 because of the new build
setup. The fix means that for now the threaded solver is disabled on Windows. 
In practice this should not be a big problem, the performance benefit of the 
threaded solver on a desktop running windows is unclear.

Changes: 

- Disable threaded solver on Windows.

Pymunk 5.4.1
------------
*Victor - 2018-12-31*

**Improved packaging**

This release consists of a number of fixes to the packaging of Pymunk. One fix
that will allow building for conda, and a number of changes to build binary 
wheels on linux.

Changes:

- Fixes to help Pymunk work with freezers such as cx_Freeze.
- Better wheels, now they contain the proper tags
- Fix problems using custom CFLAGS when compiling chipmunk

Enjoy!

Pymunk 5.4.0
------------
*Victor - 2018-10-24*

**Fix support for MacOS 10.14**

Main fix is to allow Pymunk to be installed on latest version of MacOS. This 
release also contain a bunch of minor fixes and as usual an improvement of 
the docs, tests and examples.

Changes:

- On newer versions of MacOS only compile in 64bit mode (32bit is deprecated)
- Improved docs, examples and tests
- Fix in moment_for_* when passed Vec2d instead of tuple
- Fix case when adding or removing more than one obj to space during step.
- Allow threaded solver on Windows.
- Use msys mingw to compile chipmunk on Windows (prev solution was deprecated).

Enjoy!

Introductory video tutorials
----------------------------
*Victor - 2018-02-25*

Youtube user Attila has created a series of videos covering the basics of 
Pymunk. Take a look here for a gentle introduction into Pymunk:
 
.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=PL1P11yPQAo7pH9SWZtWdmmLumbp_r19Hs" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>


Pymunk 5.3.2
------------
*Victor - 2017-09-16*

**Fixes ContactPointSet updating in Arbiter**

This release contains a fix for the ContactPointSet on Arbiters. With this fix
its possible to update the contacts during a collision callback, for example
to update the normal like in the breakout game example. 

Changes:

- Fix Arbiter.contact_point_set 


Pymunk 5.3.1
------------
*Victor - 2017-07-15*

**Fix for Pycparser 2.18**

This release contains a fix for the recently released Pycparser 2.18 which
is used by Pymunk indirectly from its use of CFFI.

Changes:

- Fix broken callbacks when using Pycparser 2.18.


Pymunk 5.3.0
------------
*Victor - 2017-06-11*

**Pickle and copy support!**

New in this release is pickle (save and load) and copy support. This has been 
on my mind for a long time, and when I got a feature request for it on Github 
by Rick-C-137 I had the final push to make it happen.  See 
`examples/copy_and_pickle.py 
<https://github.com/viblo/pymunk/tree/master/examples/copy_and_pickle.py>`_ 
for an example.

The feature itself is very easy to use, pickle works just as expected, and copy
is a simple method call. However, be aware that support for pickle of Spaces 
with callback functions depends on the pickle protocol version. The oldest 
pickle protocol have limited capability to pickle functions, so to get maximum 
functionality use the latest pickle protocol possible.

Changes:

- Pickle support. Most objects can be pickled and un-pickled.
- Copy support and method. Most objects now have a copy() function. Also the 
  standard library copy.deepcopy() function works as expected.
- Fixed bugs in BB.merge and other BB functions.
- Improved documentation and tests.
- New Kivy example (as mentioned in earlier news entry).

I hope you will like it!


New page theme
------------------
*Victor - 2017-06-07*

**An mobile friendlier experience!**

A couple of days ago I noticed that the Pymunk web page get a significant 
amount of traffic from mobile, and at the same time the Sphinx theme it uses 
is not built for mobile browsing. So as a result I decided to change theme to 
something that can scale down to mobile size better. I hope the new page gives 
a better experience for everyone!


Pymunk on Android
-----------------
*Victor - 2017-06-04*

**Pymunk runs on Android!**

With the latest version (5.2.0) Pymunk can now be compiled and run on Android 
phones. Available as an example: `examples/kivy_pymunk_demo 
<https://github.com/viblo/pymunk/tree/master/examples/kivy_pymunk_demo>`_
is a Kivy example that can be built and run on Android. 

Below is a screen cap from my phone (an Xperia X Compact) running the Kivy 
example. The example itself is an interactive variant of the logo animation 
used on the front page of Pymunk.org

.. raw:: html

    <iframe width="560" height="315" 
    src="https://www.youtube.com/embed/AUfK7IJITEk" frameborder="0" 
    allowfullscreen></iframe>


Pymunk 5.2.0
------------
*Victor - 2017-03-25*

**Customized compile for ARM / Android**

The main reason for this release is the ARM / Android cross compilation support 
thanks to the possibility to override the ccompiler and linker. After this 
release is out its possible to create a python-for-android build recipe for 
Pymunk without patching the Pymunk code. It should also be easier to build for 
other environments.

Changes

- Allow customization of the compilation of chipmunk by allowing overriding the 
  compiler and linker with the CC, CFLAGS, LD and LDFLAGS environment variables.
  (usually you dont need this, but in some cases its useful)
- Fix sometimes broken Poly draw with pyglet_util.
- Add feature to let you set the mass of shapes and let Pymunk automatically 
  calculate the body mass and moment.
- Dont use separate library naming for 32 and 64 bit builds. (Should not have 
  any visible effect)


Pymunk 5.1.0
------------
*Victor - 2016-10-17*

**A speedier Pymunk has been released!**

This release is made as follow up on the :doc:`benchmarks` done on 
Pymunk 5.0 and 4.0. Pymunk 5.0 is already very fast on Pypy, but had some 
regressions in CPython. Turns out one big part in the change is how Vec2ds are 
handled in the two versions. Pymunk 5.1 contains optimized code to help reduce 
a big portion of this difference. 

Changes

- Big performance increase compared to Pymunk 5.0 thanks to improved Vec2d 
  handling.
- Documentation improvements.
- Small change in the return type of Shape.point_query. Now it correctly 
  return a tuple of (distance, info) as is written in the docs.
- Split Poly.create_box into two methods, Poly.create_box and 
  Poly.create_box_bb to make it more clear what is happening. 

I hope you will enjoy this new release!


Pymunk 5.0.0
------------
*Victor - 2016-07-17*

**A new version of Pymunk!**

This is a BIG release of Pymunk! Just in time before Pymunk turns 10 next year! 

* Support for 64 bit Python on Windows
* Updated to use Chipmunk 7 which includes lots of great improvements
* Updated to use CFFI for wrapping, giving improved development and packaging 
  (wheels, yay!)
* New util module with draw help for matplotlib (with example Jupyter notebooks)
* Support for automatically generate geometry. Can be used for such things as
  deformable terrain (example included).
* Deprecated obsolete submodule pymunk.util.
* Lots of smaller improvements

New in this release is also testing on Travis and Appveyor to ensure good code 
quality.

I hope you will enjoy this new release!


Move from ctypes to CFFI?
-------------------------
*Victor - 2016-05-19*

**Should pymunk move to CFFI?**

To make development of pymunk easier Im planning to move from using ctypes
to CFFI for the low level Chipmunk wrapping. The idea is that CFFI is a 
active project which should mean it will be easier to get help, for example
around the 64bit python problems on windows.

Please take a look at Issue 99 on github which tracks this switch.
https://github.com/viblo/pymunk/issues/99


Travis-ci & tox
---------------
*Victor - 2014-11-13*

**pymunk is now using travis-ci for continuous integration**

In an effort to make testing and building of pymunk easier travis has been 
configured to build pymunk. At the same time support for tox was added to 
streamline local testing.


Move to Github
--------------
*Victor - 2013-10-04*

**pymunk has moved its source and issue list to Github!**

From the start pymunk has been hosted at Google Code, in the beginning using 
it for everything, source control, issue tracker, documentation and so on. 
During that time Github has become more and more popular and overall a better 
hosting platform. 

At the same time distributed version control systems have risen in popularity 
over traditional ones like Subversion.

Adding to this Google Code will stop hosting binaries in January 2014.

Because of this I have been thinking a while about moving pymunk away from 
svn and google code. I had an issue open on google code in which all feedback 
proposed git and github, and that has been my own thought as well. And so, 
today the move has been completed!

To get the latest source you will need a git client and then do::
    
    > git clone https://github.com/viblo/pymunk.git

If you prefer a graphical client (I do) I find SourceTree very good. 

Issues have been migrated to https://github.com/viblo/pymunk/issues

Binaries will be available from Pypi just like before, but the binary 
hosting at Google Code will not get any updates.

The google code page will from now on only have a redirect to pymunk.org and 
github.


pymunk 4.0.0
-------------
*Victor - 2013-08-25*

**A new release of pymunk is here!**

This release is definitely a milestone, pymunk is now over 5 years old! 
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

This release has been tested and runs on CPython 2.5, 2.6, 2.7, 3.3 and Pypy 2.1. 
At least one run of the unit tests have been made on the following platforms: 
32 bit CPython on Windows, 32 and 64 bit CPython on Linux, and 64 bit CPython 
on OSX. Pypy 2.1 on one of the above platforms.



Changes

- New draw module to help with pyglet prototyping
- Updated Chipmunk version, with new collision detected code.
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
