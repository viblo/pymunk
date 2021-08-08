"""Basic showcase on how the transform property on SpaceDebugDrawOptions can 
be used as a camera to allow panning. Use arrows to move the camera.
"""

__docformat__ = "reStructuredText"

import random
import sys

import pygame

import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 16)
    text = font.render(
        "Use Arrows (up, down, left, right) to move the camera.",
        True,
        pygame.Color("black"),
    )

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
    for l in static_lines:
        l.friction = 1
    space.add(*static_lines)

    ticks_to_next_ball = 10

    while running:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "camera.png")

        keys = pygame.key.get_pressed()
        left = int(keys[pygame.K_LEFT])
        up = int(keys[pygame.K_UP])
        down = int(keys[pygame.K_DOWN])
        right = int(keys[pygame.K_RIGHT])

        translate_speed = 10
        draw_options.transform = draw_options.transform.translated(
            translate_speed * left - translate_speed * right,
            translate_speed * up - translate_speed * down,
        )

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 10
            radius = 25
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            x = random.randint(115, 350)
            body.position = x, 200
            shape = pymunk.Circle(body, radius)
            shape.friction = 1
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

        screen.blit(text, (5, 5))

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
