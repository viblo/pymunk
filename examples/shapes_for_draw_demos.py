""" Helper function add_objects for the draw demos. 
Adds a lot of stuff to a space.
"""

import pymunk

def fill_space(space):
    ### Static
    #Static Segments
    segments = [ pymunk.Segment(space.static_body, (10, 400), (10, 600), 1)
                ,pymunk.Segment(space.static_body, (30, 400), (30, 600), 3)
                ,pymunk.Segment(space.static_body, (50, 400), (50, 600), 5)
                ]  
    space.add(segments)
    
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (40,630)
    b.angle = 3.14/7
    s = pymunk.Segment(b, (-30,0), (30,0), 2)
    space.add(s)
    
    # Static Circles
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (120,630)
    s = pymunk.Circle(b, 10)
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (120,630)
    s = pymunk.Circle(b, 10, (-30,0))
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (120,560)
    b.angle = 3.14/4
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    # Static Polys
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (120,460)
    b.angle = 3.14/4
    s = pymunk.Poly(b, [(0, -25),(30, 25),(-30, 25)])
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (120,500)
    t = pymunk.Transform(ty=-100)
    s = pymunk.Poly(b, [(0, -25),(30, 25),(-30, 25)], t, radius=3)
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (50,430)
    t = pymunk.Transform(ty=-100)
    s = pymunk.Poly(b, [(0, -50), (50, 0), (30, 50),(-30, 50),(-50, 0)], t)
    space.add(s)
    
    ### Kinematic
    # Kinematic Segments
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    segments = [ pymunk.Segment(b, (180, 400), (180, 600), 1)
                ,pymunk.Segment(b, (200, 400), (200, 600), 3)
                ,pymunk.Segment(b, (220, 400), (220, 600), 5)
                ]  
    space.add(segments)
    
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    b.position = (210,630)
    b.angle = 3.14/7
    s = pymunk.Segment(b, (-30,0), (30,0), 2)
    space.add(s)
    
    # Kinematic Circles
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    b.position = (290,630)
    s = pymunk.Circle(b, 10)
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    b.position = (290,630)
    s = pymunk.Circle(b, 10, (-30,0))
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    b.position = (290,560)
    b.angle = 3.14/4
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    # Kinematic Polys
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    b.position = (290,460)
    b.angle = 3.14/4
    s = pymunk.Poly(b, [(0, -25),(30, 25),(-30, 25)])
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    b.position = (290,500)
    t = pymunk.Transform(ty=-100)
    s = pymunk.Poly(b, [(0, -25),(30, 25),(-30, 25)], t, radius=3)
    space.add(s)
    
    b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    b.position = (230,430)
    t = pymunk.Transform(ty=-100)
    s = pymunk.Poly(b, [(0, -50), (50, 0), (30, 50),(-30, 50),(-50, 0)], t)
    space.add(s)
    
    ### Dynamic
    
    #Dynamic Segments
    b = pymunk.Body(1,1)
    segments = [pymunk.Segment(b, (350, 400), (350, 600), 1),
                pymunk.Segment(b, (370, 400), (370, 600), 3),
                pymunk.Segment(b, (390, 400), (390, 600), 5),
                ]  
    space.add(segments)
    
    b = pymunk.Body(1,1)
    b.position = (380,630)
    b.angle = 3.14/7
    s = pymunk.Segment(b, (-30,0), (30,0), 2)
    space.add(s)
    
    # Dynamic Circles
    b = pymunk.Body(1,1)
    b.position = (460,630)
    s = pymunk.Circle(b, 10)
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (460,630)
    s = pymunk.Circle(b, 10, (-30,0))
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (460,560)
    b.angle = 3.14/4
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    # Dynamic Polys
    
    b = pymunk.Body(1,1)
    b.position = (460,460)
    b.angle = 3.14/4
    s = pymunk.Poly(b, [(0, -25),(30, 25),(-30, 25)])
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (460,500)    
    s = pymunk.Poly(b, [(0, -25),(30, 25),(-30, 25)], pymunk.Transform(ty=-100), radius=3)
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (400,430)
    s = pymunk.Poly(b, [(0, -50), (50, 0), (30, 50),(-30, 50),(-50, 0)], pymunk.Transform(ty=-100))
    space.add(s)
    
    ###Constraints
    
    # PinJoints
    a = pymunk.Body(1,1)
    a.position = (450,530)
    b = pymunk.Body(1,1)
    b.position = (550,530)
    j = pymunk.PinJoint(a,b)
    space.add(a,b,j)
    
    a = pymunk.Body(1,1)
    a.position = (450,480)
    b = pymunk.Body(1,1)
    b.position = (550,480)
    j = pymunk.PinJoint(a,b, anchor_a=(0,20), anchor_b=(0,-20))
    space.add(a,b,j)
    
    # SlideJoints
    a = pymunk.Body(1,1)
    a.position = (450,430)
    b = pymunk.Body(1,1)
    b.position = (550,430)
    j = pymunk.SlideJoint(a,b, anchor_a=(0,20), anchor_b=(0,-20), min=10,max=30)
    space.add(a,b,j)
    
    
    # TODO: more stuff here :)
    
    ### Other
    
    # Object not drawn by draw_space
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (85,200)
    s = pymunk.Circle(b, 40)
    s.ignore_draw = True
    space.add(s)
    
    # Objects in custom color
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (200, 200)
    s = pymunk.Circle(b, 40)
    s.color = (255, 255, 0)
    space.add(s)
    
    b = pymunk.Body(1, 1)
    b.position = (300, 200)
    s = pymunk.Circle(b, 40)
    s.color = (255, 255, 0)
    space.add(s)
    
    # Collision
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (450, 200)
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    b = pymunk.Body(1, 1)
    b.position = (500, 250)
    s = pymunk.Circle(b, 40)
    space.add(s)

    # Sleeping
    b = pymunk.Body(1,1)
    b.position = (75, 80)
    space.sleep_time_threshold = 0.01
    s = pymunk.Circle(b, 40)
    space.add(s, b)
    b.sleep()


def main():
    space = pymunk.Space()
    fill_space(space)

    options = pymunk.SpaceDebugDrawOptions()
    #space.step(1)
    #space.step(2)
    space.debug_draw(options)


if __name__ == '__main__':
    import sys
    sys.exit(main())