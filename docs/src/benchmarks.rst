Benchmarks
==========
.. _benchmark:

To get a grip of the actual performance of Pymunk this page contains a number
of benchmarks.  

The full code of all benchmarks are available under the `benchmarks
<https://github.com/viblo/pymunk/blob/master/benchmarks>`_ folder.

Note that the the benchmarks are not yet updated for Pymunk 6.0, but tests 
look promising.

Get and Callbacks
-----------------

In order to measure the overhead created by Pymunk in the most common cases I 
have created two micro benchmarks. They should show the speed of the actual 
wrapping code, which can tell how big overhead Pymunk creates, and how big 
difference different wrapping methods does.

The most common thing a typical program using Pymunk does is to read out the 
position and angle from a Pymunk object. Usually this is done each frame for 
every object in the simulation, so this is an important factor in how fast 
something will be.

Given this our first test is::

    t += b.position.x + b.position.y + b.angle

(see `pymunk-get.py`)

Running it is simple, for example like this for Pymunk 4.0::

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

Tests run on an HP G1 1040 laptop with a Intel i7-4600U. Laptop runs Windows, 
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


Batch API 
---------

Pymunk 6.6.0 introduces a new experimental batch API to retrieve body and 
collision data efficiently in batches optimized to be processed further 
efficiently, for example with NumPy.

In order to test this there's a new benchmark which compares fetching position 
and angle (data that almost every user of the batch API will use) normally and 
with the new API. The benchmark runs with different amount of bodies, and 
scales number of iterations to complete in reasonable time. 

(see `pymunk-batch-api.py`)

The benchmark were run using an internal pre-release of Pymunk 6.6.0 running 
on Windows using CPython 3.11 and Pypy 3.10-v7.3.12 on a ThinkPad X1 Carbon 7 
gen.

Results:
########

Below we can see that using the Batch API is faster already at 5 bodies in a 
space, and it handles high amounts of bodies about 40x faster than the normal
non-batch API if you use CPython. With Pypy the improvements are much more 
modest.

======  ==========  =========  ===========  ==========
Bodies  Normal API  Batch API  Normal Pypy  Batch Pypy
======  ==========  =========  ===========  ==========
1       2.2s        4.2s       0.4s         0.5s
5       2.0s        0.8s       0.3s         0.3s
10      2.1s        0.4s       0.3s         0.2s
100     2.2s        0.09s      0.3s         0.2s
1000    2.3s        0.05s      0.3s         0.2s
10000   n/a         0.04s      n/a          0.2s
50000   n/a         0.06s      n/a          0.2s
100000  n/a         0.07s      n/a          0.2s
======  ==========  =========  ===========  ==========

The resulting times are the time to get the position and angle data 1000000 
times divided by the number of bodies.

From this we can see that if there's only 1 body, then using the normal API
is twice as fast as the batch API if CPython is used. However, already at 5 
bodies the Batch API is (more than) twice as fast as the normal API. This was 
better than expected, and shows the potential. 

For higher amounts of bodies its clear that the runtime for normal API scales 
more or less linearly, which means that the overhead to get a single body is 
constant regardless of number of bodies. For the batch API, we can see that 
there's a high overhead from the batch, and its first when we reach about 
1000 bodies that it starts to scale like the normal API with a more or less 
constant overhead per body. We can also see that there's a slight increase in 
per body times, maybe because of the bigger array needed to collect the 
results, or some other overhead within Chipmunk. 

On the other hand, for Pypy the result is much less exciting. Pypy using the 
normal API is already very fast, as shown by the `Pymunk-Get` benchmark, and 
using the batch API provides only a modest improvement. 


Compared to Other Physics Libraries
-----------------------------------

.. note:: 
    Cymunk (and also pybox2d) seems to be unmaintained at the present (2023).


Cymunk
######

`Cymunk <https://github.com/kivy/cymunk>`_ is an alternative wrapper around 
Chipmunk. In contrast to Pymunk it uses Cython for wrapping (Pymunk uses CFFI) 
which gives it a different performance profile. However, since both are built 
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

(see `pymunk-collision-callback.py` and  `cymunk-collision-callback.py`)

Results
+++++++

Tests run on a HP G1 1040 laptop with a Intel i7-4600U. Laptop runs Windows, 
and the tests were run inside a VirtualBox VM running 64bit Debian. The CPython
tests uses CPython from Conda, while the Pypy tests used a manually downloaded 
Pypy. Cffi version 1.10.0 and Cython 0.25.2.

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
Cymunk 20170916  0.95s          (7.01s)
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
