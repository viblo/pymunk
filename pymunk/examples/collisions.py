"""This example attempts to display collision points, and the callbacks
"""

import math
import random
import sys

import pygame

import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


def begin(arbiter, space, data):
    data["log"] = {
        "begin": 1,
        "pre_solve": 0,
        "post_solve": "N/A (no post_solve for sensors)",
        "separate": 0,
    }

    return True


def pre_solve(arbiter: pymunk.Arbiter, space, data):
    data["log"]["pre_solve"] += 1

    screen = data["screen"]

    screen.blit(
        data["font"].render(
            "collision normal",
            True,
            pygame.Color("black"),
        ),
        (5, 500),
    )
    n = arbiter.normal * 30
    pygame.draw.aaline(screen, pygame.Color("red"), (50, 550), (50 + n.x, 550 + n.y))

    cps: pymunk.ContactPointSet = arbiter.contact_point_set
    for p in cps.points:
        pygame.draw.circle(screen, pygame.Color("darkblue"), p.point_a, 5, 1)
        pygame.draw.circle(screen, pygame.Color("darkred"), p.point_b, 5, 1)
        pygame.draw.aaline(screen, pygame.Color("yellow"), p.point_a, p.point_b)

        screen.blit(
            data["font"].render(
                f"distance {p.distance:.2f}",
                True,
                pygame.Color("black"),
            ),
            (p.point_a.interpolate_to(p.point_b, 0.5)),
        )

    return True


def post_solve(arbiter, space, data):
    # Will not be called, since the shapes are kinematic sensors
    pass


def separate(arbiter, space, data):
    data["log"]["separate"] += 1
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 20)

    space = pymunk.Space()
    # space.gravity = Vec2d(0.0, 900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    segment_body.position = 600, 200
    segment = pymunk.Segment(segment_body, Vec2d(-100, 0), Vec2d(100, 0), 5)
    segment.sensor = True
    space.add(segment_body, segment)

    circle_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    circle_body.position = 200, 300
    circle = pymunk.Circle(circle_body, 50)
    circle.sensor = True
    space.add(circle_body, circle)

    poly_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    poly_body.position = 600, 400
    poly = pymunk.Poly.create_box(poly_body, (200, 100), 10)
    poly.sensor = True
    space.add(poly_body, poly)

    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    space.add(mouse_body)

    circle = pymunk.Circle(mouse_body, 60)
    circle.sensor = True
    circle.collision_type = 1
    segment = pymunk.Segment(mouse_body, Vec2d(-100, 0), Vec2d(100, 0), 20)
    segment.sensor = True
    segment.collision_type = 1
    poly = pymunk.Poly.create_box(mouse_body, (200, 100), 10)
    poly.sensor = True
    poly.collision_type = 1

    shapes = [circle, segment, poly]
    selected_shape_idx = 0
    space.add(shapes[selected_shape_idx])

    h = space.add_collision_handler(0, 1)
    h.data["screen"] = screen
    h.data["log"] = {"begin": 0, "pre_solve": 0, "post_solve": 0, "separate": 0}
    h.data["font"] = font
    h.begin = begin
    h.pre_solve = pre_solve
    h.post_solve = post_solve
    h.separate = separate

    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "collisions.png")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                space.remove(shapes[selected_shape_idx])
                selected_shape_idx = (selected_shape_idx + 1) % len(shapes)
                space.add(shapes[selected_shape_idx])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_body.angle += math.pi / 8

        p = pygame.mouse.get_pos()
        mouse_body.position = p[0], p[1]

        screen.fill(pygame.Color("white"))
        space.debug_draw(draw_options)

        screen.blit(
            font.render(
                "Left click to switch shape type, right click to rotate. (The shape follows the mouse)",
                True,
                pygame.Color("black"),
            ),
            (5, 5),
        )

        y = 30
        for k in h.data["log"]:
            screen.blit(
                font.render(
                    f"{k}: {h.data['log'][k]}",
                    True,
                    pygame.Color("black"),
                ),
                (5, y),
            )
            y += 20

        space.step(1.0 / 60.0)

        pygame.display.flip()
        clock.tick(50)


if __name__ == "__main__":
    sys.exit(main())
