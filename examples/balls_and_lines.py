"""This example lets you dynamically create static walls and dynamic balls

"""
__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk as pm
from pymunk import Vec2d


X,Y = 0,1
### Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
COLLTYPE_BALL = 2


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

def mouse_coll_func(space, arbiter):
    """Simple callback that increases the radius of circles touching the mouse"""
    s1,s2 = arbiter.shapes
    s2.unsafe_set_radius(s2.radius + 0.15)
    return False

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
    
    ### Mouse
    mouse_body = pm.Body()
    mouse_shape = pm.Circle(mouse_body, 3, Vec2d(0,0))
    mouse_shape.collision_type = COLLTYPE_MOUSE
    space.add(mouse_shape)

    space.add_collision_handler(COLLTYPE_MOUSE, COLLTYPE_BALL, None, mouse_coll_func, None, None)   
    
    ### Static line
    line_point1 = None
    static_lines = []
    run_physics = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "balls_and_lines.png")
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                p = event.pos[X], flipy(event.pos[Y])
                body = pm.Body(10, 100)
                body.position = p
                shape = pm.Circle(body, 10, (0,0))
                shape.friction = 0.5
                shape.collision_type = COLLTYPE_BALL
                space.add(body, shape)
                balls.append(shape)
                
            elif event.type == MOUSEBUTTONDOWN and event.button == 3: 
                if line_point1 is None:
                    line_point1 = Vec2d(event.pos[X], flipy(event.pos[Y]))
            elif event.type == MOUSEBUTTONUP and event.button == 3: 
                if line_point1 is not None:
                    
                    line_point2 = Vec2d(event.pos[X], flipy(event.pos[Y]))
                    print line_point1, line_point2
                    body = pm.Body()
                    shape= pm.Segment(body, line_point1, line_point2, 0.0)
                    shape.friction = 0.99
                    space.add(shape)
                    static_lines.append(shape)
                    line_point1 = None
            
            elif event.type == KEYDOWN and event.key == K_SPACE:    
                run_physics = not run_physics
        
        p = pygame.mouse.get_pos()
        mouse_pos = Vec2d(p[X],flipy(p[Y]))
        mouse_body.position = mouse_pos
        
        
        if pygame.key.get_mods() & KMOD_SHIFT and pygame.mouse.get_pressed()[0]:
            body = pm.Body(10, 10)
            body.position = mouse_pos
            shape = pm.Circle(body, 10, (0,0))
            shape.collision_type = COLLTYPE_BALL
            space.add(body, shape)
            balls.append(shape)
       
        ### Update physics
        if run_physics:
            dt = 1.0/60.0
            for x in range(1):
                space.step(dt)
            
        ### Draw stuff
        screen.fill(THECOLORS["white"])

        # Display some text
        font = pygame.font.Font(None, 16)
        text = """LMB: Create ball
LMB + Shift: Create many balls
RMB: Drag to create wall, release to finish
Space: Pause physics simulation"""
        y = 5
        for line in text.splitlines():
            text = font.render(line, 1,THECOLORS["black"])
            screen.blit(text, (5,y))
            y += 10

        for ball in balls:           
            r = ball.radius
            v = ball.body.position
            rot = ball.body.rotation_vector
            p = int(v.x), int(flipy(v.y))
            p2 = Vec2d(rot.x, -rot.y) * r * 0.9
            pygame.draw.circle(screen, THECOLORS["blue"], p, int(r), 2)
            pygame.draw.line(screen, THECOLORS["red"], p, p+p2)

        if line_point1 is not None:
            p1 = line_point1.x, flipy(line_point1.y)
            p2 = mouse_pos.x, flipy(mouse_pos.y)
            pygame.draw.lines(screen, THECOLORS["black"], False, [p1,p2])

        for line in static_lines:
            body = line.body
            
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = pv1.x, flipy(pv1.y)
            p2 = pv2.x, flipy(pv2.y)
            pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
if __name__ == '__main__':
    doprof = 0
    if not doprof: 
        main()
    else:
        import cProfile, pstats
        
        prof = cProfile.run("main()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats('cumulative', 'time', 'calls')
        stats.print_stats(30)
