"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math, sys, random

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)
    
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

### Physics stuff
space = pm.Space()
space.gravity = (0.0, -900.0)

## Balls
balls = []
   
### walls
static_body = pm.Body()
static_lines = [pm.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0)
                ,pm.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                ]  
for line in static_lines:
    line.elasticity = 0.95
space.add(static_lines)

ticks_to_next_ball = 10

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == KEYDOWN and event.key == K_p:
            pygame.image.save(screen, "bouncing_balls.png")
            
    ticks_to_next_ball -= 1
    if ticks_to_next_ball <= 0:
        ticks_to_next_ball = 100
        mass = 10
        radius = 25
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, inertia)
        x = random.randint(115,350)
        body.position = x, 400
        shape = pm.Circle(body, radius, (0,0))
        shape.elasticity = 0.95
        space.add(body, shape)
        balls.append(shape)
    
    ### Clear screen
    screen.fill(THECOLORS["white"])
    
    ### Draw stuff
    balls_to_remove = []
    for ball in balls:
        if ball.body.position.y < 200: balls_to_remove.append(ball)

        p = to_pygame(ball.body.position)
        pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)

    for ball in balls_to_remove:
        space.remove(ball, ball.body)
        balls.remove(ball)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])
        
    ### Update physics
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)
    
    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
