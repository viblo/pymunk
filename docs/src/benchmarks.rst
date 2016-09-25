Benchmarks
==========

To get a grip of the actual performance of Pymunk this page contains a number
of benchmarks.  

The full code of all benchmarks are available under the `benchmarks` folder.

Micro benchmarks
----------------

In order to measure the overhead created by Pymunk in the most common cases I 
have created two micro bechmarks. They should show the speed of the actual 
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

Pymunk-Get:
+++++++++++

==========  ==============  =============  ==========
..          CPython 2.7.12  CPython 3.5.2  Pypy 5.4.1
==========  ==============  =============  ==========
Pymunk 5.0  4.3s            4.5s           0.37s
Pymunk 4.0  1.0s            0.9s           0.52s
==========  ==============  =============  ==========

Pymunk-Callback:
++++++++++++++++

==========  ==============  =============  ==========
..          CPython 2.7.12  CPython 3.5.2  Pypy 5.4.1
==========  ==============  =============  ==========
Pymunk 5.0  6.5s            7.3s           1.0s
Pymunk 4.0  5.1s            6.5s           4.5s
==========  ==============  =============  ==========

What we can see from these results is that you should use Pypy if you have the 
possibility since that is much faster than regular CPython. We can also see 
that moving from Ctypes to Cffi between Pymunk 4 and 5 had a negative impact in 
CPython, but positive impact on Pypy, and Pymunk 5 together with Pypy is with a 
big margin the fastest option. 
