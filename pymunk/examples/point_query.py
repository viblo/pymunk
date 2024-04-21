"""This example showcase point queries by highlighting the shape under the 
mouse pointer.
"""

__docformat__ = "reStructuredText"

import random
import sys

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = Vec2d(0.0, 900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    ## Balls
    balls = []

    ### walls
    static_lines = [
        pymunk.Segment(space.static_body, Vec2d(111, 320), Vec2d(407, 354), 1.0),
        pymunk.Segment(space.static_body, Vec2d(407, 354), Vec2d(407, 257), 1.0),
    ]
    space.add(*static_lines)

    ticks_to_next_ball = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "point_query.png")

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 10
            radius = 25
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            x = random.randint(115, 350)
            body.position = x, 200
            shape = pymunk.Circle(body, radius, Vec2d(0, 0))
            shape.color = pygame.Color("lightgrey")
            space.add(body, shape)
            balls.append(shape)

        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        space.debug_draw(draw_options)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y > 400:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)

        shape = space.point_query_nearest(
            mouse_pos, float("inf"), pymunk.ShapeFilter()
        ).shape
        if shape is not None and isinstance(shape, pymunk.Circle):
            r = shape.radius + 4
            p = pymunk.pygame_util.to_pygame(shape.body.position, screen)
            pygame.draw.circle(screen, pygame.Color("red"), p, int(r), 2)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    sys.exit(main())
