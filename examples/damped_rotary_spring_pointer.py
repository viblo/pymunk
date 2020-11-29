"""This example showcase an arrow pointing or aiming towards the cursor.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys

import pygame

import pymunk
import pymunk.constraints
import pymunk.pygame_util
from pymunk import Vec2d


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    pointer_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    ps = [(80, 0), (0, 20), (0, -20)]
    moment = pymunk.moment_for_poly(1, ps)
    gun_body = pymunk.Body(1, moment)
    gun_body.position = Vec2d(300, 300)
    gun_shape = pymunk.Poly(gun_body, ps)

    rest_angle = 0
    stiffness = 125000.0
    damping = 6000.0

    rotary_spring = pymunk.constraints.DampedRotarySpring(
        pointer_body, gun_body, rest_angle, stiffness, damping
    )

    space.add(gun_body, gun_shape, rotary_spring)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "damped_rotary_sprint_pointer.png")
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
                pointer_body.position = mouse_pos
                pointer_body.angle = (pointer_body.position - gun_body.position).angle

            # to easily find good values for the damped rortary spring
            # as with most simulations done with pymunk, the imporant thing
            # is that it looks good, not the exact parameters
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                rotary_spring.stiffness *= 0.5
                print(rotary_spring.stiffness, rotary_spring.damping)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                rotary_spring.stiffness *= 2
                print(rotary_spring.stiffness, rotary_spring.damping)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                rotary_spring.damping *= 0.5
                print(rotary_spring.stiffness, rotary_spring.damping)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                rotary_spring.damping *= 2
                print(rotary_spring.stiffness, rotary_spring.damping)

        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        space.debug_draw(draw_options)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)


if __name__ == "__main__":
    sys.exit(main())
