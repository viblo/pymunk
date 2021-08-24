Advanced 
========

In this section different "Advanced" topics are covered, things you normally 
dont need to worry about when you use Pymunk but might be of interest if you
want a better understanding of Pymunk for example to extend it. 

First off, Pymunk is a pythonic library built around the C-library 
Chipmunk2D, which provides almost all of the base functionality around the 
physics simulation such as collision detection, impulse solving etc. 
Bascially it runs the simulation, and Pymunk calls it with input, and 
receives the result.

To wrap Chipmunk Pymunk uses CFFI in API mode. On top of the CFFI wrapping is
a handmade pythonic layer to make it nice to use from Python code.


Impulse Solver Algorithm
------------------------

Pymunk in itself only performs a minimum amount of physics calculation, 
instead those are handled by the underlying C-library Chipmunk 2D. Chipmunk2D 
(and therefor Pymunk) uses standard Euler to perform the integration

Scott/slembcke (the creator of Chipmunk2D), wrote this to describe the method 
used on the 
`Chipmunk2D Forum <https://chipmunk-physics.net/forum/viewtopic.php?f=1&t=1432&p=6652&hilit=euler#p6652>`_:

  Chipmunk works like this:
  
  1. Integrate the positions of everything and finds colliding pairs.
  2. Pre-calculate a number of properties of the contacts and joints. 
     (mass properties, bounce velocities, etc)
  3. Integrate the velocities of everything.
  4. Run a number of solver iterations, to fix velocity constraints.

  Case 1, a box sitting on the ground:

  1. The box is at rest, it's velocity is (very near) zero, it's position 
     doesn't change. Generate a contact with the ground.
  2. Precalculate the contact properties, if elasticity is set, the 
     "bounce" velocity is calculated now (as 0).
  3. Integrate the velocity, gravity makes the object accelerate downwards.
  4. Solve the contact. Velocity should converge back to 0. If elasticity 
     was set, it will be handled correctly without resorting to threshold 
     velocities.

  #1 is really the most important part. If you were to update the 
  velocity before the postition, it would cause the box to move itself 
  into a position where it would intersect the ground. While Chipmunk has 
  to solve these overlaps anyway, avoiding them seems desirable. Another 
  very useful property is that when cpSpaceStep() returns, all of the 
  collision detection data structures are up to date. No need to reindex 
  them twice in a single frame if you want to make queries.


Collision Detection Algorithm
-----------------------------

Just as the impulse solver, the collision detection is also handled by the 
underlying C-library Chipmunk2D.

Chipmunk uses GJK/EPA to find collisions between the tricky cases (e.g. 
polygons, segment shapes). There is a blog post 
`here <http://howlingmoonsoftware.com/wordpress/enhanced-collision-algorithms-for-chipmunk-6-2/>`_ 
with more details.


Why CFFI?
---------

This is a straight copy from the github issue tracking the CFFI upgrade. 
https://github.com/viblo/pymunk/issues/99

CFFI have a number of advantages but also a downsides.

Advantages (compared to ctypes):

* Its an active project. The developers and users are active, there are new 
  releases being made and its possible to ask and get answers within a day on 
  the CFFI mailing list.
* Its said to be the way forward for Pypy, with promise of better performance 
  compares to ctypes.
* A little easier than ctypes to wrap things since you can just copy-paste the 
  c headers.

Disadvatages (compared to ctypes):

* ctypes is part of the CPython standard library, CFFI is not. That means that 
  it will be more difficult to install Pymunk if it uses CFFI, since a 
  copy-paste install is no longer possible in an easy way.

For me I see the 1st advantage as the main point. I have had great difficulties 
with strange segfaults with 64bit pythons on windows, and also sometimes on 
32bit python, and support for 64bit python on both windows and linux is 
something I really want. Hopefully those problems will be easier to handle with 
CFFI since it has an active community.

Then comes the 3rd advantage, that its a bit easier to wrap the c code. For 
ctypes I have a automatic wrapping script that does most of the low level 
wrapping, but its not supported, very difficult to set up (I only managed 
inside a VM with linux) and quite annoying. CFFI would be a clear improvement.

For the disadvantage of ctypes I think it will be acceptable, even if not 
ideal. Many python packages have to be installed in some way (like pygame), 
and nowadays with pip its very easy to do. So I hope that it will be ok.

See the next section on why ctypes was used initially.

Why ctypes? (OBSOLETE)
----------------------

The reasons for ctypes instead of [your favorite wrapping solution] can be 
summarized as

* You only need to write pure python code when wrapping. This is good for 
  several reasons. I can not really code in c. Sure, I can read it and write 
  easy things, but Im not a good c coder. What I do know quite well is 
  python. I imagine that the same is true for most people using pymunk, 
  after all its a python library. :) Hopefully this means that users of 
  pymunk can look at how stuff is actually done very easily, and for example 
  add a missing chipmunk method/property on their own in their own code 
  without much problem, and without being required to compile/build anything. 

* ctypes is included in the standard library. Anyone with python has it 
  already, no dependencies on 3rd party libraries, and some guarantee that it 
  will stick around for a long time.

* The only thing required to run pymunk is python and a c compiler (in those 
  cases a prebuilt version of chipmunk is not included). This should maximize 
  the multiplatformness of pymunk, only thing that would even better would 
  be a pure python library (which might be a bad idea for other reasons, 
  mainly speed).

* Not much magic going on. Working with ctypes is quite straight forward. 
  Sure, pymunk uses a generator which is a bit of a pain, but at least its 
  possible to sidestep it if required, which Ive done in some cases. Ive also 
  got a share amount of problems when stuff didnt work as expected, but I 
  imagine it would have been even worse with other solutions. At least its 
  only the c library and python, and not some 3rd party in between.

* Non api-breaking fixes in chipmunk doesnt affect pymunk. If a bugfix, some 
  optimization or whatever is done in chipmunk that doesnt affect the API, 
  then its enough with a recompile of chipmunk with the new code to benefit 
  from the fix. Easy for everyone.

* Ctypes can run on other python implementations than cpython. Right now pypy 
  feels the most promising and it is be able to run ctypes just fine.

As I see it, the main benefit another solution could give would be speed. 
However, there are a couple of arguments why I dont find this as important as 
the benefits of ctypes

* You are writing your game in python in the first place, if you really 
  required top performance than maybe rewrite the whole thing in c would be 
  better anyway? Or make a optimized binding to chipmunk.

  For example, if you really need excellent performance then one possible 
  optimization would be to write the drawing code in c as well, and have that 
  interact with chipmunk directly. That way it can be made more performant 
  than any generic wrapping solution as it would skip the whole layer.

* The bottleneck in a full game/application is somewhere else than in the 
  physics wrapping in many cases. If your game has AI, logic and so on in 
  python, then the wrapper overhead added by ctypes is not so bad in 
  comparison.

* Pypy. ctypes on pypy has the potential to be very quick. However, right now 
  with pypy-1.9 the speed of pymunk is actually a bit slower on pypy than on 
  cpython. Hopefully this will improve in the future.
  
Note that pymunk has been around since late 2007 which means not all 
wrapping options that exist today did exist or was not stable/complete 
enough for use by pymunk in the beginning. There are more options available 
today, and using ctypes is not set in stone. If a better alternative comes 
around then pymunk might switch given the improvements are big enough.
  

Code Layout
-----------

Most of Pymunk should be quite straight forward.

Except for the documented API Pymunk has a couple of interesting parts. Low 
level bindings to Chipmunk, a custom documentation generation extension and a
customized setup.py file to allow compilation of Chipmunk.

The low level chipmunk bindings are located in the file 
pymunk_extension_build.py. 

docs/src/ext/autoexample.py
    A Sphinx extension that scans a directory and extracts the toplevel 
    docstring. Used to autogenerate the examples documentation.

pymunk/_chipmunk_cffi.py
    This file only contains a call to _chipmunk_cffi_abi.py, and exists mostly
    as a wrapper to be able to switch between abi and api mode of Cffi. This 
    is currently not in use in the relased code, but is used during 
    experimentation.
    
pymunk/_chipmkunk_cffi_abi.py
    This file contains the pure Cffi wrapping definitons. Bascially a giant 
    string created by copy-paster from the relevant header files of Chipmunk.  

setup.py
    Except for the standard setup stuff this file also contain the custom 
    build commands to build Chipmunk from source, using a build_ext extension.

pymunk/tests/*
    Collection of (unit) tests. Does not cover all cases, but most core 
    things are there. The tests require a working chipmunk library file.
    
tools/*
    Collection of helper scripts that can be used to various development tasks
    such as generating documentation.


Tests
-----

There are a number of unit tests included in the pymunk.tests package 
(pymunk/tests). Not exactly all the code is tested, but most of it (at the time
of writing its about 85% of the core parts). 

The tests can be run by calling the module ::

    > python -m pymunk.tests

Its possible to control which tests to run, by specifying a filtering 
argument. The matching is as broad as possible, so `UnitTest` matches all the 
unit tests, `test_arbiter` all tests in `test_arbiter.py` and 
`testResetitution` matches the exact `testRestitution` test case ::

    > python -m pymunk.tests -f testRestitution

To see all options to the tests command use -h ::

    > python -m pymunk.tests -h

Since the tests cover even the optional parts, you either have to make sure 
all the optional dependencies are installed, or filter out those tests.
    
    
Working with non-wrapped parts of Chipmunk
------------------------------------------

In case you need to use something that exist in Chipmunk but currently is not 
included in pymunk the easiest method is to add it manually. 

For example, lets assume that the is_sleeping property of a body was not 
wrapped by pymunk. The Chipmunk method to get this property is named 
cpBodyIsSleeping.

First we need to check if its included in the cdef definition in 
pymunk_extension_build.py. If its not just add it.
    
    `cpBool cpBodyIsSleeping(const cpBody *body);`
    
Then to make it easy to use we want to create a python method that looks nice::

    def is_sleeping(body):
        return cp.cpBodyIsSleeping(body._body)

Now we are ready with the mapping and ready to use our new method.
    

Weak References and free Methods
-----------------------------------

Internally Pymunk allocates structs from Chipmunk (the c library). For example a 
Body struct is created from inside the constructor method when a pymunk.Body is 
created. Because of this its important that the corresponding c side memory is 
deallocated properly when not needed anymore, usually when the Python side 
object is garbage collected. Most Pymunk objects use `ffi.gc` with a custom 
free function to do this. Note that the order of freeing is very important to 
avoid errors.
