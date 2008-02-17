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


def flipy(y):
    """Small hack to convert pymunk to pygame coordinates"""
    return -y+600

def coll_func(shapeA, shapeB, contacts, normal_coef, screen):
    """Draw a circle at the contact, with larger radius for greater collisions"""
    for c in contacts:
        r = max( 3, abs(c.distance*5) )
        p = c.position.x, flipy(c.position.y)
        pygame.draw.circle(screen, THECOLORS["red"], p, r, 0)
    return True

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

    ### Here we set the collision callback function
    space.set_default_collisionpair_func(coll_func, screen)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 10
            radius = 25
            inertia = pm.moment_for_circle(mass, 0, radius, vec2d(0,0))
            body = pm.Body(mass, inertia)
            x = random.randint(115,350)
            body.position = x, 400
            shape = pm.Circle(body, radius, vec2d(0,0))
            space.add(body, shape)
            balls.append(shape)
        
        ### Clear screen
        screen.fill(THECOLORS["white"])
        
        ### Draw stuff
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 200: balls_to_remove.append(ball)

            p = ball.body.position.x, flipy(ball.body.position.y)
            pygame.draw.circle(screen, THECOLORS["blue"], p, ball.radius, 2)
    
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        for line in static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(math.degrees(body.angle))
            pv2 = body.position + line.b.rotated(math.degrees(body.angle))
            p1 = pv1.x, flipy(pv1.y)
            p2 = pv2.x, flipy(pv2.y)
            pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])

        ### Update physics
        # (this will also draw the contacts)
        dt = 1.0/60.0
        for x in range(1):
            space.step(dt)
        
        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
if __name__ == '__main__':
    sys.exit(main())
    