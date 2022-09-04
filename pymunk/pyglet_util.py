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
from typing import TYPE_CHECKING, Any, Optional, Sequence, Tuple, Type

import pyglet  # type: ignore

import pymunk
from pymunk.space_debug_draw_options import SpaceDebugColor
from pymunk.vec2d import Vec2d

if TYPE_CHECKING:
    from types import TracebackType


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

        if "batch" not in kwargs:
            self.new_batch = True
        else:
            self.batch = kwargs["batch"]

        super(DrawOptions, self).__init__()

    def __enter__(self) -> None:
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
        circle_center = pos

        # http://slabode.exofire.net/circle_draw.shtml
        num_segments = int(4 * math.sqrt(radius))
        theta = 2 * math.pi / num_segments
        c = math.cos(theta)
        s = math.sin(theta)

        x = radius  # we start at angle 0
        y: float = 0

        ps = []

        for _ in range(num_segments):
            ps += [Vec2d(circle_center.x + x, circle_center.y + y)]
            t = x
            x = c * x - s * y
            y = s * t + c * y

        mode = pyglet.gl.GL_TRIANGLE_STRIP
        ps2 = [ps[0]]
        for i in range(1, int(len(ps) + 1 / 2)):
            ps2.append(ps[i])
            ps2.append(ps[-i])
        ps = ps2
        vs = []
        for p in [ps[0]] + ps + [ps[-1]]:
            vs += [p.x, p.y]

        cc = circle_center + Vec2d(radius, 0).rotated(angle)
        cvs = [circle_center.x, circle_center.y, cc.x, cc.y]

        bg = pyglet.graphics.OrderedGroup(0)
        fg = pyglet.graphics.OrderedGroup(1)

        l = len(vs) // 2

        self.batch.add(
            len(vs) // 2, mode, bg, ("v2f", vs), ("c4B", fill_color.as_int() * l)
        )
        self.batch.add(
            2, pyglet.gl.GL_LINES, fg, ("v2f", cvs), ("c4B", outline_color.as_int() * 2)
        )

    def draw_segment(self, a: Vec2d, b: Vec2d, color: SpaceDebugColor) -> None:
        pv1 = a
        pv2 = b
        line = (int(pv1.x), int(pv1.y), int(pv2.x), int(pv2.y))

        self.batch.add(
            2, pyglet.gl.GL_LINES, None, ("v2i", line), ("c4B", color.as_int() * 2)
        )

    def draw_fat_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        pv1 = a
        pv2 = b
        d = pv2 - pv1
        atan = -math.atan2(d.x, d.y)
        radius = max(radius, 1)
        dx = radius * math.cos(atan)
        dy = radius * math.sin(atan)

        p1 = pv1 + Vec2d(dx, dy)
        p2 = pv1 - Vec2d(dx, dy)
        p3 = pv2 + Vec2d(dx, dy)
        p4 = pv2 - Vec2d(dx, dy)

        vs = [i for xy in [p1, p2, p3] + [p2, p3, p4] for i in xy]

        l = len(vs) // 2
        self.batch.add(
            l,
            pyglet.gl.GL_TRIANGLES,
            None,
            ("v2f", vs),
            ("c4B", fill_color.as_int() * l),
        )

        self.draw_circle(a, 0, radius, fill_color, fill_color)
        self.draw_circle(b, 0, radius, fill_color, fill_color)

    def draw_polygon(
        self,
        verts: Sequence[Vec2d],
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        mode = pyglet.gl.GL_TRIANGLE_STRIP

        l = len(verts)
        mid = len(verts) // 2
        vs = []
        for i in range(mid):
            vs += [verts[i].x, verts[i].y]
            vs += [verts[l - 1 - i].x, verts[l - 1 - i].y]

        if l % 2:
            vs += [verts[mid].x, verts[mid].y]

        vs = [vs[0], vs[1]] + vs + [vs[-2], vs[-1]]

        l = len(vs) // 2
        self.batch.add(l, mode, None, ("v2f", vs), ("c4B", fill_color.as_int() * l))

        if radius > 0:
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i + 1) % len(verts)]
                # print(a, b)
                self.draw_fat_segment(a, b, radius, outline_color, outline_color)

    def draw_dot(self, size: float, pos: Vec2d, color: SpaceDebugColor) -> None:
        # todo: optimize this functions
        self.batch.add(
            1,
            pyglet.gl.GL_POINTS,
            _GrPointSize(size),
            ("v2f", pos),
            ("c4B", color.as_int() * 1),
        )


class _GrPointSize(pyglet.graphics.Group):  # type: ignore
    """
    This pyglet rendering group sets a specific point size.
    """

    def __init__(self, size: float = 1.0) -> None:
        super(_GrPointSize, self).__init__()
        self.size = size

    def set_state(self) -> None:
        pyglet.gl.glPointSize(self.size)

    def unset_state(self) -> None:
        pyglet.gl.glPointSize(1.0)
