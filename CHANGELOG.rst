=========
Changelog 
=========

Pymunk 6.8.1 (2024-06-05)
-------------------------

**Space lock bug fix**

This is a patch version, that fixes a bug in the separate collision callback 
which could result in hard crash if after the separate another collision 
callback ran and that callback added or removed something from the space.

    Changes:

    - Build/run MacOs ARM on ARM github runners. 
    - Fix lock bug in separate callback
    - Improve documentation


Pymunk 6.8.0 (2024-05-10)
-------------------------

**Spring improvements**

This release makes the max force property on the two spring constraints work 
as expected (previously it did not have any effect). It is also possible to 
fully override the force/torque calculation of the springs with new callback.
Apart from this a collection of fixes in the underlying Chipmunk2D library 
has been added. Finally, it's now possible to create static bodies with 
constraints between them, and then change the bodies to dynamic to "start" 
simulation of them.

Changes:

- Fix for 2 static bodies that are changed to dynamic and are attached to 
  constraints
- Updated the fork of Chipmunk2D used by Pymunk, fixing a number of issues, 
  including maxForce on Spring constraints.
- Added callback functions for DampedSpring and DampedRotarySpring to allow 
  customized force/torque calculations.
  
  
Pymunk 6.7.0 (2024-05-01)
-------------------------

**Batch API can set body properties**

This release expands the experimental Batch API introduced in Pymunk 6.6.0. 
It now comes with functions to efficiently set properties on the body such as 
velocity. Similar to the previous API the new API reduces overhead of the 
Python / C bridge, but also makes it very easy to use for example Numpy to 
perform calculations over many bodies. The existing planet.py demo has been 
updated to showcase the new Batch API and easily toggle between batch / no 
batch to see the difference in performance.

Changes:

- Add set body function to pymunk.batch 
- Fix crash with sensor shapes in pymunk.batch
- Improved types
- New interactive example to show collisions
- Fix constraints of bodies that change type


Pymunk 6.6.0 (2023-11-02)
-------------------------

**Experimental Batch API**

This release adds a (experimental) batch API that can be used to efficiently 
get body properties such as positions, and collision data for all bodies /
collisions in a space in one call. This way the overhead of calling the 
underlying c library (Chipmunk2D) is minimized, enabling a massive speedup
in some cases.

Changes:

- New pymunk.batch module with batch API.
- Batch Api benchmark
- Batch version of colors.py example
- Improved types
- Improve build/packaging


Pymunk 6.5.2 (2023-10-22)
-------------------------

**Python 3.12**

This is a minor release mainly for publishing wheels for CPython 3.12.

Changes:

- Build wheels for CPython 3.12
- Documentation improvements
- Added experimental env PYMUNK_BUILD_SLIM to slim down wheels for 
  WASM/Pyodide.
- Added assert for circular reference when pickling/copy
- Fixed memory leak in batched api benchmark


Pymunk 6.5.1 (2023-06-26)
-------------------------

**Fix source dist**

Some custom cffi c headers and source files are now included in the source 
distributions so that Pymunk can be fully built from it.

Changes:

- Include pymunk custom c files in source dist zip


Pymunk 6.5.0 (2023-06-23)
-------------------------

**Repeatable pickle/unpickle of simulation!**

When pickling the internal collision state will now be pickled as well, 
meaning that the unpickled space will behave as the original even when
collisions where ongoing while pickling. This is useful if you want to 
replay a simulation.

Changes:

- Pickle of internal collision state
- Merged the latest upstream Chipmunk version
- Improved type hints
- Improved docs 
  

Pymunk 6.4.0 (2022-11-20)
-------------------------

**Support Pyglet 2 debug drawing!**

This is a minor update, with the main change being support for the recently 
released Pyglet 2. At the same time support for Pyglet 1.5.x has been 
deprecated, and when using pyglet_util with pyglet 1.x a warning will be 
logged about the deprecation. The other big change is that the examples
have been moved into pymunk.examples subpackage, so they can easily be run 
even when Pymunk is installed from a wheel.

Changes:

- Support for debug drawing using Pyglet 2.0
- Using pyglet 1.5 is deprecated and will be removed in a future version. 
- Moved examples into the distribution as the pyumnk.examples package. 
- Improved type hints


Pymunk 6.3.0 (2022-11-04)
-------------------------

**Build wheel for CPython 3.11!**

This is a minor update with changes to be build pipe to build wheels for 
CPython 3.11. Some internal parts have been rewritten as well.

Changes:

- Update callbacks implemention to the cffi recommended way
- Improve Asserts to catch errors earlier
- Improve type hints
- Build wheels for more targets
- Remove experimental body._id
  

Pymunk 6.2.1 (2021-10-31)
-------------------------

**Build wheel for CPython 3.10!**

This is a minor update with changes to the build pipe to build wheels for more
cases, notably the recently released CPython 3.10.

Changes:

- Use pyproject.toml 
- Require CFFI 1.15 to make sure wheels are build ok on Apple ARM64/M1.
- Doc improvements
- Build wheels for more targets

Pymunk 6.2.0 (2021-08-25)
-------------------------

**Improved transforms for debug drawing!**

This release contains enhancements to transform usage with debug drawing,
and an update to latest git version of Chipmunk. It also contains a new 
example of how gravity in the center could be implemented.

Changes:

- Updated Chipmunk to latest git version
- Updated debug draw to support rotation, and fixed scaling of constraints
- New example of "planet" gravity (ported from Chipmunk)
- Fixed potential corner case bug in garbage collection logic  


Pymunk 6.1.0 (2021-08-11)
-------------------------

**Transforms for debug drawing!**

The main improvement in this release is that its now possible to set a 
Transform on the SpaceDebugDrawOptions object, which is applied before 
anything is drawn. This works in all the debug draw implementation, e.g. for 
pygame. In this way its possible to easily implement features such as camera 
panning easily for debug draw code. See the new camera.py example for an 
example of this. 

Changes:

- Added transform property to SpaceDebugDrawOptions.
- Extended Transform to allow allow matrix multiplication using @, either 
  with another Transform or with a Vec2d.
- Improved error handling when adding objects to a space.
- Improved docs.


Pymunk 6.0.0 (2020-12-07)
-------------------------

**Typehints, dropped Python 2, and Vec2d rework and wrapping upgrade!** 

This release is a very big update to Pymunk, with a number of breaking 
API changes. It is likely that most users of Pymunk that upgrade will need 
to do some changes to work, but in the majority of cases the changes should
be minor.


Highlights - Major changes:

- Python 3.6 or newer required. Support for older Pythons including 2.7 has 
  been dropped.
- Type hints added. Type hints have been added for all public interfaces.
- Vec2d (the vector class) has been completely overhauled. It is now a 
  immutable subclass of ``NamedTuple``, with a streamlined API interface. See
  below for details. 


Vec2d changes:

- Vec2d no longer accept objects that have ``.x`` and ``.y`` properties, 
  but do not support ``__getitem__`` for ``[0]`` & ``[1]`` in the 
  constructor. If you have such an objects, rewrite ``Vec2d(myobj)`` to 
  ``Vec2d(myobj.x, myobj.y)``.
- Vec2d is now Immutable.

  - removed ``__setitem__`` (you can not do ``Vec2d(1,2)[1] = 3`` anymore).
  - not possible to set the length property. ``Vec2d(1,2).length = 10``, 
    instead use ``Vec2d(1,2).scale_to_length(10)``.
  - removed ``Vec2d.get_length`` method (use the length property instead).
  - removed ``Vec2d.rotate()`` method. use ``Vec2d.rotated()`` instead.
  - removed ``Vec2d.rotate_degrees()`` method. use ``Vec2d.rotated_degrees`` 
    instead.
  - not possible to set the angle property (``Vec2d(1,2).angle = 3.14``). Use 
    ``Vec2d.rotated()`` instead. 
  - removed ``Vec2d.get_angle`` method (use the ``angle`` property instead).
  - not possible to set the ``angle_degrees`` property 
    (``Vec2d(1,2).angle_degrees = 180``). Use ``Vec2d.rotated_degress`` 
    instead.
  - removed ``Vec2d.get_angle_degrees`` method (use the ``angle_degrees`` 
    property instead)
  - removed ``Vec2d.normalize_return_length`` method (use ``Vec2d.length`` and 
    ``Vec2d.normalized()``, or the new ``Vec2d.normalized_and_length method``).
  - removed ``__iadd__``, ``__isub__``, ``__imul__``, ``__ifloordiv__`` and 
    ``__itruediv__``).

- Removed ``__nonzero__`` magic. This never worked in Python 3, and was not 
  included in any tests.
- Removed ``__pow__`` and ``__rpow__`` magic. Its no longer possible to do 
  ``Vec2d(1,2)**2``, instead you need to do the calculation manually. 
- Removed ``__invert__`` magic. Its no longer possible to do ``~Vec2d(1,2)``.
- Removed ``__mod__`` and ``__divmod__`` magic. Its no longer possible to do 
  ``Vec2d(1,2) % 2`` or ``divmod(Vec2d(1,2), 2)``.
- Removed bit operations right shift, left shift, or, and, xor. 
  (``<<``, ``>>``, ``|``, ``&``, ``^``).
- Changed ``abs(Vec2d(1,2))`` to return the expected vector length instead of 
  ``Vec2d(abs(x), abs(y))``.
- Vec2d now only support addition with other Vec2ds or tuples (sequences) of 
  length 2.
- Vec2d now only support subtraction with other Vec2ds or tuples (sequences) 
  of length 2.
- Vec2d now only support multiplicaton with ints and floats.
- Vec2d now only support division by ints and floats. Note that reverse 
  division is not supported, i.e. ``1 / Vec2d(1,2)``.
- Vec2d now only support floor division (``//``) by ints and floats. Note 
  that reverse floor division is not supported, i.e. ``1 // Vec2d(1,2)``.
- Improved error checking in Vec2d when an opertor (magics like ``__add__``) 
  is used with incompatible types.
- Removed option to create a zero Vec2d with empty constructor. ``Vec2d()`` 
  should be replaced with ``Vec2d.zero()``.
- Made ``Vec2d`` a subclass of ``NamedTuple``.

  - Vec2ds has to be constructed with separate ``x`` and a ``y`` values.
  - ``Vec2d((1,2))`` can be changed to ``Vec2d(*(1,2))``.
  - ``Vec2d(Vec2d(1,2))`` can be changed to ``Vec2d(*Vec2d(1,2))``.
  - ``Vec2d()`` can be changed to ``Vec2d(0,0)`` or ``Vec2d.zero()``. 
  - ``Vec2d(1,2)`` is no longer equal to ``[1,2]`` since they are of 
    different types. (but ``Vec2d(1,2) == (1,2)`` is still true)

- Relaxed ``get_angle_between``, ``convert_to_basis``, ``cpvrotate`` and 
  ``cpunvrotate`` to accept tuples of size 2 as arguments just like most 
  other methods on Vec2d.


General Changes:

- ``add_collision_handler(a,b)`` and ``add_collision_handler(b,a)`` will return the 
  same handler. Issue #132.
- Bodies used by shapes must be added to the space before (or at the same 
  time) the shape is added. This change will help users of Pymunk uncover 
  bugs, and it should be straight forward to fix old code.
- Python 3.6+ required. If you use a older Python, please continue to use the
  5.x series of Pymunk until its possible to upgrade.
- ``Space.add()`` and ``Space.remove()`` no longer accept lists of objects 
  (shapes, bodies or constraints), only the objects directly. Existing code 
  can be updated to unpack the arguments: ``space.add(list_of_stuff)`` becomes 
  ``space.add(*list_of_stuff)``.
- ``ShapeFilter.ALL_MASKS`` and ``CATEGORIES`` changed to static methods. 
  ``ShapeFilter.ALL_MASKS`` becomes ``ShapeFilter.ALL_MASKS()`` and 
  ``ShapeFilter.CATEGORIES`` becoems ``ShapeFilter.CATEGORIES()``.  
- Note: a tuple of 4 numbers are required when specifying a color (or use the 
  ``SpaceDebugColor`` class directly). During testing it was found that some 
  demos used a tuple of 3 instead which does not work in Pymunk 6.0 (or 
  earlier version).
- Return a ``PointQueryInfo`` object from ``Shape.point_query``, not the 
  previous ``(distance, PointQueryInfo)`` tuple. Code that need the distance 
  can access it from ``PointQueryInfo.distance``.
- Removed ``pymunk.inf``. Use standard Python ``float('inf')`` instead.
- Renamed package ``pymunk.constraint`` to ``pymunk.constraints``. Code that 
  imported the previous name should be updated to import from the new name 
  instead.
- Changed ``pygame_util.positive_y_is_up`` default value to ``False``. 
  Existing code dependent on the old default should set the desired value 
  (``True``). For new code it might be better to instead make the Pymunk 
  simulation behave like the native pygame coordinates. See examples in 
  examples folder for examples. 
- It is now expected that places functions expecting a ``Vec2d`` or tuple of 
  length 2 already are a tuple (or ``Vec2d``). Previously a conversion happed 
  by calling ``tuple(argument)``. To fix old code simply wrap the argument in 
  ``tuple( ... )``. (Note: Due to no type checks a list of length 2 might 
  also work, however, this is not supported and can change any time. 
- ``BB`` base class changed to ``NamedTuple``. They now has to be 
  constructed with ``left``, ``bottom``, ``right``, ``top`` as separate 
  arguments.  
- Repr of ``BB`` will return ``BB(left=1, bottom=5, right=20, top=10)`` 
  instead of ``(1, 5, 20, 10)``.
- ``BB`` is now immutable. 
- New callbacks on ``Constraint`` object, ``pre_solve`` and ``post_solve``, 
  which can be used to run a function just before or after the solver on the 
  constraint.
- Added helper methods on ``Transform`` to easily create transforms to 
  translate, scale and rotate.
- Removed now unused pymunkoptions module.
- Changed type of autogeometry ``march_*.sample_func`` to expect a tuple of 
  length 2 instead of a Vec2d (to improve performance). Issue #126.
- Removed ``march_*.segment_func`` argument, and instead return a 
  ``PolylineSet`` with the result. This allows future optimizations, and is 
  easier to use. Issue #126.
- Added code to make Pymunk work without extra config in PyInstaller, py2exe 
  and probably other bundlers as well.
- Debug logging addded to easier understand c memory issues. Uses 
  logging.debug so should be easy to work around.  

Minor changes unlikely to affect existing code:

- Removed ``pymunk.chipmunk_path``. 
- Changed ``Shape.sensor`` type to bool (from int).
- Add check that pickled objects were pickled by the same Pymunk version as 
  the code loading it. The internal pickled format can change between major, 
  minor and point releases of Pymunk.
- Slight change of format of ``pymunk.chipmunk_version`` version string.
- Small change to make the collision handler functions (``begin``, 
  ``pre_step``...) return the function assigned, not the wrapped function.
- Removed extra ``*args`` and ``**kwargs`` arguments to 
  ``CollisionHandler.__init__`` method.
- Pymunk source code formatted with black & isort.
- ``moment_for_poly()`` and ``area_for_poly()`` now expects a Sequence 
  (tuple/list like object) of tuples of length 2. 
- Added default value of argument ``point`` to ``apply_force_at_local_point``.
- Removed default value of argument point from 
  ``apply_impulse_at_world_point``. Just specify ``point = (0,0)`` to mimic 
  the old default.
- Added many asserts to check that whenever a tuple of length 2 or ``Vec2d`` 
  is expected the length of the tuple is 2. Working code is unlikely 
  affected, but bugs will be easier to find.
   

Behind the scenes:

- In order to allow adding some advanced features that are not available in 
  Chipmunk today the method used to call C-code has changed to CFFI API mode.
  In addition to easier expansion it also provides increased performance.


Pymunk 5.7.0 (2020-09-16)
-------------------------

**Fix release**

This release contains a bunch of smaller fixes and improvements. 

Changes:

- Fixed issue with PyInstaller onefile.
- Improved performance of Vec2d creation. Thanks Mikhail Simin!
- Handle debug drawing of springs with 0 length.
- Made bodies and constraints ordered when accessed from the space.
- Added Space.use_spatial_hash function to enable use of Spatial hash as its 
  spatial index which can improve performance when there's lots of similarly 
  sized objects.
- Fixed case when Vec2d.projection get a tuple as other paramter.
- Fixed ZeroDivisionError for Vec2d.projection. Thanks Mohamed Saad Ibn Seddik!
- Fixed return type of Shape.center_of_gravity property (now returns Vec2d 
  instead of cdata).
- Fixed issue when installing dev dependencies.
- Added chipmunk tank example (available in examples folder).
- Improved docs.

Heads up! A major update to Pymunk is on the way that will be released as 
Pymunk 6.0. It will contain big changes, some of them very API breaking, and 
it will also drop support for Python 2.


Pymunk 5.6.0 (2019-11-02)
-------------------------

**Fix to avoid incompatible CFFI version**

The main goal of this release is to ensure a compatible version of CFFI is 
installed when installing Pymunk though pip. Unfortunately there is a problem on 
Linux with CFFI 1.13.1. (Later and earlier versions will work fine)

Changes:

- Added a requirement on CFFI to not be 1.13.1 (since 1.13.1 doesnt work).
- Update cffi definitions to prevent deprecation warning in latest cffi.
- Added normal property to Arbiter object.
- Remove compiled docs from committed code.
- Removed build/test of CPython 3.4 from Travis and Appveyor configs since its 
  not supported anymore.
- Update pyglet examples to work with pyglet 1.4.
- Fixed minor issue in platformer example.
- Improved docs.


Pymunk 5.5.0 (2019-05-03)
-------------------------

**Updated Chipmunk version, FreeBSD, Android/Termux support and more!**

This release contains a number of improvements. Chipmunk was updated to the 
latest version, and then a number of unmerged PRs were merged in. (The 
Chipmunk git repo is quite dead, so Pymunk will include unmerged PRs after 
manual review). Another major improvement is that now Pymunk can run on 
FreeBSD. It was also tested on Termux on Android, and several improvements to 
the installation process has been included. A bunch of smaller fixes are also 
included.

Changes:

- Update Chipmunk to 7.0.2 + unmerged PRs 
- Pymunk can be installed and run on FreeBSD
- Pymunk can be installed and run on Termux on Android
- Fix debug drawing of polygons with radius
- Improved debug drawing of segments on pygame
- Fix problem when installing without wheel package installed
- New Constraints demo
- Improved docs


Pymunk 5.4.2 (2019-01-07)
-------------------------

**Fix for chipmunk.dll load troubles on windows**

This release fixes a problem on Windows that made the chipmunk.dll file depend
on libwinpthread-1.dll which happened in Pymunk 5.4.1 because of the new build
setup. The fix means that for now the threaded solver is disabled on Windows. 
In practice this should not be a big problem, the performance benefit of the 
threaded solver on a desktop running windows is unclear.

Changes: 

- Disable threaded solver on Windows.


Pymunk 5.4.1 (2018-12-31)
-------------------------

**Improved packaging**

This release consists of a number of fixes to the packaging of Pymunk. One fix
that will allow building for conda, and a number of changes to build binary 
wheels on linux.

Changes:

- Fixes to help Pymunk work with freezers such as cx_Freeze.
- Better wheels, now they contain the proper tags
- Fix problems using custom CFLAGS when compiling chipmunk

Enjoy!


Pymunk 5.4.0 (2018-10-24)
-------------------------

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


Pymunk 5.3.2 (2017-09-16)
-------------------------

**Fixes ContactPointSet updating in Arbiter**

This release contains a fix for the ContactPointSet on Arbiters. With this fix
its possible to update the contacts during a collision callback, for example
to update the normal like in the breakout game example. 

Changes:

- Fix Arbiter.contact_point_set 


Pymunk 5.3.1 (2017-07-15)
-------------------------

**Fix for Pycparser 2.18**

This release contains a fix for the recently released Pycparser 2.18 which
is used by Pymunk indirectly from its use of CFFI.

Changes:

- Fix broken callbacks when using Pycparser 2.18.


Pymunk 5.3.0 (2017-06-11)
-------------------------

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


Pymunk 5.2.0 (2017-03-25)
-------------------------

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


Pymunk 5.1.0 (2016-10-17)
-------------------------

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


Pymunk 5.0.0 (2016-07-17)
-------------------------

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


Pymunk 4.0.0 (2013-08-25)
-------------------------

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


Pymunk 3.0.0 (2012-09-02)
-------------------------

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


Pymunk 2.1.0 (2011-12-03)
-------------------------

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


Pymunk 2.0.0 (2011-09-04)
-------------------------
    
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

Pymunk 1.0.0 (2010-07-16)
-------------------------

Pymunk 0.8.3 (2009-07-26)
-------------------------

Pymunk 0.8.2 (2009-04-22)
-------------------------

Pymunk 0.8.1 (2008-11-02)
-------------------------

Pymunk 0.8 (2008-06-15)
-----------------------

First public release on Pypi.


Pymunk 0.1 (2007-08-01)
-----------------------

First public release. On the Pyweek game competition forum, and later used in 
our entry in Pyweek 5.
