__docformat__ = "reStructuredText"

from collections import namedtuple

from . import _chipmunk_cffi
cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi    

from .vec2d import Vec2d

class SpaceDebugColor(namedtuple("SpaceDebugColor", ["r","g","b","a"])):
    """Color to be used by the debug drawing API.
    """
    __slots__ = ()    


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

    def __init__(self, draw_circle, draw_segment, draw_fat_segment, draw_polygon, 
        draw_dot, flags, shape_outline_color, color_for_shape, 
        constraint_color, collision_point_color, data):

        def c(color):
            return SpaceDebugColor(color.r, color.g, color.b, color.a)

        _options = ffi.new("cpSpaceDebugDrawOptions *")
        @ffi.callback("typedef void (*cpSpaceDebugDrawCircleImpl)"
            "(cpVect pos, cpFloat angle, cpFloat radius, "
            "cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, "
            "cpDataPointer data)")
        def f1(pos, angle, radius, outline_color, fill_color, data):
            draw_circle(
                Vec2d(pos), angle, radius, 
                c(outline_color), c(fill_color))
        _options.drawCircle = f1

        @ffi.callback("typedef void (*cpSpaceDebugDrawSegmentImpl)"
            "(cpVect a, cpVect b, cpSpaceDebugColor color, cpDataPointer data)")
        def f2(a, b, color, data):
            draw_segment(Vec2d(a), Vec2d(b), c(color))
        _options.drawSegment = f2

        @ffi.callback("typedef void (*cpSpaceDebugDrawFatSegmentImpl)"
            "(cpVect a, cpVect b, cpFloat radius, "
            "cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, "
            "cpDataPointer data)")
        def f3(a, b, radius, outline_color, fill_color, data):
            draw_fat_segment(
                Vec2d(a), Vec2d(b), radius, 
                c(outline_color), c(fill_color))
        _options.drawFatSegment = f3

        @ffi.callback("typedef void (*cpSpaceDebugDrawPolygonImpl)"
            "(int count, const cpVect *verts, cpFloat radius, "
            "cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, "
            "cpDataPointer data)")
        def f4(count, verts, radius, outline_color, fill_color, data):
            vs = []
            for i in range(count):
                vs.append(Vec2d(verts[i]))

            draw_polygon(vs, radius, c(outline_color), c(fill_color))
                    
        _options.drawPolygon = f4

        @ffi.callback("typedef void (*cpSpaceDebugDrawDotImpl)"
            "(cpFloat size, cpVect pos, cpSpaceDebugColor color, "
            "cpDataPointer data)")
        def f5(size, pos, color, data):
            draw_dot(size, Vec2d(pos), c(color))
        _options.drawDot = f5

        @ffi.callback("typedef cpSpaceDebugColor "
            "(*cpSpaceDebugDrawColorForShapeImpl)"
            "(cpShape *shape, cpDataPointer data)")
        def f6(shape, data):
        
            return SpaceDebugColor(255,0,0,255)

        _options.colorForShape = f6

        _color = ffi.new("cpSpaceDebugColor *")

        _options.flags = flags

        _options.shapeOutlineColor = shape_outline_color

        _options.constraintColor = constraint_color

        _options.collisionPointColor = collision_point_color

        self._options = _options
        self._callbacks = [f1,f2,f3,f4,f5,f6]

    def __repr__(self):
        r = ('SpaceDebugDrawOptions(draw_circle={}, draw_segment={}, '
            'draw_fat_segment={}, draw_polygon={}, draw_dot={}, flags={}, '
            'shape_outline_color={}, color_for_shape={}, constraint_color={}, '
            'collision_point_color={}, data={})').format(
            draw_circle, draw_segment, draw_fat_segment, draw_polygon, 
            draw_dot, flags, shape_outline_color, color_for_shape, 
            constraint_color, collision_point_color, data)
        return r

    @staticmethod
    def text_options():
        def draw_circle(*args):
            print("draw_circle", args)

        def draw_segment(*args):
            print("draw_segment", args)

        def draw_fat_segment(*args):
            print("draw_fat_segment", args)

        def draw_polygon(*args):
            print("draw_polygon", args)

        def draw_dot(*args):
            print("draw_dot", args)

        def color_for_shape(*args):
            print("color_for_shape", args)
            return 244,255,255,2

        flags = SpaceDebugDrawOptions.DRAW_SHAPES | \
                SpaceDebugDrawOptions.DRAW_CONSTRAINTS | \
                SpaceDebugDrawOptions.DRAW_COLLISION_POINTS
                
        options = SpaceDebugDrawOptions(
            draw_circle=draw_circle,
            draw_segment=draw_segment,
            draw_fat_segment=draw_fat_segment,
            draw_polygon=draw_polygon,
            draw_dot=draw_dot,
            flags=flags,
            shape_outline_color=(150,150,150,255),
            color_for_shape=color_for_shape,
            constraint_color=(150,150,150,255),
            collision_point_color=(200,0,0,150),
            data=None
        )
        return options