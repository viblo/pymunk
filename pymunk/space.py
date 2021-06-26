__docformat__ = "reStructuredText"

import logging
import platform
import weakref
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Hashable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from pymunk.shape_filter import ShapeFilter
from pymunk.space_debug_draw_options import SpaceDebugDrawOptions

from . import _chipmunk_cffi, _version

cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi

from pymunk.constraints import Constraint

from ._pickle import PickleMixin, _State
from .body import Body
from .collision_handler import CollisionHandler
from .contact_point_set import ContactPointSet
from .query_info import PointQueryInfo, SegmentQueryInfo, ShapeQueryInfo
from .shapes import Shape
from .vec2d import Vec2d

if TYPE_CHECKING:
    from .bb import BB

_AddableObjects = Union[Body, Shape, Constraint]


class Space(PickleMixin, object):
    """Spaces are the basic unit of simulation. You add rigid bodies, shapes
    and joints to it and then step them all forward together through time.

    A Space can be copied and pickled. Note that any post step callbacks are
    not copied. Also note that some internal collision cache data is not copied,
    which can make the simulation a bit unstable the first few steps of the
    fresh copy.

    Custom properties set on the space will also be copied/pickled.

    Any collision handlers will also be copied/pickled. Note that depending on
    the pickle protocol used there are some restrictions on what functions can
    be copied/pickled.

    Example::

    >>> import pymunk, pickle
    >>> space = pymunk.Space()
    >>> space2 = space.copy()
    >>> space3 = pickle.loads(pickle.dumps(space))
    """

    _pickle_attrs_init = PickleMixin._pickle_attrs_init + ["threaded"]
    _pickle_attrs_general = PickleMixin._pickle_attrs_general + [
        "iterations",
        "gravity",
        "damping",
        "idle_speed_threshold",
        "sleep_time_threshold",
        "collision_slop",
        "collision_bias",
        "collision_persistence",
        "threads",
    ]

    def __init__(self, threaded: bool = False) -> None:
        """Create a new instance of the Space.

        If you set threaded=True the step function will run in threaded mode
        which might give a speedup. Note that even when you set threaded=True
        you still have to set Space.threads=2 to actually use more than one
        thread.

        Also note that threaded mode is not available on Windows, and setting
        threaded=True has no effect on that platform.
        """

        self.threaded = threaded and platform.system() != "Windows"

        if self.threaded:
            cp_space = cp.cpHastySpaceNew()
            freefunc = cp.cpHastySpaceFree
        else:
            cp_space = cp.cpSpaceNew()
            freefunc = cp.cpSpaceFree

        def spacefree(cp_space):  # type: ignore
            logging.debug("spacefree start %s", cp_space)
            cp_shapes = []

            @ffi.callback("cpSpaceShapeIteratorFunc")
            def cf1(cp_shape, data):  # type: ignore
                # print("spacefree shapecallback")
                cp_shapes.append(cp_shape)
                # cp_space = cp.cpShapeGetSpace(cp_shape)
                # cp.cpSpaceRemoveShape(cp_space, cp_shape)

            # print("spacefree shapes", cp_space)
            cp.cpSpaceEachShape(cp_space, cf1, ffi.NULL)
            for cp_shape in cp_shapes:
                logging.debug("spacefree remove shape %s %s", cp_space, cp_shape)
                cp.cpSpaceRemoveShape(cp_space, cp_shape)
                cp.cpShapeSetBody(cp_shape, ffi.NULL)

            cp_constraints = []

            @ffi.callback("cpSpaceConstraintIteratorFunc")
            def cf2(cp_constraint, data):  # type: ignore
                # print("spacefree shapecallback")
                cp_constraints.append(cp_constraint)

            cp.cpSpaceEachConstraint(cp_space, cf2, ffi.NULL)
            for cp_constraint in cp_constraints:
                logging.debug(
                    "spacefree remove constraint %s %s", cp_space, cp_constraint
                )
                cp.cpSpaceRemoveConstraint(cp_space, cp_constraint)

            cp_bodies = []

            @ffi.callback("cpSpaceBodyIteratorFunc")
            def cf3(cp_body, data):  # type:ignore
                # print("spacefree shapecallback")
                cp_bodies.append(cp_body)

            cp.cpSpaceEachBody(cp_space, cf3, ffi.NULL)
            for cp_body in cp_bodies:
                logging.debug("spacefree remove body %s %s", cp_space, cp_body)
                cp.cpSpaceRemoveBody(cp_space, cp_body)

            logging.debug("spacefree free %s", cp_space)
            freefunc(cp_space)

        self._space = ffi.gc(cp_space, spacefree)

        self._handlers: Dict[
            Any, CollisionHandler
        ] = {}  # To prevent the gc to collect the callbacks.

        self._post_step_callbacks: Dict[Any, Callable[["Space"], None]] = {}
        self._removed_shapes: Dict[int, Shape] = {}

        self._shapes: Dict[int, Shape] = {}
        self._bodies: Dict[Body, None] = {}
        self._static_body: Optional[Body] = None
        self._constraints: Dict[Constraint, None] = {}

        self._locked = False

        self._add_later: Set[_AddableObjects] = set()
        self._remove_later: Set[_AddableObjects] = set()

    def _get_self(self) -> "Space":
        return self

    @property
    def shapes(self) -> List[Shape]:
        """A list of all the shapes added to this space

        (includes both static and non-static)
        """
        return list(self._shapes.values())

    @property
    def bodies(self) -> List[Body]:
        """A list of the bodies added to this space"""
        return list(self._bodies)

    @property
    def constraints(self) -> List[Constraint]:
        """A list of the constraints added to this space"""
        return list(self._constraints)

    def _setup_static_body(self, static_body: Body) -> None:
        static_body._space = weakref.proxy(self)  # type: ignore
        cp.cpSpaceAddBody(self._space, static_body._body)

    @property
    def static_body(self) -> Body:
        """A dedicated static body for the space.

        You don't have to use it, but many times it can be convenient to have
        a static body together with the space.
        """
        if self._static_body is None:
            self._static_body = Body(body_type=Body.STATIC)
            self._setup_static_body(self._static_body)
            # self.add(self._static_body)

            # b = cp.cpSpaceGetStaticBody(self._space)
            # self._static_body = Body._init_with_body(b)
            # self._static_body._space = self
            # assert self._static_body is not None
        return self._static_body

    def _set_iterations(self, value: int) -> None:
        cp.cpSpaceSetIterations(self._space, value)

    def _get_iterations(self) -> int:
        return cp.cpSpaceGetIterations(self._space)

    iterations = property(
        _get_iterations,
        _set_iterations,
        doc="""Iterations allow you to control the accuracy of the solver.

        Defaults to 10.

        Pymunk uses an iterative solver to figure out the forces between
        objects in the space. What this means is that it builds a big list of
        all of the collisions, joints, and other constraints between the
        bodies and makes several passes over the list considering each one
        individually. The number of passes it makes is the iteration count,
        and each iteration makes the solution more accurate. If you use too
        many iterations, the physics should look nice and solid, but may use
        up too much CPU time. If you use too few iterations, the simulation
        may seem mushy or bouncy when the objects should be solid. Setting
        the number of iterations lets you balance between CPU usage and the
        accuracy of the physics. Pymunk's default of 10 iterations is
        sufficient for most simple games.
        """,
    )

    def _set_gravity(self, gravity_vector: Tuple[float, float]) -> None:
        assert len(gravity_vector) == 2
        cp.cpSpaceSetGravity(self._space, gravity_vector)

    def _get_gravity(self) -> Vec2d:
        v = cp.cpSpaceGetGravity(self._space)
        return Vec2d(v.x, v.y)

    gravity = property(
        _get_gravity,
        _set_gravity,
        doc="""Global gravity applied to the space.

        Defaults to (0,0). Can be overridden on a per body basis by writing
        custom integration functions and set it on the body:
        :py:meth:`pymunk.Body.velocity_func`.
        """,
    )

    def _set_damping(self, damping: float) -> None:
        cp.cpSpaceSetDamping(self._space, damping)

    def _get_damping(self) -> float:
        return cp.cpSpaceGetDamping(self._space)

    damping = property(
        _get_damping,
        _set_damping,
        doc="""Amount of simple damping to apply to the space.

        A value of 0.9 means that each body will lose 10% of its velocity per
        second. Defaults to 1. Like gravity, it can be overridden on a per
        body basis.
        """,
    )

    def _set_idle_speed_threshold(self, idle_speed_threshold: float) -> None:
        cp.cpSpaceSetIdleSpeedThreshold(self._space, idle_speed_threshold)

    def _get_idle_speed_threshold(self) -> float:
        return cp.cpSpaceGetIdleSpeedThreshold(self._space)

    idle_speed_threshold = property(
        _get_idle_speed_threshold,
        _set_idle_speed_threshold,
        doc="""Speed threshold for a body to be considered idle.

        The default value of 0 means the space estimates a good threshold
        based on gravity.
        """,
    )

    def _set_sleep_time_threshold(self, sleep_time_threshold: float) -> None:
        cp.cpSpaceSetSleepTimeThreshold(self._space, sleep_time_threshold)

    def _get_sleep_time_threshold(self) -> float:
        return cp.cpSpaceGetSleepTimeThreshold(self._space)

    sleep_time_threshold = property(
        _get_sleep_time_threshold,
        _set_sleep_time_threshold,
        doc="""Time a group of bodies must remain idle in order to fall
        asleep.

        The default value of `inf` disables the sleeping algorithm.
        """,
    )

    def _set_collision_slop(self, collision_slop: float) -> None:
        cp.cpSpaceSetCollisionSlop(self._space, collision_slop)

    def _get_collision_slop(self) -> float:
        return cp.cpSpaceGetCollisionSlop(self._space)

    collision_slop = property(
        _get_collision_slop,
        _set_collision_slop,
        doc="""Amount of overlap between shapes that is allowed.

        To improve stability, set this as high as you can without noticeable
        overlapping. It defaults to 0.1.
        """,
    )

    def _set_collision_bias(self, collision_bias: float) -> None:
        cp.cpSpaceSetCollisionBias(self._space, collision_bias)

    def _get_collision_bias(self) -> float:
        return cp.cpSpaceGetCollisionBias(self._space)

    collision_bias = property(
        _get_collision_bias,
        _set_collision_bias,
        doc="""Determines how fast overlapping shapes are pushed apart.

        Pymunk allows fast moving objects to overlap, then fixes the overlap
        over time. Overlapping objects are unavoidable even if swept
        collisions are supported, and this is an efficient and stable way to
        deal with overlapping objects. The bias value controls what
        percentage of overlap remains unfixed after a second and defaults
        to ~0.2%. Valid values are in the range from 0 to 1, but using 0 is
        not recommended for stability reasons. The default value is
        calculated as cpfpow(1.0f - 0.1f, 60.0f) meaning that pymunk attempts
        to correct 10% of error ever 1/60th of a second.

        ..Note::
            Very very few games will need to change this value.
        """,
    )

    def _set_collision_persistence(self, collision_persistence: float) -> None:
        cp.cpSpaceSetCollisionPersistence(self._space, collision_persistence)

    def _get_collision_persistence(self) -> float:
        return cp.cpSpaceGetCollisionPersistence(self._space)

    collision_persistence = property(
        _get_collision_persistence,
        _set_collision_persistence,
        doc="""The number of frames the space keeps collision solutions
        around for.

        Helps prevent jittering contacts from getting worse. This defaults
        to 3.

        ..Note::
            Very very few games will need to change this value.
        """,
    )

    def _get_current_time_step(self) -> int:
        return cp.cpSpaceGetCurrentTimeStep(self._space)

    current_time_step = property(
        _get_current_time_step,
        doc="""Retrieves the current (if you are in a callback from
        Space.step()) or most recent (outside of a Space.step() call)
        timestep.
        """,
    )

    def add(self, *objs: _AddableObjects) -> None:
        """Add one or many shapes, bodies or constraints (joints) to the space

        Unlike Chipmunk and earlier versions of pymunk its now allowed to add
        objects even from a callback during the simulation step. However, the
        add will not be performed until the end of the step.
        """

        if self._locked:
            self._add_later.update(objs)
            return

        # add bodies first, since the shapes require their bodies to be
        # already added. This allows code like space.add(shape, body).
        for o in objs:
            if isinstance(o, Body):
                self._add_body(o)

        for o in objs:
            if isinstance(o, Body):
                pass
            elif isinstance(o, Shape):
                self._add_shape(o)
            elif isinstance(o, Constraint):
                self._add_constraint(o)
            else:
                raise Exception(f"Unsupported type  {type(o)} of {o}.")

    def remove(self, *objs: _AddableObjects) -> None:
        """Remove one or many shapes, bodies or constraints from the space

        Unlike Chipmunk and earlier versions of Pymunk its now allowed to
        remove objects even from a callback during the simulation step.
        However, the removal will not be performed until the end of the step.

        .. Note::
            When removing objects from the space, make sure you remove any
            other objects that reference it. For instance, when you remove a
            body, remove the joints and shapes attached to it.
        """
        if self._locked:
            self._remove_later.update(objs)
            return

        for o in objs:
            if isinstance(o, Body):
                self._remove_body(o)
            elif isinstance(o, Shape):
                self._remove_shape(o)
            elif isinstance(o, Constraint):
                self._remove_constraint(o)
            else:
                raise Exception(f"Unsupported type  {type(o)} of {o}.")

    def _add_shape(self, shape: "Shape") -> None:
        """Adds a shape to the space"""
        # print("addshape", self._space, shape)
        assert shape._id not in self._shapes, "Shape already added to space."
        assert (
            shape.space == None
        ), "Shape already added to another space. A shape can only be in one space at a time."
        assert shape.body != None, "The shape's body is not set."
        assert (
            shape.body.space == self
        ), "The shape's body must be added to the space before (or at the same time) as the shape."

        shape._space = weakref.proxy(self)
        self._shapes[shape._id] = shape
        cp.cpSpaceAddShape(self._space, shape._shape)

    def _add_body(self, body: "Body") -> None:
        """Adds a body to the space"""
        assert body not in self._bodies, "Body already added to this space."
        assert body.space == None, "Body already added to another space."

        body._space = weakref.proxy(self)
        self._bodies[body] = None
        cp.cpSpaceAddBody(self._space, body._body)

    def _add_constraint(self, constraint: "Constraint") -> None:
        """Adds a constraint to the space"""
        assert constraint not in self._constraints, "Constraint already added to space."

        self._constraints[constraint] = None
        cp.cpSpaceAddConstraint(self._space, constraint._constraint)

    def _remove_shape(self, shape: "Shape") -> None:
        """Removes a shape from the space"""
        assert shape._id in self._shapes, "shape not in space, already removed?"
        self._removed_shapes[shape._id] = shape
        shape._space = None
        # During GC at program exit sometimes the shape might already be removed. Then skip this step.
        if cp.cpSpaceContainsShape(self._space, shape._shape):
            cp.cpSpaceRemoveShape(self._space, shape._shape)
        del self._shapes[shape._id]

    def _remove_body(self, body: "Body") -> None:
        """Removes a body from the space"""
        assert body in self._bodies, "body not in space, already removed?"
        body._space = None
        # During GC at program exit sometimes the shape might already be removed. Then skip this step.
        if cp.cpSpaceContainsBody(self._space, body._body):
            cp.cpSpaceRemoveBody(self._space, body._body)
        del self._bodies[body]

    def _remove_constraint(self, constraint: "Constraint") -> None:
        """Removes a constraint from the space"""
        assert (
            constraint in self._constraints
        ), "constraint not in space, already removed?"
        # print("remove", constraint, constraint._constraint, self._constraints)
        # During GC at program exit sometimes the constraint might already be removed. Then skip this steip.
        if cp.cpSpaceContainsConstraint(self._space, constraint._constraint):
            cp.cpSpaceRemoveConstraint(self._space, constraint._constraint)
        del self._constraints[constraint]

    def reindex_shape(self, shape: Shape) -> None:
        """Update the collision detection data for a specific shape in the
        space.
        """
        cp.cpSpaceReindexShape(self._space, shape._shape)

    def reindex_shapes_for_body(self, body: Body) -> None:
        """Reindex all the shapes for a certain body."""
        cp.cpSpaceReindexShapesForBody(self._space, body._body)

    def reindex_static(self) -> None:
        """Update the collision detection info for the static shapes in the
        space. You only need to call this if you move one of the static shapes.
        """
        cp.cpSpaceReindexStatic(self._space)

    def _get_threads(self) -> int:
        if self.threaded:
            return int(cp.cpHastySpaceGetThreads(self._space))
        return 1

    def _set_threads(self, n: int) -> None:
        if self.threaded:
            cp.cpHastySpaceSetThreads(self._space, n)

    threads = property(
        _get_threads,
        _set_threads,
        doc="""The number of threads to use for running the step function. 
        
        Only valid when the Space was created with threaded=True. Currently the 
        max limit is 2, setting a higher value wont have any effect. The 
        default is 1 regardless if the Space was created with threaded=True, 
        to keep determinism in the simulation. Note that Windows does not 
        support the threaded solver.
        """,
    )

    def use_spatial_hash(self, dim: float, count: int) -> None:
        """Switch the space to use a spatial hash instead of the bounding box
        tree.

        Pymunk supports two spatial indexes. The default is an axis-aligned
        bounding box tree inspired by the one used in the Bullet Physics
        library, but caching of overlapping leaves was added to give it very
        good temporal coherence. The tree requires no tuning, and most games
        will find that they get the best performance using from the tree. The
        other available spatial index type available is a spatial hash, which
        can be much faster when you have a very large number (1000s) of
        objects that are all the same size. For smaller numbers of objects,
        or objects that vary a lot in size, the spatial hash is usually much
        slower. It also requires tuning (usually through experimentation) to
        get the best possible performance.

        The spatial hash data is fairly size sensitive. dim is the size of
        the hash cells. Setting dim to the average collision shape size is
        likely to give the best performance. Setting dim too small will cause
        the shape to be inserted into many cells, setting it too low will
        cause too many objects into the same hash slot.

        count is the suggested minimum number of cells in the hash table. If
        there are too few cells, the spatial hash will return many false
        positives. Too many cells will be hard on the cache and waste memory.
        Setting count to ~10x the number of objects in the space is probably a
        good starting point. Tune from there if necessary.

        :param dim: the size of the hash cells
        :param count: the suggested minimum number of cells in the hash table
        """
        cp.cpSpaceUseSpatialHash(self._space, dim, count)

    def step(self, dt: float) -> None:
        """Update the space for the given time step.

        Using a fixed time step is highly recommended. Doing so will increase
        the efficiency of the contact persistence, requiring an order of
        magnitude fewer iterations to resolve the collisions in the usual case.

        It is not the same to call step 10 times with a dt of 0.1 and
        calling it 100 times with a dt of 0.01 even if the end result is
        that the simulation moved forward 100 units. Performing  multiple
        calls with a smaller dt creates a more stable and accurate
        simulation. Therefor it sometimes make sense to have a little for loop
        around the step call, like in this example:

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> steps = 10
        >>> for x in range(steps): # move simulation forward 0.1 seconds:
        ...     s.step(0.1 / steps)

        :param dt: Time step length
        """
        try:
            self._locked = True
            if self.threaded:
                cp.cpHastySpaceStep(self._space, dt)
            else:
                cp.cpSpaceStep(self._space, dt)
            self._removed_shapes = {}
        finally:
            self._locked = False

        self.add(*self._add_later)
        self._add_later.clear()
        for obj in self._remove_later:
            self.remove(obj)
        self._remove_later.clear()

        for key in self._post_step_callbacks:
            self._post_step_callbacks[key](self)

        self._post_step_callbacks = {}

    def add_collision_handler(
        self, collision_type_a: int, collision_type_b: int
    ) -> CollisionHandler:
        """Return the :py:class:`CollisionHandler` for collisions between
        objects of type collision_type_a and collision_type_b.

        Fill the desired collision callback functions, for details see the
        :py:class:`CollisionHandler` object.

        Whenever shapes with collision types (:py:attr:`Shape.collision_type`)
        a and b collide, this handler will be used to process the collision
        events. When a new collision handler is created, the callbacks will all be
        set to builtin callbacks that perform the default behavior (call the
        wildcard handlers, and accept all collisions).

        :param int collision_type_a: Collision type a
        :param int collision_type_b: Collision type b

        :rtype: :py:class:`CollisionHandler`
        """
        key = min(collision_type_a, collision_type_b), max(
            collision_type_a, collision_type_b
        )
        if key in self._handlers:
            return self._handlers[key]

        h = cp.cpSpaceAddCollisionHandler(
            self._space, collision_type_a, collision_type_b
        )
        ch = CollisionHandler(h, self)
        self._handlers[key] = ch
        return ch

    def add_wildcard_collision_handler(self, collision_type_a: int) -> CollisionHandler:
        """Add a wildcard collision handler for given collision type.

        This handler will be used any time an object with this type collides
        with another object, regardless of its type. A good example is a
        projectile that should be destroyed the first time it hits anything.
        There may be a specific collision handler and two wildcard handlers.
        It's up to the specific handler to decide if and when to call the
        wildcard handlers and what to do with their return values.

        When a new wildcard handler is created, the callbacks will all be
        set to builtin callbacks that perform the default behavior. (accept
        all collisions in :py:func:`~CollisionHandler.begin` and
        :py:func:`~CollisionHandler.pre_solve`, or do nothing for
        :py:func:`~CollisionHandler.post_solve` and
        :py:func:`~CollisionHandler.separate`.

        :param int collision_type_a: Collision type
        :rtype: :py:class:`CollisionHandler`
        """

        if collision_type_a in self._handlers:
            return self._handlers[collision_type_a]

        h = cp.cpSpaceAddWildcardHandler(self._space, collision_type_a)
        ch = CollisionHandler(h, self)
        self._handlers[collision_type_a] = ch
        return ch

    def add_default_collision_handler(self) -> CollisionHandler:
        """Return a reference to the default collision handler or that is
        used to process all collisions that don't have a more specific
        handler.

        The default behavior for each of the callbacks is to call
        the wildcard handlers, ANDing their return values together if
        applicable.
        """
        if None in self._handlers:
            return self._handlers[None]

        _h = cp.cpSpaceAddDefaultCollisionHandler(self._space)
        h = CollisionHandler(_h, self)
        self._handlers[None] = h
        return h

    def add_post_step_callback(
        self,
        callback_function: Callable[
            ..., None
        ],  # TODO: Fix me once PEP-612 is implemented
        key: Hashable,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """Add a function to be called last in the next simulation step.

        Post step callbacks are registered as a function and an object used as
        a key. You can only register one post step callback per object.

        This function was more useful with earlier versions of pymunk where
        you weren't allowed to use the add and remove methods on the space
        during a simulation step. But this function is still available for
        other uses and to keep backwards compatibility.

        .. Note::
            If you remove a shape from the callback it will trigger the
            collision handler for the 'separate' event if it the shape was
            touching when removed.

        .. Note::
            Post step callbacks are not included in pickle / copy of the space.

        :param callback_function: The callback function
        :type callback_function: `func(space : Space, key, *args, **kwargs)`
        :param Any key:
            This object is used as a key, you can only have one callback
            for a single object. It is passed on to the callback function.
        :param args: Optional parameters passed to the callback
        :param kwargs: Optional keyword parameters passed on to the callback

        :return: True if key was not previously added, False otherwise
        """

        if key in self._post_step_callbacks:
            return False

        def f(x):  # type: ignore
            callback_function(self, key, *args, **kwargs)

        self._post_step_callbacks[key] = f
        return True

    def point_query(
        self, point: Tuple[float, float], max_distance: float, shape_filter: ShapeFilter
    ) -> List[PointQueryInfo]:
        """Query space at point for shapes within the given distance range.

        The filter is applied to the query and follows the same rules as the
        collision detection. If a maxDistance of 0.0 is used, the point must
        lie inside a shape. Negative max_distance is also allowed meaning that
        the point must be a under a certain depth within a shape to be
        considered a match.

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        .. Note::
            Sensor shapes are included in the result (In
            :py:meth:`Space.point_query_nearest` they are not)

        :param point: Where to check for collision in the Space
        :type point: :py:class:`~vec2d.Vec2d` or (float,float)
        :param float max_distance: Match only within this distance
        :param ShapeFilter shape_filter: Only pick shapes matching the filter

        :rtype: [:py:class:`PointQueryInfo`]
        """
        assert len(point) == 2
        query_hits: List[PointQueryInfo] = []

        @ffi.callback("cpSpacePointQueryFunc")
        def cf(_shape, point, distance, gradient, data):  # type: ignore
            # space = ffi.from_handle(data)
            shape = self._get_shape(_shape)
            p = PointQueryInfo(
                shape, Vec2d(point.x, point.y), distance, Vec2d(gradient.x, gradient.y)
            )
            nonlocal query_hits
            query_hits.append(p)

        data = ffi.new_handle(self)
        cp.cpSpacePointQuery(self._space, point, max_distance, shape_filter, cf, data)
        return query_hits

    def _get_shape(self, _shape: Any) -> Optional[Shape]:
        if not bool(_shape):
            return None

        shapeid = int(ffi.cast("int", cp.cpShapeGetUserData(_shape)))
        # return self._shapes[hashid_private]

        if shapeid in self._shapes:
            return self._shapes[shapeid]
        elif shapeid in self._removed_shapes:
            return self._removed_shapes[shapeid]
        else:
            return None

    def point_query_nearest(
        self, point: Tuple[float, float], max_distance: float, shape_filter: ShapeFilter
    ) -> Optional[PointQueryInfo]:
        """Query space at point the nearest shape within the given distance
        range.

        The filter is applied to the query and follows the same rules as the
        collision detection. If a maxDistance of 0.0 is used, the point must
        lie inside a shape. Negative max_distance is also allowed meaning that
        the point must be a under a certain depth within a shape to be
        considered a match.

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        .. Note::
            Sensor shapes are not included in the result (In
            :py:meth:`Space.point_query` they are)

        :param point: Where to check for collision in the Space
        :type point: :py:class:`~vec2d.Vec2d` or (float,float)
        :param float max_distance: Match only within this distance
        :param ShapeFilter shape_filter: Only pick shapes matching the filter

        :rtype: :py:class:`PointQueryInfo` or None
        """
        assert len(point) == 2
        info = ffi.new("cpPointQueryInfo *")
        _shape = cp.cpSpacePointQueryNearest(
            self._space, point, max_distance, shape_filter, info
        )

        shape = self._get_shape(_shape)

        if shape != None:
            return PointQueryInfo(
                shape,
                Vec2d(info.point.x, info.point.y),
                info.distance,
                Vec2d(info.gradient.x, info.gradient.y),
            )
        return None

    def segment_query(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        radius: float,
        shape_filter: ShapeFilter,
    ) -> List[SegmentQueryInfo]:
        """Query space along the line segment from start to end with the
        given radius.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        .. Note::
            Sensor shapes are included in the result (In
            :py:meth:`Space.segment_query_first` they are not)

        :param start: Starting point
        :param end: End point
        :param float radius: Radius
        :param ShapeFilter shape_filter: Shape filter

        :rtype: [:py:class:`SegmentQueryInfo`]
        """
        assert len(start) == 2
        assert len(end) == 2
        query_hits: List[SegmentQueryInfo] = []

        @ffi.callback("cpSpaceSegmentQueryFunc")
        def cf(_shape, point, normal, alpha, data):  # type: ignore
            shape = self._get_shape(_shape)
            p = SegmentQueryInfo(
                shape, Vec2d(point.x, point.y), Vec2d(normal.x, normal.y), alpha
            )
            nonlocal query_hits
            query_hits.append(p)

        data = ffi.new_handle(self)
        cp.cpSpaceSegmentQuery(self._space, start, end, radius, shape_filter, cf, data)
        return query_hits

    def segment_query_first(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        radius: float,
        shape_filter: ShapeFilter,
    ) -> Optional[SegmentQueryInfo]:
        """Query space along the line segment from start to end with the
        given radius.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        .. Note::
            Sensor shapes are not included in the result (In
            :py:meth:`Space.segment_query` they are)

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        :rtype: :py:class:`SegmentQueryInfo` or None
        """
        assert len(start) == 2
        assert len(end) == 2
        info = ffi.new("cpSegmentQueryInfo *")
        _shape = cp.cpSpaceSegmentQueryFirst(
            self._space, start, end, radius, shape_filter, info
        )

        shape = self._get_shape(_shape)
        if shape != None:
            return SegmentQueryInfo(
                shape,
                Vec2d(info.point.x, info.point.y),
                Vec2d(info.normal.x, info.normal.y),
                info.alpha,
            )
        return None

    def bb_query(self, bb: "BB", shape_filter: ShapeFilter) -> List[Shape]:
        """Query space to find all shapes near bb.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        .. Note::
            Sensor shapes are included in the result

        :param bb: Bounding box
        :param shape_filter: Shape filter

        :rtype: [:py:class:`Shape`]
        """

        query_hits = []

        @ffi.callback("cpSpaceBBQueryFunc")
        def cf(_shape, data):  # type: ignore
            shape = self._get_shape(_shape)
            assert shape is not None
            nonlocal query_hits
            query_hits.append(shape)

        data = ffi.new_handle(self)
        cp.cpSpaceBBQuery(self._space, bb, shape_filter, cf, data)
        return query_hits

    def shape_query(self, shape: Shape) -> List[ShapeQueryInfo]:
        """Query a space for any shapes overlapping the given shape

        .. Note::
            Sensor shapes are included in the result

        :param shape: Shape to query with
        :type shape: :py:class:`Circle`, :py:class:`Poly` or :py:class:`Segment`

        :rtype: [:py:class:`ShapeQueryInfo`]
        """

        query_hits = []

        @ffi.callback("cpSpaceShapeQueryFunc")
        def cf(_shape, _points, _data):  # type: ignore
            found_shape = self._get_shape(_shape)
            point_set = ContactPointSet._from_cp(_points)
            info = ShapeQueryInfo(found_shape, point_set)
            nonlocal query_hits
            query_hits.append(info)

        data = ffi.new_handle(self)
        cp.cpSpaceShapeQuery(self._space, shape._shape, cf, data)

        return query_hits

    def debug_draw(self, options: SpaceDebugDrawOptions) -> None:
        """Debug draw the current state of the space using the supplied drawing
        options.

        If you use a graphics backend that is already supported, such as pygame
        and pyglet, you can use the predefined options in their x_util modules,
        for example :py:class:`pygame_util.DrawOptions`.

        Its also possible to write your own graphics backend, see
        :py:class:`SpaceDebugDrawOptions`.

        If you require any advanced or optimized drawing its probably best to
        not use this function for the drawing since its meant for debugging
        and quick scripting.

        :type options: :py:class:`SpaceDebugDrawOptions`
        """
        if options._use_chipmunk_debug_draw:
            h = ffi.new_handle(self)
            # we need to hold h until the end of cpSpaceDebugDraw to prevent GC
            options._options.data = h

            with options:
                cp.cpSpaceDebugDraw(self._space, options._options)
        else:
            for shape in self.shapes:
                options.draw_shape(shape)

    # def get_batched_bodies(self, shape_filter):
    #     """Return a memoryview for use when the non-batch api is not performant enough.

    #     .. note::
    #         Experimental API. Likely to change in future major, minor orpoint
    #         releases.
    #     """
    #     pass

    def __getstate__(self) -> _State:
        """Return the state of this object

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Space, self).__getstate__()

        d["special"].append(("pymunk_version", _version.version))
        # bodies needs to be added to the state before their shapes.
        d["special"].append(("bodies", self.bodies))
        if self._static_body != None:
            # print("getstate", self._static_body)
            d["special"].append(("_static_body", self._static_body))

        d["special"].append(("shapes", self.shapes))
        d["special"].append(("constraints", self.constraints))

        handlers = []
        for k, v in self._handlers.items():
            h: Dict[str, Any] = {}
            if v._begin_base is not None:
                h["_begin_base"] = v._begin_base
            if v._pre_solve_base is not None:
                h["_pre_solve_base"] = v._pre_solve_base
            if v._post_solve_base is not None:
                h["_post_solve_base"] = v._post_solve_base
            if v._separate_base is not None:
                h["_separate_base"] = v._separate_base
            handlers.append((k, h))

        d["special"].append(("_handlers", handlers))

        return d

    def __setstate__(self, state: _State) -> None:
        """Unpack this object from a saved state.

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        super(Space, self).__setstate__(state)

        for k, v in state["special"]:
            if k == "pymunk_version":
                assert (
                    _version.version == v
                ), f"Pymunk version {v} of pickled object does not match current Pymunk version {_version.version}"
            elif k == "bodies":
                self.add(*v)
            elif k == "_static_body":
                # _ = cp.cpSpaceSetStaticBody(self._space, v._body)
                # v._space = self
                # self._static_body = v
                # print("setstate", v, self._static_body)
                self._static_body = v
                self._setup_static_body(v)
                # self._static_body._space = weakref.proxy(self)
                # cp.cpSpaceAddBody(self._space, v._body)
                # self.add(v)

            elif k == "shapes":
                # print("setstate shapes", v)
                self.add(*v)
            elif k == "constraints":
                self.add(*v)
            elif k == "_handlers":
                for k2, hd in v:
                    if k2 == None:
                        h = self.add_default_collision_handler()
                    elif isinstance(k2, tuple):
                        h = self.add_collision_handler(k2[0], k2[1])
                    else:
                        h = self.add_wildcard_collision_handler(k2)
                    if "_begin_base" in hd:
                        h.begin = hd["_begin_base"]
                    if "_pre_solve_base" in hd:
                        h.pre_solve = hd["_pre_solve_base"]
                    if "_post_solve_base" in hd:
                        h.post_solve = hd["_post_solve_base"]
                    if "_separate_base" in hd:
                        h.separate = hd["_separate_base"]
