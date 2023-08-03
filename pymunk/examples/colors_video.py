"""
Fun example
"""


import math
import os
import random

import pygame

import pymunk
import pymunk.pygame_util


def new_space():
    space = pymunk.Space()
    # space.gravity = 0, 100
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (-30, -30), (630, -30), 50),  # top -
        pymunk.Segment(static_body, (-30, -30), (-30, 630), 50),  # left |
        pymunk.Segment(static_body, (-30, 630), (630, 630), 50),  # bottom -
        pymunk.Segment(static_body, (630, 630), (630, -30), 50),  # right |
    ]
    for wall in walls:
        wall.elasticity = 1.0

    space.add(*walls)

    random.seed(0)
    return space


def spawn(logo_img, space):
    cnt = 0
    r = 8
    w = logo_img.get_width()
    h = logo_img.get_height()
    offset_x = 300 - w / 2
    offset_y = 300 - h / 2
    logo_img.lock()
    for x in range(0, w, r * 2):
        for y in range(0, h, r * 2):
            color = logo_img.get_at([x, y])
            if color.a > 200:
                cnt += 1
                body = pymunk.Body()
                body.position = x + offset_x, y + offset_y

                shape = pymunk.Circle(body, r * 0.999)
                shape = pymunk.Poly.create_box(body, (r * 2, r * 2))
                shape.mass = 1
                shape.elasticity = 1
                shape.color = color.r, color.g, color.b, 255
                space.add(body, shape)
                impulse = (body.position - pymunk.Vec2d(300, 300)) * 1
                impulse = (
                    pymunk.Vec2d(random.random() - 0.5, random.random() - 0.5) * 2000
                )
                body.apply_impulse_at_local_point(impulse, (0, 0))
    print(f"total cnt {cnt}")
    return r


pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)
text = font.render(
    "Press r to reset and respawn all balls."
    " Press c to set color of each ball according to its position.",
    True,
    pygame.Color("darkgray"),
)

logo_img = pygame.image.load(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "pymunk_logo_sphinx.png")
)

draw_options = pymunk.pygame_util.DrawOptions(screen)


space = new_space()
space2 = new_space()
radius = spawn(logo_img, space)

radius = spawn(logo_img, space2)
box_surf = pygame.Surface((radius * 2, radius * 2))
box_surf.fill(pygame.Color("white"))

positions = []

total_steps = 500
steps = 0
while total_steps > 0:
    total_steps -= 1
    steps += 0.02
    ### Update physics
    dt = 1.0 / 60.0 / (1 + 20 / steps)
    space2.step(dt)
    step_positions = []
    for shape in space2.shapes:
        if isinstance(shape, pymunk.Segment):
            continue
        step_positions.append(
            (
                shape.color,
                shape.body.position - (shape.radius, shape.radius),
                shape.body.angle * 360 / math.pi / 2,
            )
        )
        # screen.blit(box_surf, shape.body.position - (shape.radius, shape.radius))
    positions.append(step_positions)

positions.reverse()
for step_positions in positions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()

    ### Draw stuff
    screen.fill(pygame.Color("white"))

    for color, position, angle in step_positions:
        box_surf.fill(color)
        rotated = pygame.transform.rotate(box_surf, angle)
        screen.blit(rotated, position)
        # screen.blit(box_surf, position)

    # screen.blit(text, (25, 2))

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

steps = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.image.save(screen, "colors_video.png")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            exp_p = pymunk.Vec2d(300, 450)
            query_info = space.point_query(exp_p, 50, shape_filter=pymunk.ShapeFilter())
            print(len(query_info))
            for info in query_info:
                if info.shape is None:
                    continue
                impulse = (
                    (info.shape.body.position - exp_p).normalized()
                    * (1 / info.distance)
                    * 100000
                )

                info.shape.body.apply_impulse_at_local_point(impulse, (0, 0))
    steps += 0.02
    ### Update physics
    dt = 1.0 / 60.0 / (1 + 20 / steps)
    space.step(dt)

    ### Draw stuff
    screen.fill(pygame.Color("white"))

    color = pygame.Color("blue")
    for shape in space.shapes:
        if isinstance(shape, pymunk.Segment):
            continue
        if hasattr(shape, "color"):
            color = shape.color

        box_surf.fill(color)
        screen.blit(box_surf, shape.body.position - (shape.radius, shape.radius))

    # screen.blit(text, (25, 2))

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
