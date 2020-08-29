# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2017 Victor Blomqvist
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
>>> s = pymunk.Space()
>>> a,b = pymunk.Body(10,10), pymunk.Body(10,10)
>>> c = pymunk.PivotJoint(a, b, (0,0))
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

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .body import Body

import logging

from . import _chipmunk_cffi
from ._pickle import PickleMixin
from .vec2d import Vec2d

cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi


class Constraint(PickleMixin, object):
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

    def __init__(self, constraint=None):
        self._constraint = constraint

    def _init(self, a: "Body", b: "Body", _constraint: Any) -> None:
        def constraintfree(cp_constraint):
            cp_space = cp.cpConstraintGetSpace(cp_constraint)
            if cp_space != ffi.NULL:
                cp.cpSpaceRemoveConstraint(cp_space, cp_constraint)

            logging.debug("constraintfree %s", cp_constraint)
            cp.cpConstraintFree(cp_constraint)

        self._constraint = ffi.gc(_constraint, constraintfree)
        self._set_bodies(a, b)

    def __xdel__(self) -> None:
        # print("del", self._constraint)
        cp.cpConstraintFree(self._constraint)

    def _get_max_force(self):
        return cp.cpConstraintGetMaxForce(self._constraint)

    def _set_max_force(self, f):
        cp.cpConstraintSetMaxForce(self._constraint, f)

    max_force = property(
        _get_max_force,
        _set_max_force,
        doc="""The maximum force that the constraint can use to act on the two
        bodies.

        Defaults to infinity
        """,
    )

    def _get_error_bias(self) -> float:
        return cp.cpConstraintGetErrorBias(self._constraint)

    def _set_error_bias(self, error_bias: float) -> None:
        cp.cpConstraintSetErrorBias(self._constraint, error_bias)

    error_bias = property(
        _get_error_bias,
        _set_error_bias,
        doc="""The percentage of joint error that remains unfixed after a
        second.

        This works exactly the same as the collision bias property of a space,
        but applies to fixing error (stretching) of joints instead of
        overlapping collisions.

        Defaults to pow(1.0 - 0.1, 60.0) meaning that it will correct 10% of
        the error every 1/60th of a second.
        """,
    )

    def _get_max_bias(self) -> float:
        return cp.cpConstraintGetMaxBias(self._constraint)

    def _set_max_bias(self, max_bias: float) -> None:
        cp.cpConstraintSetMaxBias(self._constraint, max_bias)

    max_bias = property(
        _get_max_bias,
        _set_max_bias,
        doc="""The maximum speed at which the constraint can apply error
        correction.

        Defaults to infinity
        """,
    )

    def _get_collide_bodies(self):
        return cp.cpConstraintGetCollideBodies(self._constraint)

    def _set_collide_bodies(self, collide_bodies):
        cp.cpConstraintSetCollideBodies(self._constraint, collide_bodies)

    collide_bodies = property(
        _get_collide_bodies,
        _set_collide_bodies,
        doc="""Constraints can be used for filtering collisions too.

        When two bodies collide, Pymunk ignores the collisions if this property
        is set to False on any constraint that connects the two bodies.
        Defaults to True. This can be used to create a chain that self
        collides, but adjacent links in the chain do not collide.
        """,
    )

    @property
    def impulse(self) -> float:
        """The most recent impulse that constraint applied.

        To convert this to a force, divide by the timestep passed to
        space.step(). You can use this to implement breakable joints to check
        if the force they attempted to apply exceeded a certain threshold.
        """
        return cp.cpConstraintGetImpulse(self._constraint)

    a = property(
        lambda self: self._a, doc="""The first of the two bodies constrained"""
    )
    b = property(
        lambda self: self._b, doc="""The second of the two bodies constrained"""
    )

    def activate_bodies(self) -> None:
        """Activate the bodies this constraint is attached to"""
        self._a.activate()
        self._b.activate()

    def _set_bodies(self, a: "Body", b: "Body") -> None:
        assert a is not b
        self._a = a
        self._b = b
        a._constraints.add(self)
        b._constraints.add(self)


class PinJoint(Constraint):
    """PinJoint links shapes with a solid bar or pin.

    Keeps the anchor points at a set distance from one another.
    """

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["anchor_a", "anchor_b"]

    def __init__(self, a: "Body", b: "Body", anchor_a=(0, 0), anchor_b=(0, 0)) -> None:
        """a and b are the two bodies to connect, and anchor_a and anchor_b are
        the anchor points on those bodies.

        The distance between the two anchor points is measured when the joint
        is created. If you want to set a specific distance, use the setter
        function to override it.
        """

        _constraint = cp.cpPinJointNew(
            a._body, b._body, tuple(anchor_a), tuple(anchor_b)
        )
        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpPinJointGetAnchorA(self._constraint))

    def _set_anchor_a(self, anchor):
        cp.cpPinJointSetAnchorA(self._constraint, tuple(anchor))

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpPinJointGetAnchorB(self._constraint))

    def _set_anchor_b(self, anchor):
        cp.cpPinJointSetAnchorB(self._constraint, tuple(anchor))

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_distance(self) -> float:
        return cp.cpPinJointGetDist(self._constraint)

    def _set_distance(self, distance: float) -> None:
        cp.cpPinJointSetDist(self._constraint, distance)

    distance = property(_get_distance, _set_distance)


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
        self, a: "Body", b: "Body", anchor_a, anchor_b, min: float, max: float
    ):
        """a and b are the two bodies to connect, anchor_a and anchor_b are the
        anchor points on those bodies, and min and max define the allowed
        distances of the anchor points.
        """

        _constraint = cp.cpSlideJointNew(
            a._body, b._body, tuple(anchor_a), tuple(anchor_b), min, max
        )
        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpSlideJointGetAnchorA(self._constraint))

    def _set_anchor_a(self, anchor):
        cp.cpSlideJointSetAnchorA(self._constraint, tuple(anchor))

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpSlideJointGetAnchorB(self._constraint))

    def _set_anchor_b(self, anchor):
        cp.cpSlideJointSetAnchorB(self._constraint, tuple(anchor))

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_min(self) -> float:
        return cp.cpSlideJointGetMin(self._constraint)

    def _set_min(self, min: float) -> None:
        cp.cpSlideJointSetMin(self._constraint, min)

    min = property(_get_min, _set_min)

    def _get_max(self) -> float:
        return cp.cpSlideJointGetMax(self._constraint)

    def _set_max(self, max: float) -> None:
        cp.cpSlideJointSetMax(self._constraint, max)

    max = property(_get_max, _set_max)


class PivotJoint(Constraint):
    """PivotJoint allow two objects to pivot about a single point.

    Its like a swivel.
    """

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["anchor_a", "anchor_b"]

    def __init__(self, a: "Body", b: "Body", *args) -> None:
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
            _constraint = cp.cpPivotJointNew(a._body, b._body, tuple(args[0]))
        elif len(args) == 2:
            _constraint = cp.cpPivotJointNew2(
                a._body, b._body, tuple(args[0]), tuple(args[1])
            )
        else:
            raise Exception(
                "You must specify either one pivot point" " or two anchor points"
            )

        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpPivotJointGetAnchorA(self._constraint))

    def _set_anchor_a(self, anchor) -> None:
        cp.cpPivotJointSetAnchorA(self._constraint, tuple(anchor))

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpPivotJointGetAnchorB(self._constraint))

    def _set_anchor_b(self, anchor) -> None:
        cp.cpPivotJointSetAnchorB(self._constraint, tuple(anchor))

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

    def __init__(self, a: "Body", b: "Body", groove_a, groove_b, anchor_b) -> None:
        """The groove goes from groove_a to groove_b on body a, and the pivot
        is attached to anchor_b on body b.

        All coordinates are body local.
        """
        _constraint = cp.cpGrooveJointNew(
            a._body, b._body, tuple(groove_a), tuple(groove_b), tuple(anchor_b)
        )
        self._init(a, b, _constraint)

    def _get_anchor_b(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpGrooveJointGetAnchorB(self._constraint))

    def _set_anchor_b(self, anchor) -> None:
        cp.cpGrooveJointSetAnchorB(self._constraint, tuple(anchor))

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_groove_a(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpGrooveJointGetGrooveA(self._constraint))

    def _set_groove_a(self, groove) -> None:
        cp.cpGrooveJointSetGrooveA(self._constraint, tuple(groove))

    groove_a = property(_get_groove_a, _set_groove_a)

    def _get_groove_b(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpGrooveJointGetGrooveB(self._constraint))

    def _set_groove_b(self, groove) -> None:
        cp.cpGrooveJointSetGrooveB(self._constraint, tuple(groove))

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

    def __init__(
        self,
        a: "Body",
        b: "Body",
        anchor_a,
        anchor_b,
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
        _constraint = cp.cpDampedSpringNew(
            a._body,
            b._body,
            tuple(anchor_a),
            tuple(anchor_b),
            rest_length,
            stiffness,
            damping,
        )

        self._init(a, b, _constraint)

    def _get_anchor_a(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpDampedSpringGetAnchorA(self._constraint))

    def _set_anchor_a(self, anchor) -> None:
        cp.cpDampedSpringSetAnchorA(self._constraint, tuple(anchor))

    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self) -> Vec2d:
        return Vec2d._fromcffi(cp.cpDampedSpringGetAnchorB(self._constraint))

    def _set_anchor_b(self, anchor) -> None:
        cp.cpDampedSpringSetAnchorB(self._constraint, tuple(anchor))

    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_rest_length(self) -> float:
        return cp.cpDampedSpringGetRestLength(self._constraint)

    def _set_rest_length(self, rest_length: float) -> None:
        cp.cpDampedSpringSetRestLength(self._constraint, rest_length)

    rest_length = property(
        _get_rest_length,
        _set_rest_length,
        doc="""The distance the spring wants to be.""",
    )

    def _get_stiffness(self) -> float:
        return cp.cpDampedSpringGetStiffness(self._constraint)

    def _set_stiffness(self, stiffness: float) -> None:
        cp.cpDampedSpringSetStiffness(self._constraint, stiffness)

    stiffness = property(
        _get_stiffness, _set_stiffness, doc="""The spring constant (Young's modulus)."""
    )

    def _get_damping(self) -> float:
        return cp.cpDampedSpringGetDamping(self._constraint)

    def _set_damping(self, damping: float) -> None:
        cp.cpDampedSpringSetDamping(self._constraint, damping)

    damping = property(
        _get_damping,
        _set_damping,
        doc="""How soft to make the damping of the spring.""",
    )


class DampedRotarySpring(Constraint):
    """DampedRotarySpring works like the DammpedSpring but in a angular fashion."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + [
        "rest_angle",
        "stiffness",
        "damping",
    ]

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
        _constraint = cp.cpDampedRotarySpringNew(
            a._body, b._body, rest_angle, stiffness, damping
        )
        self._init(a, b, _constraint)

    def _get_rest_angle(self) -> float:
        return cp.cpDampedRotarySpringGetRestAngle(self._constraint)

    def _set_rest_angle(self, rest_angle: float) -> None:
        cp.cpDampedRotarySpringSetRestAngle(self._constraint, rest_angle)

    rest_angle = property(
        _get_rest_angle,
        _set_rest_angle,
        doc="""The relative angle in radians that the bodies want to have""",
    )

    def _get_stiffness(self) -> float:
        return cp.cpDampedRotarySpringGetStiffness(self._constraint)

    def _set_stiffness(self, stiffness: float) -> None:
        cp.cpDampedRotarySpringSetStiffness(self._constraint, stiffness)

    stiffness = property(
        _get_stiffness, _set_stiffness, doc="""The spring constant (Young's modulus)."""
    )

    def _get_damping(self) -> float:
        return cp.cpDampedRotarySpringGetDamping(self._constraint)

    def _set_damping(self, damping: float) -> None:
        cp.cpDampedRotarySpringSetDamping(self._constraint, damping)

    damping = property(
        _get_damping,
        _set_damping,
        doc="""How soft to make the damping of the spring.""",
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
        _constraint = cp.cpRotaryLimitJointNew(a._body, b._body, min, max)
        self._init(a, b, _constraint)

    def _get_min(self) -> float:
        return cp.cpRotaryLimitJointGetMin(self._constraint)

    def _set_min(self, min: float) -> None:
        cp.cpRotaryLimitJointSetMin(self._constraint, min)

    min = property(_get_min, _set_min)

    def _get_max(self) -> float:
        return cp.cpRotaryLimitJointGetMax(self._constraint)

    def _set_max(self, max: float) -> None:
        cp.cpRotaryLimitJointSetMax(self._constraint, max)

    max = property(_get_max, _set_max)


class RatchetJoint(Constraint):
    """RatchetJoint is a rotary ratchet, it works like a socket wrench."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["phase", "ratchet"]

    def __init__(self, a: "Body", b: "Body", phase: float, ratchet: float) -> None:
        """Works like a socket wrench.

        ratchet is the distance between "clicks", phase is the initial offset
        to use when deciding where the ratchet angles are.
        """
        _constraint = cp.cpRatchetJointNew(a._body, b._body, phase, ratchet)
        self._init(a, b, _constraint)

    def _get_angle(self) -> float:
        return cp.cpRatchetJointGetAngle(self._constraint)

    def _set_angle(self, angle: float) -> None:
        cp.cpRatchetJointSetAngle(self._constraint, angle)

    angle = property(_get_angle, _set_angle)

    def _get_phase(self) -> float:
        return cp.cpRatchetJointGetPhase(self._constraint)

    def _set_phase(self, phase: float) -> None:
        cp.cpRatchetJointSetPhase(self._constraint, phase)

    phase = property(_get_phase, _set_phase)

    def _get_ratchet(self) -> float:
        return cp.cpRatchetJointGetRatchet(self._constraint)

    def _set_ratchet(self, ratchet: float) -> None:
        cp.cpRatchetJointSetRatchet(self._constraint, ratchet)

    ratchet = property(_get_ratchet, _set_ratchet)


class GearJoint(Constraint):
    """GearJoint keeps the angular velocity ratio of a pair of bodies constant."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["phase", "ratio"]

    def __init__(self, a: "Body", b: "Body", phase: float, ratio: float):
        """Keeps the angular velocity ratio of a pair of bodies constant.

        ratio is always measured in absolute terms. It is currently not
        possible to set the ratio in relation to a third body's angular
        velocity. phase is the initial angular offset of the two bodies.
        """
        _constraint = cp.cpGearJointNew(a._body, b._body, phase, ratio)
        self._init(a, b, _constraint)

    def _get_phase(self) -> float:
        return cp.cpGearJointGetPhase(self._constraint)

    def _set_phase(self, phase: float) -> None:
        cp.cpGearJointSetPhase(self._constraint, phase)

    phase = property(_get_phase, _set_phase)

    def _get_ratio(self) -> float:
        return cp.cpGearJointGetRatio(self._constraint)

    def _set_ratio(self, ratio: float) -> None:
        cp.cpGearJointSetRatio(self._constraint, ratio)

    ratio = property(_get_ratio, _set_ratio)


class SimpleMotor(Constraint):
    """SimpleMotor keeps the relative angular velocity constant."""

    _pickle_attrs_init = Constraint._pickle_attrs_init + ["rate"]

    def __init__(self, a: "Body", b: "Body", rate: float) -> None:
        """Keeps the relative angular velocity of a pair of bodies constant.

        rate is the desired relative angular velocity. You will usually want
        to set an force (torque) maximum for motors as otherwise they will be
        able to apply a nearly infinite torque to keep the bodies moving.
        """
        _constraint = cp.cpSimpleMotorNew(a._body, b._body, rate)
        self._init(a, b, _constraint)

    def _get_rate(self) -> float:
        return cp.cpSimpleMotorGetRate(self._constraint)

    def _set_rate(self, rate: float) -> None:
        cp.cpSimpleMotorSetRate(self._constraint, rate)

    rate = property(
        _get_rate, _set_rate, doc="""The desired relative angular velocity"""
    )
