import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
import pymunk.util as u
from pymunk.vec2d import vec2d
import math, sys, random
X,Y,Z = 0,1,2 # Easy indexing

### Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1


def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def main():
    
    global contact
    global shape_to_remove
        
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    pm.init_pymunk()
    space = pm.Space()
    space.gravity = vec2d(0.0, -900.0)
    
    space.resize_static_hash()
    space.resize_active_hash()
    
    ## Balls
    balls = []
       
    ### walls
    static_body = pm.Body(1e100, 1e100)
    static_lines = [pm.Segment(static_body, vec2d(111.0, 280.0), vec2d(407.0, 246.0), 0.0)
                    ,pm.Segment(static_body, vec2d(407.0, 246.0), vec2d(407.0, 343.0), 0.0)
                    ]    
    space.add_static(static_lines)
    
    ticks_to_next_ball = 10

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            body = pm.Body(10, 100)
            x = random.randint(115,350)
            body.position = x, 400
            shape = pm.Circle(body, 25, vec2d(0,0))
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
            pv1 = body.position + line.a.rotated(math.degrees(body.angle))
            pv2 = body.position + line.b.rotated(math.degrees(body.angle))
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])
            
        for arb in space.arbiters:
            for c in arb.contacts:
                r = max( 3, abs(c.distance*5) )
                r = int(r)
                p = to_pygame(c.position)
                pygame.draw.circle(screen, THECOLORS["red"], p, r, 0)
            
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
    