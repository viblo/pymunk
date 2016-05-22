__version__ = "$Id$"
__docformat__ = "reStructuredText"

from . import _chipmunk_cffi
cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi

#from . import _chipmunk as cp
#import ctypes as ct
from ._chipmunk_manual import Transform, ShapeFilter
from ._bb import BB 
from ._query_info import PointQueryInfo, SegmentQueryInfo
from .vec2d import Vec2d

class Shape(object):
    """Base class for all the shapes.

    You usually dont want to create instances of this class directly but use
    one of the specialized shapes instead.
    """

    _space = None # Weak ref to the space holding this body (if any)

    _shapeid_counter = 1

    def __init__(self, shape=None):
        self._shape = shape
        self._body = shape.body

    def __del__(self):
        try:
            cp.cpShapeFree(self._shape)
        except:
            pass

    def _get_shapeid(self):
        return cp.cpShapeGetUserData(self._shape)
    def _set_shapeid(self):
        cp.cpShapeSetUserData(self._shape, ffi.cast("cpDataPointer", Shape._shapeid_counter))
        Shape._shapeid_counter += 1

    def _get_sensor(self):
        return cp.cpShapeGetSensor(self._shape)
    def _set_sensor(self, is_sensor):
        cp.cpShapeSetSensor(self._shape, is_sensor)
    sensor = property(_get_sensor, _set_sensor,
        doc="""A boolean value if this shape is a sensor or not.

        Sensors only call collision callbacks, and never generate real
        collisions.
        """)

    def _get_collision_type(self):
        return cp.cpShapeGetCollisionType(self._shape)
    def _set_collision_type(self, t):
        cp.cpShapeSetCollisionType(self._shape, t)
    collision_type = property(_get_collision_type, _set_collision_type,
        doc="""User defined collision type for the shape.

        See add_collisionpair_func function for more information on when to
        use this property.
        """)

    def _get_filter(self):
        f = cp.cpShapeGetFilter(self._shape)
        return ShapeFilter(f.group, f.categories, f.mask)
    def _set_filter(self, f):
        cp.cpShapeSetFilter(self._shape, f)
    filter = property(_get_filter, _set_filter,
        doc="""Set the collision filter for this shape.""")



    def _get_elasticity(self):
        return cp.cpShapeGetElasticity(self._shape)
    def _set_elasticity(self, e):
        cp.cpShapeSetElasticity(self._shape, e)
    elasticity = property(_get_elasticity, _set_elasticity,
        doc="""Elasticity of the shape.

        A value of 0.0 gives no bounce, while a value of 1.0 will give a
        'perfect' bounce. However due to inaccuracies in the simulation
        using 1.0 or greater is not recommended.
        """)

    def _get_friction(self):
        return cp.cpShapeGetFriction(self._shape)
    def _set_friction(self, u):
        cp.cpShapeSetFriction(self._shape, u)
    friction = property(_get_friction, _set_friction,
        doc="""Friction coefficient.

        pymunk uses the Coulomb friction model, a value of 0.0 is
        frictionless.

        A value over 1.0 is perfectly fine.

        Some real world example values from wikipedia (Remember that
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
        """)

    def _get_surface_velocity(self):
        return Vec2d(cp.cpShapeGetSurfaceVelocity(self._shape))
    def _set_surface_velocity(self, surface_v):
        cp.cpShapeSetSurfaceVelocity(self._shape, surface_v)
    surface_velocity = property(_get_surface_velocity, _set_surface_velocity,
        doc="""The surface velocity of the object.

        Useful for creating conveyor belts or players that move around. This
        value is only used when calculating friction, not resolving the
        collision.
        """)

    def _get_body(self):
        return self._body
    def _set_body(self, body):
        if self._body != None:
            self._body._shapes.remove(self)
        body_body = ffi.NULL if body is None else body._body
        cp.cpShapeSetBody(self._shape, body_body)
        if body != None:
            body._shapes.add(self)
        
        self._body = body

    body = property(_get_body, _set_body,
        doc="""The body this shape is attached to. Can be set to None to
        indicate that this shape doesnt belong to a body.""")

    def update(self, transform):
        """Update, cache and return the bounding box of a shape with an
        explicit transformation.

        Useful if you have a shape without a body and want to use it for
        querying.
        """
        bb = cp.cpShapeUpdate(self._shape, transform)
        return BB(bb)

    def cache_bb(self):
        """Update and returns the bouding box of this shape"""
        return BB(cp.cpShapeCacheBB(self._shape))

    def _get_bb(self):
        return BB(cp.cpShapeGetBB(self._shape))

    bb = property(_get_bb, doc="""The bounding box of the shape.

    Only guaranteed to be valid after Shape.cache_bb() or Space.step() is
    called. Moving a body that a shape is connected to does not update it's
    bounding box. For shapes used for queries that aren't attached to bodies,
    you can also use Shape.update().
    """)

    def point_query(self, p):
        """Check if the given point lies within the shape."""
        #info = cp.cpPointQueryInfo()
        #info_p = ct.POINTER(cp.cpPointQueryInfo)(info)
        info = ffi.new("cpPointQueryInfo *")
        distance = cp.cpShapePointQuery(self._shape, p, info)
        #print info_p
        #print info_p.point
        #print info_p.distance
        #print info_p.gradient
        return PointQueryInfo(self, Vec2d(info.point), info.distance, Vec2d(info.gradient))
        ud = cp.cpShapeGetUserData(info.shape)
        assert ud == self._get_shapeid()
        x = PointQueryInfo(self, info.point, info.distance, info.gradient)
        return distance, x


    def segment_query(self, start, end, radius=0):
        """Check if the line segment from start to end intersects the shape.
        """
        info = ffi.new("cpSegmentQueryInfo *")
        r = cp.cpShapeSegmentQuery(self._shape, start, end, radius, info)
        if r:
            ud = cp.cpShapeGetUserData(info.shape)
            assert ud == self._get_shapeid()
            return SegmentQueryInfo(self, Vec2d(info.point), Vec2d(info.normal), info.alpha)
        else:
            return SegmentQueryInfo(None, Vec2d(info.point), Vec2d(info.normal), info.alpha)

    def _get_space(self):
        if self._space != None:
            return self._space._get_self() #ugly hack because of weakref
        else:
            return None
    space = property(_get_space,
        doc="""Get the Space that shape has been added to (or None).""")

class Circle(Shape):
    """A circle shape defined by a radius

    This is the fastest and simplest collision shape
    """
    def __init__(self, body, radius, offset = (0, 0)):
        """body is the body attach the circle to, offset is the offset from the
        body's center of gravity in body local coordinates.

        It is legal to send in None as body argument to indicate that this
        shape is not attached to a body.
        """

        self._body = body
        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)

        self._shape = cp.cpCircleShapeNew(body_body, radius, offset)
        #self._cs = ffi.csat("", self._shape, ct.POINTER(cp.cpCircleShape))
        self._set_shapeid()

    def unsafe_set_radius(self, r):
        """Unsafe set the radius of the circle.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpCircleShapeSetRadius(self._shape, r)

    def _get_radius(self):
        return cp.cpCircleShapeGetRadius(self._shape)
    radius = property(_get_radius, doc="""The Radius of the circle""")

    def unsafe_set_offset(self, o):
        """Unsafe set the offset of the circle.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpCircleShapeSetOffset(self._shape, o)

    def _get_offset (self):
        return Vec2d(cp.cpCircleShapeGetOffset(self._shape))
    offset = property(_get_offset, doc="""Offset. (body space coordinates)""")


class Segment(Shape):
    """A line segment shape between two points

    Meant mainly as a static shape. Can be beveled in order to give them a
    thickness.

    It is legal to send in None as body argument to indicate that this
    shape is not attached to a body.
    """
    def __init__(self, body, a, b, radius):
        """Create a Segment

        :Parameters:
            body : `Body`
                The body to attach the segment to
            a : (x,y) or `Vec2d`
                The first endpoint of the segment
            b : (x,y) or `Vec2d`
                The second endpoint of the segment
            radius : float
                The thickness of the segment
        """
        self._body = body
        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)
        self._shape = cp.cpSegmentShapeNew(body_body, a, b, radius)
        self._set_shapeid()

    def _get_a(self):
        return Vec2d(cp.cpSegmentShapeGetA(self._shape))
    a = property(_get_a,
        doc="""The first of the two endpoints for this segment""")

    def _get_b(self):
        return Vec2d(cp.cpSegmentShapeGetB(self._shape))
    b = property(_get_b,
        doc="""The second of the two endpoints for this segment""")

    def unsafe_set_endpoints(self, a, b):
        """Set the two endpoints for this segment

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpSegmentShapeSetEndpoints(self._shape, a, b)
        
    def _get_normal(self):
        return Vec2d(cp.cpSegmentShapeGetNormal(self._shape))
    normal = property(_get_normal,
        doc="""The normal""")

    def unsafe_set_radius(self, r):
        """Set the radius of the segment

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpSegmentShapeSetRadius(self._shape, r)
    def _get_radius(self):
        return cp.cpSegmentShapeGetRadius(self._shape)
    radius = property(_get_radius,
        doc="""The radius/thickness of the segment""")

    def set_neighbors(self, prev, next):
        """When you have a number of segment shapes that are all joined
        together, things can still collide with the "cracks" between the
        segments. By setting the neighbor segment endpoints you can tell
        Chipmunk to avoid colliding with the inner parts of the crack.
        """
        cp.cpSegmentShapeSetNeighbors(self._shape, prev, next)

class Poly(Shape):
    """A convex polygon shape

    Slowest, but most flexible collision shape.

    It is legal to send in None as body argument to indicate that this
    shape is not attached to a body.
    """

    def _init():
        pass

    def __init__(self, body, vertices, transform=None, radius=0):
        """Create a polygon.

            A convex hull will be calculated from the vertexes automatically.

            body : `Body`
                The body to attach the poly to
            vertices : [(x,y)] or [`Vec2d`]
                Define a convex hull of the polygon with a counterclockwise
                winding.
            transform : `Transform`
                Transform will be applied to every vertex.
            radius : int
                Set the radius of the poly shape. Adding a small radius will
                bevel the corners and can significantly reduce problems where
                the poly gets stuck on seams in your geometry.
        """

        self._body = body

        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)

        if transform == None:
            transform = Transform.identity()

        self._shape = cp.cpPolyShapeNew(body_body, len(vertices), vertices, transform, radius)
        self._set_shapeid()

    def unsafe_set_radius(self, radius):
        """Unsafe set the radius of the poly.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        cp.cpPolyShapeSetRadius(self._shape, radius)

    def _get_radius(self):
        return cp.cpPolyShapeGetRadius(self._shape)
    radius = property(_get_radius,
        doc="""The radius of the poly shape. Extends the poly in all
        directions with the given radius""")

    @staticmethod
    def create_box(body, size=(10,10), radius=0):
        """Convenience function to create a box.

        The boxes will always be centered at the center of gravity of the
        body you are attaching them to.  If you want to create an off-center
        box, you will need to use the normal constructor Poly(...).

            body : `Body`
                The body to attach the poly to
            size : `(w,h)` or `Vec2d` or `BB`
                Size of the box
            radius : `float`
                Adding a small radius will bevel the corners and can
                significantly reduce problems where the box gets stuck on
                seams in your geometry.

        """

        self = Poly.__new__(Poly)

        self._body = body

        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)

        if isinstance(size, BB):
            self._shape = cp.cpBoxShapeNew2(body_body, size._bb[0], radius)
        else:
            self._shape = cp.cpBoxShapeNew(body_body, size[0], size[1], radius)

        self._set_shapeid()

        return self

    def get_vertices(self):
        """Get the vertices in world coordinates for the polygon

        :return: [`Vec2d`] in world coords
        """
        verts = []
        l = cp.cpPolyShapeGetCount(self._shape)
        for i in range(l):
            verts.append(Vec2d(cp.cpPolyShapeGetVert(self._shape, i)))
        return verts

    def unsafe_set_vertices(self, vertices, transform=None):
        """Unsafe set the vertices of the poly.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        if transform == None:
            cp.cpPolyShapeSetVertsRaw(self._shape, len(vertices), vertices)
            return
            
        cp.cpPolyShapeSetVerts(self._shape, len(vertices), vertices, transform)
