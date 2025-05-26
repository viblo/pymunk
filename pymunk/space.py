__docformat__ = "reStructuredText"

import math
import platform
import weakref
from collections.abc import KeysView
from typing import TYPE_CHECKING, Any, Callable, Hashable, Optional, Union

from pymunk.constraints import Constraint
from pymunk.shape_filter import ShapeFilter
from pymunk.space_debug_draw_options import SpaceDebugDrawOptions

from . import _version
from ._callbacks import *
from ._chipmunk_cffi import ffi, lib
from ._collision_handler import CollisionHandler, _CollisionCallback
from ._pickle import PickleMixin, _State
from ._util import _dead_ref
from .arbiter import Arbiter, _arbiter_from_dict, _arbiter_to_dict
from .body import Body
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
            cp_space = lib.cpHastySpaceNew()
            freefunc = lib.cpHastySpaceFree
        else:
            cp_space = lib.cpSpaceNew()
            freefunc = lib.cpSpaceFree

        def spacefree(cp_space: ffi.CData) -> None:
            cp_shapes: list[Shape] = []
            cp_shapes_h = ffi.new_handle(cp_shapes)
            lib.cpSpaceEachShape(
                cp_space, lib.ext_cpSpaceShapeIteratorFunc, cp_shapes_h
            )

            for cp_shape in cp_shapes:
                cp_space = lib.cpShapeGetSpace(cp_shape)

                lib.cpSpaceRemoveShape(cp_space, cp_shape)
                lib.cpShapeSetBody(cp_shape, ffi.NULL)

            cp_constraints: list[Constraint] = []
            cp_constraints_h = ffi.new_handle(cp_constraints)
            lib.cpSpaceEachConstraint(
                cp_space, lib.ext_cpSpaceConstraintIteratorFunc, cp_constraints_h
            )
            for cp_constraint in cp_constraints:
                cp_space = lib.cpConstraintGetSpace(cp_constraint)
                lib.cpSpaceRemoveConstraint(cp_space, cp_constraint)

            cp_bodys: list[Body] = []
            cp_bodys_h = ffi.new_handle(cp_bodys)
            lib.cpSpaceEachBody(cp_space, lib.ext_cpSpaceBodyIteratorFunc, cp_bodys_h)
            for cp_body in cp_bodys:
                cp_space = lib.cpBodyGetSpace(cp_body)
                lib.cpSpaceRemoveBody(cp_space, cp_body)

            freefunc(cp_space)

        self._space = ffi.gc(cp_space, spacefree)

        self._handlers: dict[Any, CollisionHandler] = (
            {}
        )  # To prevent the gc to collect the callbacks.

        self._post_step_callbacks: dict[Any, Callable[["Space"], None]] = {}
        self._removed_shapes: dict[Shape, None] = {}

        self._shapes: dict[Shape, None] = {}
        self._bodies: dict[Body, None] = {}
        self._static_body: Optional[Body] = None
        self._constraints: dict[Constraint, None] = {}

        self._locked = False

        self._add_later: set[_AddableObjects] = set()
        self._remove_later: set[_AddableObjects] = set()
        self._bodies_to_check: set[Body] = set()

    @property
    def shapes(self) -> KeysView[Shape]:
        """The shapes added to this space returned as a KeysView.

        Since its a view that is returned it will update as shapes are
        added.

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> s.add(pymunk.Circle(s.static_body, 1))
        >>> shapes_view = s.shapes
        >>> len(shapes_view)
        1
        >>> s.add(pymunk.Circle(s.static_body, 2))
        >>> len(shapes_view)
        2
        """
        return self._shapes.keys()

    @property
    def bodies(self) -> KeysView[Body]:
        """The bodies added to this space returned as a KeysView.

        This includes both static and non-static bodies added to the Space.
        Since its a view that is returned it will update as bodies are added:

        >>> import pymunk
        >>> s = pymunk.Space()
        >>> s.add(pymunk.Body())
        >>> bodies_view = s.bodies
        >>> len(bodies_view)
        1
        >>> s.add(pymunk.Body())
        >>> len(bodies_view)
        2
        """
        return self._bodies.keys()

    @property
    def constraints(self) -> KeysView[Constraint]:
        """The constraints added to this space as a KeysView."""
        return self._constraints.keys()

    def _setup_static_body(self, static_body: Body) -> None:
        static_body._space = weakref.ref(self)
        lib.cpSpaceAddBody(self._space, static_body._body)

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

            # b = lib.cpSpaceGetStaticBody(self._space)
            # self._static_body = Body._init_with_body(b)
            # self._static_body._space = self
            # assert self._static_body is not None
        return self._static_body

    @property
    def iterations(self) -> int:
        """Iterations allow you to control the accuracy of the solver.

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
        """
        return lib.cpSpaceGetIterations(self._space)

    @iterations.setter
    def iterations(self, value: int) -> None:
        lib.cpSpaceSetIterations(self._space, value)

    def _set_gravity(self, gravity_vector: tuple[float, float]) -> None:
        assert len(gravity_vector) == 2
        lib.cpSpaceSetGravity(self._space, gravity_vector)

    def _get_gravity(self) -> Vec2d:
        v = lib.cpSpaceGetGravity(self._space)
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

    @property
    def damping(self) -> float:
        """Amount of simple damping to apply to the space.

        A value of 0.9 means that each body will lose 10% of its velocity per
        second. Defaults to 1. Like gravity, it can be overridden on a per
        body basis.
        """
        return lib.cpSpaceGetDamping(self._space)

    @damping.setter
    def damping(self, damping: float) -> None:
        lib.cpSpaceSetDamping(self._space, damping)

    @property
    def idle_speed_threshold(self) -> float:
        """Speed threshold for a body to be considered idle.

        The default value of 0 means the space estimates a good threshold
        based on gravity.
        """
        return lib.cpSpaceGetIdleSpeedThreshold(self._space)

    @idle_speed_threshold.setter
    def idle_speed_threshold(self, idle_speed_threshold: float) -> None:
        lib.cpSpaceSetIdleSpeedThreshold(self._space, idle_speed_threshold)

    @property
    def sleep_time_threshold(self) -> float:
        """Time a group of bodies must remain idle in order to fall
        asleep.

        The default value of `inf` disables the sleeping algorithm.
        """
        return lib.cpSpaceGetSleepTimeThreshold(self._space)

    @sleep_time_threshold.setter
    def sleep_time_threshold(self, sleep_time_threshold: float) -> None:
        lib.cpSpaceSetSleepTimeThreshold(self._space, sleep_time_threshold)

    @property
    def collision_slop(self) -> float:
        """Amount of overlap between shapes that is allowed.

        To improve stability, set this as high as you can without noticeable
        overlapping. It defaults to 0.1.
        """
        return lib.cpSpaceGetCollisionSlop(self._space)

    @collision_slop.setter
    def collision_slop(self, collision_slop: float) -> None:
        lib.cpSpaceSetCollisionSlop(self._space, collision_slop)

    @property
    def collision_bias(self) -> float:
        """Determines how fast overlapping shapes are pushed apart.

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
        """
        return lib.cpSpaceGetCollisionBias(self._space)

    @collision_bias.setter
    def collision_bias(self, collision_bias: float) -> None:
        lib.cpSpaceSetCollisionBias(self._space, collision_bias)

    @property
    def collision_persistence(self) -> float:
        """The number of frames the space keeps collision solutions
        around for.

        Helps prevent jittering contacts from getting worse. This defaults
        to 3.

        ..Note::
            Very very few games will need to change this value.
        """
        return lib.cpSpaceGetCollisionPersistence(self._space)

    @collision_persistence.setter
    def collision_persistence(self, collision_persistence: float) -> None:
        lib.cpSpaceSetCollisionPersistence(self._space, collision_persistence)

    @property
    def current_time_step(self) -> float:
        """Retrieves the current (if you are in a callback from
        Space.step()) or most recent (outside of a Space.step() call)
        timestep.
        """
        return lib.cpSpaceGetCurrentTimeStep(self._space)

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
        assert shape not in self._shapes, "Shape already added to space."
        assert (
            shape.space == None
        ), "Shape already added to another space. A shape can only be in one space at a time."
        assert shape.body != None, "The shape's body is not set."
        assert (
            shape.body.space == self
        ), "The shape's body must be added to the space before (or at the same time) as the shape."

        shape._space = weakref.ref(self)
        self._shapes[shape] = None
        lib.cpSpaceAddShape(self._space, shape._shape)

    def _add_body(self, body: "Body") -> None:
        """Adds a body to the space"""
        assert body not in self._bodies, "Body already added to this space."
        assert body.space == None, "Body already added to another space."

        body._space = weakref.ref(self)
        self._bodies[body] = None
        self._bodies_to_check.add(body)
        lib.cpSpaceAddBody(self._space, body._body)

    def _add_constraint(self, constraint: "Constraint") -> None:
        """Adds a constraint to the space"""
        assert constraint not in self._constraints, "Constraint already added to space."

        assert (
            constraint.a.body_type == Body.DYNAMIC
            or constraint.b.body_type == Body.DYNAMIC
        ), "At leasts one of a constraint's bodies must be DYNAMIC."

        self._constraints[constraint] = None
        lib.cpSpaceAddConstraint(self._space, constraint._constraint)

    def _remove_shape(self, shape: "Shape") -> None:
        """Removes a shape from the space"""
        assert shape in self._shapes, "shape not in space, already removed?"
        self._removed_shapes[shape] = None
        shape._space = _dead_ref
        # During GC at program exit sometimes the shape might already be removed. Then skip this step.
        if lib.cpSpaceContainsShape(self._space, shape._shape):
            lib.cpSpaceRemoveShape(self._space, shape._shape)
        del self._shapes[shape]

    def _remove_body(self, body: "Body") -> None:
        """Removes a body from the space"""
        assert body in self._bodies, "body not in space, already removed?"
        body._space = _dead_ref
        if body in self._bodies_to_check:
            self._bodies_to_check.remove(body)
        # During GC at program exit sometimes the shape might already be removed. Then skip this step.
        if lib.cpSpaceContainsBody(self._space, body._body):
            lib.cpSpaceRemoveBody(self._space, body._body)
        del self._bodies[body]

    def _remove_constraint(self, constraint: "Constraint") -> None:
        """Removes a constraint from the space"""
        assert (
            constraint in self._constraints
        ), "constraint not in space, already removed?"
        # print("remove", constraint, constraint._constraint, self._constraints)
        # During GC at program exit sometimes the constraint might already be removed. Then skip this steip.
        if lib.cpSpaceContainsConstraint(self._space, constraint._constraint):
            lib.cpSpaceRemoveConstraint(self._space, constraint._constraint)
        del self._constraints[constraint]

    def reindex_shape(self, shape: Shape) -> None:
        """Update the collision detection data for a specific shape in the
        space.
        """
        lib.cpSpaceReindexShape(self._space, shape._shape)

    def reindex_shapes_for_body(self, body: Body) -> None:
        """Reindex all the shapes for a certain body."""
        lib.cpSpaceReindexShapesForBody(self._space, body._body)

    def reindex_static(self) -> None:
        """Update the collision detection info for the static shapes in the
        space. You only need to call this if you move one of the static shapes.
        """
        lib.cpSpaceReindexStatic(self._space)

    @property
    def threads(self) -> int:
        """The number of threads to use for running the step function.

        Only valid when the Space was created with threaded=True. Currently the
        max limit is 2, setting a higher value wont have any effect. The
        default is 1 regardless if the Space was created with threaded=True,
        to keep determinism in the simulation. Note that Windows does not
        support the threaded solver.
        """
        if self.threaded:
            return int(lib.cpHastySpaceGetThreads(self._space))
        return 1

    @threads.setter
    def threads(self, n: int) -> None:
        if self.threaded:
            lib.cpHastySpaceSetThreads(self._space, n)

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

        count is the minimum number of cells in the hash table. If
        there are too few cells, the spatial hash will return many false
        positives. Too many cells will be hard on the cache and waste memory.
        Setting count to ~10x the number of objects in the space is probably a
        good starting point. Tune from there if necessary.

        :param dim: the size of the hash cells
        :param count: the suggested minimum number of cells in the hash table
        """
        lib.cpSpaceUseSpatialHash(self._space, dim, count)

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

        for b in self._bodies_to_check:
            assert b.body_type != Body.DYNAMIC or (
                b.mass > 0 and b.mass < math.inf and b.moment > 0
            ), f"Dynamic bodies must have a mass > 0 and < inf and moment > 0. {b} has mass {b.mass}, moment {b.moment}."
        self._bodies_to_check.clear()

        try:
            self._locked = True
            if self.threaded:
                lib.cpHastySpaceStep(self._space, dt)
            else:
                lib.cpSpaceStep(self._space, dt)
            self._removed_shapes.clear()
        finally:
            self._locked = False
        self.add(*self._add_later)
        self._add_later.clear()
        for obj in self._remove_later:
            self.remove(obj)
        self._remove_later.clear()

        for key in self._post_step_callbacks:
            self._post_step_callbacks[key](self)

        self._post_step_callbacks.clear()

    def on_collision(
        self,
        collision_type_a: Optional[int] = None,
        collision_type_b: Optional[int] = None,
        begin: Optional[_CollisionCallback] = None,
        pre_solve: Optional[_CollisionCallback] = None,
        post_solve: Optional[_CollisionCallback] = None,
        separate: Optional[_CollisionCallback] = None,
        data: Any = None,
    ) -> None:
        """Set callbacks that will be called during the 4 phases of collision
        handling.

        Whenever shapes with collision types (:py:attr:`Shape.collision_type`)
        a and b collide, the callback will be used to process the collision
        events. If no callback is set, the default is to process collision
        normally.

        Its possible to pass in None for one or both of the collision types.
        None matches any collision type on a Shape. However, if
        collision_type_a is None, then collision_type_b must also be None.

        If you call this multiple times with the same combination of
        collision_type_a and collision_type_b, then the last call will
        overwrite the earlier.

        If multiple callbacks match the collision, the order will be that the
        most specific handler is called first.

        Callback phases:

            - **begin**: Two shapes just started touching for the first time
              this step.
            - **pre_solve**: Two shapes are touching during this step, before
              collision resolution. You may override collision values using
              Arbiter.friction, Arbiter.elasticity or Arbiter.surfaceVelocity
              to provide custom friction, elasticity, or surface velocity
              values. See Arbiter for more info.
            - **post_solve**: Two shapes are touching and their collision response
              has been processed. You can retrieve the collision impulse or
              kinetic energy at this time if you want to use it to calculate
              sound volumes or damage amounts. See Arbiter for more info.
            - **separate**: Two shapes have just stopped touching for the
              first time this step. To ensure that begin()/separate() are
              always called in balanced pairs, it will also be called when
              removing a shape while its in contact with something or when
              de-allocating the space.

        From each callback you can set process_collision on the Arbiter,
        which decides if the collision should be processed or not.

        data will be passed in to the callback function unchanged.

        """
        # key = min(collision_type_a, collision_type_b), max(
        #     collision_type_a, collision_type_b
        # )
        assert (
            collision_type_a != None or collision_type_b == None
        ), "collision_type_a can not be None if collision_type_b is not None. Please swap them."

        key = collision_type_a, collision_type_b
        if key not in self._handlers:
            # CP_WILDCARD_COLLISION_TYPE
            wildcard = int(ffi.cast("uintptr_t", ~0))
            if collision_type_a == None:
                collision_type_a = wildcard

            if collision_type_b == None:
                collision_type_b = wildcard

            h = lib.cpSpaceAddCollisionHandler(
                self._space, collision_type_a, collision_type_b
            )
            ch = CollisionHandler(h, self)
            self._handlers[key] = ch
        else:
            ch = self._handlers[key]

        # to avoid circular dep
        from . import empty_callback

        if begin == empty_callback:
            ch.begin = None
        elif begin != None:
            ch.begin = begin
            ch.data["begin"] = data
        if pre_solve == empty_callback:
            ch.pre_solve = None
        elif pre_solve != None:
            ch.pre_solve = pre_solve
            ch.data["pre_solve"] = data
        if post_solve == empty_callback:
            ch.post_solve = None
        elif post_solve != None:
            ch.post_solve = post_solve
            ch.data["post_solve"] = data
        if separate == empty_callback:
            ch.separate = None
        elif separate != None:
            ch.separate = separate
            ch.data["separate"] = data
        return

    def add_post_step_callback(
        self,
        callback_function: Callable[
            ..., None
        ],  # TODO: Fix me once PEP-612 is implemented (py 3.10)
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

        def f(x: "Space") -> None:
            callback_function(self, key, *args, **kwargs)

        self._post_step_callbacks[key] = f
        return True

    def point_query(
        self, point: tuple[float, float], max_distance: float, shape_filter: ShapeFilter
    ) -> list[PointQueryInfo]:
        """Query space at point for shapes within the given distance range.

        The filter is applied to the query and follows the same rules as the
        collision detection. If a maxDistance of 0.0 is used, the point must
        lie inside a shape. Negative max_distance is also allowed meaning that
        the point must be a under a certain depth within a shape to be
        considered a match.

        Sensor shapes are included in the result.

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        :param point: Where to check for collision in the Space
        :type point: :py:class:`~vec2d.Vec2d` or (float,float)
        :param float max_distance: Match only within this distance
        :param ShapeFilter shape_filter: Only pick shapes matching the filter

        :rtype: [:py:class:`PointQueryInfo`]
        """
        assert len(point) == 2
        query_hits: list[PointQueryInfo] = []
        d = (self, query_hits)
        data = ffi.new_handle(d)
        lib.cpSpacePointQuery(
            self._space,
            point,
            max_distance,
            shape_filter,
            lib.ext_cpSpacePointQueryFunc,
            data,
        )
        return query_hits

    def point_query_nearest(
        self, point: tuple[float, float], max_distance: float, shape_filter: ShapeFilter
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
            Sensor shapes are included in the result. (Changed in Pymunk 7.0)

        :param point: Where to check for collision in the Space
        :type point: :py:class:`~vec2d.Vec2d` or (float,float)
        :param float max_distance: Match only within this distance
        :param ShapeFilter shape_filter: Only pick shapes matching the filter

        :rtype: :py:class:`PointQueryInfo` or None
        """
        assert len(point) == 2
        info = ffi.new("cpPointQueryInfo *")
        _shape = lib.cpSpacePointQueryNearest(
            self._space, point, max_distance, shape_filter, info
        )

        shape = Shape._from_cp_shape(_shape)

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
        start: tuple[float, float],
        end: tuple[float, float],
        radius: float,
        shape_filter: ShapeFilter,
    ) -> list[SegmentQueryInfo]:
        """Query space along the line segment from start to end with the
        given radius.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        Sensor shapes are included in the result.

        :param start: Starting point
        :param end: End point
        :param float radius: Radius
        :param ShapeFilter shape_filter: Shape filter

        :rtype: [:py:class:`SegmentQueryInfo`]
        """
        assert len(start) == 2
        assert len(end) == 2
        query_hits: list[SegmentQueryInfo] = []

        d = (self, query_hits)
        data = ffi.new_handle(d)

        lib.cpSpaceSegmentQuery(
            self._space,
            start,
            end,
            radius,
            shape_filter,
            lib.ext_cpSpaceSegmentQueryFunc,
            data,
        )
        return query_hits

    def segment_query_first(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        radius: float,
        shape_filter: ShapeFilter,
    ) -> Optional[SegmentQueryInfo]:
        """Query space along the line segment from start to end with the
        given radius.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        .. Note::
            Sensor shapes are included in the result. (Changed in Pymunk 7.0)

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        :rtype: :py:class:`SegmentQueryInfo` or None
        """
        assert len(start) == 2
        assert len(end) == 2
        info = ffi.new("cpSegmentQueryInfo *")
        _shape = lib.cpSpaceSegmentQueryFirst(
            self._space, start, end, radius, shape_filter, info
        )

        shape = Shape._from_cp_shape(_shape)
        if shape != None:
            return SegmentQueryInfo(
                shape,
                Vec2d(info.point.x, info.point.y),
                Vec2d(info.normal.x, info.normal.y),
                info.alpha,
            )
        return None

    def bb_query(self, bb: "BB", shape_filter: ShapeFilter) -> list[Shape]:
        """Query space to find all shapes near bb.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        Sensor shapes are included in the result

        :param bb: Bounding box
        :param shape_filter: Shape filter

        :rtype: [:py:class:`Shape`]
        """

        query_hits: list[Shape] = []

        d = (self, query_hits)
        data = ffi.new_handle(d)

        lib.cpSpaceBBQuery(
            self._space, bb, shape_filter, lib.ext_cpSpaceBBQueryFunc, data
        )
        return query_hits

    def shape_query(self, shape: Shape) -> list[ShapeQueryInfo]:
        """Query a space for any shapes overlapping the given shape

        Sensor shapes are included in the result

        :param shape: Shape to query with
        :type shape: :py:class:`Circle`, :py:class:`Poly` or :py:class:`Segment`

        :rtype: [:py:class:`ShapeQueryInfo`]
        """

        query_hits: list[ShapeQueryInfo] = []
        d = (self, query_hits)
        data = ffi.new_handle(d)

        lib.cpSpaceShapeQuery(
            self._space, shape._shape, lib.ext_cpSpaceShapeQueryFunc, data
        )

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
            d = (options, self)
            h = ffi.new_handle(d)
            # we need to hold h until the end of cpSpaceDebugDraw to prevent GC
            options._options.data = h

            with options:
                lib.cpSpaceDebugDraw(self._space, options._options)
        else:
            for shape in self.shapes:
                options.draw_shape(shape)

    # def get_batched_bodies(self, shape_filter):
    #     """Return a memoryview for use when the non-batch api is not performant enough.

    #     .. note::
    #         Experimental API. Likely to change in future major, minor or point
    #         releases.
    #     """
    #     pass

    def _get_arbiters(self) -> list[ffi.CData]:
        _arbiters: list[ffi.CData] = []
        data = ffi.new_handle(_arbiters)
        lib.cpSpaceEachCachedArbiter(self._space, lib.ext_cpArbiterIteratorFunc, data)
        return _arbiters

    def __getstate__(self) -> _State:
        """Return the state of this object

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Space, self).__getstate__()

        d["special"].append(("pymunk_version", _version.version))
        # bodies needs to be added to the state before their shapes.
        d["special"].append(("bodies", list(self.bodies)))
        if self._static_body != None:
            # print("getstate", self._static_body)
            d["special"].append(("_static_body", self._static_body))

        d["special"].append(("shapes", list(self.shapes)))
        d["special"].append(("constraints", list(self.constraints)))

        # to avoid circular dep
        from . import empty_callback

        handlers = []
        for k, v in self._handlers.items():
            h: dict[str, Any] = {}
            if v._begin != empty_callback:
                h["_begin"] = v._begin
            if v._pre_solve != empty_callback:
                h["_pre_solve"] = v._pre_solve
            if v._post_solve != empty_callback:
                h["_post_solve"] = v._post_solve
            if v._separate != empty_callback:
                h["_separate"] = v._separate
            handlers.append((k, h))

        d["special"].append(("_handlers", handlers))

        d["special"].append(
            ("shapeIDCounter", lib.cpSpaceGetShapeIDCounter(self._space))
        )
        d["special"].append(("stamp", lib.cpSpaceGetTimestamp(self._space)))
        d["special"].append(
            ("currentTimeStep", lib.cpSpaceGetCurrentTimeStep(self._space))
        )

        _arbs = self._get_arbiters()
        d["special"].append(
            ("arbiters", [_arbiter_to_dict(_arb, self) for _arb in _arbs])
        )
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
                # _ = lib.cpSpaceSetStaticBody(self._space, v._body)
                # v._space = self
                # self._static_body = v
                # print("setstate", v, self._static_body)
                self._static_body = v
                self._setup_static_body(v)
                # self._static_body._space = weakref.proxy(self)
                # lib.cpSpaceAddBody(self._space, v._body)
                # self.add(v)

            elif k == "shapes":
                # print("setstate shapes", v)
                self.add(*v)
            elif k == "constraints":
                self.add(*v)
            elif k == "_handlers":
                for k2, hd in v:
                    begin = pre_solve = post_solve = separate = None
                    if "_begin" in hd:
                        begin = hd["_begin"]
                    if "_pre_solve" in hd:
                        pre_solve = hd["_pre_solve"]
                    if "_post_solve" in hd:
                        post_solve = hd["_post_solve"]
                    if "_separate" in hd:
                        separate = hd["_separate"]
                    if k2 == None:
                        self.on_collision(
                            None,
                            None,
                            begin=begin,
                            pre_solve=pre_solve,
                            post_solve=post_solve,
                            separate=separate,
                        )
                    elif isinstance(k2, tuple):
                        self.on_collision(
                            k2[0],
                            k2[1],
                            begin=begin,
                            pre_solve=pre_solve,
                            post_solve=post_solve,
                            separate=separate,
                        )
                    else:
                        self.on_collision(
                            k2,
                            None,
                            begin=begin,
                            pre_solve=pre_solve,
                            post_solve=post_solve,
                            separate=separate,
                        )

            elif k == "stamp":
                lib.cpSpaceSetTimestamp(self._space, v)
            elif k == "shapeIDCounter":
                lib.cpSpaceSetShapeIDCounter(self._space, v)
            elif k == "currentTimeStep":
                lib.cpSpaceSetCurrentTimeStep(self._space, v)
            elif k == "arbiters":
                for d in v:
                    # lib.cpSpaceTest(self._space)
                    _arbiter = _arbiter_from_dict(d, self)
                    lib.cpSpaceAddCachedArbiter(self._space, _arbiter)
