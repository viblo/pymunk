**********************************
Collision Handlers: Reacting to Physics
**********************************

This tutorial explains how to use collision handlers to react when shapes
collide in your simulation. You will learn how to detect collisions, customize
collision responses, and implement common game mechanics like one-way platforms
and object destruction.

This tutorial assumes you are familiar with the basics of Pymunk covered in the
:doc:`SlideAndPinJoint` tutorial.

.. image :: /_static/examples/breakout.png

What are Collision Handlers?
============================

By default, Pymunk handles all collisions automatically - shapes bounce off
each other based on their physical properties like elasticity and friction.
But what if you want to:

- Play a sound when two objects collide?
- Remove an object when it's hit (like a brick in Breakout)?
- Let the player jump through a platform from below but stand on it from above?
- Calculate damage based on collision force?

Collision handlers let you run custom code when shapes collide. You can use
them to detect collisions, modify how collisions are resolved, or even ignore
collisions entirely.

The Four Collision Phases
=========================

A collision goes through four phases, and you can set a callback for each:

**begin**
    Called once when two shapes first start touching. Return False from this
    callback to ignore the collision completely (the shapes will pass through
    each other).

**pre_solve**
    Called every frame while shapes are touching, before the collision
    response is calculated. You can modify collision properties like friction
    and elasticity here, or return False to ignore the collision for this frame.

**post_solve**
    Called every frame while shapes are touching, after the collision response
    has been calculated. Use this to get information about the collision like
    the impulse or energy - useful for damage calculations or sound effects.

**separate**
    Called once when two shapes stop touching.

.. note::
    Shapes marked as sensors (``shape.sensor = True``) don't generate physical
    collision responses, but their begin, pre_solve, and separate callbacks
    still fire. This is useful for trigger zones.

Setting Up Collision Types
==========================

Before you can handle collisions between specific shapes, you need to assign
them **collision types**. A collision type is just an integer that identifies
a category of shapes::

    # Define collision types as constants for clarity
    COLLISION_TYPE_BALL = 1
    COLLISION_TYPE_BRICK = 2
    COLLISION_TYPE_PLAYER = 3

    # Assign collision types to shapes
    ball_shape = pymunk.Circle(ball_body, 10)
    ball_shape.collision_type = COLLISION_TYPE_BALL

    brick_shape = pymunk.Poly.create_box(brick_body, (40, 20))
    brick_shape.collision_type = COLLISION_TYPE_BRICK

Registering a Collision Handler
===============================

Use ``space.on_collision()`` to register callbacks for when shapes with
specific collision types collide::

    def on_ball_hit_brick(arbiter, space, data):
        # Get the shapes involved in the collision
        ball_shape, brick_shape = arbiter.shapes

        # Remove the brick from the simulation
        space.remove(brick_shape, brick_shape.body)
        print("Brick destroyed!")

    space.on_collision(
        COLLISION_TYPE_BALL,
        COLLISION_TYPE_BRICK,
        begin=on_ball_hit_brick
    )

The callback receives three arguments:

- **arbiter**: Contains information about the collision (shapes, contact points,
  impulse, etc.)
- **space**: The Space where the collision occurred
- **data**: Optional data you can pass when registering the handler

Example 1: Destroying Bricks (Breakout-style)
=============================================

Let's build a simple example where balls destroy bricks on contact::

    import sys
    import pygame
    import pymunk
    import pymunk.pygame_util

    COLLISION_TYPE_BALL = 1
    COLLISION_TYPE_BRICK = 2

    def create_ball(space, position):
        body = pymunk.Body(1, float("inf"))  # infinite moment = won't rotate
        body.position = position
        shape = pymunk.Circle(body, 10)
        shape.elasticity = 1.0
        shape.collision_type = COLLISION_TYPE_BALL
        space.add(body, shape)
        return body

    def create_brick(space, position):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = position
        shape = pymunk.Poly.create_box(body, (60, 20))
        shape.elasticity = 1.0
        shape.collision_type = COLLISION_TYPE_BRICK
        space.add(body, shape)

    def remove_brick(arbiter, space, data):
        """Called when a ball hits a brick."""
        brick_shape = arbiter.shapes[1]  # Second shape is the brick
        space.remove(brick_shape, brick_shape.body)
        data["score"] += 10

    def main():
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        clock = pygame.time.Clock()

        space = pymunk.Space()
        space.gravity = (0, 0)  # No gravity for this example
        draw_options = pymunk.pygame_util.DrawOptions(screen)

        # Create walls
        walls = [
            pymunk.Segment(space.static_body, (10, 10), (590, 10), 5),
            pymunk.Segment(space.static_body, (10, 10), (10, 390), 5),
            pymunk.Segment(space.static_body, (10, 390), (590, 390), 5),
            pymunk.Segment(space.static_body, (590, 10), (590, 390), 5),
        ]
        for wall in walls:
            wall.elasticity = 1.0
        space.add(*walls)

        # Create bricks
        for row in range(3):
            for col in range(8):
                create_brick(space, (80 + col * 70, 100 + row * 30))

        # Create ball with initial velocity
        ball = create_ball(space, (300, 300))
        ball.velocity = (200, -200)

        # Register collision handler with data for score tracking
        game_data = {"score": 0}
        space.on_collision(
            COLLISION_TYPE_BALL,
            COLLISION_TYPE_BRICK,
            separate=remove_brick,  # Use separate to remove after collision resolves
            data=game_data
        )

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill((40, 40, 40))
            space.debug_draw(draw_options)

            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {game_data['score']}", True, (255, 255, 255))
            screen.blit(text, (10, 10))

            space.step(1/60.0)
            pygame.display.flip()
            clock.tick(60)

    if __name__ == '__main__':
        main()

.. note::
    We use the ``separate`` callback to remove the brick. This ensures the
    collision physics resolves before we remove the shape, avoiding issues
    where the ball might pass through without bouncing.

Example 2: One-Way Platforms
============================

A common game mechanic is platforms you can jump through from below but stand
on from above. We implement this by checking the collision normal in a
``begin`` callback::

    COLLISION_TYPE_PLAYER = 1
    COLLISION_TYPE_PLATFORM = 2

    def passthrough_platform(arbiter, space, data):
        """Allow jumping through platforms from below."""
        # Get the player body (first shape in collision)
        player_body = arbiter.bodies[0]

        # If player is moving upward, ignore the collision
        if player_body.velocity.y > 0:
            arbiter.process_collision = False

        # process_collision defaults to True, so we don't need an else

    # Set up the player shape
    player_shape.collision_type = COLLISION_TYPE_PLAYER

    # Set up platform shapes
    platform_shape.collision_type = COLLISION_TYPE_PLATFORM

    # Register the handler
    space.on_collision(
        COLLISION_TYPE_PLAYER,
        COLLISION_TYPE_PLATFORM,
        begin=passthrough_platform
    )

The key is setting ``arbiter.process_collision = False`` to tell Pymunk to
ignore this particular collision. The player passes through when moving up
but lands normally when falling down.

Example 3: Collision Damage with Sound
======================================

Use ``post_solve`` to access collision impulse and energy for damage
calculations::

    def collision_damage(arbiter, space, data):
        """Calculate damage based on collision force."""
        # total_ke gives kinetic energy lost in collision
        energy = arbiter.total_ke

        # total_impulse gives the impulse applied
        impulse = arbiter.total_impulse.length

        if energy > 1000:  # Threshold for "hard" collision
            print(f"Hard hit! Energy: {energy:.0f}, Impulse: {impulse:.0f}")
            # Play loud sound, apply high damage
        elif energy > 100:
            print(f"Medium hit! Energy: {energy:.0f}")
            # Play medium sound, apply some damage

        # Check if this is the first frame of contact
        if arbiter.is_first_contact:
            print("Initial impact!")

    space.on_collision(
        COLLISION_TYPE_BALL,
        COLLISION_TYPE_WALL,
        post_solve=collision_damage
    )

.. note::
    ``total_impulse`` and ``total_ke`` are only valid in ``post_solve``
    callbacks or when iterating over arbiters, not in ``begin`` or
    ``pre_solve``.

Using the Arbiter
=================

The ``Arbiter`` object provides information about the collision:

**arbiter.shapes**
    Tuple of the two shapes involved, in the order you specified when
    registering the handler::

        ball, brick = arbiter.shapes

**arbiter.bodies**
    Shortcut for getting the bodies::

        ball_body, brick_body = arbiter.bodies

**arbiter.normal**
    The collision normal vector, pointing from the first shape to the second.

**arbiter.contact_point_set**
    Detailed contact information including contact points and penetration depth.

**arbiter.total_impulse**
    The impulse applied to resolve the collision (only valid in post_solve).

**arbiter.total_ke**
    Kinetic energy lost in the collision (only valid in post_solve).

**arbiter.is_first_contact**
    True if this is the first step the shapes started touching. Useful for
    playing sounds only once per collision.

**arbiter.process_collision**
    Set to False in begin or pre_solve to ignore the collision.

**arbiter.friction / arbiter.restitution**
    Override the calculated friction or elasticity for this collision.

Wildcard Handlers
=================

You can use ``None`` as a collision type to match any shape::

    # Called for ALL collisions involving balls
    space.on_collision(COLLISION_TYPE_BALL, None, begin=on_ball_collision)

    # Called for ALL collisions in the space
    space.on_collision(None, None, begin=on_any_collision)

When multiple handlers match a collision (e.g., a specific handler and a
wildcard), the most specific handler is called first.

Passing Data to Handlers
========================

Use the ``data`` parameter to pass information to your callbacks::

    game_state = {
        "score": 0,
        "sound_manager": my_sound_manager,
        "player_health": 100
    }

    def on_collision(arbiter, space, data):
        data["score"] += 10
        data["sound_manager"].play("hit")

    space.on_collision(
        COLLISION_TYPE_BALL,
        COLLISION_TYPE_BRICK,
        begin=on_collision,
        data=game_state
    )

Tips and Common Pitfalls
========================

**Don't remove shapes during begin or pre_solve**
    Removing shapes while the collision is being processed can cause issues.
    Either use the ``separate`` callback, or schedule removal for after the
    step completes.

**Remember to add collision types**
    Shapes have ``collision_type = 0`` by default. If your handlers aren't
    being called, check that you've set the collision types correctly.

**Sensors don't call post_solve**
    Sensor shapes (``shape.sensor = True``) trigger begin, pre_solve, and
    separate callbacks but never post_solve, since there's no physical
    response to process.

**Handler order matters**
    If both shapes in a collision have handlers registered, the handler for
    collision_type_a fires first. The shapes in ``arbiter.shapes`` are always
    in the order (collision_type_a, collision_type_b).

Next Steps
==========

Now that you understand collision handlers, you can:

- Study the included ``breakout.py`` example for a complete game using
  collision handlers
- Look at ``platformer.py`` for one-way platforms and player mechanics
- Read about :py:class:`pymunk.Arbiter` in the API reference for all available
  collision information
- Explore sensors for trigger zones that detect but don't physically collide
