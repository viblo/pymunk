"""
Remake of the veritcal stack demo from the box2d testbed.
"""

import math

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import pymunk
from pymunk import Vec2d
import pymunk.pyglet_util

class Main(pyglet.window.Window):
    def __init__(self):
        
        pyglet.window.Window.__init__(self, vsync=False)
        self.set_caption('Vertical stack from box2d')

        pyglet.clock.schedule_interval(self.update, 1/60.0)
        self.fps_display = pyglet.clock.ClockDisplay()
        
        self.text = pyglet.text.Label('Press space to fire bullet',
                          font_size=10,
                          x=10, y=400)
        self.create_world()
        
    

    def create_world(self):
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.,-900.)
        
        static_body = pymunk.Body()
        static_lines = [pymunk.Segment(static_body, Vec2d(50,100), Vec2d(550,100), 1),
                        pymunk.Segment(static_body, Vec2d(450,100), Vec2d(450,300), 1)
                        ]
        for l in static_lines:
            l.friction = 0.3
        self.space.add(static_lines)
        
        for x in range(5):
            for y in range(12):
                size= 5
                points = [(-size, -size), (-size, size), (size,size), (size, -size)]
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
        elif symbol == pyglet.window.key.P:
            pyglet.image.get_buffer_manager().get_color_buffer().save('box2d_vertical_stack.png')
            

    def on_draw(self):
        self.clear()
        self.text.draw()
        self.fps_display.draw()       
        pymunk.pyglet_util.draw(self.space)
        
if __name__ == '__main__':
    main = Main()
    pyglet.app.run()