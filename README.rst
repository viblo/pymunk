Pymunk
======

.. image::  https://raw.githubusercontent.com/viblo/pymunk/master/docs/src/_static/pymunk_logo_animation.gif

Pymunk is a easy-to-use pythonic 2d physics library that can be used whenever 
you need 2d rigid body physics from Python. Perfect when you need 2d physics 
in your game, demo or other application! It is built on top of the very 
capable 2d physics library `Chipmunk <http://chipmunk-physics.net>`_.

The first version was released in 2007 and Pymunk is still actively developed 
and maintained today, more than 10 years of active development!

Pymunk has been used with success in many projects, big and small. For example: 
3 Pyweek game competition winners, more than a dozen published scientific 
papers and even in a self-driving car simulation! See the Showcases section on 
the Pymunk webpage for some examples.

2007 - 2020, Victor Blomqvist - vb@viblo.se, MIT License

This release is based on the latest Pymunk release (6.0.0.dev1), 
using Chipmunk 7 rev 080c51480f018040b567e8f0440b121ae3acbae4 .


Installation
------------

In the normal case pymunk can be installed from PyPI with pip::

    > pip install pymunk

It has one direct dependency, CFFI.

Pymunk can also be installed with conda, from the conda-forge channel::

    > conda install -c conda-forge pymunk


Example
-------

Quick code example::
    
    import pymunk               # Import pymunk..

    space = pymunk.Space()      # Create a Space which contain the simulation
    space.gravity = 0,-1000     # Set its gravity

    body = pymunk.Body(1,1666)  # Create a Body with mass and moment
    body.position = 50,100      # Set the position of the body

    poly = pymunk.Poly.create_box(body) # Create a box shape and attach to body
    space.add(body, poly)       # Add both body and shape to the simulation

    print_options = pymunk.SpaceDebugDrawOptions() # For easy printing

    while True:                 # Infinite loop simulation
        space.step(0.02)        # Step the simulation one step forward
        space.debug_draw(print_options) # Print the state of the simulation
    
For more detailed and advanced examples, take a look at the included demos 
(in examples/).

Examples are not included if you install with `pip install pymunk`. Instead you
need to download the source archive (pymunk-x.y.z.zip). Download available from 
https://pypi.org/project/pymunk/#files


Documentation
-------------

The source distribution of Pymunk ships with a number of demos of different 
simulations in the examples directory, and it also contains the full 
documentation including API reference.

You can also find the full documentation including examples and API reference 
on the Pymunk homepage, http://www.pymunk.org


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
    Please use the issue tracker at github to report any issues you find:
    https://github.com/viblo/pymunk/issues
    
Regardless of the method you use I will try to answer your questions as soon 
as I see them. (And if you ask on SO other people might help as well!)


Dependencies / Requirements
---------------------------

Basically Pymunk have been made to be as easy to install and distribute as 
possible, usually `pip install` will take care of everything for you.

- Python (Runs on CPython 3.6 and later and Pypy3)
- Chipmunk (Compiled library already included on common platforms)
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


Install from source / Chipmunk Compilation
------------------------------------------

This section is only required in case you do not install pymunk from the 
prebuild binary wheels (normally if you do not use `pip install` or you are 
on a uncommon platform).

Pymunk is built on top of the c library Chipmunk. It uses CFFI to interface
with the Chipmunk library file. Because of this Chipmunk has to be compiled
together with Pymunk as an extension module. 

There are basically two options, either building it automatically as part of 
installation using for example Pip::

    > pip install pymunk-source-dist.zip

Or if you have the source unpacked / you got Pymunk by cloning its git repo, 
you can explicitly tell Pymunk to compile it inplace::    

    > python setup.py build_ext --inplace
