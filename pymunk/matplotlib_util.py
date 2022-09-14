"""This submodule contains helper functions to help with quick prototyping 
using pymunk together with pyglet.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated 
about your coordinate system and not very optimized (they use batched 
drawing, but there is probably room for optimizations still). 
"""

__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, Any, Sequence

import matplotlib.pyplot as plt  # type: ignore

import pymunk
from pymunk.space_debug_draw_options import SpaceDebugColor
from pymunk.vec2d import Vec2d

if TYPE_CHECKING:
    import matplotlib as mpl


class DrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, ax: Any) -> None:
        """DrawOptions for space.debug_draw() to draw a space on a ax object.

        Typical usage::

        >>> import matplotlib as mpl
        >>> import matplotlib.pyplot as plt
        >>> import pymunk
        >>> import pymunk.matplotlib_util
        >>> space = pymunk.Space()
        >>> ax = plt.subplot()
        >>> options = pymunk.matplotlib_util.DrawOptions(ax)
        >>> space.debug_draw(options)

        You can control the color of a Shape by setting shape.color to the color
        you want it drawn in.

        >>> shape = pymunk.Circle(space.static_body, 10)
        >>> shape.color = (1, 0, 0, 1) # will draw shape in red

        See matplotlib_util.demo.py for a full example

        :Param:
            ax: matplotlib.Axes
                A matplotlib Axes object.

        """
        super(DrawOptions, self).__init__()

        self.ax = ax

    def draw_circle(
        self,
        pos: Vec2d,
        angle: float,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        p = plt.Circle(
            pos,
            radius,
            facecolor=fill_color.as_float(),
            edgecolor=outline_color.as_float(),
        )
        self.ax.add_patch(p)

        circle_edge = pos + Vec2d(radius, 0).rotated(angle)
        line = plt.Line2D(
            [pos.x, circle_edge.x],
            [pos.y, circle_edge.y],
            linewidth=1,
            color=outline_color.as_float(),
        )
        line.set_solid_capstyle("round")
        self.ax.add_line(line)

    def draw_segment(self, a: Vec2d, b: Vec2d, color: SpaceDebugColor) -> None:
        line = plt.Line2D([a.x, b.x], [a.y, b.y], linewidth=1, color=color.as_float())
        line.set_solid_capstyle("round")
        self.ax.add_line(line)

    def draw_fat_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        radius = max(1, 2 * radius)
        line = plt.Line2D(
            [a.x, b.x], [a.y, b.y], linewidth=radius, color=fill_color.as_float()
        )
        line.set_solid_capstyle("round")
        self.ax.add_line(line)

    def draw_polygon(
        self,
        verts: Sequence[Vec2d],
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        radius = max(1, 2 * radius)
        p = plt.Polygon(
            verts,
            linewidth=radius,
            joinstyle="round",
            facecolor=fill_color.as_float(),
            edgecolor=outline_color.as_float(),
        )
        self.ax.add_patch(p)

    def draw_dot(self, size: float, pos: Vec2d, color: SpaceDebugColor) -> None:
        p = plt.Circle(pos, size, facecolor=color.as_float(), edgecolor="None")
        self.ax.add_patch(p)
