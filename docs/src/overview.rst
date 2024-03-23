********
Overview
********

Basics
======

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
    You can attach constraints between two bodies to constrain their behavior, 
    for example to keep a fixed distance between two bodies.

**Spaces** (:py:class:`pymunk.Space`)
    Spaces are the basic simulation unit in Pymunk. You add bodies, shapes 
    and constraints to a space, and then update the space as a whole. They 
    control how all the rigid bodies, shapes, and constraints interact together.

The actual simulation is done by the Space. After adding the objects that 
should be simulated to the Space time is moved forward in small steps with the
:py:meth:`pymunk.Space.step` function. 


Model your physics objects
==========================

Object shape
------------

What you see on the screen doesn't necessarily have to be exactly the same 
shape as the actual physics object. Usually the shape used for collision 
detection (and other physics simulation) is much simplified version of what is 
drawn on the screen. Even high-end AAA games separate the collision shape from 
what is drawn on screen.

There are a number of reasons why it's good to separate the collision shape and 
what is drawn.

* Using simpler collision shapes are faster. So if you have a very complicated 
  object, for example a pine tree, maybe it can make sense to simplify its 
  collision shape to a triangle for performance.
* Using a simpler collision shape make the simulation better. Let's say you have 
  a floor made of stone with a small crack in the middle. If you drag a box 
  over this floor it will get stuck on the crack. But if you simplify the floor 
  to just a plane you avoid having to worry about stuff getting stuck in the 
  crack.
* Making the collision shape smaller (or bigger) than the actual object makes 
  gameplay better. Let's say you have a player controlled ship in a shoot-em-up 
  type game. Many times it will feel more fun to play if you make the collision 
  shape a little smaller compared to what it should be based on how it 
  looks.

You can see an example of this in the :ref:`using_sprites.py` example included 
in Pymunk. There the physics shape is a triangle, but what is drawn is 3 boxes 
in a pyramid with a snake on top. Another example is in the 
:ref:`platformer.py` example, where the player is drawn as a girl in red and 
gray. However, the physics shape is just a couple of circle shapes on top of 
each other.

Center of gravity
-----------------

An important part of creating the shape of an object is to ensure its center 
of gravity is where it should. In most cases you want it to be in the center 
of the shape(s), but just like in real life it can create interesting objects
if the center of gravity is not in the actual center.

Below is a couple of examples how the center easily ends up in one corner of 
the shape:

.. aafig::

  Poly(b, [(0,0),(5,0),(5,5),(0,5)])| Segment(b, (0,0), (6,6))
                                    |
      (0,5)      (5,5)              |        (6,6)
        +--------+                  |        / 
        |        |                  |       / 
        |        |                  |      /
        |        |                  |     / 
        |        |                  |    / 
   (0,0)|        |(5,0)             |   /
        +--------+                  |  /(0,0)  
        ^                           |  ^
        |                           |  | 
        Center of gravity           |  Center of gravity

Note however that a Circle is created at the center automatically, and that 
a box created by the helper :py:meth:`pymunk.Poly.create_box` will also have 
its center of gravity in the middle.

.. aafig::

  "Poly.create_box(b, size=(6,6))"
  
  "(-3, 3)"
    +---------+(3,3)
    |         |
    |         |
    |    o<------ Center of gravity at (0,0)
    |         |
    |         |
    +---------+"(-3,3)"
  "(-3,-3)"
    

The center of gravity can be moved in a couple of different ways:

- ``Segment(body, (0,0), (6,6))`` can be changed to 
  ``Segment(body, (-3,-3), (-3,-3))``.
- The center of gravity can be adjusted directly on the body: 
  ``body.center_of_gravity = (3,3)``
- Poly shapes can be transformed with a :class:`pymunk.Transform`. 
  ``Poly(body, [...], pymunk.Transform.translation(3,3)``

Mass, weight and units
----------------------

Sometimes users of Pymunk can be confused as to what unit everything is 
defined in. For example, is the mass of a Body in grams or kilograms? Pymunk 
is unit-less and does not care which unit you use. If you pass in seconds to 
a function expecting time, then your time unit is seconds. If you pass in 
pixels to functions that expect a distance, then your unit of distance is pixels. 

Then derived units are just a combination of the above. So in the case with 
seconds and pixels the unit of velocity would be pixels / second.

(This is in contrast to some other physics engines which can have fixed units 
that you should use)


Looks before realism
--------------------

How heavy is a bird in angry birds? It doesn't matter, it's a cartoon!

Together with the units another key insight when setting up your simulation is 
to remember that it is a simulation, and in many cases the look and feel is 
much more important than actual realism. So for example, if you want to model 
a flipper game, the real power of the flipper and launchers doesn't matter at 
all, what is important is that the game feels "right" and is fun to use for 
your users. 

Sometimes it makes sense to start out with realistic units, to give you a feel 
for how big mass should be in comparison to gravity for example. 

There are exceptions to this of course, when you actually want realism over the 
looks. In the end it is up to you as a user of Pymunk to decide. 


Game loop / moving time forward
===============================

The most important part in your game loop is to keep the dt argument to the 
:py:meth:`pymunk.Space.step` function constant. A constant time step makes the 
simulation much more stable and reliable.

There are several ways to do this, some more complicated than others. Which one 
is best for a particular program depends on the requirements.

Some good articles:

* http://gameprogrammingpatterns.com/game-loop.html
* http://gafferongames.com/game-physics/fix-your-timestep/
* http://www.koonsolo.com/news/dewitters-gameloop/


Object tunneling
================

Sometimes an object can pass through another object even though it's not 
supposed to. Usually this happens because the object is moving so fast, that 
during a single call to space.step() the object moves from one side to the 
other.

.. aafig::

      step 1    |  step 2     |  step 3
                |             |
          ++    |    ++       |   ++ 
          ||    |    ||       |   ||
      XX  ||    |    ||  XX   |   ||      XX
      XX  ||    |    ||  XX   |   ||      XX
      v-> ||    |    ||  v->  |   ||      v->
          ||    |    ||       |   ||


There are several ways to mitigate this problem. Sometimes it might be a good 
idea to do more than one of these.

* Make sure the velocity of objects never get too high. One way to do that is 
  to use a custom velocity function with a limit built in on the bodies that 
  have a tendency to move too fast::

    def limit_velocity(body, gravity, damping, dt):
        max_velocity = 1000
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale

    body_to_limit.velocity_func = limit_velocity

  Depending on the requirements it might make more sense to clamp the velocity 
  over multiple frames instead. Then the limit function could look like this 
  instead::

    def limit_velocity(body, gravity, damping, dt):
        max_velocity = 1000
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        if body.velocity.length > max_velocity:
            body.velocity = body.velocity * 0.99


* For objects such as bullets, use a space query such as 
  space.segment_query or space.segment_first.

* Use a smaller value for dt in the call to space.step. A simple way is to call 
  space.step multiple times each frame in your application. This will also help 
  to make the overall simulation more stable.

* Double check that the center of gravity is at a reasonable point for all 
  objects.


Unstable simulation? 
====================

Sometimes the simulation might not behave as expected. In extreme cases it can 
"blow up" and parts move anywhere without logic. 

There are a number of things to try if this happens:

* Make all the bodies of similar mass. It is easier for the physics engine to 
  handle bodies with similar weight.

* Don't let two objects with infinite mass touch each other.

* Make the center of gravity in the middle of shapes instead of at the edge.

* Very thin shapes can behave strange, try to make them a little wider.

* Have a fixed time step (see the other sections of this guide).

* Call the Space.step function several times with smaller dt instead of only 
  one time but with a bigger dt. (See the docs of `Space.step`)

* If you use a Motor joint, make sure to set its max force. Otherwise, its power
  will be near infinite.  

* Double check that the center of gravity is at a reasonable point for all 
  objects.

(Most of these suggestions are the same for most physics engines, not just 
Pymunk.)


Performance
===========

Various tips that can improve performance:

* Run Python with optimizations on (will disable various useful but 
  non-critical asserts). ``python -O mycode.py``
* If possible use Pypy instead of CPython. See 
  :ref:`Benchmarks <benchmark>` for some examples of the speed difference.
* Tweak the ``Space.iterations`` property.
* If possible let objects fall asleep with ``Space.sleep_time_threshold``.
* Reduce usage of callback methods (like collision callbacks or custom update 
  functions). These are much slower than the default built in code.

Note that many times the actual simulation is quick enough, but reading out 
the result after each step and manipulating the objects manually can have a 
significant overhead and performance cost.


Copy and Load/Save Pymunk objects
=================================

Most Pymunk objects can be copied and/or saved with pickle from the standard 
library. Since the implementation is generic it will also work to use other 
serializer libraries such as `jsonpickle <https://jsonpickle.github.io/>`_ (in 
contrast to pickle the jsonpickle serializes to/from json) as long as they make 
use of the pickle infrastructure.

See the :ref:`copy_and_pickle.py` example for an example on how to save, load 
and copy Pymunk objects.

Note that the version of Pymunk used must be the same for the code saving as 
the version used when loading the saved object.


Additional info
===============

As a complement to the Pymunk docs it can be good to read the `Chipmunk docs 
<http://chipmunk-physics.net/release/ChipmunkLatest-Docs/>`_. It's made for 
Chipmunk, but Pymunk is build on top of Chipmunk and share most of the concepts,
with the main difference being that Pymunk is used from Python while Chipmunk is 
a C-library.

For the backstory of why Pymunk exists there's a short post about the 
background and history including a screenshot of the first game made with 
Pymunk on my own website, at https://www.viblo.se/projects/pymunk/ 