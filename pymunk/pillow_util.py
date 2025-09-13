# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2025 Victor Blomqvist
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
using pymunk together with Pillow/PIL.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated
about your coordinate system and not in any way optimized.
"""

__docformat__ = "reStructuredText"

__all__ = [
    "DrawOptions",
]

from typing import Sequence

from PIL import ImageDraw, Image

import pymunk
from pymunk.space_debug_draw_options import SpaceDebugColor
from pymunk.vec2d import Vec2d


class DrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, im: Image.Image) -> None:
        """Draw a pymunk.Space on a pygame.Surface object.

        This class should work both with Pygame and Pygame-CE.

        Typical usage::

        >>> import pymunk
        >>> surface = pygame.Surface((10,10))
        >>> space = pymunk.Space()
        >>> options = pymunk.pygame_util.DrawOptions(surface)
        >>> space.debug_draw(options)

        You can control the color of a shape by setting shape.color to the color
        you want it drawn in::

        >>> c = pymunk.Circle(None, 10)
        >>> c.color = pygame.Color("pink")

        See pygame_util.demo.py for a full example


        >>> space = pymunk.Space()
        >>> space.gravity = (0, -1000)
        >>> body = pymunk.Body()
        >>> body.position = (0, 0) # will be positioned in the top left corner
        >>> space.debug_draw(options)

        >>> body = pymunk.Body()
        >>> body.position = (0, 0)
        >>> # Body will be position in bottom left corner

        :Parameters:
                im : Image.Image
                    Image that the objects will be drawn on
        """
        self.image = im
        self.draw = ImageDraw.Draw(im)
        super(DrawOptions, self).__init__()

    def draw_circle(
        self,
        pos: Vec2d,
        angle: float,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        self.draw.circle(pos, radius, fill_color.as_int(), outline_color.as_int(), 1)

        circle_edge = pos + Vec2d.from_polar(radius, angle)
        p2 = circle_edge
        line_r = 2 if radius > 20 else 1
        self.draw.line([pos, p2], outline_color.as_int(), line_r)
        

    def draw_segment(self, a: Vec2d, b: Vec2d, color: SpaceDebugColor) -> None:
        self.draw.line([a,b], color.as_int())

    def draw_fat_segment(
        self,
        a: tuple[float, float],
        b: tuple[float, float],
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        p1 = a
        p2 = b

        r = round(max(1, radius * 2))
        self.draw.line([a,b], fill_color.as_int(), r)
        
        if r > 2:
            orthog = [abs(p2[1] - p1[1]), abs(p2[0] - p1[0])]
            if orthog[0] == 0 and orthog[1] == 0:
                return
            scale = radius / (orthog[0] * orthog[0] + orthog[1] * orthog[1]) ** 0.5
            orthog[0] = round(orthog[0] * scale)
            orthog[1] = round(orthog[1] * scale)
            points = [
                (p1[0] - orthog[0], p1[1] - orthog[1]),
                (p1[0] + orthog[0], p1[1] + orthog[1]),
                (p2[0] + orthog[0], p2[1] + orthog[1]),
                (p2[0] - orthog[0], p2[1] - orthog[1]),
            ]
            self.draw.polygon(points, fill_color.as_int())
            self.draw.circle((round(p1[0]), round(p1[1])), radius-1, fill_color.as_int())
            self.draw.circle((round(p2[0]), round(p2[1])), radius-1, fill_color.as_int())
            
    def draw_polygon(
        self,
        verts: Sequence[tuple[float, float]],
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        ps = [v for v in verts]
        ps += [ps[0]]

        self.draw.polygon(ps, fill_color.as_int())

        if radius > 0:
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i + 1) % len(verts)]
                self.draw_fat_segment(a, b, radius, outline_color, outline_color)

    def draw_dot(
        self, size: float, pos: tuple[float, float], color: SpaceDebugColor
    ) -> None:
        self.draw.circle(pos, size, color.as_int(), width=0)


