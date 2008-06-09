"""
pymunk is a python wrapper for the 2d physics library Chipmunk

IRC: #pymunk on irc.freenode.net

Homepage: http://pymunk.googlecode.com/

Forum: http://www.slembcke.net/forums/viewforum.php?f=6
"""
__version__ = "$Id$"
__docformat__ = "reStructuredText"

import ctypes as ct
import _chipmunk as cp
import util as u
from vec2d import Vec2d

#: The release version of this pymunk installation
#:
#: Valid only if pymunk was installed from a source or binary 
#: distribution (i.e. not in a checked-out copy from svn).
version = "0.7.2"

#: Infinity that can be passed as mass or inertia to Body 
#:
#: Use this as mass and inertia when you need to create a static body.
inf = 1e100


def init_pymunk():
    """Call this method to initialize pymunk"""
    cp.cpInitChipmunk()

class Space(object):
    def __init__(self, iterations=10):
        self._space = cp.cpSpaceNew(iterations)
        self._callbacks = {} # To prevent the gc to collect the callbacks.
        self._default_callback = None
        self._shapes = {}
        self._static_shapes = {}
        self._bodies = set()
        self._joints = set()

    def _get_shapes(self):
        return self._shapes.values()
    shapes = property(_get_shapes)

    def _get_static_shapes(self):
        return self._static_shapes.values()
    static_shapes = property(_get_static_shapes)

    def _get_bodies(self):
        return self._bodies
    bodies = property(_get_bodies)

    def __del__(self):
        cp.cpSpaceFree(self._space)


    def _set_gravity(self, gravvec):
        self._space.contents.gravity = gravvec
    def _get_gravity(self):
        return self._space.contents.gravity
    gravity = property(_get_gravity, _set_gravity)

    def _set_damping(self, damping):
        self._space.contents.damping = damping
    def _get_damping(self):
        return self._space.contents.damping
    damping = property(_get_damping, _set_damping)

    def add(self, *objs):
        """Add one or many shapes, bodies or joints to the space"""
        for o in objs:
            if isinstance(o, Body):
                self._add_body(o)
            elif isinstance(o, Shape):
                self._add_shape(o)
            elif isinstance(o, Joint):
                self._add_joint(o)
            else:
                for oo in o:
                    self.add(oo)
                    
    def add_static(self, *objs):
        """Add one or many static shapes to the space"""
        for o in objs:
            if isinstance(o, Shape):
                self._add_static_shape(o)
            else:
                for oo in o:
                    self.add_static(oo)
                    
    def remove(self, *objs):
        """Remove one or many shapes, bodies or joints from the space"""
        for o in objs:
            if isinstance(o, Body):
                self._remove_body(o)
            elif isinstance(o, Shape):
                self._remove_shape(o)
            elif isinstance(o, Joint):
                self._remove_joint(o)
            else:
                for oo in o:
                    self.remove(oo)
                    
    def remove_static(self, *os):
        """Remove one or many static shapes from the space"""
        for o in os:
            if isinstance(o, Shape):
                self._remove_static_shape(o)
            else:
                for oo in o:
                    self.remove_static(oo)
                    
    def _add_shape(self, shape):
        """Adds a shape to the space"""
        self._shapes[shape.id] = shape
        cp.cpSpaceAddShape(self._space, shape._shape)
    def _add_static_shape(self, static_shape):
        """Adds a shape to the space. Static shapes should be be attached to 
        a rigid body with an infinite mass and moment of inertia. Also, don't 
        add the rigid body used to the space, as that will cause it to fall 
        under the effects of gravity."""
        self._static_shapes[static_shape.id] = static_shape
        cp.cpSpaceAddStaticShape(self._space, static_shape._shape)
    def _add_body(self, body):
        """Adds a body to the space"""
        self._bodies.add(body)
        cp.cpSpaceAddBody(self._space, body._body)
    def _add_joint(self, joint):
        """Adds a joint to the space"""
        self._joints.add(joint)
        cp.cpSpaceAddJoint(self._space, joint._joint)

    def _remove_shape(self, shape):
        """Removes a shape from the space"""
        del self._shapes[shape.id]
        cp.cpSpaceRemoveShape(self._space, shape._shape)
    def _remove_static_shape(self, static_shape):
        """Removes a static shape from the space."""
        del self._static_shapes[static_shape.id]
        cp.cpSpaceRemoveStaticShape(self._space, static_shape._shape)
    def _remove_body(self, body):
        """Removes a body from the space"""
        self._bodies.remove(body)
        cp.cpSpaceRemoveBody(self._space, body._body)
    def _remove_joint(self, joint):
        """Removes a joint from the space"""
        self._joints.remove(joint)
        cp.cpSpaceRemoveJoint(self._space, joint._joint)

    def resize_static_hash(self, dim=100.0, count=1000):
        """The spatial hashes used by Chipmunk's collision detection are fairly
        size sensitive. dim is the size of the hash cells. Setting dim to the
        average objects size is likely to give the best performance.

        count is the suggested minimum number of cells in the hash table.
        Bigger is better, but only to a point. Setting count to ~10x the number
        of objects in the hash is probably a good starting point."""
        cp.cpSpaceResizeStaticHash(self._space, dim, count)

    def resize_active_hash(self, dim=100.0, count=1000):
        """The spatial hashes used by Chipmunk's collision detection are fairly
        size sensitive. dim is the size of the hash cells. Setting dim to the
        average objects size is likely to give the best performance.

        count is the suggested minimum number of cells in the hash table.
        Bigger is better, but only to a point. Setting count to ~10x the number
        of objects in the hash is probably a good starting point."""
        cp.cpSpaceResizeActiveHash(self._space, dim, count)

    def rehash_static(self):
        """Rehashes the shapes in the static spatial hash. You only need to
        call this if you move one of the static shapes."""
        cp.cpSpaceRehashStatic(self._space)

    def step(self, dt):
        """Update the space for the given time step. Using a fixed time step is
        highly recommended. Doing so will increase the efficiency of the
        contact persistence, requiring an order of magnitude fewer iterations
        to resolve the collisions in the usual case."""
        cp.cpSpaceStep(self._space, dt)
   
    def _get_stamp(self):
        return self._space.contents.stamp
    stamp = property(_get_stamp, 
        doc="""Time stamp. Is incremented on every call to step()""")
    
    def _get_arbiters(self):        
        num = self._space.contents.arbiters.contents.num
        arr = self._space.contents.arbiters.contents.arr
        arbs = []
        for i in xrange(num):
            arb = ct.cast(arr[i], ct.POINTER(cp.cpArbiter))
            arbs.append(Arbiter(arb, self._shapes, self._static_shapes))
        return arbs
    arbiters = property(_get_arbiters, 
        doc="""List of active arbiters for the impulse solver.""")
        
    def add_collisionpair_func(self, a, b, func, data=None):
        """Register func to be called when a collision is found between a 
        shapes with collision_type fields that match a and b. Pass None
        as func to reject any collision with the given collision type pair.
        
        func(shapeA, shapeB, contacts, normal_coef, data) -> bool
        
        shapeA, shapeB is the colliding shapes
        contacts is a list of contacts
        normal_coef is a float :)
        data is the data argument sent to the add_collisionpair_func function
        
        WARNING: It is not safe for collision pair functions to remove or
        free shapes or bodies from a space. Doing so will likely end in a 
        segfault as an earlier collision may already be referencing the shape
        or body. You must wait until after the step() function returns.
        """
        if func is None:
            cp.cpSpaceAddCollisionPairFunc(self._space, a, b, ct.cast(ct.POINTER(ct.c_int)(), cp.cpCollFunc), None)
        else:
            f = self._get_cf(func, data)
            self._callbacks[(a, b)] = f
            cp.cpSpaceAddCollisionPairFunc(self._space, a, b, f, None)
            
    def remove_collisionpair_func(self, a, b):
        """Remove the collision pair function between the shapes a and b"""
        if (a, b) in self._callbacks:
            del self._callbacks[(a, b)]
        cp.cpSpaceRemoveCollisionPairFunc(self._space, a, b)
    
    def set_default_collisionpair_func(self, func, data=None):
        """Sets the default collsion pair function. Passing None as func will 
        reset it to default.. :)
        """
        if func is None:
            self._default_callback = None
            cp.cpSpaceSetDefaultCollisionPairFunc(self._space, ct.cast(ct.POINTER(ct.c_int)(), cp.cpCollFunc), None)
        else:
            f = self._get_cf(func, data)
            self._default_callback = f
            cp.cpSpaceSetDefaultCollisionPairFunc(self._space, f, None)
    
    def _get_cf(self, func, data):
        def cf (cpShapeA, cpShapeB, cpContacts, numContacts, normal_coef, _data):
            ### Translate chipmunk shapes to Shapes.
            if cpShapeA.contents.id in self._shapes:
                shapeA = self._shapes[cpShapeA.contents.id]
            else:
                shapeA = self._static_shapes[cpShapeA.contents.id]
            if cpShapeB.contents.id in self._shapes:
                shapeB = self._shapes[cpShapeB.contents.id]
            else:
                shapeB = self._static_shapes[cpShapeB.contents.id]
            return func(shapeA, shapeB, [Contact(cpContacts[i]) for i in xrange(numContacts)], normal_coef, data)
        
        return cp.cpCollFunc(cf)
    
    
    def _get_query_cf(self, func, data):
        def cf (cpShape, _data):
            ### Translate chipmunk shapes to Shapes.
            if cpShape.contents.id in self._shapes:
                shape = self._shapes[cpShape.contents.id]
            else:
                shape = self._static_shapes[cpShape.contents.id]
            return func(shape, data)
        return cp.cpSpacePointQueryFunc(cf)
    
    def point_query(self, point, func, data=None):
        """Query the space for collisions between a point and its shapes 
        (both static and nonstatic shapes)
        
        func(shape, data)
        
        shape is the colliding shape
        data is the data argument sent to the point_query function
        """       
        f = self._get_query_cf(func, data)
        cp.cpSpaceShapePointQuery(self._space, point, f, None)
        cp.cpSpaceStaticShapePointQuery(self._space, point, f, None)
        
    def static_point_query(self, point, func, data=None):
        """Query the space for collisions between a point and the static 
        shapes in the space
        
        func(shape, data)
        
        shape is the colliding shape
        data is the data argument sent to the point_query function
        """       
        f = self._get_query_cf(func, data)
        cp.cpSpaceStaticShapePointQuery(self._space, point, f, None)
        
    def nonstatic_point_query(self, point, func, data=None):
        """Query the space for collisions between a point and the non static 
        shapes in the space
        
        func(shape, data)
        
        shape is the colliding shape
        data is the data argument sent to the point_query function
        """       
        f = self._get_query_cf(func, data)
        cp.cpSpaceShapePointQuery(self._space, point, f, None)    
    
class Body(object):
    def __init__(self, mass, inertia):
        self._body = cp.cpBodyNew(mass, inertia)
        self._bodycontents =  self._body.contents 
        
    def __del__(self):
        cp.cpBodyFree(self._body)

    def _set_mass(self, mass):
        cp.cpBodySetMass(self._body, mass)
    def _get_mass(self):
        return self._bodycontents.m
    mass = property(_get_mass, _set_mass)

    def _set_moment(self, moment):
        cp.cpBodySetMoment(self._body, moment)
    def _get_moment(self):
        return self._bodycontents.i
    moment = property(_get_moment, _set_moment)

    def _set_angle(self, angle):
        cp.cpBodySetAngle(self._body, angle)
    def _get_angle(self):
        #return self._bodycontents.a
        return self._bodycontents.a
    angle = property(_get_angle, _set_angle)
    
    def _get_rotation_vector(self):
        return self._bodycontents.rot
    rotation_vector = property(_get_rotation_vector)

    def _set_torque(self, t):
        self._bodycontents.t = t
    def _get_torque(self):
        return self._bodycontents.t
    torque = property(_get_torque, _set_torque)

    def _set_position(self, pos):
        self._bodycontents.p = pos
    def _get_position(self):
        return self._bodycontents.p
    position = property(_get_position, _set_position)

    def _set_velocity(self, vel):
        self._bodycontents.v = vel
    def _get_velocity(self):
        return self._bodycontents.v
    velocity = property(_get_velocity, _set_velocity)

    def _set_angular_velocity(self, w):
        self._bodycontents.w = w
    def _get_angular_velocity(self):
        return self._bodycontents.w
    angular_velocity = property(_get_angular_velocity, _set_angular_velocity)


    def apply_impulse(self, j, r):
        """Apply the impulse j to body with offset r."""
        
        #TODO: Test me and figure out if r is in local or world coords.
        self.velocity = self.velocity + j * self._bodycontents.m_inv
        self._bodycontents.w += self._bodycontents.i_inv* r.cross(j)
    
    def reset_forces(self):
        """Reset the forces on the body"""
        cp.cpBodyResetForces(self._body)

    def apply_force(self, f, r):
        """Apply (accumulate) the force f on body with offset r. Both f and r 
        should be in world coordinates."""
        cp.cpBodyApplyForce(self._body, f, r)


    def update_velocity(self, gravity, damping, dt):
        """Updates the velocity of the body using Euler integration. You don't 
        need to call this unless you are managing the object manually instead 
        of adding it to a Space."""
        cp.cpBodyUpdateVelocity(self._body, gravity, damping, dt)

    def update_position(self, dt):
        """Updates the position of the body using Euler integration. Like 
        updateVelocity() you shouldn't normally need to call this yourself."""
        cp.cpBodyUpdatePosition(self._body, dt)


    def local_to_world(self, v):
        """Convert body local to world coordinates"""
        #TODO: Test me
        return self.position + v.cpvrotate(self.rotation_vector)
        
    def world_to_local(self, v):
        """Convert world to body local coordinates"""
        #TODO: Test me
        return (v - self.position).cpvunrotate(self.rotation_vector)


    def damped_spring(self, b, anchor1, anchor2, rlen, k, dmp, dt):
        """Apply a spring force between this and body b at anchors anchr1 and 
        anchr2 respectively. k is the spring constant (force/distance), rlen 
        is the rest length of the spring, dmp is the damping constant 
        (force/velocity), and dt is the time step to apply the force over.
        """
        cp.cpDampedSpring(self._body, b._body, anchor1, anchor2, rlen, k, dmp, dt)

class Shape(object):
    def __init__(self, shape=None):
        self._shape = shape
        self._shapecontents = self._shape.contents
        self._body = shape.body
        self.data = None

    def __del__(self):
        cp.cpShapeFree(self._shape)

    id = property(lambda self: self._shapecontents.id)

    def _get_collision_type(self):
        return self._shapecontents.collision_type
    def _set_collision_type(self, t):
        self._shapecontents.collision_type = t
    collision_type = property(_get_collision_type, _set_collision_type)

    def _get_group(self):
        return self._shapecontents.group
    def _set_group(self, group):
        self._shapecontents.group = group
    group = property(_get_group, _set_group, 
        doc="""Shapes in the same non-zero group do not generate collisions. 
        Useful when creating an object out of many shapes that you don't want 
        to self collide. Defaults to 0""")

    def _get_layers(self):
        return self._shapecontents.layers
    def _set_layers(self, layers):
        self._shapecontents.layers = layers
    layers = property(_get_layers, _set_layers, 
        doc="""Shapes only collide if they are in the same bit-planes. 
        i.e. (a->layers & b->layers) != 0 By default, a shape occupies all 
        32 bit-planes.""")

    def _get_elasticity(self):
        return self._shapecontents.e
    def _set_elasticity(self, e):
        self._shapecontents.e = e
    elasticity = property(_get_elasticity, _set_elasticity, 
        doc="""Elasticity of the shape. A value of 0.0 gives no bounce, 
        while a value of 1.0 will give a 'perfect' bounce. However due to 
        inaccuracies in the simulation using 1.0 or greater is not 
        recommended.""")

    def _get_friction(self):
        return self._shapecontents.u
    def _set_friction(self, u):
        self._shapecontents.u = u
    friction = property(_get_friction, _set_friction, 
        doc="""Friction coefficient. Chipmunk uses the Coulomb friction model, 
        a value of 0.0 is frictionless.""")

    def _get_surface_velocity(self):
        return self._shapecontents.surface_v
    def _set_surface_velocity(self, surface_v):
        self._shapecontents.surface_v = surface_v
    surface_velocity = property(_get_surface_velocity, _set_surface_velocity, 
        doc="""The surface velocity of the object. Useful for creating 
        conveyor belts or players that move around. This value is only used 
        when calculating friction, not the collision.""")

    body = property(lambda self: self._body)

    def cache_bb(self):
        return BB(cp.cpShapeCacheBB(self._shape))

class Circle(Shape):
    """A circle shape defined by a radius"""
    def __init__(self, body, radius, offset):
        """body is the body attach the circle to, offset is the offset from the
        body's center of gravity in body local coordinates."""
        self._body = body
        self._shape = cp.cpCircleShapeNew(body._body, radius, offset)
        self._shapecontents = self._shape.contents

    def _set_radius(self, r):
        ct.cast(self._shape, ct.POINTER(cp.cpCircleShape)).contents.r = r
    def _get_radius(self):
        return ct.cast(self._shape, ct.POINTER(cp.cpCircleShape)).contents.r
    radius = property(_get_radius, _set_radius)
    
    def _get_center (self):
        return ct.cast(self._shape, ct.POINTER(cp.cpCircleShape)).contents.c
    center = property(_get_center, doc="""Center. (body space coordinates)""")

class Segment(Shape):
    """A line segment shape between two points
    This shape is mainly intended as a static shape.
    """
    def __init__(self, body, a, b, radius):
        """body is the body to attach the segment to, a and b are the
        endpoints, and radius is the thickness of the segment."""
        self._body = body
        self._shape = cp.cpSegmentShapeNew(body._body, a, b, radius)
        self._shapecontents = self._shape.contents
    
    def _set_a(self, a):
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.a = a
    def _get_a(self):
        return ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.a
    a = property(_get_a, _set_a, 
        doc="""One of the two endpoints for this segment""")

    def _set_b(self, b):
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.b = b
    def _get_b(self):
        return ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.b
    b = property(_get_b, _set_b, 
        doc="""One of the two endpoints for this segment""")


class Poly(Shape):
    """A polygon shape"""
    def __init__(self, body, vertices, offset, auto_order_vertices=False):
        """body is the body to attach the poly to, verts is an array of
        cpVect's defining a convex hull with a counterclockwise winding, offset
        is the offset from the body's center of gravity in body local
        coordinates. Set auto_order_vertices to automatically order the
        vertices"""
        if auto_order_vertices: 
            raise Exception(NotImplemented)
        self._body = body
        #self.verts = (Vec2d * len(vertices))(*vertices)
        self.verts = (Vec2d * len(vertices))
        self.verts = self.verts(Vec2d(0, 0))
        for (i, vertex) in enumerate(vertices):
            self.verts[i].x = vertex[0]
            self.verts[i].y = vertex[1]
            
        self._shape = cp.cpPolyShapeNew(body._body, len(vertices), self.verts, offset)
        self._shapecontents = self._shape.contents
        
    def get_points(self):
        #shape = ct.cast(self._shape, ct.POINTER(cp.cpPolyShape))
        #num = shape.contents.numVerts
        #verts = shape.contents.verts
        points = []
        rv = self._body.rotation_vector
        bp = self._body.position
        vs = self.verts
        for i in xrange(len(vs)):
            p = vs[i].cpvrotate(rv)+bp
            points.append(Vec2d(p))
            
        return points

def moment_for_circle(mass, inner_radius, outer_radius, offset):
    """Calculate the moment of inertia for a circle"""
    return cp.cpMomentForCircle(mass, inner_radius, outer_radius, offset)

def moment_for_poly(mass, vertices,  offset):
    """Calculate the moment of inertia for a polygon"""
    verts = (Vec2d * len(vertices))
    verts = verts(Vec2d(0, 0))
    for (i, vertex) in enumerate(vertices):
        verts[i].x = vertex[0]
        verts[i].y = vertex[1]
    return cp.cpMomentForPoly(mass, len(verts), verts, offset)
    
def reset_shapeid_counter():
    cp.cpResetShapeIdCounter()

class BB(object):
    """Deprecated"""
    def __init__(self, *args):
        if len(args) == 1:
            self._bb = args[0]
        else:
            self._bb = cp.cpBB()
            self._bb.l = args[0]
            self._bb.b = args[1]
            self._bb.r = args[2]
            self._bb.t = args[3]
    
    def intersects(self, other):
        a = self._bb
        b = other._bb
        return a.l <= b.r and b.l <= a.r and a.b <= b.t and b.b <= a.t

    left = property(lambda self: self._bb.l)
    bottom = property(lambda self: self._bb.b)
    right = property(lambda self: self._bb.r)
    top = property(lambda self: self._bb.t)

class Joint(object):
    def __init__(self, joint=None):
        self._joint = joint
    
    def __del__(self):
        cp.cpJointFree(self._joint)

class PinJoint(Joint):
    """Keeps the anchor points at a set distance from one another."""
    def __init__(self, a, b, anchr1, anchr2):
        """a and b are the two bodies to connect, and anchr1 and anchr2 are the
        anchor points on those bodies.
        """
        self._a = a
        self._b = b
        self._joint = cp.cpPinJointNew(a._body, b._body, anchr1, anchr2)

class SlideJoint(Joint):
    """Like pin joints, but have a minimum and maximum distance.
        A chain could be modeled using this joint. It keeps the anchor points 
        from getting to far apart, but will allow them to get closer together.
        """
    def __init__(self, a, b, anchr1, anchr2, min, max):
        """a and b are the two bodies to connect, anchr1 and anchr2 are the
        anchor points on those bodies, and min and max define the allowed
        distances of the anchor points.
        """
        self._a = a
        self._b = b
        self._joint = cp.cpSlideJointNew(a._body, b._body, anchr1, anchr2, min, max)

class PivotJoint(Joint):
    """Simply allow two objects to pivot about a single point."""
    def __init__(self, a, b, pivot):
        """a and b are the two bodies to connect, and pivot is the point in
        world coordinates of the pivot. Because the pivot location is given in
        world coordinates, you must have the bodies moved into the correct
        positions already.
        """
        self._a = a
        self._b = b
        self._joint = cp.cpPivotJointNew(a._body, b._body, pivot)

class GrooveJoint(Joint):
    """Similar to a pivot joint, but one of the anchors is
        on a linear slide instead of being fixed."""
    def __init__(self, a, b, groove_a, groove_b, anchr2):
        """a and b are the two bodies to conenct, 
        groove_a and groove_b is two points or vectors or something.
        anchr2 is an anchor point
        """
        self._a = a 
        self._b = b
        self._joint = cp.cpGrooveJointNew(a._body, b._body, groove_a, groove_b, anchr2)

class Contact(object):
    def __init__(self, contact):
        self._contact = contact

    def _get_position(self):
        return self._contact.p
    position = property(_get_position, doc="""Contact position""")

    def _get_normal(self):
        return self._contact.n
    normal = property(_get_normal, doc="""Contact normal""")

    def _get_distance(self):
        return self._contact.dist
    distance = property(_get_distance, doc="""Penetration distance""")
    
    # TODO: figure out how this works..
    def _get_jn_acc(self):
        return self._contact.jnAcc
    jn_acc = property(_get_distance, 
        doc="""The normal component of the accumulated (final) impulse applied
        to resolve the collision. Will not be valid until after the call to 
        Space.step() returns""")

    def _get_jt_acc(self):
        return self._contact.jtAcc
    jt_acc = property(_get_jt_acc, 
        doc="""The tangential component of the accumulated (final) impulse 
        applied to resolve the collision. Will not be valid until after the 
        call to Space.step() returns""")


class Arbiter(object):
    """Class for tracking collisions between shapes."""
    def __init__(self, arbiter, shapes, static_shapes):
        self._arbiter = arbiter
        self._shapes = shapes
        self._static_shapes = static_shapes
    
    def _get_contacts(self):
        cs = [Contact(self._arbiter.contents.contacts[i]) for i in xrange(self._arbiter.contents.numContacts)]
        return cs
    contacts = property(_get_contacts, 
        doc="""Information on the contact points between the objects.""")
        
    def _get_a(self):
        a = self._arbiter.contents.a.contents
        if a.id in self._shapes:
            shapeA = self._shapes[a.id]
        elif a.id in self._static_shapes:
            shapeA = self._static_shapes[a.id]
        else:
            shapeA = None # What to do here, the shape has been removed from the space.
        return shapeA
    a = property(_get_a, doc="""The first shape involved in the collision""")    
    
    def _get_b(self):
        b = self._arbiter.contents.b.contents
        if b.id in self._shapes:
            shapeB = self._shapes[b.id]
        elif b.id in self._static_shapes:
            shapeB = self._static_shapes[b.id]
        else:
            shapeB = None # What to do here, the shape has been removed from the space.
        return shapeB
    b = property(_get_b, doc="""The second shape involved in the collision""")

    def _get_elasticity(self):
        return self._arbiter.contents.e
    elasticity = property(_get_elasticity, doc="""Elasticity""")
    
    def _get_friction(self):
        return self._arbiter.contents.u
    friction = property(_get_friction, doc="""Friction""")
    
    def _get_surface_velocity(self):
        return self._arbiter.contents.target_v
    surface_velocity = property(_get_surface_velocity, doc="""Surface velocity""")

    def _get_stamp(self):
        return self._arbiter.contents.stamp
    stamp = property(_get_stamp, doc="""Time stamp of the arbiter. (from the space)""")

#del cp, ct, u

__all__ = ["inf", "version", "init_pymunk"
        , "Space", "Body", "Shape", "Circle", "Poly", "Segment"
        , "moment_for_circle", "moment_for_poly", "reset_shapeid_counter"
        , "Joint", "PinJoint", "SlideJoint", "PivotJoint", "GrooveJoint" 
        , "Contact", "Arbiter"]
