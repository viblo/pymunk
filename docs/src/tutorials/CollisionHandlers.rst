*******************************
Collision Handlers Step by Step
*******************************

This tutorial explains how collision handlers work in Pymunk and demonstrates 
practical use cases. It builds upon the concepts from the basic 
:doc:`SlideAndPinJoint` tutorial, so make sure you're comfortable with those 
basics first.

What are Collision Handlers?
============================

In many games and simulations, you need to know when objects collide and 
react to those collisions in custom ways. For example:

* Remove a brick when a ball hits it (Breakout)
* Play a sound when objects collide
* Create a one-way platform the player can jump through
* Track score when collecting coins
* Apply damage when enemies touch the player

Pymunk's collision handlers let you define callbacks that are triggered during 
different phases of a collision. You can use these to run custom code, modify 
collision behavior, or even prevent collisions entirely.

The Four Collision Phases
=========================

Each collision goes through up to four phases, and you can set callbacks for 
any of them:

**begin**
    Called once when two shapes first start touching. Return behavior can be 
    used to accept or reject the collision.

**pre_solve**
    Called every frame while shapes are touching, before the collision is 
    resolved. You can modify collision properties like friction and elasticity 
    here.

**post_solve**
    Called every frame after the collision response has been calculated. 
    Useful for reading collision data like impulses to calculate damage or 
    play sounds.

**separate**
    Called once when two shapes stop touching. Always called as a pair with 
    ``begin``, even if shapes are removed while touching.

Setting Up Collision Types
==========================

Before creating collision handlers, you need to assign collision types to your 
shapes. A collision type is just an integer that identifies a category of 
shapes::

    # Define collision types as constants for clarity
    COLLISION_TYPE_BALL = 1
    COLLISION_TYPE_BRICK = 2
    COLLISION_TYPE_BOTTOM = 3

    # Assign collision types to shapes
    ball_shape.collision_type = COLLISION_TYPE_BALL
    brick_shape.collision_type = COLLISION_TYPE_BRICK

Example 1: Removing Objects on Collision
========================================

Let's create a simple example where balls fall and break bricks on contact. 
This is similar to a Breakout-style game mechanic.

First, set up the basic simulation::

    import sys
    import random
    import pygame
    import pymunk
    import pymunk.pygame_util

    # Collision type constants
    COLLISION_TYPE_BALL = 1
    COLLISION_TYPE_BRICK = 2

    def add_ball(space, position):
        """Add a ball that will break bricks on contact"""
        body = pymunk.Body()
        body.position = position
        shape = pymunk.Circle(body, 15)
        shape.mass = 1
        shape.elasticity = 0.8
        shape.collision_type = COLLISION_TYPE_BALL
        space.add(body, shape)
        return shape

    def add_brick(space, position):
        """Add a breakable brick"""
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = position
        shape = pymunk.Poly.create_box(body, (60, 20))
        shape.collision_type = COLLISION_TYPE_BRICK
        shape.color = pygame.Color("blue")
        space.add(body, shape)
        return shape

Now, set up the collision handler to remove bricks when hit::

    def setup_collision_handlers(space):
        """Set up collision handler to remove bricks when hit by balls"""
        
        def remove_brick(arbiter, space, data):
            """Called when ball and brick start touching"""
            # arbiter.shapes contains the shapes in collision
            # The order matches the collision types in on_collision()
            brick_shape = arbiter.shapes[1]  # Second shape is the brick
            
            # Remove the brick from the space
            space.remove(brick_shape, brick_shape.body)
            
            # Return True to process the collision normally
            return True
        
        # Register the handler for ball-brick collisions
        space.on_collision(
            COLLISION_TYPE_BALL, 
            COLLISION_TYPE_BRICK, 
            begin=remove_brick
        )

The complete example::

    import sys
    import random
    import pygame
    import pymunk
    import pymunk.pygame_util

    COLLISION_TYPE_BALL = 1
    COLLISION_TYPE_BRICK = 2

    def add_ball(space, position):
        body = pymunk.Body()
        body.position = position
        shape = pymunk.Circle(body, 15)
        shape.mass = 1
        shape.elasticity = 0.8
        shape.collision_type = COLLISION_TYPE_BALL
        space.add(body, shape)
        return shape

    def add_brick(space, position):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = position
        shape = pymunk.Poly.create_box(body, (60, 20))
        shape.collision_type = COLLISION_TYPE_BRICK
        shape.color = pygame.Color("blue")
        space.add(body, shape)
        return shape

    def main():
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Collision Handlers - Break the Bricks!")
        clock = pygame.time.Clock()
        
        space = pymunk.Space()
        space.gravity = (0, 500)
        
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        
        # Add ground
        ground = pymunk.Segment(space.static_body, (50, 550), (550, 550), 5)
        ground.elasticity = 0.8
        space.add(ground)
        
        # Add bricks
        for row in range(3):
            for col in range(7):
                x = 100 + col * 70
                y = 200 + row * 30
                add_brick(space, (x, y))
        
        # Set up collision handler
        def remove_brick(arbiter, space, data):
            brick_shape = arbiter.shapes[1]
            space.remove(brick_shape, brick_shape.body)
            return True
        
        space.on_collision(
            COLLISION_TYPE_BALL,
            COLLISION_TYPE_BRICK,
            begin=remove_brick
        )
        
        balls = []
        ticks_to_next_ball = 50
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    elif event.key == pygame.K_SPACE:
                        # Spawn ball on spacebar
                        x = random.randint(100, 500)
                        balls.append(add_ball(space, (x, 50)))
            
            # Auto-spawn balls periodically
            ticks_to_next_ball -= 1
            if ticks_to_next_ball <= 0:
                ticks_to_next_ball = 100
                x = random.randint(100, 500)
                balls.append(add_ball(space, (x, 50)))
            
            screen.fill((40, 40, 40))
            space.debug_draw(draw_options)
            space.step(1/60.0)
            
            pygame.display.flip()
            clock.tick(60)

    if __name__ == '__main__':
        main()

Example 2: One-Way Platforms
============================

A common game mechanic is a platform you can jump through from below but stand 
on from above. We can implement this using the ``pre_solve`` callback to 
conditionally ignore collisions::

    COLLISION_TYPE_PLAYER = 1
    COLLISION_TYPE_PLATFORM = 2

    def add_passthrough_platform(space, position, width):
        """Add a platform that can be jumped through from below"""
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = position
        shape = pymunk.Segment(body, (-width/2, 0), (width/2, 0), 5)
        shape.friction = 1.0
        shape.collision_type = COLLISION_TYPE_PLATFORM
        shape.color = pygame.Color("yellow")
        space.add(body, shape)
        return shape

    def setup_passthrough_handler(space):
        """Set up one-way platform collision handling"""
        
        def passthrough_handler(arbiter, space, data):
            # Get the player body (first shape in the collision pair)
            player_body = arbiter.bodies[0]
            
            # Only allow collision if player is moving downward
            if player_body.velocity.y < 0:
                # Player is falling - process the collision (land on platform)
                arbiter.process_collision = True
            else:
                # Player is moving up - ignore collision (jump through)
                arbiter.process_collision = False
        
        space.on_collision(
            COLLISION_TYPE_PLAYER,
            COLLISION_TYPE_PLATFORM,
            pre_solve=passthrough_handler
        )

The key insight here is that ``pre_solve`` is called every frame while shapes 
overlap, so we can continuously evaluate whether to process the collision.

Example 3: Tracking Collision Data
==================================

Sometimes you want to track information about collisions, such as counting 
collected items or accumulating damage. The ``data`` parameter lets you pass 
information into your callbacks::

    COLLISION_TYPE_PLAYER = 1
    COLLISION_TYPE_COIN = 2

    def setup_coin_collection(space, game_state):
        """Set up coin collection with score tracking"""
        
        def collect_coin(arbiter, space, data):
            coin_shape = arbiter.shapes[1]
            
            # Update score using data passed to the handler
            data['score'] += 10
            print(f"Score: {data['score']}")
            
            # Remove the coin
            space.remove(coin_shape, coin_shape.body)
            
            return True
        
        space.on_collision(
            COLLISION_TYPE_PLAYER,
            COLLISION_TYPE_COIN,
            begin=collect_coin,
            data=game_state  # Pass game state to callback
        )

    # Usage:
    game_state = {'score': 0, 'lives': 3}
    setup_coin_collection(space, game_state)

Using the Arbiter
=================

The ``arbiter`` parameter passed to callbacks provides information about the 
collision:

``arbiter.shapes``
    A tuple of the two colliding shapes, in the order specified when setting 
    up the collision handler.

``arbiter.bodies``
    A tuple of the two colliding bodies.

``arbiter.contact_point_set``
    Information about the contact points, including normal vector and 
    penetration depth.

``arbiter.total_impulse``
    The total impulse applied to resolve the collision (only available in 
    ``post_solve``).

``arbiter.total_ke``
    The total kinetic energy of the collision (only available in 
    ``post_solve``).

``arbiter.process_collision``
    Set this to ``False`` to ignore the collision. Can be set in ``begin`` 
    or ``pre_solve`` callbacks.

Example: Using impulse for sound effects::

    def post_solve_sound(arbiter, space, data):
        # Get collision impulse magnitude
        impulse = arbiter.total_impulse.length
        
        # Only play sound for significant collisions
        if impulse > 100:
            volume = min(impulse / 1000, 1.0)  # Scale volume
            # play_collision_sound(volume)  # Your sound function
            print(f"Collision impulse: {impulse:.0f}")
    
    space.on_collision(
        COLLISION_TYPE_BALL,
        None,  # None matches any collision type
        post_solve=post_solve_sound
    )

Wildcard Collision Handlers
===========================

Using ``None`` for a collision type creates a wildcard handler that matches 
any shape::

    # Handle collisions between balls and ANY other shape
    space.on_collision(
        COLLISION_TYPE_BALL,
        None,
        begin=my_callback
    )

    # Handle ALL collisions in the space (use sparingly!)
    space.on_collision(
        None,
        None,
        begin=log_all_collisions
    )

Wildcard handlers are useful for debugging or implementing global behaviors 
like collision sound effects.

Important Notes
===============

**Don't store Arbiter references**
    Arbiters are temporary objects managed by the space. Use them only within 
    the callback - don't store references to them.

**Order matters**
    The order of shapes in ``arbiter.shapes`` matches the order of collision 
    types when you called ``on_collision()``.

**Sensor shapes**
    Shapes with ``sensor = True`` don't generate collision responses but still 
    trigger ``begin``, ``pre_solve``, and ``separate`` callbacks. They never 
    trigger ``post_solve``.

**Removing shapes in callbacks**
    It's safe to remove shapes from the space inside collision callbacks. 
    Pymunk handles this correctly.

Summary
=======

Collision handlers are a powerful way to add custom behavior to your physics 
simulation:

1. Assign collision types to your shapes using ``shape.collision_type``
2. Call ``space.on_collision()`` with the collision types and callback 
   functions
3. Use the ``arbiter`` parameter to access collision data
4. Set ``arbiter.process_collision = False`` to ignore collisions

For more examples, check out the ``breakout.py`` and ``platformer.py`` examples 
included with Pymunk, which demonstrate these concepts in complete games.
