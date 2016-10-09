******
Pymunk
******

Pymunk is a easy-to-use pythonic 2d physics library that can be used whenever 
you need 2d rigid body physics from Python. Perfect when you need 2d physics 
in your game, demo or other application! It is built on top of the very 
capable 2d physics library `Chipmunk <http://chipmunk-physics.net>`_.

The first version was released in 2007 and Pymunk is still actively developed 
and maintained today. 

Pymunk has been used with success in many projects, big and small. For example: 
2 Pyweek game competition winners, more than 10 published scientific papers 
and even in a self-driving car simulation! See :doc:`showcase` for some 
examples.

Getting Started
===============

To get started quickly take a look in the :doc:`readme`, it contains a 
summary of the most important things and is quick to read. When done its a 
good idea to take a look at the included :doc:`examples`, read the 
:doc:`tutorials` and take a look in the :doc:`pymunk`.


The Pymunk Vision
=================

    "*Make 2d physics easy to include in your game*"

It is (or is striving to be):

* **Easy to use** - It should be easy to use, no complicated stuff should be 
  needed to add physics to your game/program.
* **"Pythonic"** - It should not be visible that a c-library (chipmunk) is in 
  the bottom, it should feel like a Python library (no strange naming, OO, 
  no memory handling and more)
* **Simple to build & install** - You shouldn't need to have a zillion of 
  libraries installed to make it install, or do a lot of command line tricks.
* **Multi-platform** - Should work on both Windows, \*nix and OSX.
* **Non-intrusive** - It should not put restrictions on how you structure 
  your program and not force you to use a special game loop, it should be 
  possible to use with other libraries like Pygame and Pyglet. 


Python 2 & Python 3
===================

Pymunk has been tested and runs fine on both Python 2 and Python 3. It has 
been tested on recent versions of CPython (2 and 3) and Pypy. For an exact 
list of tested versions see the Travis and Appveyor test configs.
  
  
Contact & Support
=================
.. _contact-support:

**Stackoverflow**
    You can ask questions/browse old ones at stackoverflow, just look for 
    the pymunk tag. http://stackoverflow.com/questions/tagged/pymunk

**Forum**
    Currently pymunk has no separate forum, but uses the general Chipmunk 
    forum at http://chipmunk-physics.net/forum/index.php Many issues 
    are the same, like how to create a rag doll or why a fast moving object 
    pass through a wall. If you have a Pymunk specific question feel free to 
    mark your post with [pymunk] to make it stand out a bit.

**E-Mail**
    You can email me directly at vb@viblo.se

**Issue Tracker**
    Please use the issue tracker at github to report any issues you find:
    https://github.com/viblo/pymunk/issues
    
Regardless of the method you use I will try to answer your questions as soon 
as I see them. (And if you ask on SO or the forum other people might help as 
well!)
    
.. attention::
    If you like pymunk and find it useful and have a few minutes to spare I 
    would love to hear from you. What would *really* be nice is a real 
    postcard from the place where you are! :) 
    
    Pymunk's address is:
        | Pymunk c/o Victor Blomqvist
        | Carl Thunbergs Vag 9
        | 169 69 Solna
        | SWEDEN
        
Contents
========
 
.. toctree::
    :maxdepth: 4
    
    readme
    news
    installation
    pymunk
    examples
    showcase
    tutorials
    benchmarks
    advanced
    Issue Tracker <https://github.com/viblo/pymunk/issues>
    Source Repository <https://github.com/viblo/pymunk>
    Downloads <https://pypi.python.org/pypi/pymunk/>
    license

Indices and tables
==================
 
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`