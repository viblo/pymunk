# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2024 Victor Blomqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------

"""A constraint is something that describes how two bodies interact with
each other. (how they constrain each other). Constraints can be simple
joints that allow bodies to pivot around each other like the bones in your
body, or they can be more abstract like the gear joint or motors.

This submodule contain all the constraints that are supported by Pymunk.

All the constraints support copy and pickle from the standard library. Custom
properties set on a constraint will also be copied/pickled.

Chipmunk has a good overview of the different constraint on youtube which
works fine to showcase them in Pymunk as well.
http://www.youtube.com/watch?v=ZgJJZTS0aMM

.. raw:: html

    <iframe width="420" height="315" style="display: block; margin: 0 auto;"
    src="http://www.youtube.com/embed/ZgJJZTS0aMM" frameborder="0"
    allowfullscreen></iframe>


Example::

>>> import pymunk
>>> import pymunk.constraints
>>> s = pymunk.Space()
>>> a,b = pymunk.Body(10,10), pymunk.Body(10,10)
>>> c = pymunk.constraints.PivotJoint(a, b, (0,0))
>>> s.add(c)

"""
__docformat__ = "reStructuredText"

__all__ = [
    "Constraint",
    "PinJoint",
    "SlideJoint",
    "PivotJoint",
    "GrooveJoint",
    "DampedSpring",
    "DampedRotarySpring",
    "RotaryLimitJoint",
    "RatchetJoint",
    "GearJoint",
    "SimpleMotor",
]

from typing import TYPE_CHECKING, Any, Callable, Optional, Union

if TYPE_CHECKING:
    from .space import Space

from ._chipmunk_cffi import ffi, lib
from ._pickle import PickleMixin
from ._typing_attr import TypingAttrMixing
from .body import Body
from .vec2d import Vec2d

_TorqueFunc = Callable[["DampedRotarySpring", float], float]
_ForceFunc = Callable[["DampedSpring", float], float]


class Constraint(PickleMixin, TypingAttrMixing, object):
    """Base class of all constraints.

    You usually don't want to create instances of this class directly, but
    instead use one of the specific constraints such as the PinJoint.
    """

    _pickle_attrs_init = PickleMixin._pickle_attrs_init + ["a", "b"]
    _pickle_attrs_general = PickleMixin._pickle_attrs_general + [
        "max_force",
        "error_bias",
        "max_bias",
        "collide_bodies",
    ]
    _pickle_attrs_skip = PickleMixin._pickle_attrs_skip + ["pre_solve", "post_solve"]

    _pre_solve_func: Optional[Callable[["Constraint", "Space"], None]] = None
    _post_solve_func: Optional[Callable[["Constraint", "Space"], None]] = None

    _a: "Body"
    _b: "Body"

    def __init__(self, constraint: ffi.CData) -> None:
        self._constraint = constraint

    def _init(self, a: "Body", b: "Body", _constraint: Any) -> None:
        def constraintfree(cp_constraint: ffi.CData) -> None:
            cp_space = lib.cpConstraintGetSpace(cp_constraint)
            if cp_space != ffi.NULL:
                lib.cpSpaceRemoveConstraint(cp_space, cp_constraint)

            lib.cpConstraintFree(cp_constraint)

        self._constraint = ffi.gc(_constraint, constraintfree)
        self._set_bodies(a, b)

        d = ffi.new_handle(self)
        self._data_handle = d  # to prevent gc to collect the handle
        lib.cpConstraintSetUserData(self._constraint, d)

    @property
    def max_force(self) -> float:
        """The maximum force that the constraint can use to act on the two
        bodies.

        Defaults to infinity
        """
        return lib.cpConstraintGetMaxForce(self._constraint)

    @max_force.setter
    def max_force(self, f: float) -> None:
        lib.cpConstraintSetMaxForce(self._constraint, f)

    @property
    def error_bias(self) -> float:
        """The percentage of joint error that remains unfixed after a
        second.

        This works exactly the same as the collision bias property of a space,
        but applies to fixing error (stretching) of joints instead of
        overlapping collisions.

        Defaults to pow(1.0 - 0.1, 60.0) meaning that it will correct 10% of
        the error every 1/60th of a second.
        """
        return lib.cpConstraintGetErrorBias(self._constraint)

    @error_bias.setter
    def error_bias(self, error_bias: float) -> None:
        lib.cpConstraintSetErrorBias(self._constraint, error_bias)

    @property
    def max_bias(self) -> float:
        """The maximum speed at which the constraint can apply error
        correction.

        Defaults to infinity
        """
        return lib.cpConstraintGetMaxBias(self._constraint)

    @max_bias.setter
    def max_bias(self, max_bias: float) -> None:
        lib.cpConstraintSetMaxBias(self._constraint, max_bias)

    @property
    def collide_bodies(self) -> bool:
        """Constraints can be used for filtering collisions too.

        When two bodies collide, Pymunk ignores the collisions if this property
        is set to False on any constraint that connects the two bodies.
        Defaults to True. This can be used to create a chain that self
        collides, but adjacent links in the chain do not collide.
        """
        return lib.cpConstraintGetCollideBodies(self._constraint)

    @collide_bodies.setter
    def collide_bodies(self, collide_bodies: bool) -> None:
        lib.cpConstraintSetCollideBodies(self._constraint, collide_bodies)

    @property
    def impulse(self) -> float:
        """The most recent impulse that constraint applied.

        To convert this to a force, divide by the timestep passed to
        space.step(). You can use this to implement breakable joints to check
        if the force they attempted to apply exceeded a certain threshold.
        """
        return lib.cpConstraintGetImpulse(self._constraint)

    @property
    def a(self) -> "Body":
        """The first of the two bodies constrained"""
        return self._a

    @property
    def b(self) -> "Body":
        """The second of the two bodies constrained"""
        return self._b

    def activate_bodies(self) -> None:
        """Activate the bodies this constraint is attached to"""
        self.a.activate()
        self.b.activate()

    @property
    def pre_solve(self) -> Optional[Callable[["Constraint", "Space"], None]]:
        """The pre-solve function is called before the constraint solver runs.

        Note that None can be used to reset it to default value.

        >>> import pymunk
        >>> j = pymunk.PinJoint(pymunk.Body(1,2), pymunk.Body(3,4), (0,0))
        >>> def pre_solve_func(constraint, space):
        ...     print("Hello from pre-solve")
        >>> j.pre_solve = pre_solve_func
        >>> j.pre_solve = None
        """

        return self._pre_solve_func

    @pre_solve.setter
    def pre_solve(
        self, func: Optional[Callable[["Constraint", "Space"], None]]
    ) -> None:
        self._pre_solve_func = func

        if func is None:
            lib.cpConstraintSetPreSolveFunc(self._constraint, ffi.NULL)
        else:
            lib.cpConstraintSetPreSolveFunc(
                self._constraint, lib.ext_cpConstraintPreSolveFunc
            )

    @property
    def post_solve(self) -> Optional[Callable[["Constraint", "Space"], None]]:
        """The post-solve function is called after the constraint solver runs.

        Note that None can be used to reset it to default value.

        >>> import pymunk
        >>> j = pymunk.PinJoint(pymunk.Body(1,2), pymunk.Body(3,4), (0,0))
        >>> def post_solve_func(constraint, space):
        ...     print("Hello from pre-solve")
        >>> j.post_solve = post_solve_func
        >>> j.post_solve = None
        """
        return self._post_solve_func

    @post_solve.setter
    def post_solve(
        self, func: Optional[Callable[["Constraint", "Space"], None]]
    ) -> None:
        self._post_solve_func = func

        if func is None:
            lib.cpConstraintSetPostSolveFunc(self._constraint, ffi.NULL)
        else:
            lib.cpConstraintSetPostSolveFunc(
                self._constraint, lib.ext_cpConstraintPostSolveFunc
            )

    def _set_bodies(self, a: "Body", b: "Body") -> None:
        assert a is not b
        assert (
            a.body_type == Body.DYNAMIC or b.body_type == Body.DYNAMIC
        ), "At least one of the two bodies attached to a constraint must be DYNAMIC."
        self._a = a
        self._b = b
        a._constraints[self] = None
        b._constraints[self] = None

    def __getstate__(self) -> dict[str, list[tuple[str, Any]]]:
        """Return the state of this object

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        d = super(Constraint, self).__getstate__()

        d["special"].append(("_pre_solve_func", self._pre_solve_func))
        d["special"].append(("_post_solve_func", self._post_solve_func))

        return d

    def __setstate__(self, state: dict[str, list[tuple[str, Any]]]) -> None:
        """Unpack this object from a saved state.

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """
        super(Constraint, self).__setstate__(state)

        for k, v in state["special"]:
            if k == "_pre_solve_func" and v != None:
                self.pre_solve = v
            elif k == "_post_solve_func" and v != None:
                self.post_solve = v


class PinJoint(Constraint):
    """PinJoint links shapes with a solid bar or pin.

    Keeps the anchor points at a set distance from one another.
    """

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["anchor_a", "anchor_b"]

    def __init__(
        self,
        a: "Body",
        b: "Body",
        anchor_a: tuple[float, float] = (0, 0),
        anchor_b: tuple[float, float] = (0, 0),
    ) -> None:
        """a and b are the two bodies to connect, and anchor_a and anchor_b are
        the anchor points on those bodies.

        The distance between the two anchor points is measured when the joint
        is created. If you want to set a specific distance, use the setter
        function to override it.
        """
        assert len(anchor_a) == 2
        assert len(anchor_b) == 2
        _constraint = lib.cpPinJointNew(a._body, b._body, anchor_a, anchor_b)
        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        v = lib.cpPinJointGetAnchorA(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_a(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpPinJointSetAnchorA(self._constraint, anchor)

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        v = lib.cpPinJointGetAnchorB(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_b(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpPinJointSetAnchorB(self._constraint, anchor)

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    @property
    def distance(self) -> float:
        return lib.cpPinJointGetDist(self._constraint)

    @distance.setter
    def distance(self, distance: float) -> None:
        lib.cpPinJointSetDist(self._constraint, distance)


class SlideJoint(Constraint):
    """SlideJoint is like a PinJoint, but have a minimum and maximum distance.

    A chain could be modeled using this joint. It keeps the anchor points
    from getting to far apart, but will allow them to get closer together.
    """

    _pickle_attrs_init = Constraint._pickle_attrs_init + [
        "anchor_a",
        "anchor_b",
        "min",
        "max",
    ]

    def __init__(
        self,
        a: "Body",
        b: "Body",
        anchor_a: tuple[float, float],
        anchor_b: tuple[float, float],
        min: float,
        max: float,
    ) -> None:
        """a and b are the two bodies to connect, anchor_a and anchor_b are the
        anchor points on those bodies, and min and max define the allowed
        distances of the anchor points.
        """
        assert len(anchor_a) == 2
        assert len(anchor_b) == 2
        _constraint = lib.cpSlideJointNew(
            a._body, b._body, anchor_a, anchor_b, min, max
        )
        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        v = lib.cpSlideJointGetAnchorA(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_a(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpSlideJointSetAnchorA(self._constraint, anchor)

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        v = lib.cpSlideJointGetAnchorB(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_b(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpSlideJointSetAnchorB(self._constraint, anchor)

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    @property
    def min(self) -> float:
        return lib.cpSlideJointGetMin(self._constraint)

    @min.setter
    def min(self, min: float) -> None:
        lib.cpSlideJointSetMin(self._constraint, min)

    @property
    def max(self) -> float:
        return lib.cpSlideJointGetMax(self._constraint)

    @max.setter
    def max(self, max: float) -> None:
        lib.cpSlideJointSetMax(self._constraint, max)


class PivotJoint(Constraint):
    """PivotJoint allow two objects to pivot about a single point.

    Its like a swivel.
    """

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["anchor_a", "anchor_b"]

    def __init__(
        self,
        a: "Body",
        b: "Body",
        *args: Union[
            tuple[float, float], tuple[tuple[float, float], tuple[float, float]]
        ],
    ) -> None:
        """a and b are the two bodies to connect, and pivot is the point in
        world coordinates of the pivot.

        Because the pivot location is given in world coordinates, you must
        have the bodies moved into the correct positions already.
        Alternatively you can specify the joint based on a pair of anchor
        points, but make sure you have the bodies in the right place as the
        joint will fix itself as soon as you start simulating the space.

        That is, either create the joint with PivotJoint(a, b, pivot) or
        PivotJoint(a, b, anchor_a, anchor_b).

        :param Body a: The first of the two bodies
        :param Body b: The second of the two bodies
        :param args: Either one pivot point, or two anchor points
        :type args: (float,float) or (float,float) (float,float)
        """
        if len(args) == 1:
            assert len(args[0]) == 2
            _constraint = lib.cpPivotJointNew(a._body, b._body, args[0])
        elif len(args) == 2:
            assert len(args[0]) == 2
            assert len(args[1]) == 2
            _constraint = lib.cpPivotJointNew2(a._body, b._body, args[0], args[1])
        else:
            raise Exception(
                "You must specify either one pivot point" " or two anchor points"
            )

        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        v = lib.cpPivotJointGetAnchorA(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_a(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpPivotJointSetAnchorA(self._constraint, anchor)

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        v = lib.cpPivotJointGetAnchorB(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_b(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpPivotJointSetAnchorB(self._constraint, anchor)

    anchor_b = property(_get_anchor_b, _set_anchor_b)


class GrooveJoint(Constraint):
    """GrooveJoint is similar to a PivotJoint, but with a linear slide.

    One of the anchor points is a line segment that the pivot can slide in instead of being fixed.
    """

    _pickle_attrs_init = Constraint._pickle_attrs_init + [
        "groove_a",
        "groove_b",
        "anchor_b",
    ]

    def __init__(
        self,
        a: "Body",
        b: "Body",
        groove_a: tuple[float, float],
        groove_b: tuple[float, float],
        anchor_b: tuple[float, float],
    ) -> None:
        """The groove goes from groove_a to groove_b on body a, and the pivot
        is attached to anchor_b on body b.

        All coordinates are body local.
        """
        assert len(groove_a) == 2
        assert len(groove_b) == 2
        assert len(anchor_b) == 2
        _constraint = lib.cpGrooveJointNew(
            a._body, b._body, groove_a, groove_b, anchor_b
        )
        self._init(a, b, _constraint)

    def _get_anchor_b(self) -> Vec2d:
        v = lib.cpGrooveJointGetAnchorB(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_b(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpGrooveJointSetAnchorB(self._constraint, anchor)

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_groove_a(self) -> Vec2d:
        v = lib.cpGrooveJointGetGrooveA(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_groove_a(self, groove: tuple[float, float]) -> None:
        assert len(groove) == 2
        lib.cpGrooveJointSetGrooveA(self._constraint, groove)

    groove_a = property(_get_groove_a, _set_groove_a)

    def _get_groove_b(self) -> Vec2d:
        v = lib.cpGrooveJointGetGrooveB(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_groove_b(self, groove: tuple[float, float]) -> None:
        assert len(groove) == 2
        lib.cpGrooveJointSetGrooveB(self._constraint, groove)

    groove_b = property(_get_groove_b, _set_groove_b)


class DampedSpring(Constraint):
    """DampedSpring is a damped spring.

    The spring allows you to define the rest length, stiffness and damping.
    """

    _pickle_attrs_init = Constraint._pickle_attrs_init + [
        "anchor_a",
        "anchor_b",
        "rest_length",
        "stiffness",
        "damping",
    ]

    _pickle_attrs_skip = Constraint._pickle_attrs_skip + ["_force_func"]

    def __init__(
        self,
        a: "Body",
        b: "Body",
        anchor_a: tuple[float, float],
        anchor_b: tuple[float, float],
        rest_length: float,
        stiffness: float,
        damping: float,
    ) -> None:
        """Defined much like a slide joint.

        :param Body a: Body a
        :param Body b: Body b
        :param anchor_a: Anchor point a, relative to body a
        :type anchor_a: `(float,float)`
        :param anchor_b: Anchor point b, relative to body b
        :type anchor_b: `(float,float)`
        :param float rest_length: The distance the spring wants to be.
        :param float stiffness: The spring constant (Young's modulus).
        :param float damping: How soft to make the damping of the spring.
        """
        assert len(anchor_a) == 2
        assert len(anchor_b) == 2
        _constraint = lib.cpDampedSpringNew(
            a._body,
            b._body,
            anchor_a,
            anchor_b,
            rest_length,
            stiffness,
            damping,
        )

        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        v = lib.cpDampedSpringGetAnchorA(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_a(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpDampedSpringSetAnchorA(self._constraint, anchor)

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        v = lib.cpDampedSpringGetAnchorB(self._constraint)
        return Vec2d(v.x, v.y)

    def _set_anchor_b(self, anchor: tuple[float, float]) -> None:
        assert len(anchor) == 2
        lib.cpDampedSpringSetAnchorB(self._constraint, anchor)

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    @property
    def rest_length(self) -> float:
        """The distance the spring wants to be."""
        return lib.cpDampedSpringGetRestLength(self._constraint)

    @rest_length.setter
    def rest_length(self, rest_length: float) -> None:
        lib.cpDampedSpringSetRestLength(self._constraint, rest_length)

    @property
    def stiffness(self) -> float:
        """The spring constant (Young's modulus)."""
        return lib.cpDampedSpringGetStiffness(self._constraint)

    @stiffness.setter
    def stiffness(self, stiffness: float) -> None:
        lib.cpDampedSpringSetStiffness(self._constraint, stiffness)

    @property
    def damping(self) -> float:
        """How soft to make the damping of the spring."""
        return lib.cpDampedSpringGetDamping(self._constraint)

    @damping.setter
    def damping(self, damping: float) -> None:
        lib.cpDampedSpringSetDamping(self._constraint, damping)

    @staticmethod
    def spring_force(spring: "DampedSpring", dist: float) -> float:
        """Default damped spring force function."""
        return lib.defaultSpringForce(spring._constraint, dist)

    def _set_force_func(self, func: _ForceFunc) -> None:
        self._force_func = func
        if func == DampedSpring.spring_force:
            lib.cpDampedSpringSetSpringForceFunc(
                self._constraint,
                ffi.cast(
                    "cpDampedSpringForceFunc", ffi.addressof(lib, "defaultSpringForce")
                ),
            )
        else:
            lib.cpDampedSpringSetSpringForceFunc(
                self._constraint, lib.ext_cpDampedSpringForceFunc
            )

    force_func = property(
        fset=_set_force_func,
        doc="""The force callback function. 
        
        The force callback function is called each time step and is used to
        calculate the force of the spring (exclusing any damping).

        Defaults to :py:func:`DampedSpring.spring_force`
        """,
    )


class DampedRotarySpring(Constraint):
    """DampedRotarySpring works like the DammpedSpring but in a angular fashion."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + [
        "rest_angle",
        "stiffness",
        "damping",
    ]

    _pickle_attrs_skip = Constraint._pickle_attrs_skip + ["_torque_func"]

    _torque_func: Optional[_TorqueFunc] = None

    def __init__(
        self, a: "Body", b: "Body", rest_angle: float, stiffness: float, damping: float
    ) -> None:
        """Like a damped spring, but works in an angular fashion.

        :param Body a: Body a
        :param Body b: Body b
        :param float rest_angle: The relative angle in radians that the bodies
            want to have
        :param float stiffness: The spring constant (Young's modulus).
        :param float damping: How soft to make the damping of the spring.
        """
        _constraint = lib.cpDampedRotarySpringNew(
            a._body, b._body, rest_angle, stiffness, damping
        )
        self._init(a, b, _constraint)

    @property
    def rest_angle(self) -> float:
        """The relative angle in radians that the bodies want to have"""
        return lib.cpDampedRotarySpringGetRestAngle(self._constraint)

    @rest_angle.setter
    def rest_angle(self, rest_angle: float) -> None:
        lib.cpDampedRotarySpringSetRestAngle(self._constraint, rest_angle)

    @property
    def stiffness(self) -> float:
        """The spring constant (Young's modulus)."""
        return lib.cpDampedRotarySpringGetStiffness(self._constraint)

    @stiffness.setter
    def stiffness(self, stiffness: float) -> None:
        lib.cpDampedRotarySpringSetStiffness(self._constraint, stiffness)

    @property
    def damping(self) -> float:
        """How soft to make the damping of the spring."""
        return lib.cpDampedRotarySpringGetDamping(self._constraint)

    @damping.setter
    def damping(self, damping: float) -> None:
        lib.cpDampedRotarySpringSetDamping(self._constraint, damping)

    @staticmethod
    def spring_torque(spring: "DampedRotarySpring", relative_angle: float) -> float:
        """Default damped rotary spring torque function."""
        return lib.defaultSpringTorque(spring._constraint, relative_angle)

    @property
    def torque_func(self) -> _TorqueFunc:
        """The torque callback function.

        The torque callback function is called each time step and is used to
        calculate the torque of the spring (exclusing any damping).

        Defaults to :py:func:`DampedRotarySpring.spring_torque`
        """
        raise AttributeError("unreadable attribute 'torque_func'")

    @torque_func.setter
    def torque_func(self, func: _TorqueFunc) -> None:
        self._torque_func = func
        if func == DampedRotarySpring.spring_torque:
            lib.cpDampedRotarySpringSetSpringTorqueFunc(
                self._constraint,
                ffi.cast(
                    "cpDampedRotarySpringTorqueFunc",
                    ffi.addressof(lib, "defaultSpringTorque"),
                ),
            )
        else:
            lib.cpDampedRotarySpringSetSpringTorqueFunc(
                self._constraint, lib.ext_cpDampedRotarySpringTorqueFunc
            )


class RotaryLimitJoint(Constraint):
    """RotaryLimitJoint constrains the relative rotations of two bodies."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["min", "max"]

    def __init__(self, a: "Body", b: "Body", min: float, max: float) -> None:
        """Constrains the relative rotations of two bodies.

        min and max are the angular limits in radians. It is implemented so
        that it's possible to for the range to be greater than a full
        revolution.
        """
        _constraint = lib.cpRotaryLimitJointNew(a._body, b._body, min, max)
        self._init(a, b, _constraint)

    @property
    def min(self) -> float:
        return lib.cpRotaryLimitJointGetMin(self._constraint)

    @min.setter
    def min(self, min: float) -> None:
        lib.cpRotaryLimitJointSetMin(self._constraint, min)

    @property
    def max(self) -> float:
        return lib.cpRotaryLimitJointGetMax(self._constraint)

    @max.setter
    def max(self, max: float) -> None:
        lib.cpRotaryLimitJointSetMax(self._constraint, max)


class RatchetJoint(Constraint):
    """RatchetJoint is a rotary ratchet, it works like a socket wrench."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["phase", "ratchet"]

    def __init__(self, a: "Body", b: "Body", phase: float, ratchet: float) -> None:
        """Works like a socket wrench.

        ratchet is the distance between "clicks", phase is the initial offset
        to use when deciding where the ratchet angles are.
        """
        _constraint = lib.cpRatchetJointNew(a._body, b._body, phase, ratchet)
        self._init(a, b, _constraint)

    @property
    def angle(self) -> float:
        return lib.cpRatchetJointGetAngle(self._constraint)

    @angle.setter
    def angle(self, angle: float) -> None:
        lib.cpRatchetJointSetAngle(self._constraint, angle)

    @property
    def phase(self) -> float:
        return lib.cpRatchetJointGetPhase(self._constraint)

    @phase.setter
    def phase(self, phase: float) -> None:
        lib.cpRatchetJointSetPhase(self._constraint, phase)

    @property
    def ratchet(self) -> float:
        return lib.cpRatchetJointGetRatchet(self._constraint)

    @ratchet.setter
    def ratchet(self, ratchet: float) -> None:
        lib.cpRatchetJointSetRatchet(self._constraint, ratchet)


class GearJoint(Constraint):
    """GearJoint keeps the angular velocity ratio of a pair of bodies constant."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["phase", "ratio"]

    def __init__(self, a: "Body", b: "Body", phase: float, ratio: float):
        """Keeps the angular velocity ratio of a pair of bodies constant.

        ratio is always measured in absolute terms. It is currently not
        possible to set the ratio in relation to a third body's angular
        velocity. phase is the initial angular offset of the two bodies.
        """
        _constraint = lib.cpGearJointNew(a._body, b._body, phase, ratio)
        self._init(a, b, _constraint)

    @property
    def phase(self) -> float:
        return lib.cpGearJointGetPhase(self._constraint)

    @phase.setter
    def phase(self, phase: float) -> None:
        lib.cpGearJointSetPhase(self._constraint, phase)

    @property
    def ratio(self) -> float:
        return lib.cpGearJointGetRatio(self._constraint)

    @ratio.setter
    def ratio(self, ratio: float) -> None:
        lib.cpGearJointSetRatio(self._constraint, ratio)


class SimpleMotor(Constraint):
    """SimpleMotor keeps the relative angular velocity constant."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["rate"]

    def __init__(self, a: "Body", b: "Body", rate: float) -> None:
        """Keeps the relative angular velocity of a pair of bodies constant.

        rate is the desired relative angular velocity. You will usually want
        to set an force (torque) maximum for motors as otherwise they will be
        able to apply a nearly infinite torque to keep the bodies moving.
        """
        _constraint = lib.cpSimpleMotorNew(a._body, b._body, rate)
        self._init(a, b, _constraint)

    @property
    def rate(self) -> float:
        """The desired relative angular velocity"""
        return lib.cpSimpleMotorGetRate(self._constraint)

    @rate.setter
    def rate(self, rate: float) -> None:
        lib.cpSimpleMotorSetRate(self._constraint, rate)
