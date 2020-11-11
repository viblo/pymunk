"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. For each collision it draws a red circle with size 
depending on collision strength. Not interactive.
"""

import random
import sys

import pygame

import pymunk as pm
from pymunk import Vec2d


def draw_collision(arbiter, space, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)
        p = tuple(map(int, c.point_a))
        pygame.draw.circle(data["surface"], pygame.Color("red"), p, r, 0)


def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pm.Space()
    space.gravity = (0.0, 900.0)

    ## Balls
    balls = []

    ### walls
    static_lines = [
        pm.Segment(space.static_body, (111.0, 320.0), (407.0, 354.0), 0.0),
        pm.Segment(space.static_body, (407.0, 354.0), (407.0, 257.0), 0.0),
    ]
    space.add(*static_lines)

    ticks_to_next_ball = 10

    ch = space.add_collision_handler(0, 0)
    ch.data["surface"] = screen
    ch.post_solve = draw_collision

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "contact_and_no_flipy.png")

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 10
            radius = 25
            inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
            body = pm.Body(mass, inertia)
            x = random.randint(115, 350)
            body.position = x, 200
            shape = pm.Circle(body, radius, (0, 0))
            space.add(body, shape)
            balls.append(shape)

        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y > 400:
                balls_to_remove.append(ball)
            p = tuple(map(int, ball.body.position))
            pygame.draw.circle(screen, pygame.Color("blue"), p, int(ball.radius), 2)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        for line in static_lines:
            body = line.body
            p1 = tuple(map(int, body.position + line.a.rotated(body.angle)))
            p2 = tuple(map(int, body.position + line.b.rotated(body.angle)))
            pygame.draw.lines(screen, pygame.Color("lightgray"), False, [p1, p2])

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    sys.exit(main())
