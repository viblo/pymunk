*************************************
Arrows and other pointy sticky things
*************************************

.. attention::
    This tutorial is work in progress. Take a look at the arrows.py example file 
    in :ref:`Examples <examples>` for fully working code for the arrows.

This tutorial will explain one way to make arrows/sticky projectiles that can stick on the target. 

The tutorial is heavily inspired by the Box2d tutorial "Box2D C++ tutorials - Sticky projectiles" found
here http://www.iforce2d.net/b2dtut/sticky-projectiles (but adjusted for python, pymunk and chipmunk).

Before we start
===================

For this tutorial you will need to know some pymunk basics. I recommend that you read the other tutorial(s) 
and try out easier examples first before you continue. 

Except for pymunk you will also need pygame to follow this tutorial. However, it should be no problem to 
use another graphics and input library if you want, for example pyglet.

We will try to accomplish 

* An arrow that flies believable in the air
* Figure out when the arrow hits something and should stick
* Attach the arrow to an object when hit
    
In the end we should have a cannon like object shooting arrows that flies in a believable way and sticks to 
objects if they hit hard enough. 
    
Basic scene
=======================

Before we start with the arrow we need a scene to contain it and a "cannon" that can aim::

    import sys

    import pygame
    from pygame.locals import *
    from pygame.color import *
        
    import pymunk
    from pymunk.vec2d import Vec2d
    from pymunk.pygame_draw import draw_space, from_pygame

    width = height = 600
    def main():
        ### PyGame init
        pygame.init()
        screen = pygame.display.set_mode((width,height)) 
        clock = pygame.time.Clock()
        running = True
        font = pygame.font.SysFont("Arial", 16)
        
        ### Physics stuff
        space = pymunk.Space()   
        
        # walls - the left-top-right-bottom walls
        static_lines = [pymunk.Segment(space.static_body, (50, 50), (50, 550), 5)
                    ,pymunk.Segment(space.static_body, (50, 550), (550, 550), 5)
                    ,pymunk.Segment(space.static_body, (550, 550), (550, 50), 5)
                    ,pymunk.Segment(space.static_body, (50, 50), (550, 50), 5)
                    ]  
        space.add_static(static_lines)
        
        ### "Cannon" that can fire arrows
        cannon_body = pymunk.Body()
        player_shape = pymunk.Circle(cannon_body, 25)
        cannon_body.position = 100,100
        
        space.add(player_shape)
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or \
                    event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                    running = False
                            
            mpos = pygame.mouse.get_pos()
            p = from_pygame( Vec2d(mpos), screen )
            mouse_position = p
            cannon_body.angle = (mouse_position - cannon_body.position).angle
            
            ### Clear screen
            screen.fill(pygame.color.THECOLORS["black"])
            
            ### Draw stuff
            draw_space(screen, space)
                
            ### Update physics
            fps = 60
            dt = 1./fps
            space.step(dt)
            
            ### Info and flip screen
            screen.blit(font.render("fps: " + str(clock.get_fps()), 1, THECOLORS["white"]), (0,0))
            screen.blit(font.render("Aim with mouse, click to fire", 1, THECOLORS["darkgrey"]), (5,height - 35))
            screen.blit(font.render("Press R to reset, ESC or Q to quit", 1, THECOLORS["darkgrey"]), (5,height - 20))
            
            pygame.display.flip()
            clock.tick(fps)

    if __name__ == '__main__':
        sys.exit(main())
    

