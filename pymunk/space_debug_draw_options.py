__docformat__ = "reStructuredText"

from collections import namedtuple

from . import _chipmunk_cffi
cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi    

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

    DRAW_SHAPES = cp.CP_SPACE_DEBUG_DRAW_SHAPES
    """Draw shapes"""

    DRAW_CONSTRAINTS = cp.CP_SPACE_DEBUG_DRAW_CONSTRAINTS
    """Draw constraints"""

    DRAW_COLLISION_POINTS = cp.CP_SPACE_DEBUG_DRAW_COLLISION_POINTS
    """Draw collision points"""

    shape_dynamic_color = (52,152,219,255)
    shape_static_color = (149,165,166,255)
    shape_kinematic_color = (39,174,96,255)
    shape_sleeping_color = (114,148,168,255)
    shape_outline_color = (44,62,80,255)
    constraint_color = (142,68,173,255)
    collision_point_color = (231,76,60,255)

    def __init__(self):
      
        _options = ffi.new("cpSpaceDebugDrawOptions *")
        @ffi.callback("typedef void (*cpSpaceDebugDrawCircleImpl)"
            "(cpVect pos, cpFloat angle, cpFloat radius, "
            "cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, "
            "cpDataPointer data)")
        def f1(pos, angle, radius, outline_color, fill_color, data):
            self.draw_circle(
                Vec2d(pos), angle, radius, 
                self._c(outline_color), self._c(fill_color))
        _options.drawCircle = f1

        @ffi.callback("typedef void (*cpSpaceDebugDrawSegmentImpl)"
            "(cpVect a, cpVect b, cpSpaceDebugColor color, cpDataPointer data)")
        def f2(a, b, color, data):
            self.draw_segment(Vec2d(a), Vec2d(b), self._c(color))
        _options.drawSegment = f2

        @ffi.callback("typedef void (*cpSpaceDebugDrawFatSegmentImpl)"
            "(cpVect a, cpVect b, cpFloat radius, "
            "cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, "
            "cpDataPointer data)")
        def f3(a, b, radius, outline_color, fill_color, data):
            self.draw_fat_segment(
                Vec2d(a), Vec2d(b), radius, 
                self._c(outline_color), self._c(fill_color))
        _options.drawFatSegment = f3

        @ffi.callback("typedef void (*cpSpaceDebugDrawPolygonImpl)"
            "(int count, const cpVect *verts, cpFloat radius, "
            "cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, "
            "cpDataPointer data)")
        def f4(count, verts, radius, outline_color, fill_color, data):
            vs = []
            for i in range(count):
                vs.append(Vec2d(verts[i]))
            self.draw_polygon(
                vs, radius, 
                self._c(outline_color), self._c(fill_color))   
        _options.drawPolygon = f4

        @ffi.callback("typedef void (*cpSpaceDebugDrawDotImpl)"
            "(cpFloat size, cpVect pos, cpSpaceDebugColor color, "
            "cpDataPointer data)")
        def f5(size, pos, color, data):
            self.draw_dot(size, Vec2d(pos), self._c(color))
        _options.drawDot = f5

        @ffi.callback("typedef cpSpaceDebugColor "
            "(*cpSpaceDebugDrawColorForShapeImpl)"
            "(cpShape *shape, cpDataPointer data)")
        def f6(_shape, data):
            space = ffi.from_handle(data)
            shape = space._get_shape(_shape)
            return self.color_for_shape(shape)
        _options.colorForShape = f6

        
        _options.shapeOutlineColor = self.shape_outline_color
        _options.constraintColor = self.constraint_color
        _options.collisionPointColor = self.collision_point_color

        self._options = _options

        self.flags = SpaceDebugDrawOptions.DRAW_SHAPES | \
                SpaceDebugDrawOptions.DRAW_CONSTRAINTS | \
                SpaceDebugDrawOptions.DRAW_COLLISION_POINTS

        self._callbacks = [f1,f2,f3,f4,f5,f6]

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
    flags = property(_get_flags, _set_flags)

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

    def color_for_shape(self, shape):
        if hasattr(shape, "color"):
            return shape.color

        color = self.shape_dynamic_color
        if shape.body != None:
            if shape.body.body_type == Body.STATIC:
                color = self.shape_static_color
            elif shape.body.body_type == Body.KINEMATIC:
                color = self.shape_kinematic_color
            elif shape.body.is_sleeping:
                color = self.shape_sleeping_color
                
        return color
