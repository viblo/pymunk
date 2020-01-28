__docformat__ = "reStructuredText"

from weakref import WeakSet
import copy
    
from . import _chipmunk_cffi
cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi    
from .vec2d import Vec2d
from .arbiter import Arbiter
from ._pickle import PickleMixin

class Body(PickleMixin, object):
    """A rigid body

    * Use forces to modify the rigid bodies if possible. This is likely to be
      the most stable.
    * Modifying a body's velocity shouldn't necessarily be avoided, but
      applying large changes can cause strange results in the simulation.
      Experiment freely, but be warned.
    * Don't modify a body's position every step unless you really know what
      you are doing. Otherwise you're likely to get the position/velocity badly
      out of sync.

    A Body can be copied and pickled. Sleeping bodies that are copied will be 
    awake in the fresh copy. When a Body is copied any spaces, shapes or 
    constraints attached to the body will not be copied.
    """

    DYNAMIC = cp.CP_BODY_TYPE_DYNAMIC
    """Dynamic bodies are the default body type.

    They react to collisions,
    are affected by forces and gravity, and have a finite amount of mass.
    These are the type of bodies that you want the physics engine to
    simulate for you. Dynamic bodies interact with all types of bodies
    and can generate collision callbacks.
    """

    KINEMATIC = cp.CP_BODY_TYPE_KINEMATIC
    """Kinematic bodies are bodies that are controlled from your code
    instead of inside the physics engine.

    They arent affected by gravity and they have an infinite amount of mass
    so they don't react to collisions or forces with other bodies. Kinematic
    bodies are controlled by setting their velocity, which will cause them
    to move. Good examples of kinematic bodies might include things like
    moving platforms. Objects that are touching or jointed to a kinematic
    body are never allowed to fall asleep.
    """

    STATIC = cp.CP_BODY_TYPE_STATIC
    """Static bodies are bodies that never (or rarely) move.

    Using static bodies for things like terrain offers a big performance
    boost over other body types- because Chipmunk doesn't need to check for
    collisions between static objects and it never needs to update their
    collision information. Additionally, because static bodies don't
    move, Chipmunk knows it's safe to let objects that are touching or
    jointed to them fall asleep. Generally all of your level geometry
    will be attached to a static body except for things like moving
    platforms or doors. Every space provide a built-in static body for
    your convenience. Static bodies can be moved, but there is a
    performance penalty as the collision information is recalculated.
    There is no penalty for having multiple static bodies, and it can be
    useful for simplifying your code by allowing different parts of your
    static geometry to be initialized or moved separately.
    """

    _pickle_attrs_init = ['mass', 'moment', 'body_type']
    _pickle_attrs_general = ['force', 'angle', 'position', 'center_of_gravity', 
        'velocity',  'angular_velocity', 'torque']
    _pickle_attrs_skip = ['is_sleeping', '_velocity_func', '_position_func']

    def __init__(self, mass=0, moment=0, body_type=DYNAMIC):
        """Create a new Body

        Mass and moment are ignored when body_type is KINEMATIC or STATIC.

        Guessing the mass for a body is usually fine, but guessing a moment
        of inertia can lead to a very poor simulation so it's recommended to
        use Chipmunk's moment calculations to estimate the moment for you.

        There are two ways to set up a dynamic body. The easiest option is to
        create a body with a mass and moment of 0, and set the mass or
        density of each collision shape added to the body. Chipmunk will
        automatically calculate the mass, moment of inertia, and center of
        gravity for you. This is probably preferred in most cases. Note that 
        these will only be correctly calculated after the body and shape are 
        added to a space.

        The other option is to set the mass of the body when it's created,
        and leave the mass of the shapes added to it as 0.0. This approach is
        more flexible, but is not as easy to use. Don't set the mass of both
        the body and the shapes. If you do so, it will recalculate and
        overwrite your custom mass value when the shapes are added to the body.

        Examples of the different ways to set up the mass and moment:

        >>> import pymunk
        >>> radius = 2
        >>> mass = 3
        >>> density = 3
        >>> def print_mass_moment(b): 
        ...    print("mass={:.0f} moment={:.0f}".format(b.mass, b.moment))
        
        >>> # Using Shape.density
        >>> s = pymunk.Space()
        >>> b = pymunk.Body()
        >>> c = pymunk.Circle(b, radius)
        >>> c.density = density
        >>> print_mass_moment(b)
        mass=0 moment=0
        >>> s.add(b, c)
        >>> print_mass_moment(b)
        mass=38 moment=75

        >>> # Using Shape.mass
        >>> b = pymunk.Body()
        >>> c = pymunk.Circle(b, radius)
        >>> c.mass = mass
        >>> print_mass_moment(b)
        mass=0 moment=0
        >>> s.add(b, c)
        >>> print_mass_moment(b)
        mass=3 moment=6

        >>> # Using Body constructor
        >>> moment = pymunk.moment_for_circle(mass, 0, radius)
        >>> b = pymunk.Body()
        >>> c = pymunk.Circle(b, radius)
        >>> c.mass = mass
        >>> print_mass_moment(b)
        mass=0 moment=0
        >>> s.add(b, c)
        >>> print_mass_moment(b)
        mass=3 moment=6

        It becomes even more useful to use the mass or density properties of 
        the shape when you attach multiple shapes to one body, like in this 
        example with density:

        >>> # Using multiple Shape.density
        >>> b = pymunk.Body()
        >>> c1 = pymunk.Circle(b, radius, offset=(10,0))
        >>> c1.density = density
        >>> c2 = pymunk.Circle(b, radius, offset=(0,10))
        >>> c2.density = density
        >>> s.add(b, c1, c2)
        >>> print_mass_moment(b)
        mass=75 moment=3921

        """
        if body_type == Body.DYNAMIC:
            self._body = ffi.gc(cp.cpBodyNew(mass, moment), cp.cpBodyFree)
        elif body_type == Body.KINEMATIC:
            self._body = ffi.gc(cp.cpBodyNewKinematic(), cp.cpBodyFree)
        elif body_type == Body.STATIC:
            self._body = ffi.gc(cp.cpBodyNewStatic(), cp.cpBodyFree)

        self._init()

    def _init(self):
        self._position_func = None # To prevent the gc to collect the callbacks.
        self._velocity_func = None # To prevent the gc to collect the callbacks.
        self._position_func_base = None # For pickle
        self._velocity_func_base = None # For pickle

        self._space = None # Weak ref to the space holding this body (if any)

        self._constraints = WeakSet() # weak refs to any constraints attached
        self._shapes = WeakSet() # weak refs to any shapes attached
            
    def __repr__(self):
        if self.body_type == Body.DYNAMIC:
            return 'Body(%r, %r, Body.DYNAMIC)' % (self.mass, self.moment)
        elif self.body_type == Body.KINEMATIC:
            return 'Body(Body.KINEMATIC)'
        elif self.body_type == Body.STATIC:
            return 'Body(Body.STATIC)'

    @classmethod
    def _init_with_body(cls, _body):
        """Only used internally in pymunk."""
        b = cls.__new__(cls)
        b._body = _body
        b._init()
        return b

    def _set_mass(self, mass):
        cp.cpBodySetMass(self._body, mass)
    def _get_mass(self):
        return cp.cpBodyGetMass(self._body)
    mass = property(_get_mass, _set_mass,
        doc="""Mass of the body.""")

    def _set_moment(self, moment):
        cp.cpBodySetMoment(self._body, moment)
    def _get_moment(self):
        return cp.cpBodyGetMoment(self._body)
    moment = property(_get_moment, _set_moment,
        doc="""Moment of inertia (MoI or sometimes just moment) of the body.

        The moment is like the rotational mass of a body.
        """)

    def _set_position(self, pos):
        cp.cpBodySetPosition(self._body, tuple(pos))
    def _get_position(self):
        p = cp.cpBodyGetPosition(self._body)
        return Vec2d._fromcffi(p)
    position = property(_get_position, _set_position,
        doc="""Position of the body.

        When changing the position you may also want to call
        :py:func:`Space.reindex_shapes_for_body` to update the collision 
        detection information for the attached shapes if plan to make any 
        queries against the space.""")

    def _set_center_of_gravity(self, cog):
        cp.cpBodySetCenterOfGravity(self._body, tuple(cog))
    def _get_center_of_gravity(self):
        return Vec2d._fromcffi(cp.cpBodyGetCenterOfGravity(self._body))
    center_of_gravity = property(_get_center_of_gravity,
        _set_center_of_gravity,
        doc="""Location of the center of gravity in body local coordinates.

        The default value is (0, 0), meaning the center of gravity is the
        same as the position of the body.
        """)

    def _set_velocity(self, vel):
        cp.cpBodySetVelocity(self._body, tuple(vel))
    def _get_velocity(self):
        return Vec2d._fromcffi(cp.cpBodyGetVelocity(self._body))
    velocity = property(_get_velocity, _set_velocity,
        doc="""Linear velocity of the center of gravity of the body.""")

    def _set_force(self, f):
        cp.cpBodySetForce(self._body, tuple(f))
    def _get_force(self):
        return Vec2d._fromcffi(cp.cpBodyGetForce(self._body))
    force = property(_get_force, _set_force,
        doc="""Force applied to the center of gravity of the body.

        This value is reset for every time step. Note that this is not the 
        total of forces acting on the body (such as from collisions), but the 
        force applied manually from the apply force functions.""")

    def _set_angle(self, angle):
        cp.cpBodySetAngle(self._body, angle)
    def _get_angle(self):
        return cp.cpBodyGetAngle(self._body)
    angle = property(_get_angle, _set_angle,
        doc="""Rotation of the body in radians.

        When changing the rotation you may also want to call
        :py:func:`Space.reindex_shapes_for_body` to update the collision 
        detection information for the attached shapes if plan to make any 
        queries against the space. A body rotates around its center of gravity, 
        not its position.

        .. Note::
            If you get small/no changes to the angle when for example a
            ball is "rolling" down a slope it might be because the Circle shape
            attached to the body or the slope shape does not have any friction
            set.""")


    def _set_angular_velocity(self, w):
        cp.cpBodySetAngularVelocity(self._body, w)
    def _get_angular_velocity(self):
        return cp.cpBodyGetAngularVelocity(self._body)
    angular_velocity = property(_get_angular_velocity, _set_angular_velocity,
        doc="""The angular velocity of the body in radians per second.""")

    def _set_torque(self, t):
        cp.cpBodySetTorque(self._body, t)
    def _get_torque(self):
        return cp.cpBodyGetTorque(self._body)
    torque = property(_get_torque, _set_torque,
        doc="""The torque applied to the body.

        This value is reset for every time step.""")

    def _get_rotation_vector(self):
        return Vec2d._fromcffi(cp.cpBodyGetRotation(self._body))
    rotation_vector = property(_get_rotation_vector,
        doc="""The rotation vector for the body.""")

    def _get_space(self):
        if self._space != None:
            return self._space._get_self() #ugly hack because of weakref
        else:
            return None
    space = property(_get_space,
        doc="""Get the :py:class:`Space` that the body has been added to (or 
        None).""")

    def _set_velocity_func(self, func):
        @ffi.callback("cpBodyVelocityFunc")
        def _impl(_, gravity, damping, dt):
            return func(self, Vec2d._fromcffi(gravity), damping, dt)

        self._velocity_func_base = func
        self._velocity_func = _impl
        cp.cpBodySetVelocityUpdateFunc(self._body, _impl)
    velocity_func = property(fset=_set_velocity_func,
        doc="""The velocity callback function. 
        
        The velocity callback function is called each time step, and can be 
        used to set a body's velocity.

            ``func(body : Body, gravity, damping, dt)``

        There are many cases when this can be useful. One example is individual 
        gravity for some bodies, and another is to limit the velocity which is 
        useful to prevent tunneling. 
        
        Example of a callback that sets gravity to zero for a object.

        >>> import pymunk
        >>> space = pymunk.Space()
        >>> space.gravity = 0, 10
        >>> body = pymunk.Body(1,2)
        >>> space.add(body)
        >>> def zero_gravity(body, gravity, damping, dt):
        ...     pymunk.Body.update_velocity(body, (0,0), damping, dt)
        ... 
        >>> body.velocity_func = zero_gravity
        >>> space.step(1)
        >>> space.step(1)
        >>> print(body.position, body.velocity)
        Vec2d(0.0, 0.0) Vec2d(0.0, 0.0)

        Example of a callback that limits the velocity:

        >>> import pymunk
        >>> body = pymunk.Body(1,2)
        >>> def limit_velocity(body, gravity, damping, dt):
        ...     max_velocity = 1000
        ...     pymunk.Body.update_velocity(body, gravity, damping, dt)
        ...     l = body.velocity.length
        ...     if l > max_velocity:
        ...         scale = max_velocity / l
        ...         body.velocity = body.velocity * scale
        ...
        >>> body.velocity_func = limit_velocity

        """)

    def _set_position_func(self, func):
        @ffi.callback("cpBodyPositionFunc")
        def _impl(_, dt):
            return func(self, dt)
        
        self._position_func_base = func    
        self._position_func = _impl
        cp.cpBodySetPositionUpdateFunc(self._body, _impl)
    position_func = property(fset=_set_position_func,
        doc="""The position callback function. 
        
        The position callback function is called each time step and can be 
        used to update the body's position.

            ``func(body, dt) -> None``
        """)

    def _get_kinetic_energy(self):
        #todo: use ffi method
        #return cp._cpBodyKineticEnergy(self._body)

        vsq = self.velocity.dot(self.velocity)
        wsq = self.angular_velocity * self.angular_velocity
        return (vsq*self.mass if vsq else 0.) + (wsq*self.moment if wsq else 0.)

    kinetic_energy = property(_get_kinetic_energy,
        doc="""Get the kinetic energy of a body.""")


    @staticmethod
    def update_velocity(body, gravity, damping, dt):
        """Default rigid body velocity integration function.

        Updates the velocity of the body using Euler integration.
        """
        cp.cpBodyUpdateVelocity(body._body, tuple(gravity), damping, dt)

    @staticmethod
    def update_position(body, dt):
        """Default rigid body position integration function.

        Updates the position of the body using Euler integration. Unlike the
        velocity function, it's unlikely you'll want to override this
        function. If you do, make sure you understand it's source code
        (in Chipmunk) as it's an important part of the collision/joint
        correction process.
        """
        cp.cpBodyUpdatePosition(body._body, dt)

    def apply_force_at_world_point(self, force, point):
        """Add the force force to body as if applied from the world point.

        People are sometimes confused by the difference between a force and
        an impulse. An impulse is a very large force applied over a very
        short period of time. Some examples are a ball hitting a wall or
        cannon firing. Chipmunk treats impulses as if they occur
        instantaneously by adding directly to the velocity of an object.
        Both impulses and forces are affected the mass of an object. Doubling
        the mass of the object will halve the effect.
        """
        cp.cpBodyApplyForceAtWorldPoint(self._body, tuple(force), tuple(point))

    def apply_force_at_local_point(self, force, point):
        """Add the local force force to body as if applied from the body
        local point.
        """
        cp.cpBodyApplyForceAtLocalPoint(self._body, tuple(force), tuple(point))

    def apply_impulse_at_world_point(self, impulse, point=(0, 0)):
        """Add the impulse impulse to body as if applied from the world point.
        """
        cp.cpBodyApplyImpulseAtWorldPoint(self._body, tuple(impulse), tuple(point))

    def apply_impulse_at_local_point(self, impulse, point=(0, 0)):
        """Add the local impulse impulse to body as if applied from the body
        local point.
        """
        cp.cpBodyApplyImpulseAtLocalPoint(self._body, tuple(impulse), tuple(point))


    def activate(self):
        """Reset the idle timer on a body.

        If it was sleeping, wake it and any other bodies it was touching.
        """
        cp.cpBodyActivate(self._body)

    def sleep(self):
        """Forces a body to fall asleep immediately even if it's in midair.

        Cannot be called from a callback.
        """
        if self._space == None:
            raise Exception("Body not added to space")
        cp.cpBodySleep(self._body)

    def sleep_with_group(self, body):
        """Force a body to fall asleep immediately along with other bodies
        in a group.

        When objects in Pymunk sleep, they sleep as a group of all objects
        that are touching or jointed together. When an object is woken up,
        all of the objects in its group are woken up. 
        :py:func:`Body.sleep_with_group` allows you group sleeping objects 
        together. It acts identically to :py:func:`Body.sleep` if you pass 
        None as group by starting a new group. If you pass a sleeping body 
        for group, body will be awoken when group is awoken. You can use this 
        to initialize levels and start stacks of objects in a pre-sleeping 
        state.
        """
        if self._space == None:
            raise Exception("Body not added to space")
        cp.cpBodySleepWithGroup(self._body, body._body)

    def _is_sleeping(self):
        return bool(cp.cpBodyIsSleeping(self._body))
    is_sleeping = property(_is_sleeping,
        doc="""Returns true if the body is sleeping.""")


    def _set_type(self, body_type):
        cp.cpBodySetType(self._body, body_type)
    def _get_type(self):
        return cp.cpBodyGetType(self._body)
    body_type = property(_get_type
        , _set_type
        , doc="""The type of a body (:py:const:`Body.DYNAMIC`, 
        :py:const:`Body.KINEMATIC` or :py:const:`Body.STATIC`).

        When changing an body to a dynamic body, the mass and moment of
        inertia are recalculated from the shapes added to the body. Custom
        calculated moments of inertia are not preserved when changing types.
        This function cannot be called directly in a collision callback.
        """)


    def each_arbiter(self, func, *args, **kwargs):
        """Run func on each of the arbiters on this body.

            ``func(arbiter, *args, **kwargs) -> None``

            Callback Parameters
                arbiter : :py:class:`Arbiter`
                    The Arbiter
                args
                    Optional parameters passed to the callback function.
                kwargs
                    Optional keyword parameters passed on to the callback function.

        .. warning::

            Do not hold on to the Arbiter after the callback!
        """
        @ffi.callback("cpBodyArbiterIteratorFunc")
        def cf(_body, _arbiter, _data):
            arbiter = Arbiter(_arbiter, self._space)
            func(arbiter, *args, **kwargs)
            
        data = ffi.new_handle(self)
        cp.cpBodyEachArbiter(self._body, cf, data)

    def _get_constraints(self):
        return set(self._constraints)

    constraints = property(_get_constraints,
        doc="""Get the constraints this body is attached to.

        The body only keeps a weak reference to the constraints and a
        live body wont prevent GC of the attached constraints""")

    def _get_shapes(self):
        return set(self._shapes)

    shapes = property(_get_shapes,
        doc="""Get the shapes attached to this body.

        The body only keeps a weak reference to the shapes and a live
        body wont prevent GC of the attached shapes""")

    def local_to_world(self, v):
        """Convert body local coordinates to world space coordinates

        Many things are defined in coordinates local to a body meaning that
        the (0,0) is at the center of gravity of the body and the axis rotate
        along with the body.

        :param v: Vector in body local coordinates
        """
        return Vec2d._fromcffi(cp.cpBodyLocalToWorld(self._body, tuple(v)))

    def world_to_local(self, v):
        """Convert world space coordinates to body local coordinates

        :param v: Vector in world space coordinates
        """
        return Vec2d._fromcffi(cp.cpBodyWorldToLocal(self._body, tuple(v)))

    def velocity_at_world_point(self, point):
        """Get the absolute velocity of the rigid body at the given world
        point

        It's often useful to know the absolute velocity of a point on the
        surface of a body since the angular velocity affects everything
        except the center of gravity.
        """
        return Vec2d._fromcffi(
            cp.cpBodyGetVelocityAtWorldPoint(self._body, tuple(point)))

    def velocity_at_local_point(self, point):
        """ Get the absolute velocity of the rigid body at the given body
        local point
        """
        return Vec2d._fromcffi(
            cp.cpBodyGetVelocityAtLocalPoint(self._body, tuple(point)))

    def __getstate__(self):
        """Return the state of this object
        
        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Body, self).__getstate__()

        d['special'].append(('is_sleeping', self.is_sleeping))
        d['special'].append(('_velocity_func', self._velocity_func_base))
        d['special'].append(('_position_func', self._position_func_base))

        return d

    def __setstate__(self, state):
        """Unpack this object from a saved state.

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        super(Body, self).__setstate__(state)
        
        for k,v in state['special']:
            if k == 'is_sleeping' and v:
                pass
            elif k == '_velocity_func' and v != None:
                self.velocity_func = v
            elif k == '_position_func' and v != None:
                self.position_func = v
    
    def copy(self):
        """Create a deep copy of this body."""
        return copy.deepcopy(self)
