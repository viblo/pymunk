"""Showcase what the output of pymunk.pygame_util draw methods will look like.

See pyglet_util_demo.py for a comparison to pyglet.
"""

__docformat__ = "reStructuredText"

import sys

import pygame
from pygame.locals import *
    
import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util

import shapes_for_draw_demos

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000,700)) 
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    
    space = pymunk.Space()
    
    shapes_for_draw_demos.fill_space(space)
            
    ### Draw it 
    screen.fill(pygame.color.THECOLORS["white"])
    
    options = pymunk.pygame_util.DrawOptions(screen)
    space.debug_draw(options)
    #pymunk.pygame_util.draw(screen, space)

    # Info
    color = pygame.color.THECOLORS["black"]
    screen.blit(font.render("Demo example of pygame_util.DrawOptions()", 1, color), (205, 680))
    screen.blit(font.render("Static shapes", 1, color), (50, 20))
    screen.blit(font.render("Kinematic shapes", 1, color), (220, 20))
    screen.blit(font.render("Dynamic shapes", 1, color), (390, 20))
    #screen.blit(font.render("Constraints", 1, pygame.color.THECOLORS["white"]), (450, 20))
    #screen.blit(font.render("ignore_draw=True", 1, pygame.color.THECOLORS["white"]), (10, 530))
    screen.blit(font.render("custom color (static & dynamic)", 1, color), (150, 550))
    screen.blit(font.render("collisions", 1, color), (500, 550))
    screen.blit(font.render("sleeping", 1, color), (50, 670))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                return 
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "pygame_util_demo.png")                
                                  
        clock.tick(10)
        
if __name__ == '__main__':
    sys.exit(main())