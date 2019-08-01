"""Showcase what the output of pymunk.pyglet_util draw methods will look like.

See pygame_util_demo.py for a comparison to pygame.
"""

__docformat__ = "reStructuredText"

import sys

import pyglet
    
import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pyglet_util

import shapes_for_draw_demos

window = pyglet.window.Window(1000, 700, vsync=False)
space = pymunk.Space()
draw_options = pymunk.pyglet_util.DrawOptions()
captions = shapes_for_draw_demos.fill_space(space)


textbatch = pyglet.graphics.Batch()
pyglet.text.Label('Demo example of shapes drawn by pyglet_util.draw()',
                      x=5, y=5, batch=textbatch, color=(100,100,100,255))
for caption in captions:
    x, y = caption[0]
    y = y - 10
    pyglet.text.Label(caption[1], x=x, y=y, batch=textbatch, color=(50,50,50,255))

batch = pyglet.graphics.Batch()

# otherwise save screenshot wont work
_ = pyglet.window.FPSDisplay(window)

@window.event
def on_draw():
    pyglet.gl.glClearColor(255,255,255,255)
    window.clear()
    space.debug_draw(draw_options)
    textbatch.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save("pyglet_util_demo.png")
                      

pyglet.app.run()
