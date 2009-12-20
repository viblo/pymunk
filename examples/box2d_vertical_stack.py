"""
Remake of the veritcal stack demo from the box2d testbed.
"""

import math

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import pymunk
from pymunk import Vec2d

class Main(pyglet.window.Window):
    def __init__(self):
        
        pyglet.window.Window.__init__(self)
        self.set_caption('Vertical stack from box2d')
        pymunk.init_pymunk()
        
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        self.fps_display = pyglet.clock.ClockDisplay()
        
        self.text = pyglet.text.Label('Press space to fire bullet',
                          font_name='TArial',
                          font_size=10,
                          x=10, y=400)
        self.create_world()
        
    

    def create_world(self):
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.,-900.)
        
        static_body = pymunk.Body(pymunk.inf, pymunk.inf)
        static_lines = [pymunk.Segment(static_body, Vec2d(50,100), Vec2d(550,100), 1),
                        pymunk.Segment(static_body, Vec2d(450,100), Vec2d(450,300), 1)
                        ]
        for l in static_lines:
            l.friction = 0.3
        self.space.add_static(static_lines)
        
        for x in range(5):
            for y in range(12):
                size= 5
                points = [(-size, -size), (-size, size), (size,size)] #, (size, -size)]
                mass = 10.0
                moment = pymunk.moment_for_poly(mass, points, (0,0))
                body = pymunk.Body(mass, moment)
                body.position = Vec2d(200 + x*50, 105 + y * 11)
                shape = pymunk.Poly(body, points, (0,0))
                shape.friction = 0.3
                self.space.add(body,shape)
                
        
    def update(self,dt):
        steps = 10
        for x in range(steps):
            self.space.step(1/60./steps)


    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            mass = 100
            r = 5
            moment = pymunk.moment_for_circle(mass, 0, r, (0,0))
            body = pymunk.Body(mass, moment)
            body.position = (0, 165)
            shape = pymunk.Circle(body, r, (0,0))
            self.space.add(body, shape)
            f = 200000
            body.apply_impulse((f,0), (0,0))
        elif symbol == key.ESCAPE:
            pyglet.app.exit()
            

    def on_draw(self):
        self.clear()
        self.text.draw()
        self.fps_display.draw()

        for shape in self.space.static_shapes:
            if isinstance(shape, pymunk.Segment):
                body = shape.body
                pv1 = body.position + shape.a.rotated(math.degrees(body.angle))
                pv2 = body.position + shape.b.rotated(math.degrees(body.angle))
                pyglet.graphics.draw(2, GL_LINES,
                                     ('v2f', (pv1.x, pv1.y, pv2.x, pv2.y)),
                                      ('c4f', (1.0, 1.0, 1.0, 1.) * 2))
        
        b = pyglet.graphics.Batch()
        
        for shape in self.space.shapes:
            if isinstance(shape, pymunk.Poly):
                ps = shape.get_points()
                ps = [ps[0]] + ps + [ps[0], ps[0]]
                xs = []
                for p in ps:
                    xs.append(p.x)
                    xs.append(p.y)
                b.add(len(ps), GL_LINE_STRIP, None, 
                        ('v2f', xs),
                         ('c4f', (0.0, 1.0, 0.0, 1.0) * len(ps)))
                #pyglet.graphics.draw(len(ps), GL_LINE_STRIP,
                #                     ('v2f', xs),
                #                      ('c4f', (0.0, 1.0, 0.0, 1.0) * len(ps)))
                                      
            if isinstance(shape, pymunk.Circle):
                p = shape.body.position
                ps = [p + (0,shape.radius), p + (shape.radius,0),
                        p + (0,-shape.radius), p + (-shape.radius,0)]
                ps += [ps[0]]
                xs = []
                for p in ps:
                    xs.append(p.x)
                    xs.append(p.y)
                pyglet.graphics.draw(len(ps), GL_LINE_STRIP,
                                     ('v2f', xs),
                                      ('c4f', (0.0, 0.0, 1.0, 1.0) * len(ps)))
        
        b.draw()
if __name__ == '__main__':
    doprof = 0
    
    main = Main()
    if not doprof: 
        pyglet.app.run()