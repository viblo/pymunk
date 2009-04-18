import pygame
from pygame.locals import *
from pygame.color import *

from math import fabs
from pymunx import *

def blit_arrow(surface, a, b):
    pygame.draw.line(surface, (237, 248, 247), a, b, 6)

def main():
    # PyGame Init
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()

    # Create the Physical Space Class
    default_size = 18
    default_elasticity = 0.9
    default_density = 0.1
    default_friction = 0.3
    default_inertia = 10.0
    
    key_up = False
    key_down = False

    world = pymunx()
    world.set_info("F1 or h: Toggle Help \n\nLMB: Add ball, throw ball or draw a shape \nRMB: Add box, or throw one \n\nMouse-Wheel or Arrow Keys: Size [ %i m ] \n  + CTRL: Elasticity [ %.2f ] \n  + Shift:  Density [ %.2f ] \n  + Alt:     Friction [ %.2f ] \n\nc: Clear \nf: Fullscreen \nSpace: Pause\n1: Add many balls\n2: Add many squares \n\ns: Screenshot \n[,]: Start Screencast \n[.]: Stop Screencast " % (default_size, default_elasticity, default_density, default_friction))
    
    # Add A Wall
    x,y,w,h = pygame.display.get_surface().get_rect()
    world.add_wall((0, 0), (0, h), default_friction, default_elasticity)
    world.add_wall((0, h), (w, h), default_friction, default_elasticity)
    world.add_wall((w, h), (w, 0), default_friction, default_elasticity)
    world.add_wall((w, 0), (0, 0), default_friction, default_elasticity)

    # Default Settings
    running = True
    draw_poly = False
    draw_arrow = False
    points = []
    
    # Main Loop
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # Bye Bye
                running = False
                
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:    
                    # Pause with SPACE
                    world.run_physics = not world.run_physics

                elif event.key == 282 or event.unicode == "h":
                    world.toggle_help()

                elif event.unicode == "c": 
                    world.clear()
                    x,y,w,h = pygame.display.get_surface().get_rect()
                    world.add_wall((0, 0), (0, h), default_friction, default_elasticity)
                    world.add_wall((0, h), (w, h), default_friction, default_elasticity)
                    world.add_wall((w, h), (w, 0), default_friction, default_elasticity)
                    world.add_wall((w, 0), (0, 0), default_friction, default_elasticity)
                    
                elif event.unicode == "f":
                    pygame.display.toggle_fullscreen()
    
                elif event.unicode == "s":
                    world.screenshot()

                elif event.unicode == ",":
                    world.screencast_start("demo7")
                    
                elif event.unicode == ".":
                    world.screencast_stop()

                elif event.key == 273 or event.key == 275:
                    # Start: Hold Up
                    key_up = True

                elif event.key == 274 or event.key == 276:
                    # Start: Hold Down
                    key_down = True
                
                elif event.unicode == "1":
                    # Add many Balls
                    x, y = pygame.mouse.get_pos()
                    for i in range(5):
                        for j in range(5): 
                            world.add_ball((x-i,y-j), default_size, default_density, default_inertia, default_friction, default_elasticity)

                elif event.unicode == "2":
                    # Add many Balls
                    x, y = pygame.mouse.get_pos()
                    for i in range(5):
                        for j in range(5): 
                            world.add_square((x-i,y-j), default_size, default_density, default_friction, default_elasticity)

                elif event.unicode == "3":
                    if world.fixed_color:
                        world.reset_color()
                    else:
                        world.set_color((0, 0, 0))


            elif (event.type == MOUSEBUTTONDOWN and (event.button == 4 or event.button == 5)) or (event.type == KEYUP and (event.key in [273, 274, 275, 276])):
                # Change Settings with the Mouse Wheel or Up/Down (+Right/Left)
                key = pygame.key.get_mods()
                if event.type == KEYUP:
                    key_up = False
                    key_down = False
                
                if (event.type == MOUSEBUTTONDOWN and event.button == 4) or (event.type == KEYDOWN and (event.key == 273 or event.key == 275)):
                    # MW UP
                    if key == 4160 or key == 4224: # Ctrl
                        default_elasticity += 0.02
                        if default_elasticity > 1.6:
                            default_elasticity = 1.6
                            
                    elif key == 4097 or key == 4098: # Shift
                        default_density += 0.02 
                        
                    elif key == 4352: # Alt
                        default_friction += 0.02
                        
                    else: default_size += 2
                else:
                    # MW DOWN
                    if key == 4160 or key == 4224: # Ctrl
                        default_elasticity -= 0.02
                        if default_elasticity < 0.0:
                            default_elasticity = 0.0
                    
                    elif key == 4097 or key == 4098: # Shift
                        default_density -= 0.02
                        if default_density < 0.02:
                            default_density = 0.02

                    elif key == 4352: # Alt
                        default_friction -= 0.02
                        if default_friction < 0:
                            default_friction = 0.0
                        
                    else: 
                        default_size -= 2
                        if default_size < 4:
                            default_size = 4

                world.set_info("F1 or h: Toggle Help \n\nLMB: Add ball, throw ball or draw a shape \nRMB: Add box, or throw one \n\nMouse-Wheel or Arrow Keys: Size [ %i m ] \n  + CTRL: Elasticity [ %.2f ] \n  + Shift:  Density [ %.2f ] \n  + Alt:     Friction [ %.2f ] \n\nc: Clear \nf: Fullscreen \nSpace: Pause\n1: Add many balls\n2: Add many squares \n\ns: Screenshot \n[,]: Start Screencast \n[.]: Stop Screencast " % (default_size, default_elasticity, default_density, default_friction))

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Start Wall-Drawing 
                if not draw_poly:
                    draw_poly = True
                    points = []
                    points.append(event.pos)

            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                if not draw_arrow:
                    draw_arrow = True
                    points = []
                    points.append(event.pos)

            elif event.type == MOUSEBUTTONUP and event.button == 3:
                if draw_arrow:
                    # Throw Box
                    draw_arrow = False
                    x1, y1 = points[0]
                    x2, y2 = event.pos
                    x = x2 - x1
                    y = y2 - y1
                    l = sqrt((x*x)+(y*y)) * 1.8
                    box = world.add_square(points[0], default_size, default_density, default_friction, default_elasticity)
                    world.apply_impulse(box, (x*l, y*l))
                    
                else:
                    # Don't Throw, Just Append :)
                    world.add_square(event.pos, default_size, default_density, default_friction, default_elasticity)
            
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if draw_poly:
                    # Create Polygon
                    draw_poly = False
                    points.append(event.pos)

                    if len(points) < 5: 
                        world.add_ball(event.pos, default_size, default_density, default_inertia, default_friction, default_elasticity)
                    
                    else:
                        # Draw Poly or Segment
                        # Poly if Start and End are close to each other
                        x1, y1 = points[0]
                        x2, y2 = points[-1]
                        x = x2 - x1
                        y = y2 - y1

                        if fabs(x) > 100 or fabs(y) > 100:
                            # Throw Ball
                            l = sqrt((x*x)+(y*y)) * 1.8
                            ball = world.add_ball(points[0], default_size, default_density, default_inertia, default_friction, default_elasticity)
                            world.apply_impulse(ball, (x*l, y*l))

                        else:
                            world.add_poly(points, default_density, default_friction, default_elasticity)

            elif event.type == MOUSEMOTION and (draw_poly or draw_arrow):
                points.append(event.pos)
                
            
        # Clear Display
        screen.fill((255,255,255))

        # Update & Draw World
        world.update()
        world.draw(screen)

        # For holding Up/Down, call often
        if key_up:
            pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN, {'button' : 4}))
        elif key_down:
            pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN, {'button' : 5}))


        # Show line if drawing a wall
        if len(points) > 1:
            if draw_poly:
                pygame.draw.lines(screen, THECOLORS["black"], False, points)
            elif draw_arrow:
                blit_arrow(screen, points[0], points[-1])

        # Flip Display
        pygame.display.flip()
        
        # Try to stay at 50 FPS
        clock.tick(50)
        
        # output framerate in caption
        pygame.display.set_caption("elements: %i | fps: %s" % (world.get_element_count(), str(int(clock.get_fps()))))

if __name__ == "__main__":
    main()
