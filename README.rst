Pymunk
======

.. image::  https://raw.githubusercontent.com/viblo/pymunk/master/docs/src/_static/pymunk_logo_animation.gif

Pymunk is an easy-to-use pythonic 2d physics library that can be used whenever 
you need 2d rigid body physics from Python. Perfect when you need 2d physics 
in your game, demo or simulation! It is built on top of the very 
capable 2d physics library `Chipmunk <http://chipmunk-physics.net>`_.

The first version was released in 2007 and Pymunk is still actively developed 
and maintained today, more than 15 years of active development!

Pymunk has been used with success in many projects, big and small. For example: 
3 Pyweek game competition winners, dozens of published scientific 
papers and even in a self-driving car simulation! See the Showcases section on 
the Pymunk webpage for some examples.

2007 - 2023, Victor Blomqvist - vb@viblo.se, MIT License

This release is based on the latest Pymunk release (6.4.0), 
using Chipmunk 7 rev 5dd7d774053145fa37f352d7a07d2f75a9bd8039 .


Installation
------------

In the normal case pymunk can be installed from PyPI with pip::

    > pip install pymunk

It has one direct dependency, CFFI.

Pymunk can also be installed with conda, from the conda-forge channel::

    > conda install -c conda-forge pymunk

For more detailed installation instructions, please see the complete Pymunk 
documentation.

Example
-------

Quick code example::
    
    import pymunk               # Import pymunk..

    space = pymunk.Space()      # Create a Space which contain the simulation
    space.gravity = 0,-981      # Set its gravity

    body = pymunk.Body()        # Create a Body
    body.position = 50,100      # Set the position of the body

    poly = pymunk.Poly.create_box(body) # Create a box shape and attach to body
    poly.mass = 10              # Set the mass on the shape
    space.add(body, poly)       # Add both body and shape to the simulation

    print_options = pymunk.SpaceDebugDrawOptions() # For easy printing 

    for _ in range(100):        # Run simulation 100 steps in total
        space.step(0.02)        # Step the simulation one step forward
        space.debug_draw(print_options) # Print the state of the simulation

This will print (to console) the state of the simulation. For more visual, 
detailed and advanced examples, take a look at the included demos.  
They are included in the pymunk install, in the pymunk.examples subpackage. 
They can be run directly. To list the examples::

    > python -m pymunk.examples -l

And to run one of them::

    > python -m pymunk.examples.breakout


Contact & Support
-----------------
.. _contact-support:

**Homepage**
    http://www.pymunk.org/

**Stackoverflow**
    You can ask questions/browse old ones at Stackoverflow, just look for 
    the Pymunk tag. http://stackoverflow.com/questions/tagged/pymunk

**E-Mail**
    You can email me directly at vb@viblo.se

**Issue Tracker**
    Please use the issue tracker at github to report any issues you find. This 
    is also the place for feature requests:
    https://github.com/viblo/pymunk/issues
    
Regardless of the method you use I will try to answer your questions as soon 
as I see them. (And if you ask on SO other people might help as well!)


Documentation
-------------

The full documentation including API reference, showcase of usages and 
screenshots of examples is available on the Pymunk homepage, 
http://www.pymunk.org


The Pymunk Vision
-----------------

    "*Make 2d physics easy to include in your game*"

It is (or is striving to be):

* **Easy to use** - It should be easy to use, no complicated code should be 
  needed to add physics to your game or program.
* **"Pythonic"** - It should not be visible that a c-library (Chipmunk) is in 
  the bottom, it should feel like a Python library (no strange naming, OO, 
  no memory handling and more)
* **Simple to build & install** - You shouldn't need to have a zillion of 
  libraries installed to make it install, or do a lot of command line tricks.
* **Multi-platform** - Should work on both Windows, \*nix and OSX.
* **Non-intrusive** - It should not put restrictions on how you structure 
  your program and not force you to use a special game loop, it should be 
  possible to use with other libraries like Pygame and Pyglet. 

  
Dependencies / Requirements
---------------------------

Basically Pymunk have been made to be as easy to install and distribute as 
possible, usually `pip install` will take care of everything for you.

- Python (Runs on CPython 3.6 and later and Pypy3)
- Chipmunk (Prebuilt and included when using binary wheels)
- CFFI (will be installed automatically by Pip)
- Setuptools (should be included with Pip)

* GCC and friends (optional, you need it to compile Pymunk from source. On 
  windows Visual Studio is required to compile)
* Pygame (optional, you need it to run the Pygame based demos)
* Pyglet (optional, you need it to run the Pyglet based demos)
* Matplotlib & Jupyter Notebook (optional, you need it to run the Matplotlib 
  based demos)
* Sphinx & aafigure & sphinx_autodoc_typehints (optional, you need it to build 
  documentation)


Python 2 Support
----------------

Support for Python 2 (and Python 3.0 - 3.5) has been dropped with Pymunk 6.0. 
If you use these legacy versions of Python, please use Pymunk 5.x.
