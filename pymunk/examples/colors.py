"""
An example of the determinism of pymunk by coloring balls according to their 
position, and then respawning them to verify each ball ends up in the same 
place. Inspired by Pymunk user Nam Dao.
"""


import random

import pygame

import pymunk
import pymunk.pygame_util


def new_space(color_dict):
    space = pymunk.Space()
    space.gravity = 0, 900
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (20, -50), (0, 600), 20),
        pymunk.Segment(static_body, (0, 600), (600, 600), 20),
        pymunk.Segment(static_body, (600, 600), (580, -50), 20),
        # pymunk.Segment(static_body, (600, 0), (20, 0), 20),
        pymunk.Segment(static_body, (250, 300), (600, 150), 3),
    ]

    space.add(*walls)

    random.seed(0)
    for i in range(800):
        body = pymunk.Body()
        x = random.randint(270, 450)
        y = random.randint(30, 100)
        body.position = x, y
        shape = pymunk.Circle(body, 6)
        shape.mass = 1
        shape.data = i
        if color_dict != None and i in color_dict:
            shape.color = color_dict[i]
        space.add(body, shape)

    return space


pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)
text = font.render(
    "Press r to reset and respawn all balls."
    " Press c to set color of each ball according to its position.",
    True,
    pygame.Color("gray"),
)
draw_options = pymunk.pygame_util.DrawOptions(screen)

color_dict = None
space = pymunk.Space()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.image.save(screen, "colors.png")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            space = new_space(color_dict)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            color_dict = {}
            for shape in space.shapes:
                if not isinstance(shape, pymunk.Circle):
                    continue
                r = shape.body.position.x / 600 * 255
                g = max((shape.body.position.y - 400) / 200 * 255, 0)
                if r < 0 or r > 255 or g < 0 or g > 255:
                    print(shape.body.position)
                    exit()
                shape.color = (r, g, 150, 255)
                color_dict[shape.data] = shape.color

    ### Update physics
    dt = 1.0 / 60.0
    for _ in range(5):
        space.step(dt / 5)

    ### Draw stuff
    screen.fill(pygame.Color("black"))

    # space.debug_draw(draw_options)
    color = pygame.Color("blue")
    for shape in space.shapes:
        if not isinstance(shape, pymunk.Circle):
            continue
        if hasattr(shape, "color"):
            color = shape.color
        # Draw the circles with a little larger size (radius) then their
        # actual size to make it look nicer without gaps between circles.
        pygame.draw.circle(screen, color, shape.body.position, shape.radius + 4)
    screen.blit(text, (25, 2))

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
