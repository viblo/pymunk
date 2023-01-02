"""Very basic example of using a sprite image to draw a shape more similar 
how you would do it in a real game instead of the simple line drawings used 
by the other examples. 
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math
import random
from typing import List
import os.path

import pygame

import pymunk
from pymunk import Vec2d


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600


def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = Vec2d(0.0, -900.0)

    ## logo
    logo_img = pygame.image.load(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "pymunk_logo_googlecode.png"
        )
    )
    logos: List[pymunk.Shape] = []

    ### Static line
    static_lines = [
        pymunk.Segment(space.static_body, (11.0, 280.0), (407.0, 246.0), 0.0),
        pymunk.Segment(space.static_body, (407.0, 246.0), (407.0, 343.0), 0.0),
    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(*static_lines)

    ticks_to_next_spawn = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "using_sprites.png")

        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn <= 0:
            ticks_to_next_spawn = 100
            x = random.randint(20, 400)
            y = 500
            angle = random.random() * math.pi
            vs = [(-23, 26), (23, 26), (0, -26)]
            mass = 10
            moment = pymunk.moment_for_poly(mass, vs)
            body = pymunk.Body(mass, moment)
            shape = pymunk.Poly(body, vs)
            shape.friction = 0.5
            body.position = x, y
            body.angle = angle

            space.add(body, shape)
            logos.append(shape)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Draw stuff
        screen.fill(pygame.Color("black"))

        for logo_shape in logos:
            # image draw
            p = logo_shape.body.position
            p = Vec2d(p.x, flipy(p.y))

            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(logo_shape.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(logo_img, angle_degrees)

            offset = Vec2d(*rotated_logo_img.get_size()) / 2
            p = p - offset

            screen.blit(rotated_logo_img, (round(p.x), round(p.y)))

            # debug draw
            ps = [
                p.rotated(logo_shape.body.angle) + logo_shape.body.position
                for p in logo_shape.get_vertices()
            ]
            ps = [(round(p.x), round(flipy(p.y))) for p in ps]
            ps += [ps[0]]
            pygame.draw.lines(screen, pygame.Color("red"), False, ps, 1)

        for line in static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = round(pv1.x), round(flipy(pv1.y))
            p2 = round(pv2.x), round(flipy(pv2.y))
            pygame.draw.lines(screen, pygame.Color("lightgray"), False, [p1, p2], 2)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    main()
