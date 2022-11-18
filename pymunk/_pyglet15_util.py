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
using pymunk together with pyglet.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated 
about your coordinate system and not very optimized (they use batched 
drawing, but there is probably room for optimizations still). 
"""

__docformat__ = "reStructuredText"

import math
import warnings
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Type

import pyglet  # type: ignore

import pymunk
from pymunk.space_debug_draw_options import SpaceDebugColor
from pymunk.vec2d import Vec2d

if TYPE_CHECKING:
    from types import TracebackType

warnings.simplefilter("always", DeprecationWarning)
warnings.warn(
    "Use of pyglet < 2 is deprecated. Please upgrade.",
    category=DeprecationWarning,
    stacklevel=3,
)
warnings.simplefilter("default", DeprecationWarning)


class DrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, **kwargs: Any) -> None:
        """Draw a pymunk.Space.

        Typical usage::

        >>> import pymunk
        >>> import pymunk.pygame_util
        >>> s = pymunk.Space()
        >>> options = pymunk.pyglet_util.DrawOptions()
        >>> s.debug_draw(options)

        You can control the color of a Shape by setting shape.color to the color
        you want it drawn in.

        >>> c = pymunk.Circle(None, 10)
        >>> c.color = (255, 0, 0, 255) # will draw my_shape in red

        You can optionally pass in a batch to use for drawing. Just
        remember that you need to call draw yourself.

        >>> my_batch = pyglet.graphics.Batch()
        >>> s = pymunk.Space()
        >>> options = pymunk.pyglet_util.DrawOptions(batch=my_batch)
        >>> s.debug_draw(options)
        >>> my_batch.draw()

        See pyglet_util.demo.py for a full example

        :Param:
                kwargs : You can optionally pass in a pyglet.graphics.Batch
                    If a batch is given all drawing will use this batch to draw
                    on. If no batch is given a a new batch will be used for the
                    drawing. Remember that if you pass in your own batch you
                    need to call draw on it yourself.

        """
        self.new_batch = False
        self.draw_shapes: List[Any] = []

        if "batch" not in kwargs:
            self.new_batch = True
        else:
            self.batch = kwargs["batch"]

        super(DrawOptions, self).__init__()

    def __enter__(self) -> None:
        self.draw_shapes = []
        if self.new_batch:
            self.batch = pyglet.graphics.Batch()

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional["TracebackType"],
    ) -> None:
        if self.new_batch:
            self.batch.draw()

    def draw_circle(
        self,
        pos: Vec2d,
        angle: float,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:

        bg = pyglet.graphics.OrderedGroup(0)
        fg = pyglet.graphics.OrderedGroup(1)

        color = fill_color.as_int()
        c = pyglet.shapes.Circle(
            pos.x, pos.y, radius, color=color[:3], batch=self.batch, group=bg
        )
        c.opacity = color[3]
        self.draw_shapes.append(c)
        cc = pos + Vec2d(radius, 0).rotated(angle)
        c = outline_color.as_int()
        l = pyglet.shapes.Line(
            pos.x, pos.y, cc.x, cc.y, width=1, color=c[:3], batch=self.batch, group=fg
        )
        self.draw_shapes.append(l)

    def draw_segment(self, a: Vec2d, b: Vec2d, color: SpaceDebugColor) -> None:
        c = color.as_int()
        l = pyglet.shapes.Line(
            a.x, a.y, b.x, b.y, width=1, color=c[:3], batch=self.batch
        )
        self.draw_shapes.append(l)

    def draw_fat_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:

        c = fill_color.as_int()
        pv1 = a
        pv2 = b
        d = pv2 - pv1
        atan = -math.atan2(d.x, d.y)
        radius = max(radius, 1)
        dx = radius * math.cos(atan)
        dy = radius * math.sin(atan)

        p1 = pv1 + Vec2d(dx, dy)
        p2 = pv1 - Vec2d(dx, dy)
        p3 = pv2 - Vec2d(dx, dy)
        p4 = pv2 + Vec2d(dx, dy)

        s = pyglet.shapes.Polygon(p1, p2, p3, p4, color=c[:3], batch=self.batch)
        self.draw_shapes.append(s)

        self.draw_circle(a, 0, radius, fill_color, fill_color)
        self.draw_circle(b, 0, radius, fill_color, fill_color)

    def draw_polygon(
        self,
        verts: Sequence[Vec2d],
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:

        c = fill_color.as_int()
        s = pyglet.shapes.Polygon(*verts, color=c[:3], batch=self.batch)
        self.draw_shapes.append(s)

        if radius > 0:
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i + 1) % len(verts)]
                self.draw_fat_segment(a, b, radius, outline_color, outline_color)

    def draw_dot(self, size: float, pos: Vec2d, color: SpaceDebugColor) -> None:
        # todo: optimize this functions
        c = color.as_int()
        s = pyglet.shapes.Circle(pos.x, pos.y, size, color=c[:3], batch=self.batch)
        s.opacity = c[3]
        self.draw_shapes.append(s)
