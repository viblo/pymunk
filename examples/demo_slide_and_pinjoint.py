import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math, sys, random
X,Y,Z = 0,1,2 # Easy indexing

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    pm.init_pymunk()
    space = pm.Space()
    space.gravity = Vec2d(0.0, -900.0)
    
    space.resize_static_hash()
    space.resize_active_hash()
    
    ## Balls
    balls = []
       
    ### static stuff
    rot_center_body = pm.Body(1e100, 1e100)
    rot_center_body.position = Vec2d(300,300)
    
    ### To hold back the L
    rot_limit_body = pm.Body(1e100, 1e100)
    rot_limit_body.position = Vec2d(200,300)
       
    ### The moving L shape
    l1 = [Vec2d(-150, 0), Vec2d(255.0, 0.0)]
    l2 = [Vec2d(-150.0, 0), Vec2d(-150.0, 50.0)]
    
    body = pm.Body(10,10000)
    body.position = Vec2d(300,300)
    
    lines = [pm.Segment(body, l1[0], l1[1], 5.0) 
                ,pm.Segment(body, l2[0], l2[1], 5.0)
                ]

    space.add(body)
    space.add(lines)
    
    ### The L rotates around this
    rot_center = pm.PinJoint(body, rot_center_body, Vec2d(0,0), Vec2d(0,0))
    ### And is constrained by this
    joint_limit = 25
    rot_limit = pm.SlideJoint(body, rot_limit_body, Vec2d(-100,0), Vec2d(0,0), 0, joint_limit)
    space.add(rot_center, rot_limit)
    
    ticks_to_next_ball = 10

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            mass = 1
            radius = 14
            inertia = pm.moment_for_circle(mass, 0, radius, Vec2d(0,0))
            body = pm.Body(mass, inertia)
            x = random.randint(120,380)
            body.position = x, 550
            shape = pm.Circle(body, radius, Vec2d(0,0))
            space.add(body, shape)
            balls.append(shape)
        
        ### Clear screen
        screen.fill(THECOLORS["white"])
        
        ### Draw stuff
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 150: balls_to_remove.append(ball)

            p = to_pygame(ball.body.position)
            pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)
    
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        for line in lines:
            body = line.body
            pv1 = body.position + line.a.rotated(math.degrees(body.angle))
            pv2 = body.position + line.b.rotated(math.degrees(body.angle))
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])
        
        ### The rotation center of the L shape        
        pygame.draw.circle(screen, THECOLORS["red"], to_pygame(rot_center_body.position), 5)
        ### The limits where it can move.
        pygame.draw.circle(screen, THECOLORS["green"], to_pygame(rot_limit_body.position), joint_limit, 2)

        ### Update physics
        dt = 1.0/50.0/10.0
        for x in range(10):
            space.step(dt)
        
        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        
        
if __name__ == '__main__':
    sys.exit(main())
    