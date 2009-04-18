import pygame
from pygame.locals import *
from pygame.color import *

from pymunx import *

def main():
    # PyGame Init
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    # Create the Physical Space Class
    world = pymunx()
    world.set_info("LMB: Create Wall\nRMB: Add Ball\nRMB + Shift: Add Square\nSpace: Pause")
    
    # Add A Wall
    world.add_wall((100, 700), (700, 700))
    
    # Default Settings
    running = True
    draw_wall = False
    points = [(0,0), (0,0)]
    
    # Main Loop
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # Bye Bye
                running = False
                
            elif event.type == KEYDOWN and event.key == K_SPACE:    
                # Pause with SPACE
                world.run_physics = not world.run_physics

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Start/Stop Wall-Drawing 
                if not draw_wall:
                    points[0] = event.pos
                else:
                    points[1] = event.pos
                    world.add_wall(points[0], points[1])
                
                draw_wall = not draw_wall
                
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                key = pygame.key.get_mods()
#                print key

                if key == 4097 or key == 4098:
                    # Shift: Add Square
                    world.add_square(event.pos)
                else:                
                    # Add Ball
                    world.add_ball(event.pos)
            
        # Clear Display
        screen.fill((255,255,255))

        # Update & Draw World
        world.update()
        world.draw(screen)

        # Show line if drawing a wall
        if draw_wall:
            pygame.draw.line(screen, THECOLORS["black"], points[0], pygame.mouse.get_pos())
            
        # Flip Display
        pygame.display.flip()
        
        # Try to stay at 50 FPS
        clock.tick(50)
        
        # output framerate in caption
        pygame.display.set_caption("elements: %i | fps: %s" % (world.element_count, str(int(clock.get_fps()))))

if __name__ == "__main__":
    main()
