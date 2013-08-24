"""Very simple example that does not depend on any third party library such 
as pygame or pyglet like the other examples. 
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pymunk as pm
import pymunk.util as u
from pymunk import Vec2d
import math, sys, random
#import timeit

def main():
    main1()
#    print timeit.Timer('main1()', "gc.enable(); from __main__ import main1").repeat(repeat=6, number=3)  

def main1():
              
    space = pm.Space()
    space.gravity = (0.0, -900.0)
    
    ## Balls
    balls = []
       
    ### walls
    #static_body = pm.Body()
    #static_lines = [pm.Segment(static_body, Vec2d(111.0, 280.0), Vec2d(407.0, 246.0), 0.0)
    #                ,pm.Segment(static_body, Vec2d(407.0, 246.0), Vec2d(407.0, 343.0), 0.0)
    #                ]    
    #space.add(static_lines)
    
    ticks_to_next_ball = 10
    sum_of_stuff = 0
    for x in range(5000):            
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 10000
            mass = 10
            radius = 25
            inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
            body = pm.Body(mass, inertia)
            x = random.randint(115,350)
            body.position = x, 400
            shape = pm.Circle(body, radius, Vec2d(0,0))
            space.add(body, shape)
            balls.append(shape)
        
        
        balls_to_remove = []
        
        for ball in balls:
            if ball.body.position.y < 0: balls_to_remove.append(ball)
            sum_of_stuff += ball.body.position.x
            sum_of_stuff += ball.body.angle
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        if len(balls) >= 1:
           v = balls[0].body.position
           print("(in on_draw): point = %.2f, %.2f" % (v.x,v.y))

        ### Update physics
        for x in range(1):
            space.step(1/50.0)
        
    return sum_of_stuff #just to force it to not optimize the sum away, don't think it needs to be here..



if __name__ == '__main__':
    sys.exit(main())
