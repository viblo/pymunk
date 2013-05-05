# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2012 Victor Blomqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------

"""This submodule contains helper functions to help with quick prototyping 
using pymunk together with pyglet.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated 
about your coordinate system and not very optimized (they use batched 
drawing, but there is probably room for optimizations still). 
"""

__version__ = "$Id$"
__docformat__ = "reStructuredText"

__all__ = ["draw_space", "draw_shape", "draw_circle", "draw_poly"
         , "draw_segment"]

import math

import pyglet
from pyglet.gl import *

import pymunk
from pymunk.vec2d import Vec2d

def draw_space(space, batch = None):
    """Draw the contents of a pymunk.Space object
    
    This method currently supports drawing of
        * pymunk.Segment
        * pymunk.Circle
        * pymunk.Poly

    You can control the color of a shape by setting shape.color to the color 
    you want it drawn in.
    
    >>> my_shape.color = (255, 0, 0) # will draw my_shape in red
    
    If you do not want a shape to be drawn, set shape.ignore_draw to True.
    
    >>> my_shape.ignore_draw = True
        
    
    See pyglet_util.demo.py for a full example
    
    :Parameters:
            space : pymunk.Space
                The contents of this Space will be drawn on the surface. 
            batch : pyglet.graphics.Batch
                Use this batch to draw on. You can pass None to have it 
                create a new batch. If you pass in your own batch you need 
                to call draw on it yourself.
    """
    new_batch = False
    if batch == None:
        new_batch = True
        batch = pyglet.graphics.Batch()
    for s in space.shapes:
        if not (hasattr(s, "ignore_draw") and s.ignore_draw):
            draw_shape(s, batch)
    if new_batch:
        batch.draw()
            
            
def draw_shape(shape, batch = None):
    """Draw a pymunk.Shape object
    
    See the documentation of draw_space for full details
    
    :Parameters:
            surface : pygame.Surface
                Surface that the space will be drawn on
            shape : pymunk.Shape
                The Shape object to draw
    """
    if isinstance(shape, pymunk.Circle):
        draw_circle(shape, batch)
    elif isinstance(shape, pymunk.Segment):
        draw_segment(shape, batch)
    elif  isinstance(shape, pymunk.Poly):
        draw_poly(shape, batch)
    
def draw_circle(circle, batch = None):
    """Draw a pymunk.Circle object
    
    See help of draw_space for full details
    
    :Parameters:
            shape : pymunk.Circle
                The circle shape to draw
    """
    circle_center = circle.body.position + circle.offset.rotated(circle.body.angle)
    
    r = 0
    if hasattr(circle, "color"):
        color = circle.color  
    elif circle.body.is_static:
        color = (200, 200, 200)
        r = 1
    else:
        color = (255, 0, 0)
        
    #http://slabode.exofire.net/circle_draw.shtml
    num_segments = int(4 * math.sqrt(circle.radius))
    theta = 2 * math.pi / num_segments
    c = math.cos(theta)
    s = math.sin(theta)
    
    x = circle.radius # we start at angle 0
    y = 0
    
    ps = []
    
    for i in range(num_segments):
        ps += [Vec2d(circle_center.x + x, circle_center.y + y)]
        t = x
        x = c * x - s * y
        y = s * t + c * y
               
    
    
    if circle.body.is_static:
        mode = pyglet.gl.GL_LINES
        ps = [p for p in ps+ps[:1] for _ in (0, 1)]
    else:
        mode = pyglet.gl.GL_TRIANGLE_STRIP
        ps2 = [ps[0]]
        for i in range(1, len(ps)+1/2):
            ps2.append(ps[i])
            ps2.append(ps[-i])
        ps = ps2
    vs = []
    for p in [ps[0]] + ps + [ps[-1]]:
            vs += [p.x, p.y]
        
    c = circle_center + Vec2d(circle.radius, 0).rotated(circle.body.angle)
    cvs = [circle_center.x, circle_center.y, c.x, c.y]
        
    bg = pyglet.graphics.OrderedGroup(0)
        
    l = len(vs)/2
    if batch == None:
        pyglet.graphics.draw(l, mode,
                            ('v2f', vs),
                            ('c3B', color*l))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ('v2f', cvs),
                            ('c3B', (0,0,255)*2))
    else:
        batch.add(len(vs)/2, mode, bg,
                 ('v2f', vs),
                 ('c3B', color*l))
        batch.add(2, pyglet.gl.GL_LINES, None,
                 ('v2f', cvs),
                 ('c3B', (0,0,255)*2))
    return

def draw_poly(poly, batch = None):
    """Draw a pymunk.Poly object
    
    See help of draw_space for full details
    
    :Parameters:
            shape : pymunk.Poly
                The poly shape to draw
    """
    ps = poly.get_points()
    
    if hasattr(poly, "color"):
        color = poly.color  
    elif poly.body.is_static:
        color = (200, 200, 200)
    else:
        color = (0, 255, 0)
        
    if poly.body.is_static:
        mode = pyglet.gl.GL_LINES
        ps = [p for p in ps+ps[:1] for _ in (0, 1)]
    else:
        mode = pyglet.gl.GL_TRIANGLE_STRIP
        ps = [ps[1],ps[2], ps[0]] + ps[3:]
        
    vs = []
    for p in [ps[0]] + ps + [ps[-1]]:
            vs += [p.x, p.y]
        
    l = len(vs)/2
    if batch == None:
        pyglet.graphics.draw(l, mode,
                            ('v2f', vs),
                            ('c3B', color*l))
    else:
        batch.add(l, mode, None,
                 ('v2f', vs),
                 ('c3B', color*l))

def draw_segment(segment, batch = None):
    """Draw a pymunk.Segment object
    
    See help of draw_space for full details
    
    :Parameters:
            shape : pymunk.Segment
                The segment shape to draw
    """
    body = segment.body
    pv1 = body.position + segment.a.rotated(body.angle)
    pv2 = body.position + segment.b.rotated(body.angle)
    
    d = pv2 - pv1
    a = -math.atan2(d.x, d.y)
    dx = segment.radius * math.cos(a)
    dy = segment.radius * math.sin(a)
    
    p1 = pv1 + Vec2d(dx,dy)
    p2 = pv1 - Vec2d(dx,dy)
    p3 = pv2 + Vec2d(dx,dy)
    p4 = pv2 - Vec2d(dx,dy)
           
    vs = [i for xy in [p1,p2,p3]+[p2,p3,p4] for i in xy]
    
    
    if hasattr(segment, "color"):
        color = segment.color  
    elif segment.body.is_static:
        color = (200, 200, 200)
    else:
        color = (0, 0, 255)
        
    l = len(vs)/2
    if batch == None:
        pyglet.graphics.draw(l, pyglet.gl.GL_TRIANGLES,
                            ('v2f', vs),
                            ('c3B', color * l))
    else:
        batch.add(l,pyglet.gl.GL_TRIANGLES, None,
                 ('v2f', vs),
                 ('c3B', color * l))
