# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2011 Victor Blomqvist
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

This submodule contain all the constraints that are supported by pymunk.

Chipmunk has a good overview of the different constraint on youtube which 
works fine to showcase them in pymunk as well. 
http://www.youtube.com/watch?v=ZgJJZTS0aMM

.. raw:: html
    
    <iframe width="420" height="315" style="display: block; margin: 0 auto;"
    src="http://www.youtube.com/embed/ZgJJZTS0aMM" frameborder="0" 
    allowfullscreen></iframe>
    
"""
__version__ = "$Id$"
__docformat__ = "reStructuredText"

import ctypes as ct

from . import _chipmunk as cp 
from . import _chipmunk_ffi as cpffi 

class Constraint(object):
    """Base class of all constraints. 
    
    You usually don't want to create instances of this class directly, but 
    instead use one of the specific constraints such as the PinJoint.
    """
    def __init__(self, constraint=None):
        self._constraint = constraint
        self._ccontents = self._constraint.contents
        
    def _get_max_force(self):
        return self._ccontents.maxForce
    def _set_max_force(self, f):
        self._ccontents.maxForce = f
    max_force = property(_get_max_force, _set_max_force,
        doc="""The maximum force that the constraint can use to act on the two 
        bodies. Defaults to infinity""")
        
    def _get_error_bias(self):
        return self._ccontents.errorBias
    def _set_error_bias(self, error_bias):
        self._ccontents.errorBias = error_bias
    error_bias = property(_get_error_bias, _set_error_bias,
        doc="""The rate at which joint error is corrected.

        Defaults to pow(1.0 - 0.1, 60.0) meaning that it will correct 10% of 
        the error every 1/60th of a second.""")
        
    def _get_max_bias(self):
        return self._ccontents.maxBias
    def _set_max_bias(self, max_bias):
        self._ccontents.maxBias = max_bias
    max_bias = property(_get_max_bias, _set_max_bias,
        doc="""The maximum rate at which joint error is corrected. Defaults 
        to infinity""")

    def _get_impulse(self):
        return cpffi.cpConstraintGetImpulse(self._constraint)
    impulse = property(_get_impulse,
        doc="""Get the last impulse applied by this constraint.""")
        
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
    
    def __del__(self):
        if cp is not None:
            cp.cpConstraintFree(self._constraint)

class PinJoint(Constraint):
    """Keeps the anchor points at a set distance from one another."""
    def __init__(self, a, b, anchr1=(0,0), anchr2=(0,0)):
        """a and b are the two bodies to connect, and anchr1 and anchr2 are the
        anchor points on those bodies.
        """

        self._constraint = cp.cpPinJointNew(a._body, b._body, anchr1, anchr2)
        self._ccontents = self._constraint.contents
        self._pjc = cp.cast(self._constraint, ct.POINTER(cp.cpPinJoint)).contents
        self._set_bodies(a,b)        
        
    def _get_anchr1(self):
        return self._pjc.anchr1
    def _set_anchr1(self, anchr):
        self._pjc.anchr1 = anchr
    anchr1 = property(_get_anchr1, _set_anchr1)
    
    def _get_anchr2(self):
        return self._pjc.anchr2
    def _set_anchr2(self, anchr):
        self._pjc.anchr2 = anchr
    anchr2 = property(_get_anchr2, _set_anchr2)
    
    def _get_dist(self):
        return self._pjc.dist
    def _set_dist(self, dist):
        self._pjc.dist = dist
    distance = property(_get_dist, _set_dist)
    
class SlideJoint(Constraint):
    """Like pin joints, but have a minimum and maximum distance.
    A chain could be modeled using this joint. It keeps the anchor points 
    from getting to far apart, but will allow them to get closer together.
    """
    def __init__(self, a, b, anchr1, anchr2, min, max):
        """a and b are the two bodies to connect, anchr1 and anchr2 are the
        anchor points on those bodies, and min and max define the allowed
        distances of the anchor points.
        """
        self._constraint = cp.cpSlideJointNew(a._body, b._body, anchr1, anchr2, min, max)
        self._ccontents = self._constraint.contents
        self._sjc = cp.cast(self._constraint, ct.POINTER(cp.cpSlideJoint)).contents
        self._set_bodies(a,b)
        
    def _get_anchr1(self):
        return self._sjc.anchr1
    def _set_anchr1(self, anchr):
        self._sjc.anchr1 = anchr
    anchr1 = property(_get_anchr1, _set_anchr1)
    
    def _get_anchr2(self):
        return self._sjc.anchr2
    def _set_anchr2(self, anchr):
        self._sjc.anchr2 = anchr
    anchr2 = property(_get_anchr2, _set_anchr2)

    def _get_min(self):
        return self._sjc.min
    def _set_min(self, min):
        self._sjc.min = min
    min = property(_get_min, _set_min)
    
    def _get_max(self):
        return self._sjc.max
    def _set_max(self, max):
        self._sjc.max = max
    max = property(_get_max, _set_max)    
        
class PivotJoint(Constraint):
    """Simply allow two objects to pivot about a single point."""
    def __init__(self, a, b, *args):
        """a and b are the two bodies to connect, and pivot is the point in
        world coordinates of the pivot. Because the pivot location is given in
        world coordinates, you must have the bodies moved into the correct
        positions already. 
        Alternatively you can specify the joint based on a pair of anchor 
        points, but make sure you have the bodies in the right place as the 
        joint will fix itself as soon as you start simulating the space. 
        
        That is, either create the joint with PivotJoint(a, b, pivot) or 
        PivotJoint(a, b, anchr1, anchr2).
        
            a : `Body`
                The first of the two bodies
            b : `Body`
                The second of the two bodies
            args : [Vec2d] or [Vec2d,Vec2d]
                Either one pivot point, or two anchor points
        """
        
        if len(args) == 1:
            self._constraint = cp.cpPivotJointNew(a._body, b._body, args[0])
        elif len(args) == 2:
            self._constraint = cp.cpPivotJointNew2(a._body, b._body, args[0], args[1])
        else:
            raise Exception("You must specify either one pivot point or two anchor points")
            
        self._ccontents = self._constraint.contents
        self._pjc = cp.cast(self._constraint, ct.POINTER(cp.cpPivotJoint)).contents
        self._set_bodies(a,b)
    
    def _get_anchr1(self):
        return self._pjc.anchr1
    def _set_anchr1(self, anchr):
        self._pjc.anchr1 = anchr
    anchr1 = property(_get_anchr1, _set_anchr1)
    
    def _get_anchr2(self):
        return self._pjc.anchr2
    def _set_anchr2(self, anchr):
        self._pjc.anchr2 = anchr
    anchr2 = property(_get_anchr2, _set_anchr2)
    
class GrooveJoint(Constraint):
    """Similar to a pivot joint, but one of the anchors is
    on a linear slide instead of being fixed.
    """
    def __init__(self, a, b, groove_a, groove_b, anchr2):
        """The groove goes from groove_a to groove_b on body a, and the pivot 
        is attached to anchr2 on body b. All coordinates are body local. 
        """
        self._constraint = cp.cpGrooveJointNew(a._body, b._body, groove_a, groove_b, anchr2)
        self._ccontents = self._constraint.contents
        self._pjc = cp.cast(self._constraint, ct.POINTER(cp.cpGrooveJoint)).contents
        self._set_bodies(a,b)
        
    def _get_anchr2(self):
        return self._pjc.anchr2
    def _set_anchr2(self, anchr):
        self._pjc.anchr2 = anchr
    anchr2 = property(_get_anchr2, _set_anchr2)
    
    def _get_groove_a(self):
        return self._pjc.grv_a
    groove_a = property(_get_groove_a)
    
    def _get_groove_b(self):
        return self._pjc.grv_b
    groove_b = property(_get_groove_b)
    
class DampedSpring(Constraint):
    """A damped spring"""
    def __init__(self, a, b, anchr1, anchr2, rest_length, stiffness, damping):
        """Defined much like a slide joint. 
        
        :Parameters:
            anchr1 : Vec2d or (x,y)
                Anchor point 1, relative to body a
            anchr2 : Vec2d or (x,y)
                Anchor point 2, relative to body b
            rest_length : float
                The distance the spring wants to be.
            stiffness : float
                The spring constant (Young's modulus). 
            damping : float
                How soft to make the damping of the spring. 
        """
        self._constraint = cp.cpDampedSpringNew(a._body, b._body, anchr1, anchr2, rest_length, stiffness, damping)
        self._ccontents = self._constraint.contents
        self._dsc = cp.cast(self._constraint, ct.POINTER(cp.cpDampedSpring)).contents
        self._set_bodies(a,b)
        
    def _get_anchr1(self):
        return self._dsc.anchr1
    def _set_anchr1(self, anchr):
        self._dsc.anchr1 = anchr
    anchr1 = property(_get_anchr1, _set_anchr1)
    
    def _get_anchr2(self):
        return self._dsc.anchr2
    def _set_anchr2(self, anchr):
        self._dsc.anchr2 = anchr
    anchr2 = property(_get_anchr2, _set_anchr2)

    def _get_rest_length(self):
        return self._dsc.restLength
    def _set_rest_length(self, rest_length):
        self._dsc.restLength = rest_length
    rest_length = property(_get_rest_length, _set_rest_length,
        doc="""The distance the spring wants to be.""")
    
    def _get_stiffness(self):
        return self._dsc.stiffness
    def _set_stiffness(self, stiffness):
        self._dsc.stiffness = stiffness
    stiffness = property(_get_stiffness, _set_stiffness,
        doc="""The spring constant (Young's modulus).""")    
    
    def _get_damping(self):
        return self._dsc.damping
    def _set_damping(self, damping):
        self._dsc.damping = damping
    damping = property(_get_damping, _set_damping, 
        doc="""How soft to make the damping of the spring.""")   
    
class DampedRotarySpring(Constraint):
    """Like a damped spring, but works in an angular fashion"""
    def __init__(self, a, b, rest_angle, stiffness, damping):
        """Like a damped spring, but works in an angular fashion. 
        
        :Parameters:
            rest_angle
                The relative angle in radians that the bodies want to have
            stiffness
                The spring constant (Young's modulus). 
            damping
                How soft to make the damping of the spring. 
        """
        self._constraint = cp.cpDampedRotarySpringNew(a._body, b._body, rest_angle, stiffness, damping)
        self._ccontents = self._constraint.contents
        self._dsc = cp.cast(self._constraint, ct.POINTER(cp.cpDampedRotarySpring)).contents
        self._set_bodies(a,b)
        
    def _get_rest_angle(self):
        return self._dsc.restAngle
    def _set_rest_angle(self, rest_angle):
        self._dsc.restAngle = rest_angle
    rest_angle = property(_get_rest_angle, _set_rest_angle, 
        doc="""The relative angle in radians that the bodies want to have""")
    
    def _get_stiffness(self):
        return self._dsc.stiffness
    def _set_stiffness(self, stiffness):
        self._dsc.stiffness = stiffness
    stiffness = property(_get_stiffness, _set_stiffness,
        doc="""The spring constant (Young's modulus).""")  
    
    def _get_damping(self):
        return self._dsc.damping
    def _set_damping(self, damping):
        self._dsc.damping = damping
    damping = property(_get_damping, _set_damping, 
        doc="""How soft to make the damping of the spring.""") 

    def _set_torque_func(self, func):
        """Set the torque function
            
            func(self, relative_angle) -> torque
            
            Callback Parameters
                relative_angle : float
                    The relative angle
        
        """
        def _impl(_, relative_angle):
            return func(self, relative_angle)
        
        self._torque_func_callback = cp.cpDampedRotarySpringTorqueFunc(_impl)
        self._dsc.springTorqueFunc = self._torque_func_callback
    torque_func = property(fset=_set_torque_func, 
        doc=_set_torque_func.__doc__)
        
        
class RotaryLimitJoint(Constraint):
    """Constrains the relative rotations of two bodies."""
    def __init__(self, a, b, min, max):
        """Constrains the relative rotations of two bodies. min and max are 
        the angular limits in radians. It is implemented so that it's possible 
        to for the range to be greater than a full revolution.
        """
        self._constraint = cp.cpRotaryLimitJointNew(a._body, b._body, min, max)
        self._ccontents = self._constraint.contents
        self._rlc = cp.cast(self._constraint, ct.POINTER(cp.cpRotaryLimitJoint)).contents
        self._set_bodies(a,b)
        
    def _get_min(self):
        return self._rlc.min
    def _set_min(self, min):
        self._rlc.min = min
    min = property(_get_min, _set_min)
    
    def _get_max(self):
        return self._rlc.max
    def _set_max(self, max):
        self._rlc.max = max
    max = property(_get_max, _set_max)    
    
class RatchetJoint(Constraint):
    """Works like a socket wrench."""
    def __init__(self, a, b, phase, ratchet):
        """Works like a socket wrench. ratchet is the distance between 
        "clicks", phase is the initial offset to use when deciding where the 
        ratchet angles are.  
        """
        self._constraint = cp.cpRatchetJointNew(a._body, b._body, phase, ratchet)
        self._ccontents = self._constraint.contents
        self._dsc = cp.cast(self._constraint, ct.POINTER(cp.cpRatchetJoint)).contents
        self._set_bodies(a,b)
        
    def _get_angle(self):
        return self._dsc.angle
    def _set_angle(self, angle):
        self._dsc.angle = angle
    angle = property(_get_angle, _set_angle)
    
    def _get_phase(self):
        return self._dsc.phase
    def _set_phase(self, phase):
        self._dsc.phase = phase
    phase = property(_get_phase, _set_phase)  
    
    def _get_ratchet(self):
        return self._dsc.ratchet
    def _set_ratchet(self, ratchet):
        self._dsc.ratchet = ratchet
    ratchet = property(_get_ratchet, _set_ratchet) 
    
class GearJoint(Constraint):
    """Keeps the angular velocity ratio of a pair of bodies constant."""
    def __init__(self, a, b, phase, ratio):
        """Keeps the angular velocity ratio of a pair of bodies constant. 
        ratio is always measured in absolute terms. It is currently not 
        possible to set the ratio in relation to a third body's angular 
        velocity. phase is the initial angular offset of the two bodies.  
        """
        self._constraint = cp.cpGearJointNew(a._body, b._body, phase, ratio)
        self._ccontents = self._constraint.contents
        self._dsc = cp.cast(self._constraint, ct.POINTER(cp.cpGearJoint)).contents
        self._set_bodies(a,b)
        
    def _get_phase(self):
        return self._dsc.phase
    def _set_phase(self, phase):
        self._dsc.phase = phase
    phase = property(_get_phase, _set_phase)  
    
    def _get_ratio(self):
        return self._dsc.ratio
    def _set_ratio(self, ratio):
        self._dsc.ratio = ratio
    ratio = property(_get_ratio, _set_ratio) 
    
class SimpleMotor(Constraint):
    """Keeps the relative angular velocity of a pair of bodies constant."""
    def __init__(self, a, b, rate):
        """Keeps the relative angular velocity of a pair of bodies constant. 
        rate is the desired relative angular velocity. You will usually want 
        to set an force (torque) maximum for motors as otherwise they will be 
        able to apply a nearly infinite torque to keep the bodies moving.  
        """
        self._constraint = cp.cpSimpleMotorNew(a._body, b._body, rate)
        self._ccontents = self._constraint.contents
        self._dsc = cp.cast(self._constraint, ct.POINTER(cp.cpSimpleMotor)).contents
        self._set_bodies(a,b)
        
    def _get_rate(self):
        return self._dsc.rate
    def _set_rate(self, rate):
        self._dsc.rate = rate
    rate = property(_get_rate, _set_rate,
        doc="""The desired relative angular velocity""")  


