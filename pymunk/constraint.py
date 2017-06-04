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
    "Constraint", "PinJoint", "SlideJoint", "PivotJoint", "GrooveJoint",
    "DampedSpring", "DampedRotarySpring", "RotaryLimitJoint", "RatchetJoint",
    "GearJoint", "SimpleMotor"
    ]

import copy

from .vec2d import Vec2d
from ._pickle import PickleMixin

from . import _chipmunk_cffi
cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi

class Constraint(PickleMixin, object):
    """Base class of all constraints.

    You usually don't want to create instances of this class directly, but
    instead use one of the specific constraints such as the PinJoint.
    """

    _pickle_attrs_init = ['a', 'b']
    _pickle_attrs_general = ['max_force', 'error_bias', 'max_bias', 
        'collide_bodies']

    def __init__(self, constraint=None):
        self._constraint = constraint
        
    def _get_max_force(self):
        return cp.cpConstraintGetMaxForce(self._constraint)
    def _set_max_force(self, f):
        cp.cpConstraintSetMaxForce(self._constraint, f)
    max_force = property(_get_max_force, _set_max_force,
        doc="""The maximum force that the constraint can use to act on the two
        bodies.

        Defaults to infinity
        """)

    def _get_error_bias(self):
        return cp.cpConstraintGetErrorBias(self._constraint)
    def _set_error_bias(self, error_bias):
        cp.cpConstraintSetErrorBias(self._constraint, error_bias)
    error_bias = property(_get_error_bias, _set_error_bias,
        doc="""The percentage of joint error that remains unfixed after a
        second.

        This works exactly the same as the collision bias property of a space,
        but applies to fixing error (stretching) of joints instead of
        overlapping collisions.

        Defaults to pow(1.0 - 0.1, 60.0) meaning that it will correct 10% of
        the error every 1/60th of a second.
        """)

    def _get_max_bias(self):
        return cp.cpConstraintGetMaxBias(self._constraint)
    def _set_max_bias(self, max_bias):
        cp.cpConstraintSetMaxBias(self._constraint, max_bias)
    max_bias = property(_get_max_bias, _set_max_bias,
        doc="""The maximum speed at which the constraint can apply error
        correction.

        Defaults to infinity
        """)

    def _get_collide_bodies(self):
        return cp.cpConstraintGetCollideBodies(self._constraint)
    def _set_collide_bodies(self, collide_bodies):
        cp.cpConstraintSetCollideBodies(self._constraint, collide_bodies)
    collide_bodies = property(_get_collide_bodies, _set_collide_bodies,
        doc="""Constraints can be used for filtering collisions too.

        When two bodies collide, Pymunk ignores the collisions if this property
        is set to False on any constraint that connects the two bodies.
        Defaults to True. This can be used to create a chain that self
        collides, but adjacent links in the chain do not collide.
        """)

    def _get_impulse(self):
        return cp.cpConstraintGetImpulse(self._constraint)
    impulse = property(_get_impulse,
        doc="""The most recent impulse that constraint applied.

        To convert this to a force, divide by the timestep passed to
        space.step(). You can use this to implement breakable joints to check
        if the force they attempted to apply exceeded a certain threshold.
        """)

    a = property(lambda self: self._a,
        doc="""The first of the two bodies constrained""")
    b = property(lambda self: self._b,
        doc="""The second of the two bodies constrained""")

    def activate_bodies(self):
        """Activate the bodies this constraint is attached to"""
        self._a.activate()
        self._b.activate()

    def _set_bodies(self, a, b):
        self._a = a
        self._b = b
        a._constraints.add(self)
        b._constraints.add(self)
    
    def copy(self):
        """Create a deep copy of this constraint."""
        return copy.deepcopy(self)


    
class PinJoint(Constraint):
    """Keeps the anchor points at a set distance from one another."""

    _pickle_attrs_init = ['anchor_a', 'anchor_b']

    def __init__(self, a, b, anchor_a=(0,0), anchor_b=(0,0)):
        """a and b are the two bodies to connect, and anchor_a and anchor_b are
        the anchor points on those bodies.

        The distance between the two anchor points is measured when the joint
        is created. If you want to set a specific distance, use the setter
        function to override it.
        """

        self._constraint = ffi.gc(
            cp.cpPinJointNew(
                a._body, b._body, 
                tuple(anchor_a), tuple(anchor_b)), 
            cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_anchor_a(self):
        return Vec2d._fromcffi(cp.cpPinJointGetAnchorA(self._constraint))
    def _set_anchor_a(self, anchor):
        cp.cpPinJointSetAnchorA(self._constraint, tuple(anchor))
    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self):
        return Vec2d._fromcffi(cp.cpPinJointGetAnchorB(self._constraint))
    def _set_anchor_b(self, anchor):
        cp.cpPinJointSetAnchorB(self._constraint, tuple(anchor))
    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_distance(self):
        return cp.cpPinJointGetDist(self._constraint)
    def _set_distance(self, distance):
        cp.cpPinJointSetDist(self._constraint, distance)
    distance = property(_get_distance, _set_distance)

class SlideJoint(Constraint):
    """Like pin joints, but have a minimum and maximum distance.
    A chain could be modeled using this joint. It keeps the anchor points
    from getting to far apart, but will allow them to get closer together.
    """

    _pickle_attrs_init = ['anchor_a', 'anchor_b', 'min', 'max']

    def __init__(self, a, b, anchor_a, anchor_b, min, max):
        """a and b are the two bodies to connect, anchor_a and anchor_b are the
        anchor points on those bodies, and min and max define the allowed
        distances of the anchor points.
        """
        self._constraint = ffi.gc(
            cp.cpSlideJointNew(a._body, b._body, 
                tuple(anchor_a), tuple(anchor_b), min, max), 
            cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_anchor_a(self):
        return Vec2d._fromcffi(cp.cpSlideJointGetAnchorA(self._constraint))
    def _set_anchor_a(self, anchor):
        cp.cpSlideJointSetAnchorA(self._constraint, tuple(anchor))
    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self):
        return Vec2d._fromcffi(cp.cpSlideJointGetAnchorB(self._constraint))
    def _set_anchor_b(self, anchor):
        cp.cpSlideJointSetAnchorB(self._constraint, tuple(anchor))
    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_min(self):
        return cp.cpSlideJointGetMin(self._constraint)
    def _set_min(self, min):
        cp.cpSlideJointSetMin(self._constraint, min)
    min = property(_get_min, _set_min)

    def _get_max(self):
        return cp.cpSlideJointGetMax(self._constraint)
    def _set_max(self, max):
        cp.cpSlideJointSetMax(self._constraint, max)
    max = property(_get_max, _set_max)

class PivotJoint(Constraint):
    """Simply allow two objects to pivot about a single point."""

    _pickle_attrs_init = ['anchor_a', 'anchor_b']

    def __init__(self, a, b, *args):
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
            self._constraint = ffi.gc(
                cp.cpPivotJointNew(a._body, b._body, tuple(args[0])), 
                cp.cpConstraintFree)
        elif len(args) == 2:
            self._constraint = ffi.gc(
                cp.cpPivotJointNew2(
                    a._body, b._body, tuple(args[0]), tuple(args[1])), 
                cp.cpConstraintFree)
        else:
            raise Exception("You must specify either one pivot point"
                " or two anchor points")

        self._set_bodies(a,b)

    def _get_anchor_a(self):
        return Vec2d._fromcffi(cp.cpPivotJointGetAnchorA(self._constraint))
    def _set_anchor_a(self, anchor):
        cp.cpPivotJointSetAnchorA(self._constraint, tuple(anchor))
    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self):
        return Vec2d._fromcffi(cp.cpPivotJointGetAnchorB(self._constraint))
    def _set_anchor_b(self, anchor):
        cp.cpPivotJointSetAnchorB(self._constraint, tuple(anchor))
    anchor_b = property(_get_anchor_b, _set_anchor_b)

class GrooveJoint(Constraint):
    """Similar to a pivot joint, but one of the anchors is
    on a linear slide instead of being fixed.
    """

    _pickle_attrs_init = ['groove_a', 'groove_b', 'anchor_b']

    def __init__(self, a, b, groove_a, groove_b, anchor_b):
        """The groove goes from groove_a to groove_b on body a, and the pivot
        is attached to anchor_b on body b.

        All coordinates are body local.
        """
        self._constraint = ffi.gc(
            cp.cpGrooveJointNew(
                a._body, b._body, 
                tuple(groove_a), tuple(groove_b), 
                tuple(anchor_b)), 
            cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_anchor_b(self):
        return Vec2d._fromcffi(cp.cpGrooveJointGetAnchorB(self._constraint))
    def _set_anchor_b(self, anchor):
        cp.cpGrooveJointSetAnchorB(self._constraint, tuple(anchor))
    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_groove_a(self):
        return Vec2d._fromcffi(cp.cpGrooveJointGetGrooveA(self._constraint))
    def _set_groove_a(self, groove):
        cp.cpGrooveJointSetGrooveA(self._constraint, tuple(groove))
    groove_a = property(_get_groove_a, _set_groove_a)

    def _get_groove_b(self):
        return Vec2d._fromcffi(cp.cpGrooveJointGetGrooveB(self._constraint))
    def _set_groove_b(self, groove):
        cp.cpGrooveJointSetGrooveB(self._constraint, tuple(groove))
    groove_b = property(_get_groove_b, _set_groove_b)

class DampedSpring(Constraint):
    """A damped spring"""

    _pickle_attrs_init = ['anchor_a', 'anchor_b', 'rest_length', 'stiffness', 
        'damping']

    def __init__(self, a, b, anchor_a, anchor_b, rest_length, stiffness, damping):
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
        c = cp.cpDampedSpringNew(
            a._body, b._body,
            tuple(anchor_a), tuple(anchor_b), 
            rest_length, stiffness, damping)
        self._constraint = ffi.gc(c, cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_anchor_a(self):
        return Vec2d._fromcffi(cp.cpDampedSpringGetAnchorA(self._constraint))
    def _set_anchor_a(self, anchor):
        cp.cpDampedSpringSetAnchorA(self._constraint, tuple(anchor))
    anchor_a = property(_get_anchor_a, _set_anchor_a)

    def _get_anchor_b(self):
        return Vec2d._fromcffi(cp.cpDampedSpringGetAnchorB(self._constraint))
    def _set_anchor_b(self, anchor):
        cp.cpDampedSpringSetAnchorB(self._constraint, tuple(anchor))
    anchor_b = property(_get_anchor_b, _set_anchor_b)

    def _get_rest_length(self):
        return cp.cpDampedSpringGetRestLength(self._constraint)
    def _set_rest_length(self, rest_length):
        cp.cpDampedSpringSetRestLength(self._constraint, rest_length)
    rest_length = property(_get_rest_length, _set_rest_length,
        doc="""The distance the spring wants to be.""")

    def _get_stiffness(self):
        return cp.cpDampedSpringGetStiffness(self._constraint)
    def _set_stiffness(self, stiffness):
        cp.cpDampedSpringSetStiffness(self._constraint, stiffness)
    stiffness = property(_get_stiffness, _set_stiffness,
        doc="""The spring constant (Young's modulus).""")

    def _get_damping(self):
        return cp.cpDampedSpringGetDamping(self._constraint)
    def _set_damping(self, damping):
        cp.cpDampedSpringSetDamping(self._constraint, damping)
    damping = property(_get_damping, _set_damping,
        doc="""How soft to make the damping of the spring.""")

class DampedRotarySpring(Constraint):
    """Like a damped spring, but works in an angular fashion"""

    _pickle_attrs_init = ['rest_angle', 'stiffness', 'damping']

    def __init__(self, a, b, rest_angle, stiffness, damping):
        """Like a damped spring, but works in an angular fashion.

        :param Body a: Body a
        :param Body b: Body b
        :param float rest_angle: The relative angle in radians that the bodies 
            want to have
        :param float stiffness: The spring constant (Young's modulus).
        :param float damping: How soft to make the damping of the spring.
        """
        c = cp.cpDampedRotarySpringNew(a._body, b._body, 
            rest_angle, stiffness, damping)
        self._constraint = ffi.gc(c, cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_rest_angle(self):
        return cp.cpDampedRotarySpringGetRestAngle(self._constraint)
    def _set_rest_angle(self, rest_angle):
        cp.cpDampedRotarySpringSetRestAngle(self._constraint, rest_angle)
    rest_angle = property(_get_rest_angle, _set_rest_angle,
        doc="""The relative angle in radians that the bodies want to have""")

    def _get_stiffness(self):
        return cp.cpDampedRotarySpringGetStiffness(self._constraint)
    def _set_stiffness(self, stiffness):
        cp.cpDampedRotarySpringSetStiffness(self._constraint, stiffness)
    stiffness = property(_get_stiffness, _set_stiffness,
        doc="""The spring constant (Young's modulus).""")

    def _get_damping(self):
        return cp.cpDampedRotarySpringGetDamping(self._constraint)
    def _set_damping(self, damping):
        cp.cpDampedRotarySpringSetDamping(self._constraint, damping)
    damping = property(_get_damping, _set_damping,
        doc="""How soft to make the damping of the spring.""")


class RotaryLimitJoint(Constraint):
    """Constrains the relative rotations of two bodies."""

    _pickle_attrs_init = ['min', 'max']

    def __init__(self, a, b, min, max):
        """Constrains the relative rotations of two bodies.

        min and max are the angular limits in radians. It is implemented so
        that it's possible to for the range to be greater than a full
        revolution.
        """
        self._constraint = ffi.gc(
            cp.cpRotaryLimitJointNew(a._body, b._body, min, max), 
            cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_min(self):
        return cp.cpRotaryLimitJointGetMin(self._constraint)
    def _set_min(self, min):
        cp.cpRotaryLimitJointSetMin(self._constraint, min)
    min = property(_get_min, _set_min)

    def _get_max(self):
        return cp.cpRotaryLimitJointGetMax(self._constraint)
    def _set_max(self, max):
        cp.cpRotaryLimitJointSetMax(self._constraint, max)
    max = property(_get_max, _set_max)

class RatchetJoint(Constraint):
    """Works like a socket wrench."""

    _pickle_attrs_init = ['phase', 'ratchet']

    def __init__(self, a, b, phase, ratchet):
        """Works like a socket wrench.

        ratchet is the distance between "clicks", phase is the initial offset
        to use when deciding where the ratchet angles are.
        """
        self._constraint = ffi.gc(
            cp.cpRatchetJointNew(a._body, b._body, phase, ratchet), 
            cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_angle(self):
        return cp.cpRatchetJointGetAngle(self._constraint)
    def _set_angle(self, angle):
        cp.cpRatchetJointSetAngle(self._constraint, angle)
    angle = property(_get_angle, _set_angle)

    def _get_phase(self):
        return cp.cpRatchetJointGetPhase(self._constraint)
    def _set_phase(self, phase):
        cp.cpRatchetJointSetPhase(self._constraint, phase)
    phase = property(_get_phase, _set_phase)

    def _get_ratchet(self):
        return cp.cpRatchetJointGetRatchet(self._constraint)
    def _set_ratchet(self, ratchet):
        cp.cpRatchetJointSetRatchet(self._constraint, ratchet)
    ratchet = property(_get_ratchet, _set_ratchet)

class GearJoint(Constraint):
    """Keeps the angular velocity ratio of a pair of bodies constant."""

    _pickle_attrs_init = ['phase', 'ratio']

    def __init__(self, a, b, phase, ratio):
        """Keeps the angular velocity ratio of a pair of bodies constant.

        ratio is always measured in absolute terms. It is currently not
        possible to set the ratio in relation to a third body's angular
        velocity. phase is the initial angular offset of the two bodies.
        """
        self._constraint = ffi.gc(
            cp.cpGearJointNew(a._body, b._body, phase, ratio), 
            cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_phase(self):
        return cp.cpGearJointGetPhase(self._constraint)
    def _set_phase(self, phase):
        cp.cpGearJointSetPhase(self._constraint, phase)
    phase = property(_get_phase, _set_phase)

    def _get_ratio(self):
        return cp.cpGearJointGetRatio(self._constraint)
    def _set_ratio(self, ratio):
        cp.cpGearJointSetRatio(self._constraint, ratio)
    ratio = property(_get_ratio, _set_ratio)

class SimpleMotor(Constraint):
    """Keeps the relative angular velocity of a pair of bodies constant."""

    _pickle_attrs_init = ['rate']

    def __init__(self, a, b, rate):
        """Keeps the relative angular velocity of a pair of bodies constant.

        rate is the desired relative angular velocity. You will usually want
        to set an force (torque) maximum for motors as otherwise they will be
        able to apply a nearly infinite torque to keep the bodies moving.
        """
        self._constraint = ffi.gc(
            cp.cpSimpleMotorNew(a._body, b._body, rate), 
            cp.cpConstraintFree)
        self._set_bodies(a,b)

    def _get_rate(self):
        return cp.cpSimpleMotorGetRate(self._constraint)
    def _set_rate(self, rate):
        cp.cpSimpleMotorSetRate(self._constraint, rate)
    rate = property(_get_rate, _set_rate,
        doc="""The desired relative angular velocity""")
