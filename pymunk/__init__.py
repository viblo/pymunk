"""
pymunk is a python wrapper for the 2d physics library Chipmunk

IRC: #pymunk on irc.freenode.net

Homepage: http://code.google.com/p/pymunk/

Forum: http://www.slembcke.net/forums/viewforum.php?f=6
"""
__version__ = "$Id$"
__docformat__ = "reStructuredText"

__all__ = ["inf", "version", "chipmunk_version", "init_pymunk"
        , "Space", "Body", "Shape", "Circle", "Poly", "Segment"
        , "moment_for_circle", "moment_for_poly", "reset_shapeid_counter"
        , "Constraint", "PinJoint", "SlideJoint", "PivotJoint", "GrooveJoint"
        , "DampedSpring", "DampedRotarySpring", "RotaryLimitJoint"
        , "RatchetJoint", "GearJoint", "SimpleMotor"
        , "SegmentQueryInfo", "Contact", "Arbiter", "BB"]

import ctypes as ct
import pymunk._chipmunk as cp 
import pymunk.util as u
from .vec2d import Vec2d

from constraint import *

version = "0.9.0"
"""The release version of this pymunk installation.
Valid only if pymunk was installed from a source or binary 
distribution (i.e. not in a checked-out copy from svn).
"""

chipmunk_version = "rev343"
"""The chipmunk version compatible with this pymunk version.
Other (newer) chipmunk versions might also work if the new version does not 
contain any breaking API changes.

*Note:* This is also the version of the chipmunk source files included in the 
chipmunk_src folder (normally included in the pymunk source distribution).
"""

#inf = float('inf') # works only on python 2.6+
inf = 1e100
"""Infinity that can be passed as mass or inertia to Body. 
Use this as mass and inertia when you need to create a static body.
"""


def init_pymunk():
    """Call this method to initialize pymunk"""
    cp.cpInitChipmunk()

class Space(object):
    """Spaces are the basic unit of simulation. You add rigid bodies, shapes 
    and joints to it and then step them all forward together through time. 
    """
    def __init__(self, iterations=10, elastic_iterations=10):
        """Create a new instace of the Space
        
        If the objects in your Space does not have any elasticity set
        elastic_iterations to 0 to gain a little speedup.
        
        :Parameters:
            iterations : int
                Number of iterations to use in the impulse solver to solve 
                contacts.
            elastic_iterations : int
                Number of iterations to use in the impulse solver to solve 
                elastic contacts.
        """
        self._space = cp.cpSpaceNew()
        self._space.contents.iterations = iterations
        self._space.contents.elasticIterations = elastic_iterations
        
        self._handlers = {} # To prevent the gc to collect the callbacks.
        self._default_handler = None
        
        self._post_step_callbacks = {}
        
        self._shapes = {}
        self._static_shapes = {}
        self._bodies = set()
        self._constraints = set()

    def _get_shapes(self):
        return list(self._shapes.values())
    shapes = property(_get_shapes, 
        doc="""A list of the shapes added to this space""")

    def _get_static_shapes(self):
        return list(self._static_shapes.values())
    static_shapes = property(_get_static_shapes,
        doc="""A list of the static shapes added to this space""")

    def _get_bodies(self):
        return list(self._bodies)
    bodies = property(_get_bodies,
        doc="""A list of the bodies added to this space""")
    
    def _get_constraints(self):
        return list(self._constraints)
    constraints = property(_get_constraints,
        doc="""A list of the constraints added to this space""")

    def __del__(self):
        cp.cpSpaceFree(self._space)


    def _set_gravity(self, gravity_vec):
        self._space.contents.gravity = gravity_vec
    def _get_gravity(self):
        return self._space.contents.gravity
    gravity = property(_get_gravity, _set_gravity
        , doc="""Default gravity to supply when integrating rigid body motions.""")

    def _set_damping(self, damping):
        self._space.contents.damping = damping
    def _get_damping(self):
        return self._space.contents.damping
    damping = property(_get_damping, _set_damping
        , doc="""Default damping to supply when integrating rigid body motions.""")

    def add(self, *objs):
        """Add one or many shapes, bodies or joints to the space"""
        for o in objs:
            if isinstance(o, Body):
                self._add_body(o)
            elif isinstance(o, Shape):
                self._add_shape(o)
            elif isinstance(o, Constraint):
                self._add_constraint(o)
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
        """Remove one or many shapes, bodies or constraints from the space
        
        Note: When removing objects from the space, make sure you remove any 
        other objects that reference it. For instance, when you remove a body, 
        remove the joints and shapes attached to it. 
        """
        for o in objs:
            if isinstance(o, Body):
                self._remove_body(o)
            elif isinstance(o, Shape):
                self._remove_shape(o)
            elif isinstance(o, Constraint):
                self._remove_constraint(o)
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
        assert shape._hashid not in self._shapes, "shape already added to space"
        self._shapes[shape._hashid] = shape
        cp.cpSpaceAddShape(self._space, shape._shape)
    def _add_static_shape(self, static_shape):
        """Adds a shape to the space. Static shapes should be be attached to 
        a rigid body with an infinite mass and moment of inertia. Also, don't 
        add the rigid body used to the space, as that will cause it to fall 
        under the effects of gravity."""
        assert static_shape._hashid not in self._static_shapes, "shape already added to space"
        self._static_shapes[static_shape._hashid] = static_shape
        cp.cpSpaceAddStaticShape(self._space, static_shape._shape)
    def _add_body(self, body):
        """Adds a body to the space"""
        assert body not in self._bodies, "body already added to space"
        self._bodies.add(body)
        cp.cpSpaceAddBody(self._space, body._body)
    def _add_constraint(self, constraint):
        """Adds a constraint to the space"""
        assert constraint not in self._constraints, "constraint already added to space"
        self._constraints.add(constraint)
        cp.cpSpaceAddConstraint(self._space, constraint._constraint)

    def _remove_shape(self, shape):
        """Removes a shape from the space"""
        del self._shapes[shape._hashid]
        cp.cpSpaceRemoveShape(self._space, shape._shape)
    def _remove_static_shape(self, static_shape):
        """Removes a static shape from the space."""
        del self._static_shapes[static_shape._hashid]
        cp.cpSpaceRemoveStaticShape(self._space, static_shape._shape)
    def _remove_body(self, body):
        """Removes a body from the space"""
        self._bodies.remove(body)
        cp.cpSpaceRemoveBody(self._space, body._body)
    def _remove_constraint(self, constraint):
        """Removes a constraint from the space"""
        self._constraints.remove(constraint)
        cp.cpSpaceRemoveConstraint(self._space, constraint._constraint)

    def resize_static_hash(self, dim=100.0, count=1000):
        """The spatial hashes used by Chipmunk's collision detection are fairly
        size sensitive. dim is the size of the hash cells. Setting dim to the
        average objects size is likely to give the best performance.

        count is the suggested minimum number of cells in the hash table.
        Bigger is better, but only to a point. Setting count to ~10x the number
        of objects in the hash is probably a good starting point.
        
        Because static shapes are only rehashed when you request it, it's 
        possible to use a much higher count argument to resize_static_hash() 
        than to resize_active_hash(). Doing so will use more memory though. 
        """
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
        
        for obj,(func, args, kwargs) in self._post_step_callbacks.items():
            func(obj, *args, **kwargs)
        self._post_step_callbacks = {}
    
    def add_collision_handler(self, a, b, begin, pre_solve, post_solve, separate):
        """Add a collision handler for given collision type pair. 
        
        Whenever a shapes with collision_type a and collision_type b collide, 
        these callbacks will be used to process the collision. data is a user 
        definable context pointer that is passed to each of the callbacks. 
        None can be provided for callbacks you do not wish to implement, 
        however Chipmunk will call it's own default versions for these and not 
        the default ones you've set up for the space. If you need to fall back 
        on the space's default callbacks, you'll have to provide them 
        individually to each handler definition.
        """
        
        _functions = self._collision_function_helper(begin, pre_solve, post_solve, separate)
        
        self._handlers[(a,b)] = _functions
        cp.cpSpaceAddCollisionHandler(self._space, a, b, 
            _functions[0], _functions[1], _functions[2], _functions[3], None)
            
    def set_default_collision_handler(self, begin, pre_solve, post_solve, separate):
        """Register a default collision handler to be used when no specific 
        collision handler is found. If you do nothing, the space will be given 
        a default handler that accepts all collisions in begin() and 
        pre_solve() and does nothing for the post_solve() and separate() 
        callbacks. 
        """
        
        _functions = self._collision_function_helper(begin, pre_solve, post_solve, separate)
        self._default_handler = _functions
        cp.cpSpaceSetDefaultCollisionHandler(self._space,
            _functions[0], _functions[1], _functions[2], _functions[3], None)
    
    def _collision_function_helper(self, begin, pre_solve, post_solve, separate):
        
        functions = [(begin, cp.cpCollisionBeginFunc)
                    , (pre_solve, cp.cpCollisionPreSolveFunc)
                    , (post_solve, cp.cpCollisionPostSolveFunc)
                    , (separate, cp.cpCollisionSeparateFunc)]
        
        _functions = []
        
        for func, func_type in functions:
            if func is None:
                _f = ct.cast(ct.POINTER(ct.c_int)(), func_type)
            else:
                
                _f = self._get_cf1(func, func_type)
            _functions.append(_f)
        return _functions
    
    def remove_collision_handler(self, a, b):
        """Remove a collision handler for a given collision type pair.
        
        :Parameters:
            a : int
                The collision_type for the first shape
            b : int
                The collision_type for the second shape
        """
        if (a, b) in self._handlers:
            del self._handlers[(a, b)]
        cp.cpSpaceRemoveCollisionHandler(self._space, a, b)
        
    
    def _get_cf1(self, func, function_type):
        def cf(_arbiter, _space, _data):
            arbiter = Arbiter(_arbiter, self)
            return func(self, arbiter)
        return function_type(cf)
        
    
    def add_post_step_callback(self, func, obj, *args, **kwargs):
        if obj in self._post_step_callbacks:
            return
        self._post_step_callbacks[obj] = func, args, kwargs
        pass
        
    def point_query(self, point, layers = -1, group = 0):
        """Query space at point filtering out matches with the given layers 
        and group. Return a list of found shapes.
        
        If you don't want to filter out any matches, use -1 for the layers 
        and 0 as the group.
        
        :Parameters:    
            point : (x,y) or `Vec2d`
                Define where to check for collision in the space.
            layers : int
                Only pick shapes matching the bit mask. i.e. (layers & shape.layers) != 0
            group : int
                Only pick shapes in this group.
                
        """
        self.__query_hits = []
        def cf(_shape, data):
            shape = self._shapes[_shape.contents.hashid]
            self.__query_hits.append(shape)
        f = cp.cpSpacePointQueryFunc(cf)
        cp.cpSpacePointQuery(self._space, point, layers, group, f, None)
        
        return self.__query_hits
        
    def point_query_first(self, point, layers = -1, group = 0):
        """Query space at point and return the first shape found matching the 
        given layers and group. Returns None if no shape was found.
        """
        shape = None
        _shape = cp.cpSpacePointQueryFirst(self._space, point, layers, group)
        if _shape:
            shape = self._shapes[_shape.contents.hashid]
        return shape
        
    def segment_query(self, start, end, layers = -1, group = 0):
        """Query space along the line segment from start to end filtering out 
        matches with the given layers and group. 
        
        Segment queries are like ray casting, but because Chipmunk uses a 
        spatial hash to process collisions, it cannot process infinitely long 
        queries like a ray. In practice this is still very fast and you don't 
        need to worry too much about the performance as long as you aren't 
        using very long segments for your queries. 
        
        :Return:
            a list of SegmentQueryInfo objects of all hits
        """
        
        self.__query_hits = []
        def cf(_shape, t, n, data):
            shape = self._shapes[_shape.contents.hashid]
            info = SegmentQueryInfo(shape, start, end, t, n)
            self.__query_hits.append(info)
        
        f = cp.cpSpaceSegmentQueryFunc(cf)
        cp.cpSpaceSegmentQuery(self._space, start, end, layers, group, f, None)
        
        return self.__query_hits
        
            
    def segment_query_first(self, start, end, layers = -1, group = 0):
        """Query space along the line segment from start to end filtering out 
        matches with the given layers and group. Only the first shape 
        encountered is returned and the search is short circuited. 
        Returns None if no shape was found.
        """
        info = cp.cpSegmentQueryInfo()
        info_p = ct.POINTER(cp.cpSegmentQueryInfo)(info)
        _shape = cp.cpSpaceSegmentQueryFirst(self._space, start, end, layers, group, info_p)
        if bool(_shape):
            shape = self._shapes[_shape.contents.hashid]
            return SegmentQueryInfo(shape, start, end, info.t, info.n)
        else:
            return None
            
     
    
class Body(object):
    """A rigid body
    
    * Use forces to modify the rigid bodies if possible. This is likely to be 
      the most stable.
    * Modifying a body's velocity shouldn't necessarily be avoided, but 
      applying large changes can cause strange results in the simulation. 
      Experiment freely, but be warned.
    * Don't modify a body's position every step unless you really know what 
      you are doing. Otherwise you're likely to get the position/velocity badly 
      out of sync. 
    """
    def __init__(self, mass, moment):
        """Create a new Body"""
        self._body = cp.cpBodyNew(mass, moment)
        self._bodycontents =  self._body.contents 
        self._position_callback = None # To prevent the gc to collect the callbacks.
        self._velocity_callback = None # To prevent the gc to collect the callbacks.
        
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

    def _set_force(self, f):
        self._bodycontents.f = f
    def _get_force(self):
        return self._bodycontents.f
    force = property(_get_force, _set_force)

    def _set_velocity_func(self, func):
        """Set the velocity callback function. The velocity callback function 
        is called each time step, and can be used to set a body's velocity.
        
            func(body, gravity, damping, dt) -> None
            
            Parameters
                body : `Body`
                    Body that should have its velocity calculated
                gravity : `Vec2d`
                    The gravity vector
                damping : float
                    The damping
                dt : float
                    Delta time since last step.
        """
        def _impl(_, gravity, damping, dt):
            return func(self, gravity, damping, dt)
        self._velocity_callback = cp.cpBodyVelocityFunc(_impl)
        self._bodycontents.velocity_func = self._velocity_callback
    velocity_func = property(fset=_set_velocity_func, 
        doc=_set_velocity_func.__doc__)    

    def _set_position_func(self, func):
        """Set the position callback function. The position callback function 
        is called each time step and can be used to update the body's position.
        
            func(body, dt) -> None
            
            Parameters
                body : `Body`
                    Body that should have its velocity calculated
                dt : float
                    Delta time since last step.
        """
        def _impl(_, dt):
            return func(self, dt)
        self._position_callback = cp.cpBodyPositionFunc(_impl)    
        self._bodycontents.position_func = self._position_callback
    position_func = property(fset=_set_position_func, 
        doc=_set_position_func.__doc__)
    
    
    def apply_impulse(self, j, r=(0,0)):
        """Apply the impulse j to body at a relative offset (important!) r 
        from the center of gravity. Both r and j are in world coordinates. 
        
        :Parameters:
            j : (x,y) or `Vec2d`
                Impulse to be applied
            r : (x,y) or `Vec2d`
                Offset the impulse with this vector
        """
        j,r = Vec2d(j), Vec2d(r)
        self.velocity = self.velocity + j * self._bodycontents.m_inv
        self._bodycontents.w += self._bodycontents.i_inv* r.cross(j)
    
    def reset_forces(self):
        """Zero both the forces and torques accumulated on body"""
        cp.cpBodyResetForces(self._body)

    def apply_force(self, f, r=(0,0)):
        """Apply (accumulate) the force f on body at a relative offset 
        (important!) r from the center of gravity. 
        
        Both r and f are in world coordinates. 
        
            f : (x,y) or `Vec2d`
                Force in world coordinates
            r : (x,y) or `Vec2d`
                Offset in world coordinates
        """
        cp.cpBodyApplyForce(self._body, f, r)

    def apply_damped_spring(self, b, anchor1, anchor2, rlen, k, dmp, dt):
        """Apply a spring force between this body and b at anchors anchr1 and 
        anchr2 respectively. 
        
        Note: not solving the damping forces in the impulse solver causes 
        problems with large damping values. There is a new constraint type 
        DampedSpring that should be used instead.        
        
        :Parameters:
            b : `Body`
                The other body
            anchor1 : (x,y) or `Vec2d`
                Anchor point on the first body
            anchor2 : (x,y) or `Vec2d`
                Anchor point on the second body
            k : float
                The spring constant (force/distance) (Young's modulus)
            rlen : float
                The rest length of the spring
            dmp : float
                The damping constant (force/velocity)
            dt : float
                The time step to apply the force over.
        """
        cp.cpApplyDampedSpring(self._body, b._body, anchor1, anchor2, rlen, k, dmp, dt)
        
        
    def slew(self, pos, dt):
        """Modify the velocity of the body so that it will move to the 
        specified absolute coordinates in the next timestep. 
        
        Intended for objects that are moved manually with a custom velocity 
        integration function.
        """ 
        cp.cpBodySlew(self._body, pos, dt)
        
    def update_velocity(self, gravity, damping, dt):
        """Default rigid body velocity integration function. 
        
        Updates the velocity of the body using Euler integration.
        """
        cp.cpBodyUpdateVelocity(self._body, gravity, damping, dt)

    def update_position(self, dt):
        """Default rigid body position integration function. 
        
        Updates the position of the body using Euler integration. Unlike the 
        velocity function, it's unlikely you'll want to override this 
        function. If you do, make sure you understand it's source code 
        (in Chipmunk) as it's an important part of the collision/joint 
        correction process. 
        """
        cp.cpBodyUpdatePosition(self._body, dt)


    def local_to_world(self, v):
        """Convert body local coordinates to world space coordinates"""
        #TODO: Test me
        v = Vec2d(v)
        return self.position + v.cpvrotate(self.rotation_vector)
        
    def world_to_local(self, v):
        """Convert world space coordinates to body local coordinates"""
        #TODO: Test me
        v = Vec2d(v)
        return (v - self.position).cpvunrotate(self.rotation_vector)


    

class Shape(object):
    """Base class for all the shapes. 
    
    You usually dont want to create instances of this class directly but use 
    one of the specialized shapes instead.
    """
    def __init__(self, shape=None):
        self._shape = shape
        self._shapecontents = self._shape.contents
        self._body = shape.body
        self.data = None

    def __del__(self):
        cp.cpShapeFree(self._shape)

    def _get_hashid(self):
        return self._shapecontents.hashid
    _hashid = property(_get_hashid)
        
    def _get_sensor(self):
        return bool(self._shapecontents.sensor)
    def _set_sensor(self, is_sensor):
        self._shapecontents.sensor = is_sensor
    sensor = property(_get_sensor, _set_sensor, 
        doc="""A boolean value if this shape is a sensor or not. Sensors only
        call collision callbacks, and never generate real collisions.""")
    
    def _get_collision_type(self):
        return self._shapecontents.collision_type
    def _set_collision_type(self, t):
        self._shapecontents.collision_type = t
    collision_type = property(_get_collision_type, _set_collision_type,
        doc="""User defined collision type for the shape. See 
        add_collisionpair_func function for more information on when to use 
        this property""")

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
        i.e. (a.layers & b.layers) != 0. By default, a shape occupies all 
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
        doc="""Friction coefficient. Chipmunk (and therefor pymunk) uses the 
        Coulomb friction model, a value of 0.0 is frictionless.""")

    def _get_surface_velocity(self):
        return self._shapecontents.surface_v
    def _set_surface_velocity(self, surface_v):
        self._shapecontents.surface_v = surface_v
    surface_velocity = property(_get_surface_velocity, _set_surface_velocity, 
        doc="""The surface velocity of the object. Useful for creating 
        conveyor belts or players that move around. This value is only used 
        when calculating friction, not resolving the collision.""")

    body = property(lambda self: self._body, 
        doc="""The body this shape is attached to""")

    def cache_bb(self):
        """Update and returns the bouding box of this shape"""
        return BB(cp.cpShapeCacheBB(self._shape))

    def point_query(self, p):
        """Check if the given point lies within the shape."""
        return bool(cp.cpShapePointQuery(self._shape, p))
        
    def segment_query(self, start, end):
        """Check if the line segment from start to end intersects the shape. 
        
        Return either SegmentQueryInfo object or None
        """
        info = cp.cpSegmentQueryInfo()
        info_p = ct.POINTER(cp.cpSegmentQueryInfo)(info)
        r = cp.cpShapeSegmentQuery(self._shape, start, end, info_p)
        if bool(r):
            return SegmentQueryInfo(self, start, end, info.t, info.n)
        else:
            return None
    
class SegmentQueryInfo(object):
    """Segment queries return more information than just a simple yes or no, 
    they also return where a shape was hit and it's surface normal at the hit 
    point. This object hold that information.
    """
    def __init__(self, shape, start, end, t, n):
        """You shouldn't need to initialize SegmentQueryInfo objects on your 
        own.
        """
        self._shape = shape
        self._t = t
        self._n = n
        self._start = start
        self._end = end
        
    def __str__(self):
        return "SegmentQueryInfo(%s, %s, %s, %s, %s)" % (self.shape, self._start, self._end, self.t, self.n)
    shape = property(lambda self: self._shape
        , doc = """Shape that was hit""")
        
    t = property(lambda self: self._t
        , doc = """Distance along query segment, will always be in the range [0, 1]""")
        
    n = property(lambda self: self._n
        , doc = """Normal of hit surface""")
        
    def get_hit_point(self):
        """Return the hit point in world coordinates where the segment first 
        intersected with the shape
        """
        return cp._cpvlerp(self._start, self._end, self.t)
        
    def get_hit_distance(self):
        """Return the absolute distance where the segment first hit the shape
        """
        return cp._cpvdist(self._start, self._end) * self.t
    
    
class Circle(Shape):
    """A circle shape defined by a radius
    
    This is the fastest and simplest collision shape
    """
    def __init__(self, body, radius, offset = (0,0)):
        """body is the body attach the circle to, offset is the offset from the
        body's center of gravity in body local coordinates."""
        self._body = body
        self._shape = cp.cpCircleShapeNew(body._body, radius, offset)
        self._shapecontents = self._shape.contents
        self._cs = ct.cast(self._shape, ct.POINTER(cp.cpCircleShape))
        
    def unsafe_set_radius(self, r):
        """Unsafe set the radius of the circle. 
    
        *WARNING:* This change is only picked up as a change to the position 
        of the shape's surface, but not it's velocity. Changing it will not 
        result in realistic physical behavior. Only use if you know what you 
        are doing!
        """
        cp.cpCircleShapeSetRadius(self._shape, r)
        
    def _get_radius(self):
        return cp.cpCircleShapeGetRadius(self._shape)
    radius = property(_get_radius, doc="""The Radius of the circle""")

    def unsafe_set_offset(self, o):
        """Unsafe set the offset of the circle. 
    
        *WARNING:* This change is only picked up as a change to the position 
        of the shape's surface, but not it's velocity. Changing it will not 
        result in realistic physical behavior. Only use if you know what you 
        are doing!
        """
        cp.cpCircleShapeSetOffset(self._shape, o)
    
    def _get_offset (self):
        return cp.cpCircleShapeGetOffset(self._shape)
    offset = property(_get_offset, doc="""Offset. (body space coordinates)""")

    
class Segment(Shape):
    """A line segment shape between two points
    
    This shape can be attached to moving bodies, but don't currently generate 
    collisions with other line segments. Can be beveled in order to give it a 
    thickness. 
    """
    def __init__(self, body, a, b, radius):
        """Create a Segment
        
        :Parameters:
            body : `Body`
                The body to attach the segment to
            a : (x,y) or `Vec2d`
                The first endpoint of the segment
            b : (x,y) or `Vec2d`
                The first endpoint of the segment
            radius : float
                The thickness of the segment
        """
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
        
    def _set_radius(self, r):
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.r = r
    def _get_radius(self):
        return ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.r
    radius = property(_get_radius, _set_radius, 
        doc="""The thickness of the segment""")


class Poly(Shape):
    """A convex polygon shape
    
    Slowest, but most flexible collision shape. 
    """
    def __init__(self, body, vertices, offset=(0,0), auto_order_vertices=True):
        """Create a polygon
        
            body : `Body`
                The body to attach the poly to
            vertices : [(x,y)] or [`Vec2d`]
                Define a convex hull of the polygon with a counterclockwise
                winding.
            offset : (x,y) or `Vec2d`
                The offset from the body's center of gravity in body local 
                coordinates. 
            auto_order_vertices : bool 
                Set to True to automatically order the vertices. If you know 
                the vertices are in the correct (clockwise) orded you can gain 
                a little performance by setting this to False.
        """
        
        self._body = body
        self.offset = offset
        #self.verts = (Vec2d * len(vertices))(*vertices)
        self.verts = (Vec2d * len(vertices))
        self.verts = self.verts(Vec2d(0, 0))
        
        i_vs = enumerate(vertices)
        if auto_order_vertices and not u.is_clockwise(vertices):
            i_vs = zip(xrange(len(vertices)-1, -1, -1), vertices)
        
        for (i, vertex) in i_vs:
            self.verts[i].x = vertex[0]
            self.verts[i].y = vertex[1]

        self._shape = cp.cpPolyShapeNew(body._body, len(vertices), self.verts, offset)
        self._shapecontents = self._shape.contents
        
    def get_points(self):
        """Get the points in world coordinates for the polygon"""
        #shape = ct.cast(self._shape, ct.POINTER(cp.cpPolyShape))
        #num = shape.contents.numVerts
        #verts = shape.contents.verts
        points = []
        rv = self._body.rotation_vector
        bp = self._body.position
        vs = self.verts
        o = self.offset
        for i in xrange(len(vs)):
            p = (vs[i]+o).cpvrotate(rv)+bp
            points.append(Vec2d(p))
            
        return points

def moment_for_circle(mass, inner_radius, outer_radius, offset=(0,0)):
    """Calculate the moment of inertia for a circle"""
    return cp.cpMomentForCircle(mass, inner_radius, outer_radius, offset)

def moment_for_poly(mass, vertices,  offset=(0,0)):
    """Calculate the moment of inertia for a polygon"""
    verts = (Vec2d * len(vertices))
    verts = verts(Vec2d(0, 0))
    for (i, vertex) in enumerate(vertices):
        verts[i].x = vertex[0]
        verts[i].y = vertex[1]
    return cp.cpMomentForPoly(mass, len(verts), verts, offset)
    
def reset_shapeid_counter():
    """Reset the internal shape counter
    
    Chipmunk (and therefor pymunk) keeps a counter so that every new shape 
    is given a unique hash value to be used in the spatial hash. Because this 
    affects the order in which the collisions are found and handled, you 
    should reset the shape counter every time you populate a space with new 
    shapes. If you don't, there might be (very) slight differences in the 
    simulation.
    """
    cp.cpResetShapeIdCounter()

    
class Contact(object):
    """Contact information"""
    def __init__(self, _contact):
        """Initialize a Contact object from the chipmunk equivalent struct
        
        *Note:* You should never need to create an instance of this class 
        directly.
        """
        self._p = _contact.p
        self._n = _contact.n
        self._dist = _contact.dist
        #self._contact = contact

    def __repr__(self):
        return "Contact(%s, %s, %s)" % (self.position, self.normal, self.distance)
        
    def _get_position(self):
        return self._p
    position = property(_get_position, doc="""Contact position""")

    def _get_normal(self):
        return self._n
    normal = property(_get_normal, doc="""Contact normal""")

    def _get_distance(self):
        return self._dist
    distance = property(_get_distance, doc="""Penetration distance""")
    


class Arbiter(object):
    """Arbiters are collision pairs between shapes that are used with the 
    collision callbacks.
    
    *IMPORTANT:* Because arbiters are handled by the space you should never 
    hold onto a reference to an arbiter as you don't know when it will be 
    destroyed! Use them within the callback where they are given to you and 
    then forget about them or copy out the information you need from them.
    """
    def __init__(self, _arbiter, space):
        """You should never need to create an Arbiter yourself, consider this 
        method private :)
        """
        self._arbiter = _arbiter
        self._arbitercontents = self._arbiter.contents
        self._space = space
        self._contacts = None # keep a lazy loaded cache of converted contacts
        
    def _get_contacts(self):
        if self._contacts is None:
            self._contacts = []
            for i in xrange(self._arbitercontents.numContacts):
                self.contacts.append(Contact(self._arbitercontents.contacts[i]))
        return self._contacts
    contacts = property(_get_contacts, 
        doc="""Information on the contact points between the objects.""")
        
    def _get_shapes(self):
        _a = self._arbitercontents.a
        _b = self._arbitercontents.b
        def _get_shape(_s):
            if _s.contents.hashid in self._space._shapes:
                s = self._space._shapes[_s.contents.hashid]
            elif _s.contents.hashid in self._space._static_shapes:
                s = self._space._static_shapes[_s.contents.hashid]
            else:
                s = None
            return s
        a,b = _get_shape(_a), _get_shape(_b)
        if self.swapped_coll:
            return b,a
        else:
            return a,b
            
    shapes = property(_get_shapes, 
        doc="""Get the shapes in the order that they were defined in the collision handler associated with this arbiter""")
            
    def _get_elasticity(self):
        return self._arbiter.contents.e
    elasticity = property(_get_elasticity, doc="""Elasticity""")
    
    def _get_friction(self):
        return self._arbiter.contents.u
    friction = property(_get_friction, doc="""Friction""")
    
    def _get_surface_velocity(self):
        return self._arbiter.contents.surface_vr
    surface_velocity = property(_get_surface_velocity, 
        doc="""Used for surface_v calculations, implementation may change""")

    def _get_stamp(self):
        return self._arbiter.contents.stamp
    stamp = property(_get_stamp, 
        doc="""Time stamp of the arbiter. (from the space)""")

    def _get_swapped_coll(self):
        return bool(self._arbiter.contents.swappedColl)
    swapped_coll = property(_get_swapped_coll,
        doc="""Are the shapes swapped in relation to the collision handler?""")
    
    def _get_is_first_contact(self):
        return bool(self._arbiter.contents.firstColl)
    is_first_contact = property(_get_is_first_contact,
        doc="""Returns true if this is the first step that an arbiter existed. You can use this from preSolve and postSolve to know if a collision between two shapes is new without needing to flag a boolean in your begin callback.""")
        
    
    
class BB(object):
    """Simple bounding box class. Stored as left, bottom, right, top values."""
    def __init__(self, *args):
        """Create a new instance of a bounding box. Can be created with zero 
        size with bb = BB() or with four args defining left, bottom, right and
        top: bb = BB(left, bottom, right, top)
        """
        if len(args) == 0:
            self._bb = cp.cpBB()
        elif len(args) == 1:
            self._bb = args[0]
        else:
            self._bb = cp._cpBBNew(args[0],args[1], args[2],args[3])
            
    # String representaion (for debugging)
    def __repr__(self):
        return 'BB(%s, %s, %s, %s)' % (self.left, self.bottom, self.right, self.top)
        
    def __eq__(self, other):
        return self.left == other.left and self.bottom == other.bottom and \
            self.right == other.right and self.top == other.top
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def intersects(self, other):
        """Returns true if the bounding boxes intersect"""
        return bool(cp._cpBBintersects(self._bb, other._bb))

    def contains(self, other):
        """Returns true if bb completley contains the other bb"""
        return bool(cp._cpBBcontainsBB(self._bb, other._bb))
        
    def contains_vect(self, v):
        """Returns true if this bb contains the vector v"""
        return bool(cp._cpBBcontainsVect(self._bb, v))
        
    def merge(self, other):
        """Return the minimal bounding box that contains both this bb and the 
        other bb
        """
        return BB(cp._cpBBmerge(self._bb, other._bb))
        
    def expand(self, v):
        """Return the minimal bounding box that contans both this bounding box 
        and the vector v
        """
        return BB(cp._cpBBexpand(self._bb, v))
        
    left = property(lambda self: self._bb.l)
    bottom = property(lambda self: self._bb.b)
    right = property(lambda self: self._bb.r)
    top = property(lambda self: self._bb.t)
    
    def clamp_vect(self, v):
        """Returns a copy of the vector v clamped to the bounding box"""
        return cp.cpBBClampVect(self._bb, v)
    
    def wrap_vect(self, v):
        """Returns a copy of v wrapped to the bounding box.
        That is, BB(0,0,10,10).wrap_vect((5,5)) == Vec2d(10,10)
        """
        return cp.cpBBWrapVect(self._bb, v)
        
"""       
v1 = Vec2d(1,3)
v2 = Vec2d(1,3)

b = Body(10,100)
bb = BB(1,2,3,4)
bb1 = BB(0,0,10,10)
bb2 = BB(1,2,3,4)
c = Circle(b, 10, (0.1,0.1))
s = Segment(b, (10,10), (100,100),5)
ss = Space()
ss.add(c)
ss.step(1)
"""

def test(): 
    try:
        bb = cp.cpBB(1,2,3,4)
        print cp.cpBBWrapVect(bb, Vec2d(10,12))
    except Exception, e: 
        print e
    
    try:
        test_bb = BB(1,2,3,4)
        test_v = Vec2d(12,14)
        print  test_bb.wrap_vect(test_v)
    except Exception, e: 
        print e
    try:
        test_b = Body(10,100)
        test_c = Circle(test_b, 10, (3.1,5.9))
        print test_c.offset
    except Exception, e:
        print e

 
        
#del cp, ct, u

