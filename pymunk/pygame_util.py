# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2016 Victor Blomqvist
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
using pymunk together with pygame.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated 
about your coordinate system and not in any way optimized. 
"""

__docformat__ = "reStructuredText"

__all__ = [
    "DrawOptions", "get_mouse_pos", "to_pygame", "from_pygame", 
    "positive_y_is_up"
    ]

import pygame

import pymunk
from pymunk.vec2d import Vec2d

positive_y_is_up = True
"""Make increasing values of y point upwards.

When True::

        y
        ^
        |   . (2, 2)
        |
    ----+------ > x
        |
        |     . (3, -2)
        |

When False::

        y
        ^
        |   . (2, -2)
        |
    ----+------ > x
        |
        |      . (3, 2)
        |

"""

class DrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, surface):
        """Draw a pymunk.Space on a pygame.Surface object.
        
        Typical usage::

        >>> import pymunk
        >>> import pymunk.pygame_util
        >>> surface = pygame.Surface((10,10))
        >>> s = pymunk.Space()
        >>> options = pymunk.pygame_util.DrawOptions(surface)
        >>> s.debug_draw(options)

        Since pygame uses a coordinate system where y points down (compared to
        most other cases where a positive y points upwards), we might want to
        make adjustments for that with the :py:data:`positive_y_is_up` variable.

        By default drawing is done with positive y pointing up, but that will 
        make conversion from pygame coordinate to pymunk coordinate necessary. 
        If you do a lot of those (for example, lots of mouse input) it might be 
        more convenient to set it to False::

        >>> positive_y_is_up = False
        >>> # Draw verything the pygame way, (0,0) in the top left corner 
        >>> positive_y_is_up = True
        >>> # Draw everything the pymunk way, (0,0) in the bottom left corner

        You can control the color of a shape by setting shape.color to the color 
        you want it drawn in.
        
        >>> c = pymunk.Circle(None, 10)
        >>> c.color = pygame.color.THECOLORS["pink"]
        
        See pygame_util.demo.py for a full example
        
        :Parameters:
                surface : pygame.Surface
                    Surface that the objects will be drawn on
        """
        self.surface = surface
        super(DrawOptions, self).__init__()

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        p = to_pygame(pos, self.surface)
    
        pygame.draw.circle(self.surface, fill_color, p, _rndint(radius), 0)
        
        circle_edge = pos + Vec2d(radius, 0).rotated(angle)
        p2 = to_pygame(circle_edge, self.surface)
        line_r = 2 if radius > 20 else 1
        pygame.draw.lines(self.surface, outline_color, False, [p,p2], line_r)    

    def draw_segment(self, a, b, color):
        p1 = to_pygame(a, self.surface)
        p2 = to_pygame(b, self.surface)

        pygame.draw.aalines(self.surface, color, False, [p1,p2])

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        p1 = to_pygame(a, self.surface)
        p2 = to_pygame(b, self.surface)
        
        r = _rndint(max(1, radius*2))
        pygame.draw.lines(self.surface, fill_color, False, [p1,p2], r)
        if r > 2:
            orthog = [ abs(p2[1]-p1[1]), abs(p2[0]-p1[0]) ]
            if orthog[0] == 0 and orthog[1] == 0:
                return
            scale = radius / (orthog[0]*orthog[0] + orthog[1]*orthog[1])**0.5
            orthog[0]*=scale; orthog[1]*=scale
            points = [
                ( p1[0]-orthog[0], p1[1]-orthog[1] ),
                ( p1[0]+orthog[0], p1[1]+orthog[1] ),
                ( p2[0]+orthog[0], p2[1]+orthog[1] ),
                ( p2[0]-orthog[0], p2[1]-orthog[1] )
            ]
            pygame.draw.polygon(self.surface, fill_color, points)
            pygame.draw.circle(self.surface, fill_color, 
                (_rndint(p1[0]),_rndint(p1[1])), _rndint(radius))
            pygame.draw.circle(self.surface, fill_color, 
                (_rndint(p2[0]),_rndint(p2[1])), _rndint(radius))
        
    def draw_polygon(self, verts, radius, outline_color, fill_color):
        ps = [to_pygame(v, self.surface) for v in verts]
        ps += [ps[0]]

        pygame.draw.polygon(self.surface, fill_color, ps)

        if radius > 0:
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i+1) % len(verts)]
                self.draw_fat_segment(a, b, radius, outline_color, 
                    outline_color)

    def draw_dot(self, size, pos, color):
        p = to_pygame(pos, self.surface)
        pygame.draw.circle(self.surface, color, p, _rndint(size), 0)

    
def get_mouse_pos(surface):
    """Get position of the mouse pointer in pymunk coordinates."""
    p = pygame.mouse.get_pos()
    return from_pygame(p, surface)

def to_pygame(p, surface):
    """Convenience method to convert pymunk coordinates to pygame surface 
    local coordinates. 
    
    Note that in case positive_y_is_up is False, this function wont actually do
    anything except converting the point to integers.
    """
    if positive_y_is_up:
        return int(p[0]), surface.get_height()-int(p[1])
    else:
        return int(p[0]), int(p[1])
    
def from_pygame(p, surface):
    """Convenience method to convert pygame surface local coordinates to 
    pymunk coordinates    
    """
    return to_pygame(p,surface)

def _rndint(x): 
    return int(round(x))            
