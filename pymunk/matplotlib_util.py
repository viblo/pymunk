"""This submodule contains helper functions to help with quick prototyping 
using pymunk together with pyglet.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated 
about your coordinate system and not very optimized (they use batched 
drawing, but there is probably room for optimizations still). 
"""

__docformat__ = "reStructuredText"

__all__ = ["DrawOptions"]

import matplotlib.pyplot as plt

import pymunk
from pymunk.vec2d import Vec2d

class DrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, ax):
        """DrawOptions for space.debug_draw() to draw a space on a ax object. 

        Typical usage::
        
        >>> import matplotlib as mpl
        >>> import pymunk
        >>> import pymunk.matplotlib_util
        >>> my_space = pymunk.Space()
        >>> fix, ax = mpl.subplot()
        >>> options = pymunk.matplotlib_util.DrawOptions(ax)
        >>> my_space.debug_draw(options)

        You can control the color of a Shape by setting shape.color to the color 
        you want it drawn in.

        >>> my_shape.color = (1, 0, 0, 1) # will draw my_shape in red

        See matplotlib_util.demo.py for a full example

        :Param:
            ax: matplotlib.Axes
                A matplotlib Axes object.

        """
        super(DrawOptions, self).__init__()

        self.ax = ax
        self.shape_dynamic_color = self.shape_dynamic_color.as_float()
        self.shape_static_color = self.shape_static_color.as_float()
        self.shape_kinematic_color = self.shape_kinematic_color.as_float()
        self.shape_sleeping_color = self.shape_sleeping_color.as_float()
        self.shape_outline_color = self.shape_outline_color.as_float()
        self.constraint_color = self.constraint_color.as_float()
        self.collision_point_color = self.collision_point_color.as_float()
    
    def draw_circle(self, pos, angle, radius, outline_color, fill_color):        
        p = plt.Circle(pos, radius, 
            facecolor=fill_color, edgecolor=outline_color)
        self.ax.add_patch(p)
        
        circle_edge = pos + Vec2d(radius, 0).rotated(angle)
        line = plt.Line2D([pos.x, circle_edge.x], [pos.y, circle_edge.y], 
            linewidth=1, color=outline_color)
        line.set_solid_capstyle("round")
        self.ax.add_line(line)

    def draw_segment(self, a, b, color):
        line = plt.Line2D([a.x, b.x], [a.y, b.y], linewidth=1, color=color)
        line.set_solid_capstyle("round")
        self.ax.add_line(line)

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        radius = max(1, 2*radius)
        line = plt.Line2D([a.x, b.x], [a.y, b.y], 
            linewidth=radius, color=fill_color)
        line.set_solid_capstyle("round")
        self.ax.add_line(line)
        
    def draw_polygon(self, verts, radius, outline_color, fill_color):
        radius = max(1, 2*radius)
        p = plt.Polygon(verts, linewidth=radius, joinstyle="round", 
            facecolor=fill_color, edgecolor=outline_color)
        self.ax.add_patch(p)
        
    def draw_dot(self, size, pos, color):
        p = plt.Circle(pos, size, facecolor=color, edgecolor='None')
        self.ax.add_patch(p)
