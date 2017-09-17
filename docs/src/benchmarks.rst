Benchmarks
==========

To get a grip of the actual performance of Pymunk this page contains a number
of benchmarks.  

The full code of all benchmarks are available under the `benchmarks
<https://github.com/viblo/pymunk/blob/master/benchmarks>`_ folder.


Micro benchmarks
----------------

In order to measure the overhead created by Pymunk in the most common cases I 
have created two micro benchmarks. They should show the speed of the actual 
wrapping code, which can tell how big overhead Pymunk creates, and how big 
difference different wrapping methods does.

The most common thing a typical program using Pymunk does is to read out the 
position and angle from a Pymunk object. Usually this is done each frame for 
every object in the simulation, so this is a important factor in how fast 
something will be.

Given this our first test is::

    t += b.position.x + b.position.y + b.angle

(see `pymunk-get.py`)

Running it is simple, for example like this for pymunk 4.0::

    > python -m pip install pymunk==4.0
    > python pymunk-get.py

The second test we do is based on the second heavy thing we can do, and that is 
using a callback, for example as a collision handler or a position function::

    def f(b,dt):
        b.position += (1,0)

    s.step(0.01)

(see `pymunk-callback.py`)

Results:
########

Tests run on a HP G1 1040 laptop with a Intel i7-4600U. Laptop runs Windows, 
and the tests were run inside a VirtualBox VM running 64bit Debian. The CPython
tests uses CPython from Conda, while the Pypy tests used a
manually downloaded Pypy. CPython 2.7 is using Cffi 1.7, the other tests 
Cffi 1.8.

Remember that these results doesn't tell you how you game/application will 
perform, they can more be seen as a help to identify performance issues and
know differences between Pythons.

Pymunk-Get:
+++++++++++

==========  ==============  =============  ==========
..          CPython 2.7.12  CPython 3.5.2  Pypy 5.4.1
==========  ==============  =============  ==========
Pymunk 5.1  2.1s            2.2s           0.36s
Pymunk 5.0  4.3s            4.5s           0.37s
Pymunk 4.0  1.0s            0.9s           0.52s
==========  ==============  =============  ==========

Pymunk-Callback:
++++++++++++++++

==========  ==============  =============  ==========
..          CPython 2.7.12  CPython 3.5.2  Pypy 5.4.1
==========  ==============  =============  ==========
Pymunk 5.1  5.7s            6.8s           1.1s
Pymunk 5.0  6.5s            7.3s           1.0s
Pymunk 4.0  5.1s            6.5s           4.5s
==========  ==============  =============  ==========

What we can see from these results is that you should use Pypy if you have the 
possibility since that is much faster than regular CPython. We can also see 
that moving from Ctypes to Cffi between Pymunk 4 and 5 had a negative impact in 
CPython, but positive impact on Pypy, and Pymunk 5 together with Pypy is with a 
big margin the fastest option. 

The speed increase between 5.0 and 5.1 happened because the Vec2d class and how
its handled internally in Pymunk was changed to improve performance.


Compared to Other Physics Libraries
-----------------------------------

Cymunk
######

`Cymunk <https://github.com/kivy/cymunk>`_ is an alternative wrapper around Chipmunk. In contrast to Pymunk it uses Cython for wrapping (Pymunk uses CFFI) which gives it a different performance profile. However, since both are built 
around Chipmunk the overall speed will be very similar, only when information 
passes from/to Chipmunk will there be a difference. This is exactly the kind of 
overhead that the micro benchmarks are made to measure.

Cymunk is not as feature complete as Pymunk, so in order to compare with Pymunk 
we have to make some adjustments. A major difference is that it does not 
implement the `position_func` function, so instead we do an alternative 
callback test using the collision handler::

    h = s.add_default_collision_handler()
    def f(arb):
        return false
    h.pre_solve = f

    s.step(0.01)

(see `pymunk-collision-callback.py and  `cymunk-collision-callback.py`)

Results
+++++++

Tests run on a HP G1 1040 laptop with a Intel i7-4600U. Laptop runs Windows, 
and the tests were run inside a VirtualBox VM running 64bit Debian. The CPython
tests uses CPython from Conda, while the Pypy tests used a manually downloaded Pypy. Cffi version 1.10.0 and Cython 0.25.2.

Since Cymunk doesnt have a proper release I used the latest master from its 
Github repository, hash 24845cc retrieved on 2017-09-16.

Get:
^^^^

===============  =============  ========
..               CPython 3.5.3  Pypy 5.8
===============  =============  ========
Pymunk 5.3       2.14s          0.33s
Cymunk 20170916  0.41s          (10.0s)
===============  =============  ========

Collision-Callback:
^^^^^^^^^^^^^^^^^^^

===============  =============  ========
..               CPython 3.5.3  Pypy 5.8
===============  =============  ========
Pymunk 5.3       3.71s          0.58s
Pymunk 20170916  0.95s          (7.01s)
===============  =============  ========

(Cymunk results on Pypy within parentheses since Cython is well known to be 
slow on Pypy)

What we can see from these results is that Cymunk on CPython is much faster 
than Pymunk on CPython, but Pymunk takes the overall victory when we include 
Pypy. 

Something we did not take into account is that you can trade convenience for 
performance and use Cython in the application code as well to speed things up. I 
think this is the approach used in KivEnt which is the primary user of Cymunk. 
However, that requires a much more complicated setup when you develop your 
application because of the compiler requirements and code changes.
