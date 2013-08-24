"""This example showcase point queries by highlighting the shape under the 
mouse pointer.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import random
import sys

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk as pm
from pymunk import Vec2d
import pymunk.pygame_util


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    space = pm.Space()
    space.gravity = Vec2d(0.0, -900.0)
    
    ## Balls
    balls = []
       
    ### walls
    static_lines = [pm.Segment(space.static_body, Vec2d(111.0, 280.0), Vec2d(407.0, 246.0), 1.0)
                    ,pm.Segment(space.static_body, Vec2d(407.0, 246.0), Vec2d(407.0, 343.0), 1.0)
                    ]    
    space.add(static_lines)
    
    ticks_to_next_ball = 10


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "point_query.png")
                
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 10
            radius = 25
            inertia = pm.moment_for_circle(mass, 0, radius, Vec2d(0,0))
            body = pm.Body(mass, inertia)
            x = random.randint(115,350)
            body.position = x, 400
            shape = pm.Circle(body, radius, Vec2d(0,0))
            shape.color = THECOLORS["lightgrey"]
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

        mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)

        shape = space.point_query_first(mouse_pos)
        if shape is not None:
            if hasattr(shape, "radius"):
                r = shape.radius + 4
            else:
                r = 10
            p = pymunk.pygame_util.to_pygame(shape.body.position, screen)
            pygame.draw.circle(screen, THECOLORS["red"], p, int(r), 2)
        
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
