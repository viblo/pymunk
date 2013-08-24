"""This example is a clone of the using_sprites example with the difference 
that it uses pyglet instead of pygame to showcase sprite drawing. 
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math, random

import pyglet

import pymunk
from pymunk import Vec2d

window = pyglet.window.Window(width=600,height=600)

fps_display = pyglet.clock.ClockDisplay()

logo_img = pyglet.resource.image('pymunk_logo_googlecode.png')
logo_img.anchor_x = logo_img.width/2
logo_img.anchor_y = logo_img.height/2
logos = []
batch = pyglet.graphics.Batch()

### Physics stuff
space = pymunk.Space()
space.gravity = Vec2d(0.0, -900.0)

### Static line
static_body = pymunk.Body()
static_lines = [pymunk.Segment(static_body, (11.0, 280.0), (407.0, 246.0), 0.0)
                ,pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                ]
for l in static_lines:
    l.friction = 0.5
space.add(static_lines)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save('using_sprites_pyglet.png')

@window.event
def on_draw():
    window.clear()
    
    fps_display.draw()

    for line in static_lines:
        body = line.body
        
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2f', (pv1.x,pv1.y,pv2.x,pv2.y)),
            ('c3f', (.8,.8,.8)*2)
            )
    batch.draw()
    
    #debug draw
    for logo_sprite in logos:
        
        ps = logo_sprite.shape.get_vertices()
        n = len(ps)
        ps = [c for p in ps for c in p]
        
        pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP,
            ('v2f', ps),
            ('c3f', (1,0,0)*n)
            )
            
def update(dt):
    dt = 1.0/60. #override dt to keep physics simulation stable
    space.step(dt)
    
    for sprite in logos:
        # We need to rotate the image 180 degrees because we have y pointing 
        # up in pymunk coords.
        sprite.rotation = math.degrees(-sprite.body.angle) + 180
        sprite.set_position(sprite.body.position.x, sprite.body.position.y)
        
def spawn_logo(dt):
    x = random.randint(20,400)
    y = 500
    angle = random.random() * math.pi
    vs = [(-23,26), (23,26), (0,-26)]
    mass = 10
    moment = pymunk.moment_for_poly(mass, vs)
    body = pymunk.Body(mass, moment)
    shape = pymunk.Poly(body, vs)
    shape.friction = 0.5
    body.position = x, y
    body.angle = angle
    
    space.add(body, shape)
    
    sprite = pyglet.sprite.Sprite(logo_img, batch=batch)
    sprite.shape = shape
    sprite.body = body
    logos.append(sprite) 
    
pyglet.clock.schedule_interval(update, 1/60.)
pyglet.clock.schedule_once(spawn_logo, .1)
pyglet.clock.schedule_interval(spawn_logo, 10/6.)
pyglet.app.run()

