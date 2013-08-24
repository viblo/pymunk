"""Showcase of a very basic 2d platformer

The red girl sprite is taken from Sithjester's RMXP Resources:
http://untamed.wild-refuge.net/rmxpresources.php?characters

.. note:: The code of this example is a bit messy. If you adapt this to your 
    own code you might want to structure it a bit differently.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys,math

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw, from_pygame, to_pygame


def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)

def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)



width, height = 690,400
fps = 60
dt = 1./fps
PLAYER_VELOCITY = 100. *2.
PLAYER_GROUND_ACCEL_TIME = 0.05
PLAYER_GROUND_ACCEL = (PLAYER_VELOCITY/PLAYER_GROUND_ACCEL_TIME)

PLAYER_AIR_ACCEL_TIME = 0.25
PLAYER_AIR_ACCEL = (PLAYER_VELOCITY/PLAYER_AIR_ACCEL_TIME)

JUMP_HEIGHT = 16.*3
JUMP_BOOST_HEIGHT = 24.
JUMP_CUTOFF_VELOCITY = 100
FALL_VELOCITY = 250.

JUMP_LENIENCY = 0.05

HEAD_FRICTION = 0.7

PLATFORM_SPEED = 1

def main():

    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)
    sound = pygame.mixer.Sound("sfx.wav")
    img = pygame.image.load("xmasgirl1.png")
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0,-1000
    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 50), (300, 50), 5)
                , pymunk.Segment(space.static_body, (300, 50), (325, 50), 5)
                , pymunk.Segment(space.static_body, (325, 50), (350, 50), 5)
                , pymunk.Segment(space.static_body, (350, 50), (375, 50), 5)
                , pymunk.Segment(space.static_body, (375, 50), (680, 50), 5)
                , pymunk.Segment(space.static_body, (680, 50), (680, 370), 5)
                , pymunk.Segment(space.static_body, (680, 370), (10, 370), 5)
                , pymunk.Segment(space.static_body, (10, 370), (10, 50), 5)
                ]  
    static[1].color = pygame.color.THECOLORS['red']
    static[2].color = pygame.color.THECOLORS['green']
    static[3].color = pygame.color.THECOLORS['red']
    
    # rounded shape
    rounded = [pymunk.Segment(space.static_body, (500, 50), (520, 60), 5)
                , pymunk.Segment(space.static_body, (520, 60), (540, 80), 5)
                , pymunk.Segment(space.static_body, (540, 80), (550, 100), 5)
                , pymunk.Segment(space.static_body, (550, 100), (550, 150), 5)
                ]
                
    # static platforms
    platforms = [pymunk.Segment(space.static_body, (170, 50), (270, 150), 5)
                #, pymunk.Segment(space.static_body, (270, 100), (300, 100), 5)
                , pymunk.Segment(space.static_body, (400, 150), (450, 150), 5)
                , pymunk.Segment(space.static_body, (400, 200), (450, 200), 5)
                , pymunk.Segment(space.static_body, (220, 200), (300, 200), 5)
                , pymunk.Segment(space.static_body, (50, 250), (200, 250), 5)
                , pymunk.Segment(space.static_body, (10, 370), (50, 250), 5)
                ]
    
    for s in static + platforms+rounded:
        s.friction = 1.
        s.group = 1
    space.add(static, platforms+rounded)
    
    # moving platform
    platform_path = [(650,100),(600,200),(650,300)]
    platform_path_index = 0
    platform_body = pymunk.Body(pymunk.inf, pymunk.inf)
    platform_body.position = 650,100
    s = pymunk.Segment(platform_body, (-25, 0), (25, 0), 5)
    s.friction = 1.
    s.group = 1
    s.color = pygame.color.THECOLORS["blue"]
    space.add(s)
    
    # pass through platform
    passthrough = pymunk.Segment(space.static_body, (270, 100), (320, 100), 5)
    passthrough.color = pygame.color.THECOLORS["yellow"]
    passthrough.friction = 1.
    passthrough.collision_type = 2
    passthrough.layers = passthrough.layers ^ 0b1000
    space.add(passthrough)
    
    def passthrough_handler(space, arbiter):
        if arbiter.shapes[0].body.velocity.y < 0:
            return True
        else:
            return False
            
    space.add_collision_handler(1,2, begin=passthrough_handler)
    
    
    # player
    body = pymunk.Body(5, pymunk.inf)
    body.position = 100,100
    
    
    head = pymunk.Circle(body, 10, (0,5))
    head2 = pymunk.Circle(body, 10, (0,13))
    feet = pymunk.Circle(body, 10, (0,-5))

    head.layers = head2.layers = 0b1000
    feet.collision_type = 1
    feet.ignore_draw = head.ignore_draw = head2.ignore_draw = True
    
    space.add(body, head, feet,head2)
    direction = 1
    remaining_jumps = 2
    landing = {'p':Vec2d.zero(), 'n':0}
    frame_number = 0
    
    landed_previous = False
    
    while running:
        
        grounding = {
            'normal' : Vec2d.zero(),
            'penetration' : Vec2d.zero(),
            'impulse' : Vec2d.zero(),
            'position' : Vec2d.zero(),
            'body' : None
        }
        # find out if player is standing on ground
        
                
        def f(arbiter):
            n = -arbiter.contacts[0].normal
            if n.y > grounding['normal'].y:
                grounding['normal'] = n
                grounding['penetration'] = -arbiter.contacts[0].distance
                grounding['body'] = arbiter.shapes[1].body
                grounding['impulse'] = arbiter.total_impulse
                grounding['position'] = arbiter.contacts[0].position
        body.each_arbiter(f)
            
        well_grounded = False
        if grounding['body'] != None and abs(grounding['normal'].x/grounding['normal'].y) < feet.friction:
            well_grounded = True
            remaining_jumps = 2
    
        ground_velocity = Vec2d.zero()
        if well_grounded:
            ground_velocity = grounding['body'].velocity
    
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "platformer.png")

            elif event.type == KEYDOWN and event.key == K_d:
                feet.ignore_draw = not feet.ignore_draw
                head.ignore_draw = not head.ignore_draw
                head2.ignore_draw = not head2.ignore_draw
                
            elif event.type == KEYDOWN and event.key == K_UP:
                if well_grounded or remaining_jumps > 0:                    
                    jump_v = math.sqrt(2.0 * JUMP_HEIGHT * abs(space.gravity.y))
                    body.velocity.y = ground_velocity.y + jump_v;
                    remaining_jumps -=1
            elif event.type == KEYUP and event.key == K_UP:                
                body.velocity.y = min(body.velocity.y, JUMP_CUTOFF_VELOCITY)
                
        # Target horizontal velocity of player
        target_vx = 0
        
        if body.velocity.x > .01:
            direction = 1
        elif body.velocity.x < -.01:
            direction = -1
        
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT]):
            direction = -1
            target_vx -= PLAYER_VELOCITY
        if (keys[K_RIGHT]):
            direction = 1
            target_vx += PLAYER_VELOCITY
        if (keys[K_DOWN]):
            direction = -3
            
        feet.surface_velocity = target_vx,0

        
        if grounding['body'] != None:
            feet.friction = -PLAYER_GROUND_ACCEL/space.gravity.y
            head.friciton = HEAD_FRICTION
        else:
            feet.friction,head.friction = 0,0
        
        # Air control
        if grounding['body'] == None:
            body.velocity.x = cpflerpconst(body.velocity.x, target_vx + ground_velocity.x, PLAYER_AIR_ACCEL*dt)
        
        body.velocity.y = max(body.velocity.y, -FALL_VELOCITY) # clamp upwards as well?
        
        # Move the moving platform
        destination = platform_path[platform_path_index]
        current = Vec2d(platform_body.position)
        distance = current.get_distance(destination)
        if distance < PLATFORM_SPEED:
            platform_path_index += 1
            platform_path_index = platform_path_index % len(platform_path)
            t = 1
        else:
            t = PLATFORM_SPEED / distance
        new = current.interpolate_to(destination, t)
        platform_body.position = new
        platform_body.velocity = (new - current) / dt
        
        ### Clear screen
        screen.fill(pygame.color.THECOLORS["black"])
        
        ### Helper lines
        for y in [50,100,150,200,250,300]:
            color = pygame.color.THECOLORS['darkgrey']
            pygame.draw.line(screen, color, (10,y), (680,y), 1)
        
        ### Draw stuff
        draw(screen, space)
        
        if feet.ignore_draw:
            direction_offset = 48+(1*direction+1)/2 * 48
            if grounding['body'] != None and abs(target_vx) > 1:
                animation_offset = 32 * (frame_number / 8 % 4)
            elif grounding['body'] is None:
                animation_offset = 32*1
            else:
                animation_offset = 32*0
            position = body.position +(-16,28)
            screen.blit(img, to_pygame(position, screen), (animation_offset, direction_offset, 32, 48))

        # Did we land?
        if abs(grounding['impulse'].y) / body.mass > 200 and not landed_previous:
            sound.play()
            landing = {'p':grounding['position'],'n':5}
            landed_previous = True
        else:
            landed_previous = False
        if landing['n'] > 0:
            pygame.draw.circle(screen, pygame.color.THECOLORS['yellow'], to_pygame(landing['p'], screen), 5)
            landing['n'] -= 1
        
        # Info and flip screen
        screen.blit(font.render("fps: " + str(clock.get_fps()), 1, THECOLORS["white"]), (0,0))
        screen.blit(font.render("Move with Left/Right, jump with Up, press again to double jump", 1, THECOLORS["darkgrey"]), (5,height - 35))
        screen.blit(font.render("Press D to toggle sprite draw, ESC or Q to quit", 1, THECOLORS["darkgrey"]), (5,height - 20))
        
       
        pygame.display.flip()
        frame_number += 1
        ### Update physics
        
        space.step(dt)
        
        clock.tick(fps)

if __name__ == '__main__':
    sys.exit(main())
