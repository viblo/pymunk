********
Overview
********

There are 4 basic classes you will use in Pymunk.

**Rigid Bodies** (:py:class:`pymunk.Body`)
    A rigid body holds the physical properties of an object. (mass, position, 
    rotation, velocity, etc.) It does not have a shape by itself. If you've 
    done physics with particles before, rigid bodies differ mostly in that they 
    are able to rotate. Rigid bodies generally tend to have a 1:1 correlation 
    to sprites in a game. You should structure your game so that you use the 
    position and rotation of the rigid body for drawing your sprite.

**Collision Shapes** (:py:class:`pymunk.Circle`, :py:class:`pymunk.Segment` and :py:class:`pymunk.Poly`)
    By attaching shapes to bodies, you can define the a body's shape. You can 
    attach many shapes to a single body to define a complex shape, or none if 
    it doesn't require a shape.

**Constraints/Joints** (:py:class:`pymunk.constraint.PinJoint`, :py:class:`pymunk.constraint.SimpleMotor` and many others)
    You can attach joints between two bodies to constrain their behavior.

**Spaces** (:py:class:`pymunk.Space`)
    Spaces are the basic simulation unit in Pymunk. You add bodies, shapes 
    and joints to a space, and then update the space as a whole. They control 
    how all the rigid bodies, shapes, and constraints interact together.

As a complement it can be good to read the Chipmunk docs 
<http://chipmunk-physics.net/release/ChipmunkLatest-Docs/>. Its made for 
Chipmunk, but Pymunk is build on top of Chipmunk and share most of the concepts,
with the main difference being that Pymunk is used from Python while Chipmunk is 
a C-library.


Model your physics objects
==========================

Object shape
------------

What you see on the screen doesn't necessarily have to be exactly the same 
shape as the actual physics object. Usually the shape used for collision 
detection (and other physics simulation) is much simplified version of what is 
drawn on the screen. Even high end AAA games separate the collision shape from 
what is drawn on screen.

There are a number of reasons why its good to separate the collision shape and 
what is drawn.

* Using simpler collision shapes are faster. So if you have a very complicated 
  object, for example a pine tree, maybe it can make sense to simplify its 
  collision shape to a triangle for performance.
* Using a simpler collision shape make the simulation better. Lets say you have 
  a floor made of stone with a small crack in the middle. If you drag a box 
  over this floor it will get stuck on the crack. But if you simplify the floor 
  to just a plane you avoid having to worry about stuff getting stuck in the 
  crack.
* Making the collision shape smaller (or bigger) than the actual object makes 
  gameplay better. Lets say you have a player controlled ship in a shoot-em-up 
  type game. Many times it will feel more fun to play if you make the collision 
  shape a little bit smaller compared to what it should be based on how it 
  looks.

You can see an example of this in the :ref:`using_sprites.py` example included 
in Pymunk. There the physics shape is a triangle, but what is drawn is 3 boxes 
in a pyramid with a snake on top. Another example is in the 
:ref:`platformer.py` example, where the player is drawn as a girl in red and 
gray. However the physics shape is just a couple of circle shapes on top of 
each other.


Mass, weight and units
----------------------

Sometimes users of Pymunk can be confused as to what unit everything is defined 
in. For example, is the mass of a Body in gram of kilogram? Pymunk is unit-less
and does not care which unit you use. If you pass in seconds to a function 
expecting time, then your time unit is seconds. If you pass in pixels to 
functions that expect a distance, then your unit of distance is pixels. 

Then derived units are just a combination of the above. So in the case with 
seconds and pixels the unit of velocity would be pixels / second.

(This is in contrast to some other physics engines which can have fixed units 
that you should use)


Looks before realism
--------------------

How heavy is a bird in angry birds? It doest matter, its a cartoon!

Together with the units another key insight when setting up your simulation is 
to remember that it is a simulation, and in many cases the look and feel is 
much more important than actual realism. So for example, if you want to model 
a flipper game, the real power of the flipper and launchers doesn't matter at 
all, what is important is that the game feels "right" and is fun to use for 
your users. 

Sometimes it make sense to start out with realistic units, to give you a feel 
for how big mass should be in comparison to gravity for example. 

There are exceptions to this of course, when you actually want realism over the 
looks. In the end it is up to you as a user of Pymunk to decide. 


Copy and Load/Save Pymunk objects
=================================

Most Pymunk objects can be copied and/or saved with pickle from the standard 
library. Since the implementation is generic it will also work to use other 
serializer libraries such as `jsonpickle <https://jsonpickle.github.io/>`_ (in 
contrast to pickle the jsonpickle serializes to/from json) as long as they make 
use of the pickle infrastructure.

See the :ref:`copy_and_pickle.py` example for an example on how to save, load 
and copy Pymunk objects.
