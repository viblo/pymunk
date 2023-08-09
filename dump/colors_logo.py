"""
An example of the determinism of pymunk by coloring balls according to their 
position, and then respawning them to verify each ball ends up in the same 
place. Inspired by Pymunk user Nam Dao.
"""


import os
import random

import pygame

import pymunk
import pymunk.pygame_util


def new_space():
    space = pymunk.Space()
    space.gravity = 0, 900
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (0, -500), (600, -500), 100),  # top -
        pymunk.Segment(static_body, (-30, -500), (-50, 650), 100),  # left |
        pymunk.Segment(static_body, (-50, 650), (600, 650), 100),  # bottom -
        pymunk.Segment(static_body, (650, 650), (630, -500), 100),  # right |
    ]
    for wall in walls:
        wall.elasticity = 0.9

    space.add(*walls)

    random.seed(0)
    return space


def set_colors(color_dict, logo_img, space):
    color_dict.clear()
    w = logo_img.get_width()
    h = logo_img.get_height()
    logo_img.lock()
    for shape in space.shapes:
        if not isinstance(shape, pymunk.Circle):
            continue
        r = shape.body.position.x / 600 * 255
        g = max((shape.body.position.y - 400) / 200 * 255, 0)
        if r < 0 or r > 255 or g < 0 or g > 255:
            print(shape.body.position)
            shape.color = (255, 255, 255, 255)
            continue
        shape.color = (r, g, 150, 255)
        p = shape.body.position
        x = int(p.x) - (600 - w) // 2
        y = int(p.y - 600 + h + 40)
        if x >= 0 and x < w and y > 0 and y < h:
            color = logo_img.get_at([x, y])
            if color.a > 200:
                shape.color = color.r, color.g, color.b, 255
        color_dict[shape.data] = shape.color
    logo_img.unlock()


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
box_surf = pygame.Surface((6, 6))
box_surf.fill(pygame.Color("white"))
draw_options = pymunk.pygame_util.DrawOptions(screen)

color_dict = {}
space = new_space()
cnt = max_cnt = 3000

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.image.save(screen, "colors.png")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if not color_dict:
                set_colors(color_dict, logo_img, space)
            space = new_space()
            cnt = max_cnt
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            set_colors(color_dict, logo_img, space)
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

    if cnt > 0:
        for _ in range(15):
            cnt -= 1
            if cnt < 1:
                continue
            body = pymunk.Body(1, 1)
            x = random.randint(550, 570)
            y = random.randint(30, 100)
            body.position = x, y
            shape = pymunk.Circle(body, 2.5)
            # shape.mass = 1
            shape.data = cnt
            shape.elasticity = 0.9
            if color_dict != None and cnt in color_dict:
                shape.color = color_dict[cnt]
            space.add(body, shape)
    elif cnt == -10 and False:
        cnt -= 1
        exp_p = pymunk.Vec2d(300, 450)
        query_info = space.point_query(exp_p, 50, shape_filter=pymunk.ShapeFilter())
        print(len(query_info))
        for info in query_info:
            if info.shape is None:
                continue
            impulse = (
                (info.shape.body.position - exp_p).normalized()
                * (1 / info.distance)
                * 25000
            )
            impulse = impulse.x, abs(impulse.y)
            info.shape.body.apply_impulse_at_local_point(impulse, (0, 0))

    ### Update physics
    dt = 1.0 / 60.0
    for _ in range(1):
        space.step(dt / 1)

    ### Draw stuff
    screen.fill(pygame.Color("white"))

    color = pygame.Color("blue")
    for shape in space.shapes:
        if not isinstance(shape, pymunk.Circle):
            continue
        if hasattr(shape, "color"):
            color = shape.color

        box_surf.fill(color)
        screen.blit(box_surf, shape.body.position)

    screen.blit(text, (25, 2))

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
