"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Displays collsion strength and rotating balls thanks to 
friction. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math, sys, random

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk as pm
from pymunk import Vec2d
import pymunk.pygame_util


def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def draw_collision(space, arb, surface):
    for c in arb.contacts:
        r = max( 3, abs(c.distance*5) )
        r = int(r)
        p = to_pygame(c.position)
        pygame.draw.circle(surface, THECOLORS["black"], p, r, 1)
    
def main():
    
    global contact
    global shape_to_remove
        
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
    static_lines = [pm.Segment(space.static_body, (11.0, 280.0), (407.0, 246.0), 0.0)
                    ,pm.Segment(space.static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)
    
    ticks_to_next_ball = 10
    
    space.add_collision_handler(0, 0, None, None, draw_collision, None, surface=screen)
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "contact_with_friction.png")
                
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 0.1
            radius = 25
            inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
            body = pm.Body(mass, inertia)
            x = random.randint(115,350)
            body.position = x, 400
            shape = pm.Circle(body, radius, (0,0))
            shape.friction = 0.5
            space.add(body, shape)
            balls.append(shape)
        
        ### Clear screen
        screen.fill(THECOLORS["white"])
        
        ### Draw stuff
        pymunk.pygame_util.draw(screen, space)
        
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 200: balls_to_remove.append(ball)
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)
            
        ### Update physics
        dt = 1.0/60.0
        for x in range(1):
            space.step(dt)
        
        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
if __name__ == '__main__':
    sys.exit(main())
