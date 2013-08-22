About
-----

pymunk is a easy-to-use pythonic 2d physics library that can be used whenever 
you need 2d rigid body physics from Python. It is built on top of the very 
nice 2d physics library Chipmunk.

2007 - 2013, Victor Blomqvist - vb@viblo.se, MIT License

This release is based on the latest pymunk release (4.0.0), 
using chipmunk 6.2 rev 3bdf1b7b3c (source included)

:Homepage: http://www.pymunk.org
:Forum: http://chipmunk-physics.net/forum/
:Email: vb@viblo.se

:Getting the latest SVN copy:
    svn checkout http://pymunk.googlecode.com/svn/trunk pymunk-read-only

:Chipmunk: http://chipmunk-physics.net/


How to Use
----------

pymunk ships with a number of demos in the examples directory, and its  
complete documentation including API Reference.  

If chipmunk doesnt ship with a chipmunk binary your platform can understand
(currently Windows and Linux 32bit and 64 bit are included) you will have to 
compile chipmunk before install. See section CHIPMUNK in this readme for 
(very simple) instructions.

To install you can either run::
    
    > python setup.py install

or simply put the pymunk folder where your program/game can find it.
(like /my_python_scripts/yourgame/pymunk). The chipmunk binary library
is located in the pymunk folder.

The easy way to get started is to check out the examples/ directory,
and run 'run.py python arrows.py' and so on, and see what each one does :)


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


Dependencies / Requirements
---------------------------

- python (tested on cpython 2.6, 2.7 and 3.2, 3.3. Also on pypy 2.1)
- chipmunk (pymunk ships with a set of chipmunk libraries)

* pygame (optional, you need it to run most of the demos)
* pyglet (optional, you need it to run the moon buggy demo)
* sphinx (optional, you need it to build documentation)
* ctypeslib & GCC_XML (optional, you need them to generate new bindings)


Chipmunk
--------

Compiled libraries of Chipmunk compatible Windows and Linux 32bit and 64bit 
are distributed with pymunk.
If pymunk doesnt have your particular platform included, you can compile 
Chipmunk by hand with a custom setup argument::

    > python setup.py build_chipmunk

The compiled file goes into the /pymunk folder (same as _chipmunk.py, 
util.py and others). If the compile fail, please check the readme in 
chipmunk_src for generic instructions on how to compile with gcc, 
or download the relevant release from Chipmunk homepage and follow its
instructions.
