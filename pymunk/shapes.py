__docformat__ = "reStructuredText"

import copy

from . import _chipmunk_cffi
cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi

from .transform import Transform
from .shape_filter import ShapeFilter
from .bb import BB 
from .query_info import PointQueryInfo, SegmentQueryInfo
from .contact_point_set import ContactPointSet
from .vec2d import Vec2d
from ._pickle import PickleMixin

class Shape(PickleMixin, object):
    """Base class for all the shapes.

    You usually dont want to create instances of this class directly but use
    one of the specialized shapes instead (:py:class:`Circle`, 
    :py:class:`Poly` or :py:class:`Segment`).

    All the shapes can be copied and pickled. If you copy/pickle a shape the 
    body (if any) will also be copied.
    """

    _pickle_attrs_init = ['body']
    _pickle_attrs_general = ['sensor', 'collision_type', 
        'filter', 'elasticity', 'friction', 'surface_velocity']
    _pickle_attrs_skip = ['mass', 'density']

    _space = None # Weak ref to the space holding this body (if any)

    _shapeid_counter = 1

    def __init__(self, shape=None):
        self._shape = shape
        self._body = shape.body

    def _get_shapeid(self):
        return cp.cpShapeGetUserData(self._shape)
    def _set_shapeid(self):
        cp.cpShapeSetUserData(
            self._shape, 
            ffi.cast("cpDataPointer", Shape._shapeid_counter))
        Shape._shapeid_counter += 1

    def _get_mass(self):
        return cp.cpShapeGetMass(self._shape)
    def _set_mass(self, mass):
        cp.cpShapeSetMass(self._shape, mass)
    mass = property(_get_mass, _set_mass, 
        doc="""The mass of this shape.

        This is useful when you let Pymunk calculate the total mass and inertia 
        of a body from the shapes attached to it. (Instead of setting the body 
        mass and inertia directly)
        """)

    def _get_density(self):
        return cp.cpShapeGetDensity(self._shape)
    def _set_density(self, density):
        cp.cpShapeSetDensity(self._shape, density)
    density = property(_get_density, _set_density, 
        doc="""The density of this shape.
        
        This is useful when you let Pymunk calculate the total mass and inertia 
        of a body from the shapes attached to it. (Instead of setting the body 
        mass and inertia directly)
        """)

    def _get_moment(self):
        """The calculated moment of this shape."""
        return cp.cpShapeGetMoment(self._shape)
    moment = property(_get_moment, doc=_get_moment.__doc__)

    def _get_area(self):
        """The calculated area of this shape."""
        return cp.cpShapeGetArea(self._shape)
    area = property(_get_area, doc=_get_area.__doc__)

    def _get_center_of_gravity(self):
        """The calculated center of gravity of this shape."""
        return Vec2d._fromcffi(cp.cpShapeGetCenterOfGravity(self._shape))
    center_of_gravity = property(_get_center_of_gravity, 
        doc=_get_center_of_gravity.__doc__)

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

        See :py:meth:`Space.add_collision_handler` function for more 
        information on when to use this property.
        """)

    def _get_filter(self):
        f = cp.cpShapeGetFilter(self._shape)
        return ShapeFilter(f.group, f.categories, f.mask)
    def _set_filter(self, f):
        cp.cpShapeSetFilter(self._shape, f)
    filter = property(_get_filter, _set_filter,
        doc="""Set the collision :py:class:`ShapeFilter` for this shape.
        """)


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
        """)

    def _get_surface_velocity(self):
        return Vec2d._fromcffi(cp.cpShapeGetSurfaceVelocity(self._shape))
    def _set_surface_velocity(self, surface_v):
        cp.cpShapeSetSurfaceVelocity(self._shape, tuple(surface_v))
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
        """Update and returns the bounding box of this shape"""
        return BB(cp.cpShapeCacheBB(self._shape))

    def _get_bb(self):
        return BB(cp.cpShapeGetBB(self._shape))

    bb = property(_get_bb, doc="""The bounding box :py:class:`BB` of the shape.

        Only guaranteed to be valid after :py:meth:`Shape.cache_bb` or 
        :py:meth:`Space.step` is called. Moving a body that a shape is 
        connected to does not update it's bounding box. For shapes used for 
        queries that aren't attached to bodies, you can also use 
        :py:meth:`Shape.update`.
    """)

    def point_query(self, p):
        """Check if the given point lies within the shape.

        A negative distance means the point is within the shape.

        :return: Tuple of (distance, info) 
        :rtype: (float, :py:class:`PointQueryInfo`) 
        """
        info = ffi.new("cpPointQueryInfo *")
        distance = cp.cpShapePointQuery(self._shape, tuple(p), info)
        
        ud = cp.cpShapeGetUserData(info.shape)
        assert ud == self._get_shapeid()
        x = PointQueryInfo(
            self, 
            Vec2d._fromcffi(info.point), 
            info.distance, 
            Vec2d._fromcffi(info.gradient))
        return distance, x


    def segment_query(self, start, end, radius=0):
        """Check if the line segment from start to end intersects the shape.

        :rtype: :py:class:`SegmentQueryInfo`
        """
        info = ffi.new("cpSegmentQueryInfo *")
        r = cp.cpShapeSegmentQuery(
            self._shape, tuple(start), tuple(end), radius, info)
        if r:
            ud = cp.cpShapeGetUserData(info.shape)
            assert ud == self._get_shapeid()
            return SegmentQueryInfo(
                self, Vec2d._fromcffi(info.point), Vec2d._fromcffi(info.normal), info.alpha)
        else:
            return SegmentQueryInfo(
                None, Vec2d._fromcffi(info.point), Vec2d._fromcffi(info.normal), info.alpha)

    def shapes_collide(self, b):
        """Get contact information about this shape and shape b.
        
        :rtype: :py:class:`ContactPointSet`
        """
        _points = cp.cpShapesCollide(self._shape, b._shape)
        return ContactPointSet._from_cp(_points)

    def _get_space(self):
        if self._space != None:
            return self._space._get_self() #ugly hack because of weakref
        else:
            return None
    space = property(_get_space,
        doc="""Get the :py:class:`Space` that shape has been added to (or 
        None).
        """)
    
    def __getstate__(self):
        """Return the state of this object
        
        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Shape, self).__getstate__()

        if self.mass > 0:
            d['general'].append(('mass', self.mass))
        if self.density > 0:
            d['general'].append(('density', self.density))

        return d

    def copy(self):
        """Create a deep copy of this shape."""
        return copy.deepcopy(self)

class Circle(Shape):
    """A circle shape defined by a radius

    This is the fastest and simplest collision shape
    """

    _pickle_attrs_init = ['radius', 'offset']

    def __init__(self, body, radius, offset = (0, 0)):
        """body is the body attach the circle to, offset is the offset from the
        body's center of gravity in body local coordinates.

        It is legal to send in None as body argument to indicate that this
        shape is not attached to a body. However, you must attach it to a body
        before adding the shape to a space or used for a space shape query.
        """

        self._body = body
        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)

        self._shape = ffi.gc(
            cp.cpCircleShapeNew(body_body, radius, tuple(offset)), 
            cp.cpShapeFree)
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
        cp.cpCircleShapeSetOffset(self._shape, tuple(o))

    def _get_offset (self):
        return Vec2d._fromcffi(cp.cpCircleShapeGetOffset(self._shape))
    offset = property(_get_offset, doc="""Offset. (body space coordinates)""")


class Segment(Shape):
    """A line segment shape between two points

    Meant mainly as a static shape. Can be beveled in order to give them a
    thickness.
    """

    _pickle_attrs_init = ['a', 'b', 'radius']

    def __init__(self, body, a, b, radius):
        """Create a Segment

        It is legal to send in None as body argument to indicate that this
        shape is not attached to a body. However, you must attach it to a body
        before adding the shape to a space or used for a space shape query.
    
        :param Body body: The body to attach the segment to
        :param a: The first endpoint of the segment
        :param b: The second endpoint of the segment
        :param float radius: The thickness of the segment
        """ 
        self._body = body
        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)
            
        self._shape = ffi.gc(
            cp.cpSegmentShapeNew(body_body, tuple(a), tuple(b), radius), 
            cp.cpShapeFree)
        self._set_shapeid()

    def _get_a(self):
        return Vec2d._fromcffi(cp.cpSegmentShapeGetA(self._shape))
    a = property(_get_a,
        doc="""The first of the two endpoints for this segment""")

    def _get_b(self):
        return Vec2d._fromcffi(cp.cpSegmentShapeGetB(self._shape))
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
        cp.cpSegmentShapeSetEndpoints(self._shape, tuple(a), tuple(b))
        
    def _get_normal(self):
        return Vec2d._fromcffi(cp.cpSegmentShapeGetNormal(self._shape))
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
        cp.cpSegmentShapeSetNeighbors(self._shape, tuple(prev), tuple(next))

class Poly(Shape):
    """A convex polygon shape

    Slowest, but most flexible collision shape.
    """

    _pickle_attrs_init = []

    def __init__(self, body, vertices, transform=None, radius=0):
        """Create a polygon.

        A convex hull will be calculated from the vertexes automatically.

        Adding a small radius will bevel the corners and can significantly 
        reduce problems where the poly gets stuck on seams in your geometry.

        It is legal to send in None as body argument to indicate that this
        shape is not attached to a body. However, you must attach it to a body
        before adding the shape to a space or used for a space shape query.
    
        .. note::
            Make sure to put the vertices around (0,0) or the shape might 
            behave strange. 

            Either directly place the vertices like the below example:
            
            >>> import pymunk
            >>> w, h = 10, 20
            >>> vs = [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)]
            >>> poly_good = pymunk.Poly(None, vs)
            >>> print(poly_good.center_of_gravity)
            Vec2d(0.0, 0.0)

            Or use a transform to move them:

            >>> import pymunk
            >>> width, height = 10, 20
            >>> vs = [(0, 0), (width, 0), (width, height), (0, height)]
            >>> poly_bad = pymunk.Poly(None, vs)
            >>> print(poly_bad.center_of_gravity)
            Vec2d(5.0, 10.0)
            >>> t = pymunk.Transform(tx=-width/2, ty=-height/2)
            >>> poly_good = pymunk.Poly(None, vs, transform=t)
            >>> print(poly_good.center_of_gravity)
            Vec2d(0.0, 0.0)

        :param Body body: The body to attach the poly to
        :param [(float,float)] vertices: Define a convex hull of the polygon 
            with a counterclockwise winding.
        :param Transform transform: Transform will be applied to every vertex.
        :param float radius: Set the radius of the poly shape
                
        """

        self._body = body

        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)

        if transform == None:
            transform = Transform.identity()

        vs = list(map(tuple, vertices))
        s = cp.cpPolyShapeNew(body_body, len(vertices), vs, transform, radius)
        self._shape = ffi.gc(s, cp.cpShapeFree)
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
        """Convenience function to create a box given a width and height.

        The boxes will always be centered at the center of gravity of the
        body you are attaching them to.  If you want to create an off-center
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
        self._body = body

        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)

        self._shape = ffi.gc(
            cp.cpBoxShapeNew(body_body, size[0], size[1], radius),
            cp.cpShapeFree)

        self._set_shapeid()
        return self

    @staticmethod
    def create_box_bb(body, bb, radius=0):
        """Convenience function to create a box shape from a :py:class:`BB`.
        
        The boxes will always be centered at the center of gravity of the
        body you are attaching them to.  If you want to create an off-center
        box, you will need to use the normal constructor Poly(..).

        Adding a small radius will bevel the corners and can significantly 
        reduce problems where the box gets stuck on seams in your geometry.

        :param Body body: The body to attach the poly to
        :param BB bb: Size of the box
        :param float radius: Radius of poly
        :rtype: :py:class:`Poly`
        """

        self = Poly.__new__(Poly)
        self._body = body

        body_body = ffi.NULL if body is None else body._body
        if body != None:
            body._shapes.add(self)

        self._shape = ffi.gc(
            cp.cpBoxShapeNew2(body_body, bb._bb, radius),
            cp.cpShapeFree)
        
        self._set_shapeid()
        return self

    def get_vertices(self):
        """Get the vertices in local coordinates for the polygon

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
        l = cp.cpPolyShapeGetCount(self._shape)
        for i in range(l):
            verts.append(Vec2d._fromcffi(cp.cpPolyShapeGetVert(self._shape, i)))
        return verts

    def unsafe_set_vertices(self, vertices, transform=None):
        """Unsafe set the vertices of the poly.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        vs = list(map(tuple, vertices))
        if transform == None:
            cp.cpPolyShapeSetVertsRaw(self._shape, len(vertices), vs)
            return
            
        cp.cpPolyShapeSetVerts(self._shape, len(vertices), vs, transform)

    def __getstate__(self):
        """Return the state of this object
        
        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Poly, self).__getstate__()

        d['init'].append(('vertices', self.get_vertices()))
        d['init'].append(('transform', None))
        d['init'].append(('radius', self.radius))
        return d
