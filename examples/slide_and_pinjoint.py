"""A L shape attached with a joint and constrained to not tip over.

This example is also used in the Get Started Tutorial. 
"""

__docformat__ = "reStructuredText"

import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
import math

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 1
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(120,380)
    body.position = x, 550
    shape = pymunk.Circle(body, radius, (0,0))
    space.add(body, shape)
    return shape

def draw_ball(screen, ball):
    """Draw a ball shape"""
    p = int(ball.body.position.x), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)

def add_L(space):
    """Add a inverted L shape with two joints"""
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (300,300)

    rotation_limit_body = pymunk.Body(body_type = pymunk.Body.STATIC) # 1
    rotation_limit_body.position = (200,300)

    body = pymunk.Body(10, 10000)
    body.position = (300,300)
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit) # 3

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1,l2

def draw_lines(screen, lines):
    """Draw the lines"""
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    lines = add_L(space)
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)


    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        screen.fill(THECOLORS["white"])

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 150:
                balls_to_remove.append(ball)
            #draw_ball(screen, ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        space.debug_draw(draw_options)


        #pygame.draw.circle(screen, THECOLORS["red"], (300,300), 5)
        #pygame.draw.circle(screen, THECOLORS["green"], (200,300), 25, 2)

        space.step(1/50.0)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())
