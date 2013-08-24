""" Helper function add_objects for the draw demos. 
Adds a lot of stuff to a space.
"""

import pymunk

def add_objects(space):
    ### Static
    #Static Segments
    segments = [ pymunk.Segment(space.static_body, (10, 50), (10, 500), 1)
                ,pymunk.Segment(space.static_body, (30, 50), (30, 500), 2)
                ,pymunk.Segment(space.static_body, (50, 50), (50, 500), 3)
                ,pymunk.Segment(space.static_body, (70, 50), (70, 500), 5)
                ]  
    space.add(segments)
    
    b = pymunk.Body()
    b.position = (40,530)
    b.angle = 3.14/7
    s = pymunk.Segment(b, (-30,0), (30,0), 2)
    space.add(s)
    
    # Static Circles
    b = pymunk.Body()
    b.position = (150,500)
    s = pymunk.Circle(b, 10)
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,500)
    s = pymunk.Circle(b, 10,(0,-30))
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,400)
    b.angle = 3.14/4
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    # Static Polys
    b = pymunk.Body()
    b.position = (150,300)
    b.angle = 3.14/4
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)])
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,300)
    b.angle = 3.14/2
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)], (-100,0), radius=3)
    space.add(s)
    
    b = pymunk.Body()
    b.position = (150,200)
    s = pymunk.Poly(b, [(0, -50), (50, 0), (30, 50),(-30, 50),(-50, 0)], (0,-100))
    space.add(s)
    
    ### Dynamic
    
    #Dynamic Segments
    b = pymunk.Body(1,1)
    segments = [ pymunk.Segment(b, (210, 50), (210, 500), 1)
                ,pymunk.Segment(b, (230, 50), (230, 500), 2)
                ,pymunk.Segment(b, (250, 50), (250, 500), 3)
                ,pymunk.Segment(b, (270, 50), (270, 500), 5)
                ]  
    space.add(segments)
    
    b = pymunk.Body(1,1)
    b.position = (240,530)
    b.angle = 3.14/7
    s = pymunk.Segment(b, (-30,0), (30,0), 2)
    space.add(s)
    
    # Dynamic Circles
    b = pymunk.Body(1,1)
    b.position = (350,500)
    s = pymunk.Circle(b, 10)
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,500)
    s = pymunk.Circle(b, 10,(0,-30))
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,400)
    b.angle = 3.14/4
    s = pymunk.Circle(b, 40)
    space.add(s)
    
    # Dynamic Polys
    b = pymunk.Body(1,1)
    b.position = (350,300)
    b.angle = 3.14/4
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)])
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,300)
    b.angle = 3.14/2
    s = pymunk.Poly(b, [(0, -50),(30, 50),(-30, 50)], (-100,0), radius=3)
    space.add(s)
    
    b = pymunk.Body(1,1)
    b.position = (350,200)
    s = pymunk.Poly(b, [(0, -50), (50, 0), (30, 50),(-30, 50),(-50, 0)], (0,-100))
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
    j = pymunk.PinJoint(a,b, anchr1=(0,20), anchr2=(0,-20))
    space.add(a,b,j)
    
    # SlideJoints
    a = pymunk.Body(1,1)
    a.position = (450,430)
    b = pymunk.Body(1,1)
    b.position = (550,430)
    j = pymunk.SlideJoint(a,b, anchr1=(0,20), anchr2=(0,-20), min=10,max=30)
    space.add(a,b,j)
    
    
    # TODO: more stuff here :)
    
    ### Other
    
    # Object not drawn by draw_space
    b = pymunk.Body()
    b.position = (500,250)
    s = pymunk.Circle(b, 40)
    s.ignore_draw = True
    space.add(s)
    
    # Objects in custom color
    b = pymunk.Body()
    b.position = (500,200)
    s = pymunk.Circle(b, 40)
    s.color = (255, 255, 0)
    space.add(s)
    
    b = pymunk.Body(1, 1)
    b.position = (500, 100)
    s = pymunk.Circle(b, 30)
    s.color = (255, 255, 0)
    space.add(s)
