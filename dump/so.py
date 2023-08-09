import random

import pygame

import pymunk
import pymunk.pygame_util


def new_space(color_dict):
    space = pymunk.Space()
    space.gravity = 0, 900
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (0, 0), (0, 600), 10),
        pymunk.Segment(static_body, (0, 600), (600, 600), 10),
        pymunk.Segment(static_body, (600, 600), (600, 0), 10),
        pymunk.Segment(static_body, (600, 0), (0, 0), 10),
        pymunk.Segment(static_body, (200, 300), (600, 150), 3),
    ]

    space.add(*walls)

    random.seed(0)
    for i in range(500):
        body = pymunk.Body()
        x = random.randint(270, 450)
        y = random.randint(30, 100)
        body.position = x, y
        shape = pymunk.Circle(body, 7)
        shape.mass = 1
        shape.data = i
        if color_dict != None:
            shape.color = color_dict[i]
        space.add(body, shape)

    return space


pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

draw_options = pymunk.pygame_util.DrawOptions(screen)

color_dict = None
space = pymunk.Space()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            space = new_space(color_dict)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            color_dict = {}
            for shape in space.shapes:
                if not isinstance(shape, pymunk.Circle):
                    continue
                r = shape.body.position.x / 600 * 255
                g = max((shape.body.position.y - 400) / 200 * 255, 0)
                shape.color = (r, g, 150, 255)
                color_dict[shape.data] = shape.color

    ### Update physics
    dt = 1.0 / 60.0

    space.step(dt)

    ### Draw stuff
    screen.fill(pygame.Color("white"))
    space.debug_draw(draw_options)

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
