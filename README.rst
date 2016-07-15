About
-----

Pymunk is a easy-to-use pythonic 2d physics library that can be used whenever 
you need 2d rigid body physics from Python. It is built on top of the very 
capable 2d physics library Chipmunk.

2007 - 2016, Victor Blomqvist - vb@viblo.se, MIT License

This release is based on the latest Pymunk release (5.0.0), 
using Chipmunk 7.0 rev d7603e3927 (source included)

:Homepage: http://www.pymunk.org
:Forum: http://chipmunk-physics.net/forum/
:Email: vb@viblo.se

:Getting the latest source:
    git clone https://github.com/viblo/pymunk.git

:Chipmunk: http://chipmunk-physics.net/


Installation
------------

In the normal case pymunk can be installed with pip::

    > pip install pymunk

It has one (or two) dependencies. CFFI and if not on Windows or OSX you also 
need a working gcc compiler.


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

    while True:                 # Infinite loop simulation
        space.step(0.02)        # Step the simulation one step forward
    
For more detailed and advanced examples, take a look at the included demos 
(in examples/).


Documentation
-------------

The source distribution of Pymunk ships with a number of demos in the examples
directory, and it also contains the full documentaiton including API reference.

You can also find the full documentation including examples and API reference 
on the pymunk homepage, http://www.pymunk.org


Dependencies / Requirements
---------------------------

Basically Pymunk have been made to be as easy to install and distribute as 
possible, usually `pip install` will take care of everything for you.

- Python (Runs on CPython 2.7 and 3.X. Pypy and Pypy3)
- Chipmunk (Source included, and on Windows and OSX its already compiled)
- CFFI (will be installed automatically by Pip)
- Setuptools (should be included with Pip)

* GCC and friends (optional, you need it to compile Chipmunk)
* Pygame (optional, you need it to run the Pygame based demos)
* Pyglet (optional, you need it to run the Pyglet based demos)
* Matplotlib & Jupyter Notebook (optional, you need it to run the Matplotlib 
  based demos)
* Sphinx (optional, you need it to build documentation)


Chipmunk
--------

Pymunk is built on top of the c library Chipmunk. It uses CFFI to interface
with the Chipmunk library file. Because of this Chipmunk has to be compiled
before it can be used with Pymunk. Compilation has to be done with GCC or 
another compiler that uses the same flags. 

The source distribution does not include a precompiled Chipmunk library file, 
instead you need to build it yourself. 

There are basically two options, either building it automatically as part of 
installation using for example Pip::

    > pip install pymunk-source-dist.zip

Or if you have the source unpacked / you got pymunk by cloning its git repo, 
you can explicitly tell pymunk to compile it inplace::    

    > python setup.py build_ext --inplace

Note that chipmunk is actually not built as a python extension, but distutils /
setuptools doesnt currently handle pure native libraries that needs to be built 
in a good way if built with build_clib.

The compiled file goes into the /pymunk folder (same as space.py, 
body.py and others).
