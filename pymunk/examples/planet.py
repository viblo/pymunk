"""
Showcase of planets/satellites (small boxes) orbiting around a star. 

Uses a custom velocity function to manually calculate the gravity, assuming 
the star is in the middle and is massive enough that the satellites does not 
affect it.

This is also a demonstration of the performance boost from the batch api in 
pymunk.batch. It uses both the batch api to get positions and velocitites, 
and to update the velocitites.

The speedup of when both batching apis are enabled is huge!

(This is a modified port of the Planet demo included in Chipmunk.)
"""

import math
import random

import numpy as np
import pygame

import pymunk
import pymunk.batch
import pymunk.pygame_util

random.seed(1)

gravityStrength = 5.0e6
planet_radius = 3
center = pymunk.Vec2d(300, 300)
screen_size = (600, 600)
starting_planets = 100

dt = 1 / 60.0


def planet_gravity(body, gravity, damping, dt):
    # Gravitational acceleration is proportional to the inverse square of
    # distance, and directed toward the origin. The central planet is assumed
    # to be massive enough that it affects the satellites but not vice versa.
    p = body.position
    sq_dist = p.get_dist_sqrd(center)
    g = (p - center) * -gravityStrength / (sq_dist * math.sqrt(sq_dist))

    # body.velocity += g * dt # setting velocity directly like would be slower
    pymunk.Body.update_velocity(body, g, damping, dt)


def batched_planet_gravity(draw_buffer, dt, update_buffer):
    # get current position and velocity
    arr = np.frombuffer(draw_buffer.float_buf())
    # pick every 4th item to position.x etc.
    p_x = arr[::4]
    p_y = arr[1::4]
    v_x = arr[2::4]
    v_y = arr[3::4]

    sq_dist = (p_x - center.x) ** 2 + (p_y - center.y) ** 2

    scaled_dist_sq_dist = -gravityStrength / (sq_dist * np.sqrt(sq_dist))
    g_x = (p_x - center.x) * scaled_dist_sq_dist
    g_y = (p_y - center.y) * scaled_dist_sq_dist
    # at this point we have calculated 'g' as in planet_graivity(...)

    # This is the simpliced update_velocity function from planet_gravity(...)
    # (since space.gravity == 0 and space.damping == 1)
    new_v_x = v_x + g_x * dt
    new_v_y = v_y + g_y * dt

    # make resulting array by altering x and y values for the velocity
    v_arr = np.ravel([new_v_x, new_v_y], "F")
    update_buffer.set_float_buf(v_arr.tobytes())


def add_planet(space):
    body = pymunk.Body()
    while True:
        # Loop to filter out planets too close to the center star
        body.position = pymunk.Vec2d(
            random.randint(-150, 750), random.randint(-150, 750)
        )
        r = body.position.get_distance(center)
        if r > 40:
            break

    body.velocity_func = planet_gravity

    # Set the planets's velocity to put it into a circular orbit from its
    # starting position.
    v = math.sqrt(gravityStrength / r) / r
    body.velocity = (body.position - center).perpendicular() * v
    # Set the planets's angular velocity to match its orbital period and
    # align its initial angle with its position.
    body.angular_velocity = v
    body.angle = math.atan2(body.position.y, body.position.x)

    circle = pymunk.Circle(body, planet_radius)
    circle.mass = 1
    circle.friction = 0.7
    circle.elasticity = 0
    space.add(body, circle)


pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

space = pymunk.Space()

for x in range(starting_planets):
    add_planet(space)

use_batch_draw = False
use_batch_update = False
draw_buffer = pymunk.batch.Buffer()
update_buffer = pymunk.batch.Buffer()
planet_color = pygame.Color("white")

while True:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            for x in range(100):
                add_planet(space)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.image.save(screen, "planet_batch.png")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            use_batch_draw = not use_batch_draw
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            use_batch_update = not use_batch_update

            if use_batch_update:
                for b in space.bodies:
                    b.velocity_func = pymunk.Body.update_velocity
            else:
                for b in space.bodies:
                    b.velocity_func = planet_gravity

    screen.fill(pygame.Color("black"))

    if use_batch_draw or use_batch_update:
        # Reuse the position / velocity buffer for both drawing and calculating velocity
        draw_buffer.clear()
        pymunk.batch.get_space_bodies(
            space,
            pymunk.batch.BodyFields.POSITION | pymunk.batch.BodyFields.VELOCITY,
            draw_buffer,
        )

    if use_batch_draw:
        ps = list(memoryview(draw_buffer.float_buf()).cast("d"))
        for idx in range(0, len(ps), 4):
            pygame.draw.circle(
                screen, planet_color, (ps[idx], ps[idx + 1]), planet_radius
            )
    else:
        for b in space.bodies:
            pygame.draw.circle(screen, planet_color, b.position, planet_radius)

    # 'Star' in the center of screen
    pygame.draw.circle(screen, pygame.Color("yellow"), center, 10)

    if use_batch_update:
        batched_planet_gravity(draw_buffer, dt, update_buffer)
        pymunk.batch.set_space_bodies(
            space, pymunk.batch.BodyFields.VELOCITY, update_buffer
        )

    space.step(dt)

    help = "Press a to add planets, d to toggle batched drawing and u to toggle batched updates."
    draw_mode = "batch" if use_batch_draw else "loop"
    update_mode = "batch" if use_batch_update else "callback"
    status = (
        f"Planets: {len(space.bodies)}. Draw mode: {draw_mode}. Update: {update_mode}"
    )

    screen.blit(font.render(status, True, pygame.Color("orange")), (5, 25))
    screen.blit(font.render(help, True, pygame.Color("orange")), (5, 5))

    pygame.display.flip()
    clock.tick(1 / dt)
    pygame.display.set_caption(f"fps: {clock.get_fps():.2f} {status}")
