"""Port of the Chipmunk tank demo. Showcase a topdown tank driving towards the
mouse, and hitting obstacles on the way.
"""

import random

import pygame

import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


def update(space, dt, surface):
    global tank_body
    global tank_control_body

    mpos = pygame.mouse.get_pos()
    mouse_pos = pymunk.pygame_util.from_pygame(Vec2d(*mpos), surface)

    mouse_delta = mouse_pos - tank_body.position
    turn = tank_body.rotation_vector.cpvunrotate(mouse_delta).angle
    tank_control_body.angle = tank_body.angle - turn

    # drive the tank towards the mouse
    if (mouse_pos - tank_body.position).get_length_sqrd() < 30 ** 2:
        tank_control_body.velocity = 0, 0
    else:
        if mouse_delta.dot(tank_body.rotation_vector) > 0.0:
            direction = 1.0
        else:
            direction = -1.0
        dv = Vec2d(30.0 * direction, 0.0)
        tank_control_body.velocity = tank_body.rotation_vector.cpvrotate(dv)

    space.step(dt)


def add_box(space, size, mass):
    radius = Vec2d(size, size).length

    body = pymunk.Body()
    space.add(body)

    body.position = Vec2d(
        random.random() * (640 - 2 * radius) + radius,
        random.random() * (480 - 2 * radius) + radius,
    )

    shape = pymunk.Poly.create_box(body, (size, size), 0.0)
    shape.mass = mass
    shape.friction = 0.7
    space.add(shape)

    return body


def init():

    space = pymunk.Space()
    space.iterations = 10
    space.sleep_time_threshold = 0.5

    static_body = space.static_body

    # Create segments around the edge of the screen.
    shape = pymunk.Segment(static_body, (1, 1), (1, 480), 1.0)
    space.add(shape)
    shape.elasticity = 1
    shape.friction = 1

    shape = pymunk.Segment(static_body, (640, 1), (640, 480), 1.0)
    space.add(shape)
    shape.elasticity = 1
    shape.friction = 1

    shape = pymunk.Segment(static_body, (1, 1), (640, 1), 1.0)
    space.add(shape)
    shape.elasticity = 1
    shape.friction = 1

    shape = pymunk.Segment(static_body, (1, 480), (640, 480), 1.0)
    space.add(shape)
    shape.elasticity = 1
    shape.friction = 1

    for _ in range(50):
        body = add_box(space, 20, 1)

        pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
        space.add(pivot)
        pivot.max_bias = 0  # disable joint correction
        pivot.max_force = 1000  # emulate linear friction

        gear = pymunk.GearJoint(static_body, body, 0.0, 1.0)
        space.add(gear)
        gear.max_bias = 0  # disable joint correction
        gear.max_force = 5000  # emulate angular friction

    # We joint the tank to the control body and control the tank indirectly by modifying the control body.
    global tank_control_body
    tank_control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    tank_control_body.position = 320, 240
    space.add(tank_control_body)
    global tank_body
    tank_body = add_box(space, 30, 10)
    tank_body.position = 320, 240
    for s in tank_body.shapes:
        s.color = (0, 255, 100, 255)

    pivot = pymunk.PivotJoint(tank_control_body, tank_body, (0, 0), (0, 0))
    space.add(pivot)
    pivot.max_bias = 0  # disable joint correction
    pivot.max_force = 10000  # emulate linear friction

    gear = pymunk.GearJoint(tank_control_body, tank_body, 0.0, 1.0)
    space.add(gear)
    gear.error_bias = 0  # attempt to fully correct the joint each step
    gear.max_bias = 1.2  # but limit it's angular correction rate
    gear.max_force = 50000  # emulate angular friction

    return space


space = init()
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)


font = pygame.font.Font(None, 24)
text = "Use the mouse to drive the tank, it will follow the cursor."
text = font.render(text, True, pygame.Color("white"))

while True:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and (event.key in [pygame.K_ESCAPE, pygame.K_q])
        ):
            exit()

    screen.fill(pygame.Color("black"))
    space.debug_draw(draw_options)
    screen.blit(text, (15, 15))
    fps = 60
    update(space, 1 / fps, screen)
    pygame.display.flip()

    clock.tick(fps)
