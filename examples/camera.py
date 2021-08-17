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

random.seed(0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 16)
    text = font.render(
        "Use Arrows (up, down, left, right) to move the camera, "
        "a and z to zoom in / out and s and x to rotate.",
        True,
        pygame.Color("black"),
    )

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = Vec2d(0.0, 900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ## Balls
    balls = []

    body = pymunk.Body()
    body.position = pymunk.Vec2d(407, 354)
    s1 = pymunk.Segment(body, Vec2d(-300, -30), Vec2d(0, 0), 1.0)
    s2 = pymunk.Segment(body, Vec2d(0, 0), Vec2d(0, -100), 1.0)
    s1.density = 0.1
    s2.density = 0.1
    s1.friction = 1
    s2.friction = 1
    space.add(body, s1, s2)

    c1 = pymunk.constraints.DampedSpring(
        space.static_body,
        body,
        (427, 200),
        (0, -100),
        Vec2d(407, 254).get_distance((427, 200)),
        2000,
        100,
    )

    c2 = pymunk.constraints.DampedSpring(
        space.static_body,
        body,
        (87, 200),
        (-300, -30),
        Vec2d(107, 324).get_distance((87, 200)),
        2000,
        100,
    )
    space.add(c1, c2)

    # extra to show how constraints are drawn when very small / large
    body = pymunk.Body(1, 100)
    body.position = 450, 305
    c3 = pymunk.constraints.DampedSpring(
        space.static_body, body, (450, 300), (0, 0), 5, 1000, 100
    )
    space.add(body, c3)
    body = pymunk.Body(1, 100)
    body.position = 500, 2025
    c3 = pymunk.constraints.DampedSpring(
        space.static_body, body, (500, 25), (0, 0), 2000, 1000, 100
    )
    space.add(body, c3)

    ticks_to_next_ball = 10

    translation = pymunk.Transform()
    scaling = 1
    rotation = 0

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

        zoom_in = int(keys[pygame.K_a])
        zoom_out = int(keys[pygame.K_z])
        rotate_left = int(keys[pygame.K_s])
        rotate_right = int(keys[pygame.K_x])

        translate_speed = 10
        translation = translation.translated(
            translate_speed * left - translate_speed * right,
            translate_speed * up - translate_speed * down,
        )

        zoom_speed = 0.1
        scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

        rotation_speed = 0.1
        rotation += rotation_speed * rotate_left - rotation_speed * rotate_right

        # to zoom with center of screen as origin we need to offset with
        # center of screen, scale, and then offset back
        draw_options.transform = (
            pymunk.Transform.translation(300, 300)
            @ pymunk.Transform.scaling(scaling)
            @ translation
            @ pymunk.Transform.rotation(rotation)
            @ pymunk.Transform.translation(-300, -300)
        )

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 10
            radius = 25
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            x = random.randint(115, 350)
            body.position = x, 100
            if random.random() > 0.5:
                shape = pymunk.Circle(body, radius)
            else:
                shape = pymunk.Poly.create_box(
                    body, size=(radius * 2, radius * 2), radius=2
                )
            shape.friction = 1
            space.add(body, shape)
            balls.append(shape)

        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        space.debug_draw(draw_options)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y > 500:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        screen.blit(text, (5, 5))

        ### Update physics
        dt = 1.0 / 60.0
        space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    sys.exit(main())
