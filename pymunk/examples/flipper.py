"""A very basic flipper game.
"""
__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import random

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
    space.gravity = (0.0, 900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ## Balls
    balls = []

    ### walls
    static_lines = [
        pymunk.Segment(space.static_body, (150, 500), (50, 50), 1.0),
        pymunk.Segment(space.static_body, (450, 500), (550, 50), 1.0),
        pymunk.Segment(space.static_body, (50, 50), (300, 0), 1.0),
        pymunk.Segment(space.static_body, (300, 0), (550, 50), 1.0),
        pymunk.Segment(space.static_body, (300, 180), (400, 200), 1.0),
    ]
    for line in static_lines:
        line.elasticity = 0.7
        line.group = 1
    space.add(*static_lines)

    fp = [(20, -20), (-120, 0), (20, 20)]
    mass = 100
    moment = pymunk.moment_for_poly(mass, fp)

    # right flipper
    r_flipper_body = pymunk.Body(mass, moment)
    r_flipper_body.position = 450, 500
    r_flipper_shape = pymunk.Poly(r_flipper_body, fp)
    space.add(r_flipper_body, r_flipper_shape)

    r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    r_flipper_joint_body.position = r_flipper_body.position
    j = pymunk.PinJoint(r_flipper_body, r_flipper_joint_body, (0, 0), (0, 0))
    # todo: tweak values of spring better
    s = pymunk.DampedRotarySpring(
        r_flipper_body, r_flipper_joint_body, 0.15, 20000000, 900000
    )
    space.add(j, s)

    # left flipper
    l_flipper_body = pymunk.Body(mass, moment)
    l_flipper_body.position = 150, 500
    l_flipper_shape = pymunk.Poly(l_flipper_body, [(-x, y) for x, y in fp])
    space.add(l_flipper_body, l_flipper_shape)

    l_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    l_flipper_joint_body.position = l_flipper_body.position
    j = pymunk.PinJoint(l_flipper_body, l_flipper_joint_body, (0, 0), (0, 0))
    s = pymunk.DampedRotarySpring(
        l_flipper_body, l_flipper_joint_body, -0.15, 20000000, 900000
    )
    space.add(j, s)

    r_flipper_shape.group = l_flipper_shape.group = 1
    r_flipper_shape.elasticity = l_flipper_shape.elasticity = 0.4

    # "bumpers"
    for p in [(240, 100), (360, 100)]:
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = p
        shape = pymunk.Circle(body, 10)
        shape.elasticity = 1.5
        space.add(body, shape)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "flipper.png")

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                r_flipper_body.apply_impulse_at_local_point(
                    Vec2d.unit() * -40000, (-100, 0)
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                l_flipper_body.apply_impulse_at_local_point(
                    Vec2d.unit() * 40000, (-100, 0)
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:

                mass = 1
                radius = 25
                inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
                body = pymunk.Body(mass, inertia)
                x = random.randint(115, 350)
                body.position = x, 200
                shape = pymunk.Circle(body, radius, (0, 0))
                shape.elasticity = 0.95
                space.add(body, shape)
                balls.append(shape)

        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        space.debug_draw(draw_options)

        r_flipper_body.position = 450, 500
        l_flipper_body.position = 150, 500
        r_flipper_body.velocity = l_flipper_body.velocity = 0, 0

        ### Remove any balls outside
        to_remove = []
        for ball in balls:
            if ball.body.position.get_distance((300, 300)) > 1000:
                to_remove.append(ball)

        for ball in to_remove:
            space.remove(ball.body, ball)
            balls.remove(ball)

        ### Update physics
        dt = 1.0 / 60.0 / 5.0
        for x in range(5):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    main()