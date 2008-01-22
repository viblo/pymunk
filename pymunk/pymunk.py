import ctypes as ct
import _chipmunk as cp
import util as u
from vec2d import vec2d

def init_pymunk():
    cp.cpInitChipmunk()

class Space(object):
    def __init__(self, iterations=10):
        self._space = cp.cpSpaceNew(iterations)
        self._callbacks = {} # To prevent the gc to collect the callbacks.
        self._shapes = {}
        self._static_shapes = {}
        self._bodies = {}

    def set_gravity(self, gravvec):
        self._space.contents.gravity = gravvec
    def get_gravity(self):
        return self._space.contents.gravity
    gravity = property(get_gravity, set_gravity)

    def set_damping(self, damping):
        self._space.contents.damping = damping
    def get_damping(self):
        return self._space.contents.damping
    damping = property(get_damping, set_gravity)

    def add(self, o):
        """Add a shape, body or joint to the space"""
        if isinstance(o, Body):
            self.add_body(o)
        elif isinstance(o, Shape):
            self.add_shape(o)
        elif isinstance(o, Joint):
            self.add_joint(o)

    def remove(self, o):
        """Remove a shape, body or joint from the space"""
        if isinstance(o, Body):
            self.remove_body(o)
        elif isinstance(o, Shape):
            self.remove_shape(o)
        elif isinstance(o, Joint):
            self.remove_joint(o)

    def add_shape(self, shape):
        """Adds a shape to the space"""
        self._shapes[shape.id] = shape
        cp.cpSpaceAddShape(self._space, shape._shape)
    def add_static_shape(self, static_shape):
        """Adds a shape to the space. Static shapes should be be attached to 
        a rigid body with an infinite mass and moment of inertia. Also, don't 
        add the rigid body used to the space, as that will cause it to fall 
        under the effects of gravity."""
        self._static_shapes[static_shape.id] = static_shape
        cp.cpSpaceAddStaticShape(self._space, static_shape._shape)
    def add_body(self, body):
        """Adds a body to the space"""
        cp.cpSpaceAddBody(self._space, body._body)
    def add_joint(self, joint):
        """Adds a joint to the space"""
        cp.cpSpaceAddJoint(self._space, joint._joint)

    def remove_shape(self, shape):
        """Removes a shape from the space"""
        cp.cpSpaceRemoveShape(self._space, shape._shape)
    def remove_static_shape(self, staticshape):
        """Removes a shape from the space."""
        cp.cpSpaceRemoveStaticShape(self._space, staticshape._shape)
    def remove_body(self, body):
        """Removes a body from the space"""
        cp.cpSpaceRemoveBody(self._space, body._body)
    def remove_joint(self, joint):
        """Removes a joint from the space"""
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

    def free(self):
        cp.cpSpaceFree(self._space)
    
    def free_children(self):
        """This function will free all of the shapes, bodies and joints that
        have been added to space."""
        cp.cpSpaceFreeChildren(self._space)

    def get_stamp(self):
        return self._space.contents.stamp
    stamp = property(get_stamp)
    
    def add_collisionpair_func(self, a, b, func, data):
        """Register func to be called when a collision is found between a 
        shapes with collision_type fields that match a and b. Pass None
        as func to reject any collision with the given collision type pair.
        
        func(shapeA, shapeB, contacts, normal_coef, data) -> bool
        
        shapeA, shapeB is the colliding shapes
        contacts is a list of contacts
        normal_coef is a float :)
        data is the data argument sent to the addCollisionPairFunc function
        
        WARNING: It is not safe for collision pair functions to remove or
        free shapes or bodies from a space. Doing so will likely end in a 
        segfault as an earlier collision may already be referencing the shape
        or body. You must wait until after the cpSpaceStep() function returns.
        """
        def getCF(func):
            def CF (cpShapeA, cpShapeB, cpContacts, numContacts, normal_coef, _data):
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
            
            return CF
        if func is None:
             cp.cpSpaceAddCollisionPairFunc(self._space, a, b, ct.cast(ct.POINTER(ct.c_int)(), cp.cpCollFunc), None)
        else:
            f = cp.cpCollFunc(getCF(func))
            self._callbacks[(a,b)] = f
            cp.cpSpaceAddCollisionPairFunc(self._space, a, b, f, None)
            
    def remove_collisionpair_func(self, a, b):
        
        if (a,b) in self._callbacks:
            del self._callbacks[(a,b)]
        cp.cpSpaceRemoveCollisionPairFunc(self._space, a, b)
    
    def set_default_collisionpair_func(self, func, data):
        pass
    
class Body(object):
    def __init__(self, mass, inertia):
        self._body = cp.cpBodyNew(mass, inertia)

    def set_mass(self, mass):
        cp.cpBodySetMass(self._body, mass)
    def get_mass(self):
        return self._body.contents.m
    mass = property(get_mass, set_mass)

    def set_moment(self, moment):
        cp.cpBodySetMoment(self._body, moment)
    def get_moment(self):
        return self._body.contents.i
    moment = property(get_moment, set_moment)

    def set_angle(self, angle):
        cp.cpBodySetAngle(self._body, angle)
    def get_angle(self):
        return self._body.contents.a
    angle = property(get_angle, set_angle)
    
    def get_rotation_vector(self):
        return self._body.contents.rot
    rotation_vector = property(get_rotation_vector)

    def set_position(self, pos):
        self._body.contents.p = pos
    def get_position(self):
        return self._body.contents.p
    position = property(get_position, set_position)

    def set_velocity(self, vel):
        self._body.contents.v = vel
    def get_velocity(self):
        return self._body.contents.v
    velocity = property(get_velocity, set_velocity)

    def apply_impulse(self, j, r):
        """Apply the impulse j to body with offset r. Both j and r should be in
        world coordinates."""
        cp.cpBodyApplyImpulse(self._body, j, r)
    
    def reset_forces(self):
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
    

def damped_spring(a, b, anchor1, anchor2, rlen, k, dmp, dt):
    """Apply a spring force between bodies a and b at anchors anchr1 and anchr2
    respectively. k is the spring constant (force/distance), rlen is the rest 
    length of the spring, dmp is the damping constant (force/velocity), and dt 
    is the time step to apply the force over."""
    cp.cpDampedSpring(a._body, b._body, anchor1, anchor2, rlen, k, dmp, dt)

class Shape(object):
    def __init__(self, shape=None):
        self._shape = shape
        self._body = shape.body
        self.data = None

    def get_id(self):
        return self._shape.contents.id
    id = property(get_id)

    def get_collision_type(self):
        return self._shape.contents.collision_type
    def set_collision_type(self, t):
        self._shape.contents.collision_type = t
    collision_type = property(get_collision_type, set_collision_type)

    def get_group(self):
        return self._shape.contents.group
    def set_group(self, group):
        self._shape.contents.group = group
    group = property(get_group, set_group, doc="""Shapes in the same non-zero
 group do not generate collisions. Useful when creating an object out of many shapes that you don't want to self collide. Defaults to 0""")

    def get_layers(self):
        return self._shape.contents.layers
    def set_layers(self, layers):
        self._shape.contents.layers = layers
    layers = property(get_layers, set_layers, doc="""Shapes only collide if they are in the same bit-planes. i.e. (a->layers & b->layers) != 0 By default, a shape occupies all 32 bit-planes.""")

    def get_elasticity(self):
        return self._shape.contents.e
    def set_elasticity(self, e):
        self._shape.contents.e = e
    elasticity = property(get_elasticity, set_elasticity, doc="""Elasticity of the shape. A value of 0.0 gives no bounce, while a value of 1.0 will give a 'perfect' bounce. However due to inaccuracies in the simulation using 1.0 or greater is not recommended however.""")

    def get_friction(self):
        return self._shape.contents.u
    def set_friction(self, u):
        self._shape.contents.u = u
    friction = property(get_friction, set_friction, doc="""Friction coefficient. Chipmunk uses the Coulomb friction model, a value of 0.0 is frictionless.""")

    def get_surface_velocity(self):
        return self._shape.contents.surface_v
    def set_surface_velocity(self, surface_v):
        self._shape.contents.surface_v = surface_v
    surface_velocity = property(get_surface_velocity, set_surface_velocity, doc="""The surface velocity of the object. Useful for creating conveyor belts or players that move around. This value is only used when calculating friction, not the collision.""")

    def get_body(self):
        return self._body
    body = property(get_body)

    def cache_bb(self):
        return BB(cp.cpShapeCacheBB(self._shape))

class Circle(Shape):
    def __init__(self, body, radius, offset):
        """body is the body attach the circle to, offset is the offset from the
        body's center of gravity in body local coordinates."""
        self._body = body
        self._shape = cp.cpCircleShapeNew(body._body, radius, offset)

    def set_radius(self, r):
        ct.cast(self._shape, ct.POINTER(cp.cpCircleShape)).contents.r = r
    def get_radius(self):
        return ct.cast(self._shape, ct.POINTER(cp.cpCircleShape)).contents.r
    radius = property(get_radius, set_radius)
        

class Segment(Shape):
    def __init__(self, body, a, b, radius):
        """body is the body to attach the segment to, a and b are the
        endpoints, and radius is the thickness of the segment."""
        self._body = body
        self._shape = cp.cpSegmentShapeNew(body._body, a, b, radius)
    def set_a(self, a):
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.a = a
    def get_a(self):
        return ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.a
    a = property(get_a, set_a)
    
    def set_b(self, b):
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.b = b
    def get_b(self):
        return ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.b
    b = property(get_b, set_b)


class Poly(Shape):
    def __init__(self, body, vertices, offset):
        """body is the body to attach the poly to, verts is an array of
        cpVect's defining a convex hull with a counterclockwise winding, offset
        is the offset from the body's center of gravity in body local
        coordinates."""
        self._body = body
        verts = (vec2d * len(vertices))(*vertices)
#		for (i, vertex) in enumerate(vertices):
#			verts[i].x = vertex.x
#			verts[i].y = vertex.y
        print cp.cpMomentForPoly(body.mass, len(vertices), verts, offset)
        self._shape = cp.cpPolyShapeNew(body._body, len(vertices), verts, offset)

def reset_shapeid_counter():
    cp.cpResetShapeIdCounter()

class BB(object):
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
    pass

class PinJoint(Joint):
    def __init__(self, a, b, anchr1, anchr2):
        """Keeps the anchor points at a set distance from one another.
        
        a and b are the two bodies to connect, and anchr1 and anchr2 are the
        anchor points on those bodies."""
        self._joint = cp.cpPinJointNew(a._body, b._body, anchr1, anchr2)

class SlideJoint(Joint):
    def __init__(self, a, b, anchr1, anchr2, min, max):
        """Like pin joints, but have a minimum and maximum distance.
        A chain could be modeled using this joint. It keeps the anchor points 
        from getting to far apart, but will allow them to get closer together.
        
        a and b are the two bodies to connect, anchr1 and anchr2 are the
        anchor points on those bodies, and min and max define the allowed
        distances of the anchor points."""
        self._joint = cp.cpSlideJointNew(a._body, b._body, anchr1, anchr2, min, max)

class PivotJoint(Joint):
    def __init__(self, a, b, pivot):
        """Simply allow two objects to pivot about a single point.
        
        a and b are the two bodies to connect, and pivot is the point in
        world coordinates of the pivot. Because the pivot location is given in
        world coordinates, you must have the bodies moved into the correct
        positions already."""
        self._joint = cp.cpPivotJointNew(a._body, b._body, pivot)

class GrooveJoint(Joint):
    """Does magic
    a and b are the two bodies to conenct, 
    groove_a and groove_b is two points or vectors or something.
    anchr2 is an anchor point"""
    def __init__(self, a, b, groove_a, groove_b, anchr2):
        pass

class Contact(object):
    def __init__(self, contact):
        self._contact = contact

    def get_position(self):
        return self._contact.contents.p
    position = property(get_position)

    def get_normal(self):
        return self._contact.contents.n
    normal = property(get_normal)

    def get_distance(self):
        return self._contact.contents.dist
    distance = property(get_distance)
