__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, ClassVar, NamedTuple, Optional, Sequence, Tuple, Type

if TYPE_CHECKING:
    from .shapes import Shape
    from types import TracebackType

import math

from ._chipmunk_cffi import ffi, lib
from .body import Body
from .transform import Transform
from .vec2d import Vec2d

_DrawFlags = int


class SpaceDebugColor(NamedTuple):
    """Color tuple used by the debug drawing API."""

    r: float
    g: float
    b: float
    a: float

    def as_int(self) -> Tuple[int, int, int, int]:
        """Return the color as a tuple of ints, where each value is rounded.

        >>> SpaceDebugColor(0, 51.1, 101.9, 255).as_int()
        (0, 51, 102, 255)
        """
        return round(self[0]), round(self[1]), round(self[2]), round(self[3])

    def as_float(self) -> Tuple[float, float, float, float]:
        """Return the color as a tuple of floats, each value divided by 255.

        >>> SpaceDebugColor(0, 51, 102, 255).as_float()
        (0.0, 0.2, 0.4, 1.0)
        """
        return self[0] / 255.0, self[1] / 255.0, self[2] / 255.0, self[3] / 255.0


class SpaceDebugDrawOptions(object):
    """SpaceDebugDrawOptions configures debug drawing.

    If appropriate its usually easy to use the supplied draw implementations
    directly: pymunk.pygame_util, pymunk.pyglet_util and pymunk.matplotlib_util.
    """

    DRAW_SHAPES: ClassVar[_DrawFlags] = lib.CP_SPACE_DEBUG_DRAW_SHAPES
    """Draw shapes.  
    
    Use on the flags property to control if shapes should be drawn or not.
    """

    DRAW_CONSTRAINTS: ClassVar[_DrawFlags] = lib.CP_SPACE_DEBUG_DRAW_CONSTRAINTS
    """Draw constraints. 
    
    Use on the flags property to control if constraints should be drawn or not.
    """

    DRAW_COLLISION_POINTS: ClassVar[
        _DrawFlags
    ] = lib.CP_SPACE_DEBUG_DRAW_COLLISION_POINTS
    """Draw collision points.
    
    Use on the flags property to control if collision points should be drawn or
    not.
    """

    shape_dynamic_color: SpaceDebugColor = SpaceDebugColor(52, 152, 219, 255)
    shape_static_color: SpaceDebugColor = SpaceDebugColor(149, 165, 166, 255)
    shape_kinematic_color: SpaceDebugColor = SpaceDebugColor(39, 174, 96, 255)
    shape_sleeping_color: SpaceDebugColor = SpaceDebugColor(114, 148, 168, 255)

    def __init__(self) -> None:
        _options = ffi.new("cpSpaceDebugDrawOptions *")
        self._options = _options
        self._options.transform = Transform.identity()
        self.shape_outline_color = SpaceDebugColor(44, 62, 80, 255)
        self.constraint_color = SpaceDebugColor(142, 68, 173, 255)
        self.collision_point_color = SpaceDebugColor(231, 76, 60, 255)

        # Set to false to bypass chipmunk shape drawing code
        self._use_chipmunk_debug_draw = True

        @ffi.callback("cpSpaceDebugDrawCircleImpl")
        def f1(pos, angle, radius, outline_color, fill_color, _):  # type: ignore
            self.draw_circle(
                Vec2d(pos.x, pos.y),
                angle,
                radius,
                self._c(outline_color),
                self._c(fill_color),
            )

        _options.drawCircle = f1

        @ffi.callback("cpSpaceDebugDrawSegmentImpl")
        def f2(a, b, color, _):  # type: ignore
            # sometimes a and/or b can be nan. For example if both endpoints
            # of a spring is at the same position. In those cases skip calling
            # the drawing method.
            if math.isnan(a.x) or math.isnan(a.y) or math.isnan(b.x) or math.isnan(b.y):
                return
            self.draw_segment(
                Vec2d(a.x, a.y),
                Vec2d(b.x, b.y),
                self._c(color),
            )

        _options.drawSegment = f2

        @ffi.callback("cpSpaceDebugDrawFatSegmentImpl")
        def f3(a, b, radius, outline_color, fill_color, _):  # type: ignore
            self.draw_fat_segment(
                Vec2d(a.x, a.y),
                Vec2d(b.x, b.y),
                radius,
                self._c(outline_color),
                self._c(fill_color),
            )

        _options.drawFatSegment = f3

        @ffi.callback("cpSpaceDebugDrawPolygonImpl")
        def f4(count, verts, radius, outline_color, fill_color, _):  # type: ignore
            vs = []
            for i in range(count):
                vs.append(Vec2d(verts[i].x, verts[i].y))
            self.draw_polygon(vs, radius, self._c(outline_color), self._c(fill_color))

        _options.drawPolygon = f4

        @ffi.callback("cpSpaceDebugDrawDotImpl")
        def f5(size, pos, color, _):  # type: ignore
            self.draw_dot(size, Vec2d(pos.x, pos.y), self._c(color))

        _options.drawDot = f5

        @ffi.callback("cpSpaceDebugDrawColorForShapeImpl")
        def f6(_shape, data):  # type: ignore
            space = ffi.from_handle(data)
            shape = space._get_shape(_shape)
            return self.color_for_shape(shape)

        _options.colorForShape = f6

        self.flags = (
            SpaceDebugDrawOptions.DRAW_SHAPES
            | SpaceDebugDrawOptions.DRAW_CONSTRAINTS
            | SpaceDebugDrawOptions.DRAW_COLLISION_POINTS
        )

        self._callbacks = [f1, f2, f3, f4, f5, f6]

    def _get_shape_outline_color(self) -> SpaceDebugColor:
        return self._c(self._options.shapeOutlineColor)

    def _set_shape_outline_color(self, c: SpaceDebugColor) -> None:
        self._options.shapeOutlineColor = c

    shape_outline_color = property(
        _get_shape_outline_color,
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

        """,
    )

    def _get_constraint_color(self) -> SpaceDebugColor:
        return self._c(self._options.constraintColor)

    def _set_constraint_color(self, c: SpaceDebugColor) -> None:
        self._options.constraintColor = c

    constraint_color = property(
        _get_constraint_color,
        _set_constraint_color,
        doc="""The color of constraints.

        Should be a tuple of 4 ints between 0 and 255 (r,g,b,a).
        
        Example:

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> b = pymunk.Body(1, 10)
        >>> j = pymunk.PivotJoint(s.static_body, b, (0,0))
        >>> s.add(j)
        >>> options = pymunk.SpaceDebugDrawOptions()
        >>> s.debug_draw(options)
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0))
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0))
        >>> options.constraint_color = (10,20,30,40)
        >>> s.debug_draw(options)
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=10.0, g=20.0, b=30.0, a=40.0))
        draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=10.0, g=20.0, b=30.0, a=40.0))

        """,
    )

    def _get_collision_point_color(self) -> SpaceDebugColor:
        return self._c(self._options.collisionPointColor)

    def _set_collision_point_color(self, c: SpaceDebugColor) -> None:
        self._options.collisionPointColor = c

    collision_point_color = property(
        _get_collision_point_color,
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
        """,
    )

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional["TracebackType"],
    ) -> None:
        pass

    def _c(self, color: ffi.CData) -> SpaceDebugColor:
        return SpaceDebugColor(color.r, color.g, color.b, color.a)

    def _get_flags(self) -> _DrawFlags:
        return self._options.flags

    def _set_flags(self, f: _DrawFlags) -> None:
        self._options.flags = f

    flags = property(
        _get_flags,
        _set_flags,
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
        
        """,
    )

    def _get_transform(self) -> Transform:
        t = self._options.transform
        return Transform(t.a, t.b, t.c, t.d, t.tx, t.ty)

    def _set_transform(self, t: Transform) -> None:
        self._options.transform = t

    transform = property(
        _get_transform,
        _set_transform,
        doc="""The transform is applied before drawing, e.g for scaling or 
        translation.

        Example: 

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> c = pymunk.Circle(s.static_body, 10)
        >>> s.add(c)
        >>> options = pymunk.SpaceDebugDrawOptions() 
        >>> s.debug_draw(options) 
        draw_circle (Vec2d(0.0, 0.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))
        >>> options.transform = pymunk.Transform.scaling(2)
        >>> s.debug_draw(options)
        draw_circle (Vec2d(0.0, 0.0), 0.0, 20.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))
        >>> options.transform = pymunk.Transform.translation(2,3)
        >>> s.debug_draw(options)
        draw_circle (Vec2d(2.0, 3.0), 0.0, 10.0, SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0))
        
        .. Note::
            Not all tranformations are supported by the debug drawing logic. 
            Uniform scaling and translation are supported, but not rotation,
            linear stretching or shearing. 
        """,
    )

    def draw_circle(
        self,
        pos: Vec2d,
        angle: float,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        print("draw_circle", (pos, angle, radius, outline_color, fill_color))

    def draw_segment(self, a: Vec2d, b: Vec2d, color: SpaceDebugColor) -> None:
        print("draw_segment", (a, b, color))

    def draw_fat_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        print("draw_fat_segment", (a, b, radius, outline_color, fill_color))

    def draw_polygon(
        self,
        verts: Sequence[Vec2d],
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        print("draw_polygon", (verts, radius, outline_color, fill_color))

    def draw_dot(self, size: float, pos: Vec2d, color: SpaceDebugColor) -> None:
        print("draw_dot", (size, pos, color))

    def draw_shape(self, shape: "Shape") -> None:
        print("draw_shape", shape)

    def color_for_shape(self, shape: "Shape") -> SpaceDebugColor:
        if hasattr(shape, "color"):
            return SpaceDebugColor(*shape.color)  # type: ignore

        color = self.shape_dynamic_color
        if shape.body != None:
            if shape.body.body_type == Body.STATIC:
                color = self.shape_static_color
            elif shape.body.body_type == Body.KINEMATIC:
                color = self.shape_kinematic_color
            elif shape.body.is_sleeping:
                color = self.shape_sleeping_color

        return color
