"""This example lets you dynamically create static walls and dynamic balls

"""

__docformat__ = "reStructuredText"

import pygame

import pymunk
import pymunk.pygame_util

pm = pymunk


def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    # draw_options.flags |= pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS

    ### Physics stuff
    space = pymunk.Space()
    # space.gravity = 0, 900
    space.iterations = 3
    space.static_body.position = 300, 100

    b = pymunk.Body()
    b.position = 300, 100
    b.angle = 3.0
    c = pymunk.Circle(b, 20)
    c.mass = 10
    space.add(c, b)
    b.angular_velocity = 0
    b.velocity = 0, 1000
    c = pymunk.constraints.DampedSpring(
        space.static_body, b, (0, 0), (0, 0), 200, 500, 20
    )
    # c = pymunk.constraints.DampedRotarySpring(space.static_body, b, 0, 90000, 2000)
    c.max_force = 5000
    space.add(c)

    dt = 1 / 50.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        space.step(dt)

        ### Draw stuff
        screen.fill(pygame.Color("white"))
        space.debug_draw(draw_options)
        print(c.impulse / dt)
        ### Flip screen
        pygame.display.flip()
        clock.tick(10)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":

    main()
