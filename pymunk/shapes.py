__docformat__ = "reStructuredText"

import weakref
from typing import TYPE_CHECKING, Optional, Sequence

if TYPE_CHECKING:
    from .body import Body
    from .space import Space

from ._chipmunk_cffi import ffi
from ._chipmunk_cffi import lib as cp
from ._pickle import PickleMixin, _State
from ._typing_attr import TypingAttrMixing
from ._util import _dead_ref
from .bb import BB
from .contact_point_set import ContactPointSet
from .query_info import PointQueryInfo, SegmentQueryInfo
from .shape_filter import ShapeFilter
from .transform import Transform
from .vec2d import Vec2d


class Shape(PickleMixin, TypingAttrMixing, object):
    """Base class for all the shapes.

    You usually don't want to create instances of this class directly but use
    one of the specialized shapes instead (:py:class:`Circle`,
    :py:class:`Poly` or :py:class:`Segment`).

    All the shapes can be copied and pickled. If you copy/pickle a shape, the
    body (if any) will also be copied.
    """

    _pickle_attrs_init = PickleMixin._pickle_attrs_init + ["body"]
    _pickle_attrs_general = PickleMixin._pickle_attrs_general + [
        "sensor",
        "collision_type",
        "filter",
        "elasticity",
        "friction",
        "surface_velocity",
        "_hashid",
    ]
    _pickle_attrs_skip = PickleMixin._pickle_attrs_skip + ["mass", "density"]

    _space: weakref.ref["Space"] = _dead_ref

    def __init__(self, shape: "Shape") -> None:
        self._shape = shape
        assert shape.body != None
        self._body: weakref.ref["Body"] = weakref.ref(shape.body)

    def _init(self, body: Optional["Body"], _shape: ffi.CData) -> None:

        if body is not None:
            self._body = weakref.ref(body)
            body._shapes[self] = None
        else:
            self._body = _dead_ref

        def shapefree(cp_shape: ffi.CData) -> None:
            cp_space = cp.cpShapeGetSpace(cp_shape)
            if cp_space != ffi.NULL:
                cp.cpSpaceRemoveShape(cp_space, cp_shape)

            # cp_body = cp.cpShapeGetBody(cp_shape)
            # if cp_body != ffi.NULL:
            #     cp.cpShapeSetBody(cp_shape, ffi.NULL)
            cp.cpShapeFree(cp_shape)

        self._shape = ffi.gc(_shape, shapefree)
        self._h = ffi.new_handle(self)  # to prevent GC of the handle
        cp.cpShapeSetUserData(self._shape, self._h)

    @property
    def mass(self) -> float:
        """The mass of this shape.

        This is useful when you let Pymunk calculate the total mass and inertia
        of a body from the shapes attached to it. (Instead of setting the body
        mass and inertia directly)
        """
        return cp.cpShapeGetMass(self._shape)

    @mass.setter
    def mass(self, mass: float) -> None:
        cp.cpShapeSetMass(self._shape, mass)

    @property
    def density(self) -> float:
        """The density of this shape.

        This is useful when you let Pymunk calculate the total mass and inertia
        of a body from the shapes attached to it. (Instead of setting the body
        mass and inertia directly)
        """
        return cp.cpShapeGetDensity(self._shape)

    @density.setter
    def density(self, density: float) -> None:
        cp.cpShapeSetDensity(self._shape, density)

    @property
    def moment(self) -> float:
        """The calculated moment of this shape."""
        return cp.cpShapeGetMoment(self._shape)

    @property
    def area(self) -> float:
        """The calculated area of this shape."""
        return cp.cpShapeGetArea(self._shape)

    @property
    def center_of_gravity(self) -> Vec2d:
        """The calculated center of gravity of this shape."""
        v = cp.cpShapeGetCenterOfGravity(self._shape)
        return Vec2d(v.x, v.y)

    @property
    def sensor(self) -> bool:
        """A boolean value if this shape is a sensor or not.

        Sensors only call collision callbacks, and never generate real
        collisions.
        """
        return bool(cp.cpShapeGetSensor(self._shape))

    @sensor.setter
    def sensor(self, is_sensor: bool) -> None:
        cp.cpShapeSetSensor(self._shape, is_sensor)

    @property
    def collision_type(self) -> int:
        """User defined collision type for the shape.

        Defaults to 0.

        See the :py:meth:`Space.add_collision_handler` function for more
        information on when to use this property.
        """
        return cp.cpShapeGetCollisionType(self._shape)

    @collision_type.setter
    def collision_type(self, t: int) -> None:
        cp.cpShapeSetCollisionType(self._shape, t)

    @property
    def filter(self) -> ShapeFilter:
        """Set the collision :py:class:`ShapeFilter` for this shape."""
        f = cp.cpShapeGetFilter(self._shape)
        return ShapeFilter(f.group, f.categories, f.mask)

    @filter.setter
    def filter(self, f: ShapeFilter) -> None:
        cp.cpShapeSetFilter(self._shape, f)

    @property
    def elasticity(self) -> float:
        """Elasticity of the shape.

        A value of 0.0 gives no bounce, while a value of 1.0 will give a
        'perfect' bounce. However due to inaccuracies in the simulation
        using 1.0 or greater is not recommended.
        """
        return cp.cpShapeGetElasticity(self._shape)

    @elasticity.setter
    def elasticity(self, e: float) -> None:
        cp.cpShapeSetElasticity(self._shape, e)

    @property
    def friction(self) -> float:
        """Friction coefficient.

        Pymunk uses the Coulomb friction model, a value of 0.0 is
        frictionless.

        A value over 1.0 is perfectly fine.

        Some real world example values from Wikipedia (Remember that
        it is what looks good that is important, not the exact value).

        ==============  ======  ========
        Material        Other   Friction
        ==============  ======  ========
        Aluminium       Steel   0.61
        Copper          Steel   0.53
        Brass           Steel   0.51
        Cast iron       Copper  1.05
        Cast iron       Zinc    0.85
        Concrete (wet)  Rubber  0.30
        Concrete (dry)  Rubber  1.0
        Concrete        Wood    0.62
        Copper          Glass   0.68
        Glass           Glass   0.94
        Metal           Wood    0.5
        Polyethene      Steel   0.2
        Steel           Steel   0.80
        Steel           Teflon  0.04
        Teflon (PTFE)   Teflon  0.04
        Wood            Wood    0.4
        ==============  ======  ========
        """
        return cp.cpShapeGetFriction(self._shape)

    @friction.setter
    def friction(self, u: float) -> None:
        cp.cpShapeSetFriction(self._shape, u)

    @property
    def surface_velocity(self) -> Vec2d:
        """The surface velocity of the object.

        Useful for creating conveyor belts or players that move around. This
        value is only used when calculating friction, not resolving the
        collision.
        """
        v = cp.cpShapeGetSurfaceVelocity(self._shape)
        return Vec2d(v.x, v.y)

    @surface_velocity.setter
    def surface_velocity(self, surface_v: tuple[float, float]) -> None:
        assert len(surface_v) == 2
        cp.cpShapeSetSurfaceVelocity(self._shape, surface_v)

    @property
    def body(self) -> Optional["Body"]:
        """The body this shape is attached to.

        Can be set to None to indicate that this shape doesnt belong to a body.
        The shape only holds a weakref to the Body, meaning it wont prevent it
        from being GCed.
        """
        return self._body()

    @body.setter
    def body(self, body: Optional["Body"]) -> None:
        if self.body is not None:
            del self.body._shapes[self]
        cp_body = ffi.NULL if body is None else body._body
        cp.cpShapeSetBody(self._shape, cp_body)
        if body is not None:
            body._shapes[self] = None
            self._body = weakref.ref(body)
        else:
            self._body = _dead_ref

    def update(self, transform: Transform) -> BB:
        """Update, cache and return the bounding box of a shape with an
        explicit transformation.

        Useful if you have a shape without a body and want to use it for
        querying.
        """
        _bb = cp.cpShapeUpdate(self._shape, transform)
        return BB(_bb.l, _bb.b, _bb.r, _bb.t)

    def cache_bb(self) -> BB:
        """Update and returns the bounding box of this shape."""
        _bb = cp.cpShapeCacheBB(self._shape)
        return BB(_bb.l, _bb.b, _bb.r, _bb.t)

    @property
    def bb(self) -> BB:
        """The bounding box :py:class:`BB` of the shape.

        Only guaranteed to be valid after :py:meth:`Shape.cache_bb` or
        :py:meth:`Space.step` is called. Moving a body that a shape is
        connected to does not update it's bounding box. For shapes used for
        queries that aren't attached to bodies, you can also use
        :py:meth:`Shape.update`.
        """
        _bb = cp.cpShapeGetBB(self._shape)
        return BB(_bb.l, _bb.b, _bb.r, _bb.t)

    def point_query(self, p: tuple[float, float]) -> PointQueryInfo:
        """Check if the given point lies within the shape.

        A negative distance means the point is within the shape.

        :return: tuple of (distance, info)
        :rtype: (float, :py:class:`PointQueryInfo`)
        """
        assert len(p) == 2
        info = ffi.new("cpPointQueryInfo *")
        _ = cp.cpShapePointQuery(self._shape, p, info)

        shape = ffi.from_handle(cp.cpShapeGetUserData(info.shape))
        assert shape == self, "This is a bug in Pymunk. Please report it."
        return PointQueryInfo(
            self,
            Vec2d(info.point.x, info.point.y),
            info.distance,
            Vec2d(info.gradient.x, info.gradient.y),
        )

    def segment_query(
        self, start: tuple[float, float], end: tuple[float, float], radius: float = 0
    ) -> Optional[SegmentQueryInfo]:
        """Check if the line segment from start to end intersects the shape.

        Returns None if it does not intersect

        :rtype: :py:class:`SegmentQueryInfo`
        """
        assert len(start) == 2
        assert len(end) == 2
        info = ffi.new("cpSegmentQueryInfo *")
        r = cp.cpShapeSegmentQuery(self._shape, start, end, radius, info)
        if r:
            shape = ffi.from_handle(cp.cpShapeGetUserData(info.shape))
            assert shape == self, "This is a bug in Pymunk. Please report it."
            return SegmentQueryInfo(
                self,
                Vec2d(info.point.x, info.point.y),
                Vec2d(info.normal.x, info.normal.y),
                info.alpha,
            )
        else:
            return None

    def shapes_collide(self, b: "Shape") -> ContactPointSet:
        """Get contact information about this shape and shape b.

        :rtype: :py:class:`ContactPointSet`
        """
        _points = cp.cpShapesCollide(self._shape, b._shape)
        return ContactPointSet._from_cp(_points)

    @property
    def space(self) -> Optional["Space"]:
        """Get the :py:class:`Space` that shape has been added to (or
        None).
        """
        return self._space()

    @property
    def _hashid(self) -> int:
        return cp.cpShapeGetHashID(self._shape)

    @_hashid.setter
    def _hashid(self, v: int) -> None:
        cp.cpShapeSetHashID(self._shape, v)

    @staticmethod
    def _from_cp_shape(cp_shape: ffi.CData) -> Optional["Shape"]:
        """Get Pymunk Shape from a Chipmunk Shape pointer"""
        if not bool(cp_shape):
            return None
        return ffi.from_handle(cp.cpShapeGetUserData(cp_shape))

    def __getstate__(self) -> _State:
        """Return the state of this object.

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Shape, self).__getstate__()

        if self.mass > 0:
            d["general"].append(("mass", self.mass))
        if self.density > 0:
            d["general"].append(("density", self.density))

        return d


class Circle(Shape):
    """A circle shape defined by a radius.

    This is the fastest and simplest collision shape.
    """

    _pickle_attrs_init = Shape._pickle_attrs_init + ["radius", "offset"]

    def __init__(
        self,
        body: Optional["Body"],
        radius: float,
        offset: tuple[float, float] = (0, 0),
    ) -> None:
        """body is the body attach the circle to, offset is the offset from the
        body's center of gravity in body local coordinates.

        It is legal to send in None as body argument to indicate that this
        shape is not attached to a body. However, you must attach it to a body
        before adding the shape to a space or used for a space shape query.
        """
        assert len(offset) == 2
        body_body = ffi.NULL if body is None else body._body
        _shape = cp.cpCircleShapeNew(body_body, radius, offset)
        self._init(body, _shape)

    def unsafe_set_radius(self, r: float) -> None:
        """Unsafe set the radius of the circle.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpCircleShapeSetRadius(self._shape, r)

    @property
    def radius(self) -> float:
        """The Radius of the circle."""
        return cp.cpCircleShapeGetRadius(self._shape)

    def unsafe_set_offset(self, o: tuple[float, float]) -> None:
        """Unsafe set the offset of the circle.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        assert len(o) == 2
        cp.cpCircleShapeSetOffset(self._shape, o)

    @property
    def offset(self) -> Vec2d:
        """Offset. (body space coordinates)"""
        v = cp.cpCircleShapeGetOffset(self._shape)
        return Vec2d(v.x, v.y)


class Segment(Shape):
    """A line segment shape between two points.

    Meant mainly as a static shape. Can be beveled in order to give them a
    thickness.
    """

    _pickle_attrs_init = Shape._pickle_attrs_init + ["a", "b", "radius"]

    def __init__(
        self,
        body: Optional["Body"],
        a: tuple[float, float],
        b: tuple[float, float],
        radius: float,
    ) -> None:
        """Create a Segment.

        It is legal to send in None as body argument to indicate that this
        shape is not attached to a body. However, you must attach it to a body
        before adding the shape to a space or used for a space shape query.

        :param Body body: The body to attach the segment to
        :param a: The first endpoint of the segment
        :param b: The second endpoint of the segment
        :param float radius: The thickness of the segment
        """
        assert len(a) == 2
        assert len(b) == 2

        body_body = ffi.NULL if body is None else body._body
        _shape = cp.cpSegmentShapeNew(body_body, a, b, radius)
        self._init(body, _shape)

    @property
    def a(self) -> Vec2d:
        """The first of the two endpoints for this segment"""
        v = cp.cpSegmentShapeGetA(self._shape)
        return Vec2d(v.x, v.y)

    @property
    def b(self) -> Vec2d:
        """The second of the two endpoints for this segment"""
        v = cp.cpSegmentShapeGetB(self._shape)
        return Vec2d(v.x, v.y)

    def unsafe_set_endpoints(
        self, a: tuple[float, float], b: tuple[float, float]
    ) -> None:
        """Set the two endpoints for this segment.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        assert len(a) == 2
        assert len(b) == 2
        cp.cpSegmentShapeSetEndpoints(self._shape, a, b)

    @property
    def normal(self) -> Vec2d:
        """The normal"""
        v = cp.cpSegmentShapeGetNormal(self._shape)
        return Vec2d(v.x, v.y)

    def unsafe_set_radius(self, r: float) -> None:
        """Set the radius of the segment.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpSegmentShapeSetRadius(self._shape, r)

    @property
    def radius(self) -> float:
        """The radius/thickness of the segment."""
        return cp.cpSegmentShapeGetRadius(self._shape)

    def set_neighbors(
        self, prev: tuple[float, float], next: tuple[float, float]
    ) -> None:
        """When you have a number of segment shapes that are all joined
        together, things can still collide with the "cracks" between the
        segments. By setting the neighbor segment endpoints you can tell
        Chipmunk to avoid colliding with the inner parts of the crack.
        """
        assert len(prev) == 2
        assert len(next) == 2
        cp.cpSegmentShapeSetNeighbors(self._shape, prev, next)


class Poly(Shape):
    """A convex polygon shape.

    Slowest, but most flexible collision shape.
    """

    def __init__(
        self,
        body: Optional["Body"],
        vertices: Sequence[tuple[float, float]],
        transform: Optional[Transform] = None,
        radius: float = 0,
    ) -> None:
        """Create a polygon.

        A convex hull will be calculated from the vertexes automatically. Note
        that concave ones will be converted to a convex hull using the Quickhull
        algorithm::

            >>> poly = Poly(None, [(-1,0), (0, -0.5), (1, 0), (0,-1)])
            >>> poly.get_vertices()
            [Vec2d(-1.0, 0.0), Vec2d(0.0, -1.0), Vec2d(1.0, 0.0)]

        Adding a small radius will bevel the corners and can significantly
        reduce problems where the poly gets stuck on seams in your geometry.

        It is legal to send in None as body argument to indicate that this
        shape is not attached to a body. However, you must attach it to a body
        before adding the shape to a space or using for a space shape query.

        .. note::
            Make sure to put the vertices around (0,0) or the shape might
            behave strange.

            Either directly place the vertices like the below example:

            >>> w, h = 10, 20
            >>> vs = [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)]
            >>> poly_good = Poly(None, vs)
            >>> print(poly_good.center_of_gravity)
            Vec2d(0.0, 0.0)

            Or use a transform to move them:

            >>> width, height = 10, 20
            >>> vs = [(0, 0), (width, 0), (width, height), (0, height)]
            >>> poly_bad = Poly(None, vs)
            >>> print(poly_bad.center_of_gravity)
            Vec2d(5.0, 10.0)
            >>> t = Transform(tx=-width/2, ty=-height/2)
            >>> poly_good = Poly(None, vs, transform=t)
            >>> print(poly_good.center_of_gravity)
            Vec2d(0.0, 0.0)

        :param Body body: The body to attach the poly to
        :param [(float,float)] vertices: Define a convex hull of the polygon
            with a counterclockwise winding
        :param Transform transform: Transform will be applied to every vertex
        :param float radius: Set the radius of the poly shape

        """
        if transform is None:
            transform = Transform.identity()

        body_body = ffi.NULL if body is None else body._body
        _shape = cp.cpPolyShapeNew(
            body_body, len(vertices), vertices, transform, radius
        )
        self._init(body, _shape)

    def unsafe_set_radius(self, radius: float) -> None:
        """Unsafe set the radius of the poly.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpPolyShapeSetRadius(self._shape, radius)

    @property
    def radius(self) -> float:
        """The radius of the poly shape.

        Extends the poly in all directions with the given radius.
        """
        return cp.cpPolyShapeGetRadius(self._shape)

    @staticmethod
    def create_box(
        body: Optional["Body"], size: tuple[float, float] = (10, 10), radius: float = 0
    ) -> "Poly":
        """Convenience function to create a box with given width and height.

        The boxes will always be centered at the center of gravity of the
        body you are attaching them to. If you want to create an off-center
        box, you will need to use the normal constructor Poly(...).

        Adding a small radius will bevel the corners and can significantly
        reduce problems where the box gets stuck on seams in your geometry.

        :param Body body: The body to attach the poly to
        :param size: Size of the box as (width, height)
        :type size: (`float, float`)
        :param float radius: Radius of poly
        :rtype: :py:class:`Poly`
        """

        self = Poly.__new__(Poly)
        body_body = ffi.NULL if body is None else body._body
        _shape = cp.cpBoxShapeNew(body_body, size[0], size[1], radius)
        self._init(body, _shape)

        return self

    @staticmethod
    def create_box_bb(body: Optional["Body"], bb: BB, radius: float = 0) -> "Poly":
        """Convenience function to create a box shape from a :py:class:`BB`.

        The boxes will always be centered at the center of gravity of the
        body you are attaching them to. If you want to create an off-center
        box, you will need to use the normal constructor Poly(..).

        Adding a small radius will bevel the corners and can significantly
        reduce problems where the box gets stuck on seams in your geometry.

        :param Body body: The body to attach the poly to
        :param BB bb: Size of the box
        :param float radius: Radius of poly
        :rtype: :py:class:`Poly`
        """

        self = Poly.__new__(Poly)
        body_body = ffi.NULL if body is None else body._body
        _shape = cp.cpBoxShapeNew2(body_body, bb, radius)
        self._init(body, _shape)

        return self

    def get_vertices(self) -> list[Vec2d]:
        """Get the vertices in local coordinates for the polygon.

        If you need the vertices in world coordinates then the vertices can be
        transformed by adding the body position and each vertex rotated by the
        body rotation in the following way::

            >>> import pymunk
            >>> b = pymunk.Body()
            >>> b.position = 1,2
            >>> b.angle = 0.5
            >>> shape = pymunk.Poly(b, [(0,0), (10,0), (10,10)])
            >>> for v in shape.get_vertices():
            ...     x,y = v.rotated(shape.body.angle) + shape.body.position
            ...     (int(x), int(y))
            (1, 2)
            (9, 6)
            (4, 15)

        :return: The vertices in local coords
        :rtype: [:py:class:`Vec2d`]
        """
        verts = []
        lines = cp.cpPolyShapeGetCount(self._shape)
        for i in range(lines):
            v = cp.cpPolyShapeGetVert(self._shape, i)
            verts.append(Vec2d(v.x, v.y))
        return verts

    def unsafe_set_vertices(
        self,
        vertices: Sequence[tuple[float, float]],
        transform: Optional[Transform] = None,
    ) -> None:
        """Unsafe set the vertices of the poly.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        if transform is None:
            cp.cpPolyShapeSetVertsRaw(self._shape, len(vertices), vertices)
            return

        cp.cpPolyShapeSetVerts(self._shape, len(vertices), vertices, transform)

    def __getstate__(self) -> _State:
        """Return the state of this object.

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Poly, self).__getstate__()

        d["init"].append(("vertices", self.get_vertices()))
        d["init"].append(("transform", None))
        d["init"].append(("radius", self.radius))
        return d
