"""
Fun example
"""


import math
import os
import random
import time

import pygame

import pymunk
import pymunk.pygame_util


def new_space():
    space = pymunk.Space()
    space.gravity = 0, 900
    static_body = space.static_body
    walls = [
        # pymunk.Segment(static_body, (-30, -30), (630, -30), 50),  # top -
        pymunk.Segment(static_body, (-30, 150), (630, 150), 50),  # top -
        pymunk.Segment(static_body, (-30, -30), (-30, 630), 50),  # left |
        pymunk.Segment(static_body, (-30, 630), (630, 630), 50),  # bottom -
        pymunk.Segment(static_body, (630, 630), (630, -30), 50),  # right |
    ]
    y = 1
    # for x in range(0, 600, 100):
    #     y += 1
    #     y %= 2
    #     walls.append(
    #         pymunk.Segment(
    #             static_body, (x, 600 - y * 50), (x + 100, 600 - (y + 1) % 2 * 50), 1
    #         )
    #     )
    # walls.append(pymunk.Segment(static_body, (200, 600), (300, 500), 1))
    # walls.append(pymunk.Segment(static_body, (300, 500), (400, 600), 1))
    # walls.append(pymunk.Segment(static_body, (250, 500), (350, 500), 50))
    # walls.append(pymunk.Segment(static_body, (250, 500), (350, 500), 50))
    box_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    box_body.position = 300 + 1, 600 - 20 - 16 - 50 + 1
    space.add(box_body)
    walls.append(pymunk.Poly.create_box(box_body, (200 - 1, 32 - 1)))
    for wall in walls:
        wall.elasticity = 1
        wall.friction = 1.0

    space.add(*walls)

    random.seed(0)
    return space


def limit_velocity(body, gravity, damping, dt):
    max_velocity = 1000
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale


def spawn(logo_img, space):
    cnt = 0
    r = 2
    w = logo_img.get_width()
    h = logo_img.get_height()
    offset_x = 300 - w / 2
    offset_y = 300 - h / 2
    logo_img.lock()
    for x in range(0, w, r * 2):
        for y in range(0, h, r * 2):
            color = logo_img.get_at([x, y])
            if color.a > 200 and color.r + color.g + color.b < 250 + 250 + 250:
                cnt += 1
                body = pymunk.Body()
                body.position = x + offset_x + random.random() / 5, y + offset_y

                # body.velocity_func = limit_velocity

                shape = pymunk.Circle(body, r * 0.999)
                # shape = pymunk.Poly.create_box(body, (r * 2, r * 2))
                shape.mass = 1
                shape.elasticity = 0.99999
                # shape.friction = 1
                shape.color = color.r, color.g, color.b, 255
                space.add(body, shape)
                impulse = (body.position - pymunk.Vec2d(300, 300)) * 1
                impulse = (
                    pymunk.Vec2d(random.random() - 0.5, random.random() - 0.5) * 20000
                )
                # body.apply_impulse_at_local_point(impulse, (0, 0))
    print(f"total cnt {cnt}")
    return r


def draw_ticks(screen: pygame.surface.Surface, font: pygame.font.Font, started=False):
    if not started:
        t = 0
    else:
        try:
            t = time.time() - draw_ticks.start_time
        except:
            draw_ticks.start_time = time.time()
            t = 0
    try:
        draw_ticks.slowmotion += 1
        draw_ticks.slowmotion %= 6
    except:
        draw_ticks.slowmotion = 0
    if dt < 1 / 60 / 4 and draw_ticks.slowmotion < 30 and False:
        msg = f"00:{draw_ticks.total_dt:05.2f} (SLOW MOTION)"
    else:
        msg = f" 00:{t/6:05.2f} "
    text = font.render(
        msg,
        False,
        (255, 255, 255, 255),
        (75, 75, 75, 255),
        # (0, 0, 0, 50),
    )
    text = pygame.transform.scale_by(text, 4)
    # screen.blit(text, (25, 600 - text.get_height() - 400))
    screen.blit(text, (300 - text.get_width() / 2, 600 - text.get_height() - 20 - 50))


def draw_border(screen):
    pygame.draw.lines(
        screen,
        (75, 75, 75, 255),
        False,
        # [(0, 0), (0, 600), (600, 600), (600, -50), (0, -50)],
        # [(0, 0), (0, 600), (600, 600), (600, 180), (192, 180)],
        [(0, 0), (0, 600), (600, 600), (600, 180), (0, 180)],
        40,
    )


def get_dt(steps):
    steps += 1
    dt = 1.0 / 60.0 / (1 + 200**2 / steps**2)
    dt = 1.0 / 60.0 / (1 + 50**2 / steps**2) / 4
    dt = 1 / 60 / 6
    return dt, steps


pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("lucidaconsole", 8)


logo_img = pygame.image.load(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "pymunk_logo_sphinx.png")
)

draw_options = pymunk.pygame_util.DrawOptions(screen)


space = new_space()
space2 = new_space()
radius = spawn(logo_img, space)

radius = spawn(logo_img, space2)
box_surf = pygame.Surface((radius * 2, radius * 2))


positions = []
total_steps = 750
steps = 0
while total_steps > 0:
    total_steps -= 1
    dt, steps = get_dt(steps)
    space2.step(dt)
    step_positions = []
    for shape in space2.shapes:
        if not isinstance(shape, pymunk.Circle):
            continue
        step_positions.append(
            (
                shape.color,
                shape.body.position - (shape.radius, shape.radius),
                shape.body.angle * 360 / math.pi / 2,
            )
        )
    positions.append((step_positions, dt))

paused = True
while paused:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            exit()
        elif event.type == pygame.KEYDOWN:
            paused = False
    screen.fill(pygame.Color("white"))
    draw_border(screen)
    draw_ticks(screen, font, 0)
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

positions.reverse()
for step_positions, dt in positions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()

    screen.fill(pygame.Color("white"))

    for color, position, angle in step_positions:
        box_surf.fill(color)
        # pygame.draw.rect(box_surf, color, (radius, radius, radius * 2, radius * 2))
        # rotated = pygame.transform.rotate(box_surf, angle)
        screen.blit(box_surf, position)
        # screen.blit(box_surf, position)
    draw_border(screen)
    draw_ticks(screen, font, dt)

    pygame.display.flip()
    clock.tick(60)
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
            exp_p = pymunk.Vec2d(300, 550)
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

    dt, steps = get_dt(steps)
    space.step(dt)

    screen.fill(pygame.Color("white"))

    for shape in space.shapes:
        if isinstance(shape, pymunk.Poly):
            continue
            vs = []
            for v in shape.get_vertices():
                x, y = v.rotated(shape.body.angle) + shape.body.position
                vs.append((int(x), int(y)))
            pygame.draw.polygon(screen, (155, 0, 0, 255), vs)
            continue
        elif not isinstance(shape, pymunk.Circle):
            continue
        color = shape.color

        box_surf.fill(color)
        screen.blit(box_surf, shape.body.position - (shape.radius, shape.radius))
    draw_border(screen)
    draw_ticks(screen, font, dt)

    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
