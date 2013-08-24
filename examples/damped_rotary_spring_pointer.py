"""This example showcase an arrow pointing or aiming towards the cursor.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys
import random
import math

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    space = pymunk.Space()
                
    pointer_body = pymunk.Body()
    
    ps = [(80,0),(0,20),(0,-20)]
    moment = pymunk.moment_for_poly(1, ps)
    gun_body = pymunk.Body(1, moment)
    gun_body.position = 300,300
    gun_shape = pymunk.Poly(gun_body, ps)
    
    rest_angle = 0
    stiffness = 125000.
    damping = 6000.
    
    rotary_spring = pymunk.constraint.DampedRotarySpring(pointer_body, gun_body, rest_angle, stiffness, damping)
    
    space.add(gun_body, gun_shape, rotary_spring)
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "aiming.png")
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
                pointer_body.position = mouse_pos
                pointer_body.angle = (pointer_body.position - gun_body.position).angle
               
            # to easily find good values for the damped rortary spring
            # as with most simulations done with pymunk, the imporant thing 
            # is that it looks good, not the exact parameters
            elif event.type == KEYDOWN and event.key == K_q:
                rotary_spring.stiffness *= .5
                print rotary_spring.stiffness, rotary_spring.damping
            elif event.type == KEYDOWN and event.key == K_w:
                rotary_spring.stiffness *= 2
                print rotary_spring.stiffness, rotary_spring.damping
            elif event.type == KEYDOWN and event.key == K_a:
                rotary_spring.damping *= .5
                print rotary_spring.stiffness, rotary_spring.damping
            elif event.type == KEYDOWN and event.key == K_s:
                rotary_spring.damping *= 2
                print rotary_spring.stiffness, rotary_spring.damping
                
        ### Clear screen
        screen.fill(THECOLORS["white"])
        
        ### Draw stuff
        pymunk.pygame_util.draw(screen, space)
        
        ### Update physics
        dt = 1.0/60.0
        for x in range(1):
            space.step(dt)
                
        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        
if __name__ == '__main__':
    sys.exit(main())
