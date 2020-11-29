"""Program used to generate the logo animation on the pymunk main page.

This program will showcase several features of Pymunk, such as collisions, 
debug drawing, automatic generation of shapes from images, motors, joints and
sleeping bodies.
"""
__docformat__ = "reStructuredText"

import random
import sys

random.seed(5)  # try keep difference the random factor the same each run.

import pygame

import pymunk
import pymunk.autogeometry
import pymunk.pygame_util
from pymunk import Vec2d

fps = 60
pygame.init()
screen = pygame.display.set_mode((690, 300))
clock = pygame.time.Clock()

clock.tick(1)

### Physics stuff
space = pymunk.Space()
space.gravity = 0, 900
space.sleep_time_threshold = 0.3

draw_options = pymunk.pygame_util.DrawOptions(screen)
pymunk.pygame_util.positive_y_is_up = False

### Generate geometry from pymunk logo image
logo_img = pygame.image.load("pymunk_logo_sphinx.png")
logo_bb = pymunk.BB(0, 0, logo_img.get_width(), logo_img.get_height())


def sample_func(point):
    try:
        p = pymunk.pygame_util.to_pygame(point, logo_img)
        color = logo_img.get_at(p)

        return color.a
        # return color.hsla[2]
    except:
        return 0


logo_img.lock()
line_set = pymunk.autogeometry.march_soft(
    logo_bb, logo_img.get_width(), logo_img.get_height(), 99, sample_func
)
logo_img.unlock()

r = 10

letter_group = 0
for line in line_set:
    line = pymunk.autogeometry.simplify_curves(line, 0.7)

    max_x = 0
    min_x = 1000
    max_y = 0
    min_y = 1000
    for l in line:
        max_x = max(max_x, l.x)
        min_x = min(min_x, l.x)
        max_y = max(max_y, l.y)
        min_y = min(min_y, l.y)
    w, h = max_x - min_x, max_y - min_y

    # we skip the line which has less than 35 height, since its the "hole" in
    # the p in pymunk, and we dont need it.
    if h < 35:
        continue

    center = Vec2d(min_x + w / 2.0, min_y + h / 2.0)
    t = pymunk.Transform(a=1.0, d=1.0, tx=-center.x, ty=-center.y)

    r += 30
    if r > 255:
        r = 0

    if True:
        for i in range(len(line) - 1):
            shape = pymunk.Segment(space.static_body, line[i], line[i + 1], 1)
            shape.friction = 0.5
            shape.color = (255, 255, 255, 255)
            space.add(shape)


floor = pymunk.Segment(space.static_body, (-100, 300), (1000, 220), 5)
floor.friction = 1.0
space.add(floor)

### events
def big_ball(space):
    mass = 1000
    radius = 50
    moment = pymunk.moment_for_circle(mass, 0, radius)
    b = pymunk.Body(mass, moment)
    c = pymunk.Circle(b, radius)
    c.friction = 1
    c.color = 255, 0, 0, 255
    b.position = 800, 100
    b.apply_impulse_at_local_point((-10000, 0), (0, -1000))

    space.add(b, c)


def boxfloor(space):
    mass = 10
    vs = [(-50, 30), (60, 22), (-50, 22)]

    moment = pymunk.moment_for_poly(mass, vs)
    b = pymunk.Body(mass, moment)
    s = pymunk.Poly(b, vs)
    s.friction = 1
    s.color = 0, 0, 0, 255
    b.position = 600, 50

    space.add(b, s)


box_y = 150


def box(space):
    global box_y

    mass = 10
    moment = pymunk.moment_for_box(mass, (40, 20))
    b = pymunk.Body(mass, moment)
    s = pymunk.Poly.create_box(b, (40, 20))
    s.friction = 1
    b.position = 600, box_y
    box_y -= 30
    space.add(b, s)


def car(space):
    pos = Vec2d(100, 200)

    wheel_color = 52, 219, 119, 255
    shovel_color = 219, 119, 52, 255
    mass = 100
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel1_b = pymunk.Body(mass, moment)
    wheel1_s = pymunk.Circle(wheel1_b, radius)
    wheel1_s.friction = 1.5
    wheel1_s.color = wheel_color
    space.add(wheel1_b, wheel1_s)

    mass = 100
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel2_b = pymunk.Body(mass, moment)
    wheel2_s = pymunk.Circle(wheel2_b, radius)
    wheel2_s.friction = 1.5
    wheel2_s.color = wheel_color
    space.add(wheel2_b, wheel2_s)

    mass = 100
    size = (50, 30)
    moment = pymunk.moment_for_box(mass, size)
    chassi_b = pymunk.Body(mass, moment)
    chassi_s = pymunk.Poly.create_box(chassi_b, size)
    space.add(chassi_b, chassi_s)

    vs = [(0, 0), (25, 45), (0, 45)]
    shovel_s = pymunk.Poly(chassi_b, vs, transform=pymunk.Transform(tx=85))
    shovel_s.friction = 0.5
    shovel_s.color = shovel_color
    space.add(shovel_s)

    wheel1_b.position = pos - (55, 0)
    wheel2_b.position = pos + (55, 0)
    chassi_b.position = pos + (0, -25)

    space.add(
        pymunk.PinJoint(wheel1_b, chassi_b, (0, 0), (-25, -15)),
        pymunk.PinJoint(wheel1_b, chassi_b, (0, 0), (-25, 15)),
        pymunk.PinJoint(wheel2_b, chassi_b, (0, 0), (25, -15)),
        pymunk.PinJoint(wheel2_b, chassi_b, (0, 0), (25, 15)),
    )

    speed = 4
    space.add(
        pymunk.SimpleMotor(wheel1_b, chassi_b, speed),
        pymunk.SimpleMotor(wheel2_b, chassi_b, speed),
    )


def cannon(space):
    mass = 100
    radius = 15
    moment = pymunk.moment_for_circle(mass, 0, radius)
    b = pymunk.Body(mass, moment)
    s = pymunk.Circle(b, radius)
    s.color = 219, 52, 152, 255
    b.position = 700, -50
    space.add(b, s)
    impulse = Vec2d(-200000, 75000)
    b.apply_impulse_at_local_point((impulse))


events = []
events.append((0.1, big_ball))
events.append((2, big_ball))
events.append((3.5, boxfloor))
for x in range(8):
    events.append((4 + x * 0.2, box))
events.append((6.5, car))
events.append((8.5, cannon))

events.sort(key=lambda x: x[0])

SMALLBALL = pygame.USEREVENT + 1
pygame.time.set_timer(SMALLBALL, 100)

small_balls = 100
total_time = 0
while True:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and (event.key in [pygame.K_ESCAPE, pygame.K_q])
        ):
            sys.exit(0)
        elif event.type == SMALLBALL:
            if small_balls <= 0:
                pygame.time.set_timer(SMALLBALL, 0)
            for x in range(10):
                small_balls -= 1
                mass = 3
                radius = 8
                moment = pymunk.moment_for_circle(mass, 0, radius)
                b = pymunk.Body(mass, moment)
                c = pymunk.Circle(b, radius)
                c.friction = 1
                x = random.randint(100, 400)
                b.position = x, 0

                space.add(b, c)

    if len(events) > 0 and total_time > events[0][0]:
        t, f = events.pop(0)

        f(space)

    space.step(1.0 / fps)

    screen.fill(pygame.Color("white"))

    space.debug_draw(draw_options)
    screen.blit(logo_img, (0, 0))

    for b in space.bodies:
        p = pymunk.pygame_util.to_pygame(b.position, screen)

    pygame.display.flip()

    dt = clock.tick(fps)
    total_time += dt / 1000.0
