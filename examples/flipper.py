"""A very basic flipper game.
"""
__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import random

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)
    
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

### Physics stuff
space = pymunk.Space(50)
space.gravity = (0.0, -900.0)

## Balls
balls = []
   
### walls
static_body = pymunk.Body()
static_lines = [pymunk.Segment(static_body, (150, 100.0), (50.0, 550.0), 1.0)
                ,pymunk.Segment(static_body, (450.0, 100.0), (550.0, 550.0), 1.0)
                ,pymunk.Segment(static_body, (50.0, 550.0), (300.0, 600.0), 1.0)
                ,pymunk.Segment(static_body, (300.0, 600.0), (550.0, 550.0), 1.0)
                ,pymunk.Segment(static_body, (300.0, 420.0), (400.0, 400.0), 1.0)
                ]  
for line in static_lines:
    line.elasticity = 0.7
    line.group = 1
space.add(static_lines)

fp = [(20,-20), (-120, 0), (20,20)]
mass = 100
moment = pymunk.moment_for_poly(mass, fp)

# right flipper
r_flipper_body = pymunk.Body(mass, moment)
r_flipper_body.position = 450, 100
r_flipper_shape = pymunk.Poly(r_flipper_body, fp)
space.add(r_flipper_body, r_flipper_shape)

r_flipper_joint_body = pymunk.Body()
r_flipper_joint_body.position = r_flipper_body.position 
j = pymunk.PinJoint(r_flipper_body, r_flipper_joint_body, (0,0), (0,0))
#todo: tweak values of spring better
s = pymunk.DampedRotarySpring(r_flipper_body, r_flipper_joint_body, 0.15, 20000000,900000)
space.add(j, s)

# left flipper
l_flipper_body = pymunk.Body(mass, moment)
l_flipper_body.position = 150, 100
l_flipper_shape = pymunk.Poly(l_flipper_body, [(-x,y) for x,y in fp])
space.add(l_flipper_body, l_flipper_shape)

l_flipper_joint_body = pymunk.Body()
l_flipper_joint_body.position = l_flipper_body.position 
j = pymunk.PinJoint(l_flipper_body, l_flipper_joint_body, (0,0), (0,0))
s = pymunk.DampedRotarySpring(l_flipper_body, l_flipper_joint_body, -0.15, 20000000,900000)
space.add(j, s)

r_flipper_shape.group = l_flipper_shape.group = 1
r_flipper_shape.elasticity = l_flipper_shape.elasticity = 0.4

# "bumpers"
for p in [(240,500), (360,500)]:
    body = pymunk.Body()
    body.position = p
    shape = pymunk.Circle(body, 10)
    shape.elasticity = 1.5
    space.add(shape)
    balls.append(shape)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == KEYDOWN and event.key == K_p:
            pygame.image.save(screen, "flipper.png")
                
        elif event.type == KEYDOWN and event.key == K_j:
            r_flipper_body.apply_impulse(Vec2d.unit() * 40000, (-100,0))
        elif event.type == KEYDOWN and event.key == K_f:
            l_flipper_body.apply_impulse(Vec2d.unit() * -40000, (-100,0))
        elif event.type == KEYDOWN and event.key == K_b:
            
            mass = 1
            radius = 25
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
            body = pymunk.Body(mass, inertia)
            x = random.randint(115,350)
            body.position = x, 400
            shape = pymunk.Circle(body, radius, (0,0))
            shape.elasticity = 0.95
            space.add(body, shape)
            balls.append(shape)
    
    ### Clear screen
    screen.fill(THECOLORS["white"])
    
    ### Draw stuff
    for ball in balls:
        p = to_pygame(ball.body.position)
        pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)


    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])
    
    
    r_flipper_body.position = 450, 100
    l_flipper_body.position = 150, 100
    r_flipper_body.velocity = l_flipper_body.velcoty = 0,0
    for f in [r_flipper_shape, l_flipper_shape]:
        ps = f.get_vertices()
        ps.append(ps[0])
        ps = map(to_pygame, ps)
        
        color = THECOLORS["red"]
        pygame.draw.lines(screen, color, False, ps)
    #if abs(flipper_body.angle) < 0.001: flipper_body.angle = 0
    
    ### Update physics
    dt = 1.0/60.0/5.
    for x in range(5):
        space.step(dt)
    
    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
