__docformat__ = "reStructuredText"

from collections import namedtuple
import math

from ._chipmunk_cffi import lib, ffi 

from .vec2d import Vec2d
from .body import Body

class SpaceDebugColor(namedtuple("SpaceDebugColor", ["r","g","b","a"])):
    """Color tuple used by the debug drawing API.
    """
    __slots__ = ()    

    def as_int(self):
        return int(self[0]), int(self[1]), int(self[2]), int(self[3])

    def as_float(self):
        return self[0]/255., self[1]/255., self[2]/255., self[3]/255.


class SpaceDebugDrawOptions(object):
    """SpaceDebugDrawOptions configures debug drawing. 

    If appropriate its usually easy to use the supplied draw implementations 
    directly: pymunk.pygame_util, pymunk.pyglet_util and pymunk.matplotlib_util.
    """

    DRAW_SHAPES = lib.CP_SPACE_DEBUG_DRAW_SHAPES
    """Draw shapes.  
    
    Use on the flags property to control if shapes should be drawn or not.
    """

    DRAW_CONSTRAINTS = lib.CP_SPACE_DEBUG_DRAW_CONSTRAINTS
    """Draw constraints. 
    
    Use on the flags property to control if constraints should be drawn or not.
    """

    DRAW_COLLISION_POINTS = lib.CP_SPACE_DEBUG_DRAW_COLLISION_POINTS
    """Draw collision points.
    
    Use on the flags property to control if collision points should be drawn or
    not.
    """

    shape_dynamic_color = SpaceDebugColor(52,152,219,255)
    shape_static_color = SpaceDebugColor(149,165,166,255)
    shape_kinematic_color = SpaceDebugColor(39,174,96,255)
    shape_sleeping_color = SpaceDebugColor(114,148,168,255)

    def __init__(self):
        _options = ffi.new("cpSpaceDebugDrawOptions *")
        self._options = _options        
        self.shape_outline_color = (44,62,80,255)
        self.constraint_color = (142,68,173,255)
        self.collision_point_color = (231,76,60,255)  
        
        # Set to false to bypass chipmunk shape drawing code
        self._use_chipmunk_debug_draw = True 
        
        
        @ffi.callback("cpSpaceDebugDrawCircleImpl")
        def f1(pos, angle, radius, outline_color, fill_color, data):
            self.draw_circle(
                Vec2d._fromcffi(pos), angle, radius, 
                self._c(outline_color), self._c(fill_color))
        _options.drawCircle = f1

        @ffi.callback("cpSpaceDebugDrawSegmentImpl")
        def f2(a, b, color, data):
            # sometimes a and/or b can be nan. For example if both endpoints 
            # of a spring is at the same position. In those cases skip calling 
            # the drawing method.
            if math.isnan(a.x) or math.isnan(a.y) or \
                math.isnan(b.x) or math.isnan(b.y):
                return
            self.draw_segment(
                Vec2d._fromcffi(a), Vec2d._fromcffi(b), self._c(color))
        _options.drawSegment = f2

        @ffi.callback("cpSpaceDebugDrawFatSegmentImpl")
        def f3(a, b, radius, outline_color, fill_color, data):
            self.draw_fat_segment(
                Vec2d._fromcffi(a), Vec2d._fromcffi(b), radius, 
                self._c(outline_color), self._c(fill_color))
        _options.drawFatSegment = f3

        @ffi.callback("cpSpaceDebugDrawPolygonImpl")
        def f4(count, verts, radius, outline_color, fill_color, data):
            vs = []
            for i in range(count):
                vs.append(Vec2d._fromcffi(verts[i]))
            self.draw_polygon(
                vs, radius, 
                self._c(outline_color), self._c(fill_color))   
        _options.drawPolygon = f4

        @ffi.callback("cpSpaceDebugDrawDotImpl")
        def f5(size, pos, color, data):
            self.draw_dot(size, Vec2d._fromcffi(pos), self._c(color))
        _options.drawDot = f5

        @ffi.callback("cpSpaceDebugDrawColorForShapeImpl")
        def f6(_shape, data):
            space = ffi.from_handle(data)
            shape = space._get_shape(_shape)
            return self.color_for_shape(shape)
        _options.colorForShape = f6

        self.flags = SpaceDebugDrawOptions.DRAW_SHAPES | \
                SpaceDebugDrawOptions.DRAW_CONSTRAINTS | \
                SpaceDebugDrawOptions.DRAW_COLLISION_POINTS

        self._callbacks = [f1,f2,f3,f4,f5,f6]

    def _get_shape_outline_color(self):
        return self._c(self._options.shapeOutlineColor)
    def _set_shape_outline_color(self, c):
        self._options.shapeOutlineColor = c
    shape_outline_color = property(_get_shape_outline_color, 
        _set_shape_outline_color,
        doc="""The outline color of shapes.
        
        Should be a tuple of 4 ints between 0 and 255 (r,g,b,a).

        Example:

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> c = pymunk.Circle(s.static_body, 10)
        >>> s.add(c)
        >>> options = pymunk.SpaceDebugDrawOptions()
        >>> s.debug_draw(options)
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))
        >>> options.shape_outline_color = (10,20,30,40)
        >>> s.debug_draw(options)
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=10.0, g=20.0, b=30.0, a=40.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))

        """)

    def _get_constraint_color(self):
        return self._c(self._options.constraintColor)
    def _set_constraint_color(self, c):
        self._options.constraintColor = c
    constraint_color = property(_get_constraint_color, 
        _set_constraint_color,
        doc="""The color of constraints.

        Should be a tuple of 4 ints between 0 and 255 (r,g,b,a).
        
        Example:

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> j = pymunk.PivotJoint(s.static_body, s.static_body, (0,0))
        >>> s.add(j)
        >>> options = pymunk.SpaceDebugDrawOptions()
        >>> s.debug_draw(options)
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0))
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0))
        >>> options.constraint_color = (10,20,30,40)
        >>> s.debug_draw(options)
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=10.0, g=20.0, b=30.0, a=40.0))
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=10.0, g=20.0, b=30.0, a=40.0))

        """)

    def _get_collision_point_color(self):
        return self._c(self._options.collisionPointColor)
    def _set_collision_point_color(self, c):
        self._options.collisionPointColor = c
    collision_point_color = property(_get_collision_point_color, 
        _set_collision_point_color,
        doc="""The color of collisions.

        Should be a tuple of 4 ints between 0 and 255 (r,g,b,a).
        
        Example:

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> b = pymunk.Body(1,10)
        >>> c1 = pymunk.Circle(b, 10)
        >>> c2 = pymunk.Circle(s.static_body, 10)
        >>> s.add(b, c1, c2)
        >>> s.step(1)
        >>> options = pymunk.SpaceDebugDrawOptions()
        >>> s.debug_draw(options)
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))
        draw_segment (Vec2d(8.0, 0.0), Vec2d(-8.0, 0.0), SpaceDebugColor(r=231.0, g=76.0, b=60.0, a=255.0))
        >>> options.collision_point_color = (10,20,30,40)
        >>> s.debug_draw(options)
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))
        draw_segment (Vec2d(8.0, 0.0), Vec2d(-8.0, 0.0), SpaceDebugColor(r=10.0, g=20.0, b=30.0, a=40.0))
        """)

    def __enter__(self):
        pass
    def __exit__(self, type, value, traceback):
        pass

    def _c(self, color):
        return SpaceDebugColor(color.r, color.g, color.b, color.a)

    def _get_flags(self):
        return self._options.flags
    def _set_flags(self, f):
        self._options.flags = f
    flags = property(_get_flags, _set_flags,
        doc="""Bit flags which of shapes, joints and collisions should be drawn.

        By default all 3 flags are set, meaning shapes, joints and collisions 
        will be drawn.

        Example using the basic text only DebugDraw implementation (normally
        you would the desired backend instead, such as 
        `pygame_util.DrawOptions` or `pyglet_util.DrawOptions`):

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> b = pymunk.Body()
        >>> c = pymunk.Circle(b, 10)
        >>> c.mass = 3
        >>> s.add(b, c)
        >>> s.add(pymunk.Circle(s.static_body, 3))
        >>> s.step(0.01)
        >>> options = pymunk.SpaceDebugDrawOptions() 
        
        >>> # Only draw the shapes, nothing else:
        >>> options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
        >>> s.debug_draw(options) 
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))
        draw_circle (Vec2d(0.0, 0.0), 0.0, 3.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))

        >>> # Draw the shapes and collision points:
        >>> options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
        >>> options.flags |= pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS
        >>> s.debug_draw(options)
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))
        draw_circle (Vec2d(0.0, 0.0), 0.0, 3.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))
        draw_segment (Vec2d(1.0, 0.0), Vec2d(-8.0, 0.0), SpaceDebugColor(r=231.0, g=76.0, b=60.0, a=255.0))
        
        """)

    def draw_circle(self, *args):
        print("draw_circle", args)

    def draw_segment(self, *args):
        print("draw_segment", args)

    def draw_fat_segment(self, *args):
        print("draw_fat_segment", args)

    def draw_polygon(self, *args):
        print("draw_polygon", args)

    def draw_dot(self, *args):
        print("draw_dot", args)

    def draw_shape(self, shape):
        print("draw_shape", shape)

    def color_for_shape(self, shape):
        if hasattr(shape, "color"):
            return SpaceDebugColor(*shape.color)

        color = self.shape_dynamic_color
        if shape.body != None:
            if shape.body.body_type == Body.STATIC:
                color = self.shape_static_color
            elif shape.body.body_type == Body.KINEMATIC:
                color = self.shape_kinematic_color
            elif shape.body.is_sleeping:
                color = self.shape_sleeping_color
                
        return color
