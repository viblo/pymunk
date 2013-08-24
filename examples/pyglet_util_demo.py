"""Showcase what the output of pymunk.pyglet_util draw methods will look like.

See pygame_util_demo.py for a comparison to pygame.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys

import pyglet
    
import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pyglet_util

from shapes_for_draw_demos import add_objects

window = pyglet.window.Window(600, 600)
space = pymunk.Space()

add_objects(space)


textbatch = pyglet.graphics.Batch()
pyglet.text.Label('Demo example of shapes drawn by pyglet_util.draw()',
                      x=5, y=5, batch=textbatch, color=(200,200,200,200))
pyglet.text.Label('Static shapes', x=50, y=570, batch=textbatch)
pyglet.text.Label('Dynamic shapes', x=250, y=570, batch=textbatch)
pyglet.text.Label('Constraints', x=450, y=570, batch=textbatch)
pyglet.text.Label('Other', x=450, y=290, batch=textbatch)


batch = pyglet.graphics.Batch()

@window.event
def on_draw():
    pyglet.gl.glClearColor(0,0,0,1)
    window.clear()
    
    pymunk.pyglet_util.draw(space)
    textbatch.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save("pyglet_util_demo.png")
                      

pyglet.app.run()