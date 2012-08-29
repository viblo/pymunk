"""Showcase what the output of pymunk.pygame_util draw methods will look like
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys

import pygame
from pygame.locals import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space

def main():
    pygame.init()
    screen = pygame.display.set_mode((600,600)) 
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    
    space = pymunk.Space()
    
    ### Static
    #Static Segments
    segments = [ pymunk.Segment(space.static_body, (10, 50), (10, 500), 1)
                ,pymunk.Segment(space.static_body, (30, 50), (30, 500), 2)
                ,pymunk.Segment(space.static_body, (50, 50), (50, 500), 3)
                ,pymunk.Segment(space.static_body, (70, 50), (70, 500), 5)
                ]  
    space.add(segments)
    
    b = pymunk.Body()
    b.position = (40,530)
    b.angle = 3.14/7
    s = pymunk.Segment(b, (-30,0), (30,0), 2)
    space.add(s)
    
    # Static Circles
    b = pymunk.Body()
    b.position = (150,500)
    s = pymunk.Circle(b, 10)
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,500)
    s = pymunk.Circle(b, 10,(0,-30))
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,400)
    b.angle = 3.14/4
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    # Static Polys
    b = pymunk.Body()
    b.position = (150,300)
    b.angle = 3.14/4
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)])
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,300)
    b.angle = 3.14/2
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)], (-100,0))
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,200)
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)], (0,-100))
    space.add(s)
    
    ### Dynamic
    
    #Dynamic Segments
    b = pymunk.Body(1,1)
    segments = [ pymunk.Segment(b, (210, 50), (210, 500), 1)
                ,pymunk.Segment(b, (230, 50), (230, 500), 2)
                ,pymunk.Segment(b, (250, 50), (250, 500), 3)
                ,pymunk.Segment(b, (270, 50), (270, 500), 5)
                ]  
    space.add(segments)
    
    b = pymunk.Body(1,1)
    b.position = (240,530)
    b.angle = 3.14/7
    s = pymunk.Segment(b, (-30,0), (30,0), 2)
    space.add(s)
    
    # Static Circles
    b = pymunk.Body(1,1)
    b.position = (350,500)
    s = pymunk.Circle(b, 10)
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,500)
    s = pymunk.Circle(b, 10,(0,-30))
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,400)
    b.angle = 3.14/4
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    # Static Polys
    b = pymunk.Body(1,1)
    b.position = (350,300)
    b.angle = 3.14/4
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)])
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,300)
    b.angle = 3.14/2
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)], (-100,0))
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,200)
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)], (0,-100))
    space.add(s)
    
    ###Constraints
    
    # PinJoints
    a = pymunk.Body(1,1)
    a.position = (450,530)
    b = pymunk.Body(1,1)
    b.position = (550,530)
    j = pymunk.PinJoint(a,b)
    space.add(a,b,j)
    
    a = pymunk.Body(1,1)
    a.position = (450,480)
    b = pymunk.Body(1,1)
    b.position = (550,480)
    j = pymunk.PinJoint(a,b, anchr1=(0,20), anchr2=(0,-20))
    space.add(a,b,j)
    
    # SlideJoints
    a = pymunk.Body(1,1)
    a.position = (450,430)
    b = pymunk.Body(1,1)
    b.position = (550,430)
    j = pymunk.SlideJoint(a,b, anchr1=(0,20), anchr2=(0,-20), min=10,max=30)
    space.add(a,b,j)
    
    
    # TODO: more stuff here :)
    
    ### Other
    
    # Object not drawn by draw_space
    b = pymunk.Body()
    b.position = (500,250)
    s = pymunk.Circle(b, 40)
    s.ignore_draw = True
    space.add(s)
    
    # Object in custom color
    b = pymunk.Body()
    b.position = (500,200)
    s = pymunk.Circle(b, 40)
    s.color = pygame.color.THECOLORS["pink"]
    space.add(s)
    
    ### Draw it 
    screen.fill(pygame.color.THECOLORS["black"])
    
    draw_space(screen, space)
                    
    # Info
    screen.blit(font.render("Demo example of shapes drawn by pygame_util.draw_space()", 1, pygame.color.THECOLORS["darkgray"]), (5, 580))
    screen.blit(font.render("Static shapes", 1, pygame.color.THECOLORS["white"]), (50, 20))
    screen.blit(font.render("Dynamic shapes", 1, pygame.color.THECOLORS["white"]), (250, 20))
    screen.blit(font.render("Constraints", 1, pygame.color.THECOLORS["white"]), (450, 20))
    screen.blit(font.render("Other", 1, pygame.color.THECOLORS["white"]), (450, 300))
   
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                return 
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "pygame_util_demo.png")                
                                  
        clock.tick()
        
if __name__ == '__main__':
    sys.exit(main())