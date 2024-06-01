import math

import pygame

import pymunk
import pymunk.pygame_util

"""
Benchmarks

# Higher is better tests (stability/accuracy) tests

- Stack boxes and see how tall until fall down
- Newtons pendulum

# Perf tests

- Big body with high velocity hit group of circle in zero gravity. 1000? bodies

- Slow explosion

"""


class FallingSquares:
    def __init__(self, space, size):
        space.gravity = 0, 10
        space.static_body.position = 0, 10
        ground = pymunk.Poly.create_box(space.static_body, (200, 20))
        space.add(ground)

        for i in range(15):
            a = 0.5 + i / 15 * 2.5
            for j in range(size):
                b = pymunk.Body()
                b.position = i * 7 - 60, -2 * a * (size - j)

                p = pymunk.Poly.create_box(b, (a, a))
                p.density = 5
                space.add(b, p)


class FallingCircles:
    def __init__(self, space, size):
        space.gravity = 0, 10
        space.static_body.position = 0, 10
        ground = pymunk.Poly.create_box(space.static_body, (200, 20))
        space.add(ground)

        for i in range(15):
            a = 0.5 + i / 15 * 2.5
            for j in range(size):
                b = pymunk.Body()
                b.position = i * 7 + j * 0.25 - 60, -2 * a * (size - j)
                c = pymunk.Circle(b, a / 2)
                c.density = 5
                space.add(b, c)


class SlowExplosion:
    def __init__(self, space, size):

        for i in range(size):
            b = pymunk.Body()
            c = pymunk.Circle(b, 0.5)
            c.density = 0.5
            s = i * 30 / size
            x = math.cos(s * 30) * (s * 30 + 5)
            y = math.sin(s * 30) * (s * 30 + 5)
            b.position = pymunk.Vec2d(x, y)
            b.velocity = 0.2 * b.position
            space.add(b, c)


class MildN2:
    def __init__(self, space, size):
        space.gravity = 0, 10
        ground = pymunk.Segment(space.static_body, (-50, 0), (50, 0), 1)
        space.add(ground)

        # table
        for i in range(size):
            b = pymunk.Body()
            b.position = -5, -1

            top = pymunk.Poly.create_box_bb(
                b,
                pymunk.BB(-3, -3, 3, -4),
            )
            left = pymunk.Poly.create_box_bb(
                b,
                pymunk.BB(-3, -3, -2, 2),
            )
            right = pymunk.Poly.create_box_bb(
                b,
                pymunk.BB(2, -3, 3, 2),
            )
            top.density = 2
            left.density = 2

            space.add(top, left, right, b)

        # triangle
        for i in range(size):
            b = pymunk.Body()
            b.position = 15, -1
            left = pymunk.Poly(b, [(-2, 0), (1, -2), (0, -4)])
            left.density = 3

            right = pymunk.Poly(b, [(2, 0), (-1, -2), (0, -4)])
            right.density = 3

            space.add(b, left, right)


class N2:
    def __init__(self, space, size):
        space.gravity = 0, 10
        # ground = pymunk.Segment(space.static_body, (-50, 0), (50, 0), 1)
        # space.add(ground)

        for i in range(size):
            b = pymunk.Body()
            b.position = (i * 0.01, -i * 0.01)
            c = pymunk.Circle(b, 1)
            c.density = 1
            space.add(b, c)


tests = [SlowExplosion, FallingSquares]

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

space = pymunk.Space()

draw_options = pymunk.pygame_util.DrawOptions(screen)
# FallingSquares(space, 200)
# FallingCircles(space, 200)
# MildN2(space, 50)
N2(space, 500)
# SlowExplosion(space, 5000)

translation = pymunk.Transform()
scaling = 2

steps = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()

    keys = pygame.key.get_pressed()
    zoom_in = int(keys[pygame.K_a])
    zoom_out = int(keys[pygame.K_z])
    zoom_speed = 0.1
    scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

    draw_options.transform = pymunk.Transform.translation(
        300, 300
    ) @ pymunk.Transform.scaling(scaling)

    fps = 60.0
    dt = 1.0 / fps
    space.step(dt)
    steps += 1

    screen.fill(pygame.Color("white"))
    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(fps)
    pygame.display.set_caption(f"step {steps} fps {clock.get_fps():.2f}")


class Stacking:

    def __init__(self):
        self.space = pymunk.Space()

        s = pymunk.Segment(self.space.static_body, (0, 500), (500, 500), 5)

    def update(self, dt):
        pass

    def draw(self):
        pass
