import math, sys, random
import os
 
import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk import Vec2d

width, height = 600,600

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+height)
def from_pygame(p): 
    return to_pygame(p)

def spawn_ball(space, position, direction):
    ball_body = pymunk.Body(1, pymunk.inf)
    ball_body.position = position
    
    ball_shape = pymunk.Circle(ball_body, 5)
    ball_shape.color =  THECOLORS["green"]
    ball_shape.elasticity = 1.0
    
    ball_body.apply_impulse(Vec2d(direction))
    
    # Keep ball velocity at a static value
    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400
    ball_body.velocity_func = constant_velocity
    
    space.add(ball_body, ball_shape)

def setup_level(space, player_body):
    
    # Remove balls and bricks
    for s in space.shapes[:]:
        if s.body not in [player_body]:
            space.remove(s.body, s)
            
    # Spawn a ball for the player to have something to play with
    spawn_ball(space, player_body.position + (0,40), random.choice([(1,1),(-1,1)]))
    
    # Spawn bricks
    for x in range(0,21):
        x = x * 20 + 100
        for y in range(0,5):
            y = y * 10 + 400
            brick_body = pymunk.Body(pymunk.inf, pymunk.inf)
            brick_body.position = x, y
            brick_shape = pymunk.Poly.create_box(brick_body, (20,10))
            brick_shape.elasticity = 1.0
            brick_shape.color = THECOLORS['blue']
            brick_shape.group = 1
            brick_shape.collision_type = 2
            space.add(brick_body, brick_shape)
    # Make bricks be removed when hit by ball
    def remove_first(space, arbiter):
        first_shape = arbiter.shapes[0]
        space.add_post_step_callback(space.remove, first_shape, first_shape.body)
    space.add_collision_handler(2, 0, separate = remove_first)

def draw_space(screen, space):
    # Static shapes (the walls)
    for line in space.static_shapes:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, line.color, False, [p1,p2], int(line.radius))
    
    # Constraints
    for c in space.constraints:
        if isinstance(c, pymunk.GrooveJoint):
            pv1 = c.a.position + c.groove_a
            pv2 = c.a.position + c.groove_b
        else:
            pv1 = c.a.position + c.anchr1
            pv2 = c.b.position + c.anchr2
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.aalines(screen, THECOLORS["darkgray"], False, [p1,p2])
        
    # moving shapes including player
    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            p = to_pygame(shape.body.position)
            pygame.draw.circle(screen, shape.color, p, int(shape.radius), 0)
        if isinstance(shape, pymunk.Poly):
            ps = shape.get_points()
            ps = [to_pygame(p) for p in ps]
            ps += [ps[0]]
            pygame.draw.lines(screen, shape.color, False, ps, 1)
    
def main():
    
    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 
    
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 16)
    
    ### Physics stuff
    space = pymunk.Space()   
    
    ### Game area
    # walls - the left-top-right walls
    static_lines = [pymunk.Segment(space.static_body, (50, 50), (50, 550), 5)
                ,pymunk.Segment(space.static_body, (50, 550), (550, 550), 5)
                ,pymunk.Segment(space.static_body, (550, 550), (550, 50), 5)
                ]  
    for line in static_lines:
        line.color = THECOLORS['lightgray']
        line.elasticity = 1.0
    
    space.add_static(static_lines)

    # bottom - a sensor that removes anything touching it
    bottom = pymunk.Segment(space.static_body, (50, 50), (550, 50), 5)
    bottom.sensor = True
    bottom.collision_type = 1
    bottom.color = THECOLORS['red']
    def remove_first(space, arbiter):
        first_shape = arbiter.shapes[0]
        space.add_post_step_callback(space.remove, first_shape, first_shape.body)
        return True
    space.add_collision_handler(0, 1, begin = remove_first)
    space.add_static(bottom)
    
    ### Player ship
    player_body = pymunk.Body(500, pymunk.inf)
    player_shape = pymunk.Circle(player_body, 35)
    player_shape.color = THECOLORS["red"]
    player_shape.elasticity = 1.0
    player_body.position = 300,100
    # restrict movement of player to a straigt line 
    move_joint = pymunk.GrooveJoint(space.static_body, player_body, (100,100), (500,100), (0,0))
    space.add(player_body, player_shape, move_joint)
    
    # Start game
    setup_level(space, player_body)
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: 
                running = False
            elif event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                running = False
                
            elif event.type == KEYDOWN and event.key == K_LEFT:
                player_body.velocity = (-600,0)
            elif event.type == KEYUP and event.key == K_LEFT:
                player_body.velocity = 0,0
                
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                player_body.velocity = (600,0)
            elif event.type == KEYUP and event.key == K_RIGHT:
                player_body.velocity = 0,0
                
            elif event.type == KEYDOWN and event.key == K_r:
                setup_level(space, player_body)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                spawn_ball(space, player_body.position + (0,40), random.choice([(1,1),(-1,1)]))
                   
        ### Clear screen
        screen.fill(THECOLORS["black"])
        
        ### Draw stuff
        draw_space(screen, space)
            
        ### Update physics
        fps = 60
        dt = 1./fps
        space.step(dt)
        
        ### Info and flip screen
        screen.blit(font.render("fps: " + str(clock.get_fps()), 1, THECOLORS["white"]), (0,0))
        screen.blit(font.render("Move with left/right arrows, space to spawn a ball", 1, THECOLORS["darkgrey"]), (5,height - 35))
        screen.blit(font.render("Press R to reset, ESC or Q to quit", 1, THECOLORS["darkgrey"]), (5,height - 20))
        
        pygame.display.flip()
        clock.tick(fps)
        
if __name__ == '__main__':
    sys.exit(main())
    