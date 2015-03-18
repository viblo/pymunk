# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2012 Victor Blomqvist
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

"""
pymunk is a easy-to-use pythonic 2d physics library that can be used whenever 
you need 2d rigid body physics from Python.

Homepage: http://www.pymunk.org

This is the main containing module of pymunk. It contains among other things 
the very central Space, Body and Shape classes.

When you import this module it will automatically load the chipmunk library 
file. As long as you haven't turned off the debug mode a print will show 
exactly which Chipmunk library file it loaded. For example::

    >>> import pymunk
    Loading chipmunk for Windows (32bit) [C:\code\pymunk\chipmunk.dll]

"""
__version__ = "$Id$"
__docformat__ = "reStructuredText"

__all__ = ["inf", "version", "chipmunk_version"
        , "Space", "Body", "Shape", "Circle", "Poly", "Segment"
        , "moment_for_circle", "moment_for_poly", "moment_for_segment"
        , "moment_for_box", "reset_shapeid_counter"
        , "SegmentQueryInfo", "Contact", "Arbiter", "BB", "ShapeFilter"
        , "Transform", "PointQueryInfo"]

import ctypes as ct
import warnings
import sys
import weakref
try:
    #Python 2.7+ 
    from weakref import WeakSet
except ImportError:
    from .weakrefset import WeakSet

from . import _chipmunk as cp
from . import _chipmunk_ffi as cpffi
from . import util as u
from .vec2d import Vec2d
from ._chipmunk_manual import ShapeFilter, Transform
from pymunk.constraint import *

version = "5.0.0"
"""The release version of this pymunk installation.
Valid only if pymunk was installed from a source or binary 
distribution (i.e. not in a checked-out copy from git).
"""

chipmunk_version = "%sR%s" % (cp.cpVersionString.value.decode(), 'd7603e392782079b691d7948405af2dd66648a7a')
"""The Chipmunk version compatible with this pymunk version.
Other (newer) Chipmunk versions might also work if the new version does not 
contain any breaking API changes.

This property does not show a valid value in the compiled documentation, only 
when you actually import pymunk and do pymunk.chipmunk_version

The string is in the following format:
<cpVersionString>R<github commit of chipmunk>
where cpVersionString is a version string set by Chipmunk and the git commit
hash corresponds to the git hash of the chipmunk source from
github.com/slembcke/Chipmunk2D included with pymunk. If the Chipmunk version 
is a release then the second part will be empty

.. note:: 
    This is also the version of the Chipmunk source files included in the 
    chipmunk_src folder (normally included in the pymunk source distribution).
"""

try:
    inf = float('inf') # works only on python 2.6+
except:
    inf = 1e100
"""Infinity that can be passed as mass or inertia to Body. 

Useful when you for example want a body that cannot rotate, just set its 
moment to inf. Just remember that if two objects with both infinite masses 
collides the world might explode. Similary effects can happen with infinite 
moment.

.. note::
    In previous versions of pymunk you used inf to create static bodies. This
    has changed and you should instead do it by invoking the body constructor 
    without any arguments.
"""

#cp.cpEnableSegmentToSegmentCollisions()

class Space(object):
    """Spaces are the basic unit of simulation. You add rigid bodies, shapes 
    and joints to it and then step them all forward together through time. 
    """
    def __init__(self, iterations=10):
        """Create a new instace of the Space
        
        Its usually best to keep the elastic_iterations setting to 0. Only 
        change if you have problem with stacking elastic objects on each other. 
        If that is the case, try to raise it. However, a value other than 0 
        will affect other parts, most importantly you wont get reliable 
        total_impulse readings from the `Arbiter` object in collsion callbacks!
        
        :Parameters:
            iterations : int
                Number of iterations to use in the impulse solver to solve 
                contacts.
        """

        self._space = cp.cpSpaceNew()
        self._space.contents.iterations = iterations
        
        self._static_body = Body(body_type=Body.STATIC)
        
        self._handlers = {} # To prevent the gc to collect the callbacks.
        self._default_handler = None
        
        self._post_step_callbacks = {}
        self._post_callback_keys = {}
        self._post_last_callback_key = 0
        self._removed_shapes = {}
        
        self._shapes = {}
        self._bodies = set()
        self._constraints = set()
        
        self._locked = False
        self._add_later = set()
        self._remove_later = set()

    def _get_self(self):
        return self
        
    def _get_shapes(self):
        return list(self._shapes.values())
    shapes = property(_get_shapes, 
        doc="""A list of all the shapes added to this space (both static and non-static)""")

    def _get_bodies(self):
        return list(self._bodies)
    bodies = property(_get_bodies,
        doc="""A list of the bodies added to this space""")
    
    def _get_constraints(self):
        return list(self._constraints)
    constraints = property(_get_constraints,
        doc="""A list of the constraints added to this space""")

    def _get_static_body(self):
        """A convenience static body already added to the space"""
        return self._static_body
    static_body = property(_get_static_body, doc=_get_static_body.__doc__)
        
    def __del__(self):
        try:
            cp.cpSpaceFree(self._space)
        except:
            pass

    def _set_iterations(self, value):
        cp.cpSpaceSetIterations(self._space, value)
    def _get_iterations(self):
        return cp.cpSpaceGetIterations(self._space)
    iterations = property(_get_iterations, _set_iterations
        , doc="""Iterations allow you to control the accuracy of the solver.
        
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
        """)

            
    def _set_gravity(self, gravity_vector):
        cp.cpSpaceSetGravity(self._space, gravity_vector)
    def _get_gravity(self):
        return cp.cpSpaceGetGravity(self._space)
    gravity = property(_get_gravity, _set_gravity
        , doc="""Global gravity applied to the space.
        
        Defaults to (0,0). Can be overridden on a per body basis by writing 
        custom integration functions.
        """)

    def _set_damping(self, damping):
        cp.cpSpaceSetDamping(self._space, damping)
    def _get_damping(self):
        return cp.cpSpaceGetDamping(self._space)
    damping = property(_get_damping, _set_damping
        , doc="""Amount of simple damping to apply to the space. 
        
        A value of 0.9 means that each body will lose 10% of its velocity per 
        second. Defaults to 1. Like gravity, it can be overridden on a per 
        body basis.
        """)

    def _set_idle_speed_threshold(self, idle_speed_threshold):
        cp.cpSpaceSetIdleSpeedThreshold(self._space, idle_speed_threshold) 
    def _get_idle_speed_threshold(self):
        return cp.cpSpaceGetIdleSpeedThreshold(self._space)
    idle_speed_threshold = property(_get_idle_speed_threshold
        , _set_idle_speed_threshold
        , doc="""Speed threshold for a body to be considered idle.
        
        The default value of 0 means the space estimates a good threshold 
        based on gravity.
        """)

    def _set_sleep_time_threshold(self, sleep_time_threshold):
        cp.cpSpaceSetSleepTimeThreshold(self._space, sleep_time_threshold)
    def _get_sleep_time_threshold(self):
        return cp.cpSpaceGetSleepTimeThreshold(self._space)
    sleep_time_threshold = property(_get_sleep_time_threshold
        , _set_sleep_time_threshold
        , doc="""Time a group of bodies must remain idle in order to fall 
        asleep.
        
        The default value of `inf` disables the sleeping algorithm.
        """)
        
    def _set_collision_slop(self, collision_slop):
        cp.cpSpaceSetCollisionSlop(self._space, collision_slop)
    def _get_collision_slop(self):
        return cp.cpSpaceGetCollisionSlop(self._space)
    collision_slop = property(_get_collision_slop
        , _set_collision_slop
        , doc="""Amount of overlap between shapes that is allowed.
        
        To improve stability, set this as high as you can without noticable 
        overlapping. It defaults to 0.1.
        """)
        
    def _set_collision_bias(self, collision_bias):
        cp.cpSpaceSetCollisionBias(self._space, collision_bias)
    def _get_collision_bias(self):
        return cp.cpSpaceGetCollisionBias(self._space)
    collision_bias = property(_get_collision_bias
        , _set_collision_bias
        , doc="""Determines how fast overlapping shapes are pushed apart.
        
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
        """)
        
    def _set_collision_persistence(self, collision_persistence):
        cp.cpSpaceSetCollisionPersistence(self._space, collision_persistence)
    def _get_collision_persistence(self):
        return cp.cpSpaceGetCollisionPersistence(self._space)
    collision_persistence = property(_get_collision_persistence
        , _set_collision_persistence
        , doc="""The number of frames the space keeps collision solutions 
        around for.
        
        Helps prevent jittering contacts from getting worse. This defaults 
        to 3.
        
        ..Note::
            Very very few games will need to change this value.
        """)
        
    def _get_current_time_step(self):
        return cp.cpSpaceGetCurrentTimeStep(self._space)
    current_time_step = property(_get_current_time_step,
        doc="""Retrieves the current (if you are in a callback from 
        Space.step()) or most recent (outside of a Space.step() call) 
        timestep.
        """)
            
    def add(self, *objs):
        """Add one or many shapes, bodies or joints to the space
        
        Unlike Chipmunk and earlier versions of pymunk its now allowed to add 
        objects even from a callback during the simulation step. However, the 
        add will not be performed until the end of the step.
        """
        
        if self._locked:
            self._add_later.add(objs)
            return
            
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
                    
    def remove(self, *objs):
        """Remove one or many shapes, bodies or constraints from the space
        
        Unlike Chipmunk and earlier versions of pymunk its now allowed to 
        remove objects even from a callback during the simulation step. 
        However, the removal will not be performed until the end of the step.
        
        .. Note:: 
            When removing objects from the space, make sure you remove any 
            other objects that reference it. For instance, when you remove a 
            body, remove the joints and shapes attached to it. 
        """
        
        if self._locked:
            self._remove_later.add(objs)
            return
            
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
                                        
    def _add_shape(self, shape):
        """Adds a shape to the space"""
        assert shape._get_shapeid() not in self._shapes, "shape already added to space"
        shape._space = weakref.proxy(self)
        self._shapes[shape._get_shapeid()] = shape
        cp.cpSpaceAddShape(self._space, shape._shape)
        
    def _add_body(self, body):
        """Adds a body to the space"""
        assert body not in self._bodies, "body already added to space"
        body._space = weakref.proxy(self)
        self._bodies.add(body)
        cp.cpSpaceAddBody(self._space, body._body)
        
    def _add_constraint(self, constraint):
        """Adds a constraint to the space"""
        assert constraint not in self._constraints, "constraint already added to space"
        self._constraints.add(constraint)
        cp.cpSpaceAddConstraint(self._space, constraint._constraint)

    def _remove_shape(self, shape):
        """Removes a shape from the space"""
        self._removed_shapes[shape._get_shapeid()] = shape
        del self._shapes[shape._get_shapeid()]
        cp.cpSpaceRemoveShape(self._space, shape._shape)
    def _remove_body(self, body):
        """Removes a body from the space"""
        body._space = None
        self._bodies.remove(body)
        cp.cpSpaceRemoveBody(self._space, body._body)
    def _remove_constraint(self, constraint):
        """Removes a constraint from the space"""
        self._constraints.remove(constraint)
        cp.cpSpaceRemoveConstraint(self._space, constraint._constraint)

    def reindex_shape(self, shape):
        """Update the collision detection data for a specific shape in the 
        space.
        """
        cp.cpSpaceReindexShape(self._space, shape._shape)
        
    def reindex_shapes_for_body(self, body):
        """Reindex all the shapes for a certain body."""
        cp.cpSpaceReindexShapesForBody(self._space, body._body)
        
    def reindex_static(self):
        """Update the collision detection info for the static shapes in the 
        space. You only need to call this if you move one of the static shapes.
        """
        cp.cpSpaceReindexStatic(self._space)
        
    def step(self, dt):
        """Update the space for the given time step. Using a fixed time step is
        highly recommended. Doing so will increase the efficiency of the
        contact persistence, requiring an order of magnitude fewer iterations
        to resolve the collisions in the usual case."""
        
        self._locked = True
        cp.cpSpaceStep(self._space, dt)
        self._removed_shapes = {}
        self._post_step_callbacks = {}
        self._post_callback_keys = {}
        self._post_last_callback_key = 0
        self._locked = False
        
        for objs in self._add_later:
            self.add(objs)
        self._add_later.clear()
        
        for objs in self._remove_later:
            self.remove(objs)
        self._remove_later.clear()
    
    def add_collision_handler(self, a, b, begin=None, pre_solve=None, post_solve=None, separate=None, *args, **kwargs):
        """Add a collision handler for given collision type pair. 
        
        Whenever a shapes with collision_type a and collision_type b collide, 
        these callbacks will be used to process the collision. 
        None can be provided for callbacks you do not wish to implement, 
        however pymunk will call it's own default versions for these and not 
        the default ones you've set up for the Space. If you need to fall back 
        on the space's default callbacks, you'll have to provide them 
        individually to each handler definition.
        
        :Parameters:
            a : int
                Collision type of the first shape
            b : int 
                Collision type of the second shape
            begin : ``func(space, arbiter, *args, **kwargs) -> bool``
                Collision handler called when two shapes just started touching 
                for the first time this step. Return false from the callback 
                to make pymunk ignore the collision or true to process it 
                normally. Rejecting a collision from a begin() callback 
                permanently rejects the collision until separation. Pass 
                `None` if you wish to use the pymunk default.
            pre_solve : ``func(space, arbiter, *args, **kwargs) -> bool``
                Collision handler called when two shapes are touching. Return 
                false from the callback to make pymunk ignore the collision or 
                true to process it normally. Additionally, you may override 
                collision values such as `Arbiter.elasticity` and 
                `Arbiter.friction` to provide custom friction or elasticity 
                values. See `Arbiter` for more info. Pass `None` if you wish 
                to use the pymunk default.
            post_solve : ``func(space, arbiter, *args, **kwargs)``
                Collsion handler called when two shapes are touching and their 
                collision response has been processed. You can retrieve the 
                collision force at this time if you want to use it to 
                calculate sound volumes or damage amounts. Pass `None` if you 
                wish to use the pymunk default.
            separate : ``func(space, arbiter, *args, **kwargs)``
                Collision handler called when two shapes have just stopped 
                touching for the first time this frame. Pass `None` if you 
                wish to use the pymunk default.
            args
                Optional parameters passed to the collision handler functions.
            kwargs
                Optional keyword parameters passed on to the collision handler 
                functions.
                
        """
        
        _functions = self._collision_function_helper(begin, pre_solve, post_solve, separate, *args, **kwargs)
        
        self._handlers[(a, b)] = _functions
        cp.cpSpaceAddCollisionHandler(self._space, a, b, 
            _functions[0], _functions[1], _functions[2], _functions[3], None)
            
    def set_default_collision_handler(self, begin=None, pre_solve=None, post_solve=None, separate=None, *args, **kwargs):
        """Register a default collision handler to be used when no specific 
        collision handler is found. If you do nothing, the space will be given 
        a default handler that accepts all collisions in begin() and 
        pre_solve() and does nothing for the post_solve() and separate() 
        callbacks. 
        
        :Parameters:
            begin : ``func(space, arbiter, *args, **kwargs) -> bool``
                Collision handler called when two shapes just started touching 
                for the first time this step. Return False from the callback 
                to make pymunk ignore the collision or True to process it 
                normally. Rejecting a collision from a begin() callback 
                permanently rejects the collision until separation. Pass 
                `None` if you wish to use the pymunk default.
            pre_solve : ``func(space, arbiter, *args, **kwargs) -> bool``
                Collision handler called when two shapes are touching. Return 
                False from the callback to make pymunk ignore the collision or 
                True to process it normally. Additionally, you may override 
                collision values such as Arbiter.elasticity and 
                Arbiter.friction to provide custom friction or elasticity 
                values. See Arbiter for more info. Pass `None` if you wish to 
                use the pymunk default.
            post_solve : ``func(space, arbiter, *args, **kwargs)``
                Collsion handler called when two shapes are touching and their 
                collision response has been processed. You can retrieve the 
                collision force at this time if you want to use it to 
                calculate sound volumes or damage amounts. Pass `None` if you 
                wish to use the pymunk default.
            separate : ``func(space, arbiter, *args, **kwargs)``
                Collision handler called when two shapes have just stopped 
                touching for the first time this frame. Pass `None` if you wish 
                to use the pymunk default.
            args
                Optional parameters passed to the collision handler functions.
            kwargs
                Optional keyword parameters passed on to the collision handler 
                functions.
        """
        
        _functions = self._collision_function_helper(
            begin, pre_solve, post_solve, separate, *args, **kwargs
            )
        self._default_handler = _functions
        cp.cpSpaceSetDefaultCollisionHandler(self._space,
            _functions[0], _functions[1], _functions[2], _functions[3], None)
    
    def _collision_function_helper(self, begin, pre_solve, post_solve, separate, *args, **kwargs):
        
        functions = [(begin, cp.cpCollisionBeginFunc)
                    , (pre_solve, cp.cpCollisionPreSolveFunc)
                    , (post_solve, cp.cpCollisionPostSolveFunc)
                    , (separate, cp.cpCollisionSeparateFunc)]
        
        _functions = []
        
        for func, func_type in functions:
            if func is None:
                _f = ct.cast(ct.POINTER(ct.c_int)(), func_type)
            else:
                _f = self._get_cf1(func, func_type, *args, **kwargs)
            _functions.append(_f)
        return _functions
    
    def remove_collision_handler(self, a, b):
        """Remove a collision handler for a given collision type pair.
        
        :Parameters:
            a : int
                Collision type of the first shape
            b : int
                Collision type of the second shape
        """
        if (a, b) in self._handlers:
            del self._handlers[(a, b)]
        cp.cpSpaceRemoveCollisionHandler(self._space, a, b)
        
    
    def _get_cf1(self, func, function_type, *args, **kwargs):
        def cf(_arbiter, _space, _data):
            arbiter = Arbiter(_arbiter, self)
            x = func(self, arbiter, *args, **kwargs)
            
            if function_type not in [cp.cpCollisionBeginFunc, cp.cpCollisionPreSolveFunc]:
                return
            if isinstance(x,int):
                return x
                
            if sys.version_info[0] >= 3:
                func_name = func.__code__.co_name
                filename = func.__code__.co_filename
                lineno = func.__code__.co_firstlineno
            else:
                func_name = func.func_name
                filename = func.func_code.co_filename
                lineno = func.func_code.co_firstlineno
                
            warnings.warn_explicit(
                "Function '" + func_name + "' should return a bool to" +
                " indicate if the collision should be processed or not when" +
                " used as 'begin' or 'pre_solve' collision callback.", 
                UserWarning, filename, lineno, func.__module__)
            return True
        return function_type(cf)
        
    
    def add_post_step_callback(self, callback_function, obj, *args, **kwargs):
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
        
        :Parameters:
            callback_function : ``func(obj, *args, **kwargs)``
                The callback function.
            obj : Any object
                This object is used as a key, you can only have one callback 
                for a single object. It is passed on to the callback function.
            args
                Optional parameters passed to the callback function.
            kwargs
                Optional keyword parameters passed on to the callback function.
                
        :Return: 
            True if key was not previously added, False otherwise
        """
        
        if obj in self._post_callback_keys:
            return False
            
        def cf(_space, key, data):
            callback_function(obj, *args, **kwargs)
            
        f = cp.cpPostStepFunc(cf)
                
        self._post_last_callback_key += 1
        self._post_callback_keys[obj] = self._post_last_callback_key    
        self._post_step_callbacks[obj] = f
        
        key = self._post_callback_keys[obj]
        return bool(cp.cpSpaceAddPostStepCallback(self._space, f, key, None))
                
    def point_query(self, point, max_distance, shape_filter):
        """Query space at point for shapes within the given distance range.
        
        Return a list of `PointQueryInfo`.
        
        The filter is applied to the query and follows the same rules as the 
        collision detection. Sensor shapes are included. If a maxDistance of 
        0.0 is used, the point must lie inside a shape. Negative max_distance 
        is also allowed meaning that the point must be a under a certain 
        depth within a shape to be considered a match.
        
        :Parameters:    
            point : (x,y) or `Vec2d`
                Define where to check for collision in the space.
            max_distnace : int
                Match only within this distance.
            shape_filter : ShapeFilter
                Only pick shapes matching the filter.
        """
              
        self.__query_hits = []
        def cf(_shape, point, distance, gradient, data):
            
            shape = self._get_shape(_shape)
            p = PointQueryInfo(shape, point, distance, gradient)
            self.__query_hits.append(p)
        f = cp.cpSpacePointQueryFunc(cf)
        cp.cpSpacePointQuery(self._space, point, max_distance, shape_filter, f, None)
        
        return self.__query_hits
            
    def _get_shape(self, _shape):
        if not bool(_shape):
            return None
        
        shapeid = cp.cpShapeGetUserData(_shape)
        #return self._shapes[hashid_private]  
        if shapeid in self._shapes:
            shape = self._shapes[shapeid]        
        elif shapeid in self._removed_shapes:
            shape = self._removed_shapes[shapeid]
        return shape
           
    def point_query_nearest(self, point, max_distance, shape_filter):
        """Query space at point the nearest shape within the given distance 
        range.
        
        Return a `PointQueryInfo` or None if nothing was hit.
        
        The filter is applied to the query and follows the same rules as the 
        collision detection. Sensor shapes are included. If a maxDistance of 
        0.0 is used, the point must lie inside a shape. Negative max_distance 
        is also allowed meaning that the point must be a under a certain 
        depth within a shape to be considered a match.
        
        :Parameters:    
            point : (x,y) or `Vec2d`
                Define where to check for collision in the space.
            max_distnace : int
                Match only within this distance.
            shape_filter : ShapeFilter
                Only pick shapes matching the filter.
        """
        info = cp.cpPointQueryInfo()
        info_p = ct.POINTER(cp.cpPointQueryInfo)(info)
        _shape = cp.cpSpacePointQueryNearest(self._space, point, max_distance, shape_filter, info_p)
        shape = self._get_shape(_shape)
        
        if shape != None:
            return PointQueryInfo(shape, info.point, info.distance, info.gradient)
        return None       
        
        
    def segment_query(self, start, end, radius, shape_filter):
        """Query space along the line segment from start to end with the 
        given radius.
        
        The filter is applied to the query and follows the same rules as the 
        collision detection. Sensor shapes are included.
        
        :Return: 
            [`SegmentQueryInfo`] - One SegmentQueryInfo object for each hit.
        """
        
        self.__query_hits = []
        def cf(_shape, point, normal, alpha, data):
            shape = self._get_shape(_shape)
            info = SegmentQueryInfo(shape, point, normal, alpha)
            self.__query_hits.append(info)
        
        f = cp.cpSpaceSegmentQueryFunc(cf)
        cp.cpSpaceSegmentQuery(self._space, start, end, radius, shape_filter, f, None)
        
        return self.__query_hits
            
    def segment_query_first(self, start, end, radius,  shape_filter):
        """Query space along the line segment from start to end with the 
        given radius.
        
        The filter is applied to the query and follows the same rules as the 
        collision detection. Sensor shapes are included.
        
        :Return: 
            `SegmentQueryInfo` - SegmentQueryInfo object or None if nothing 
            was hit.
        """
        info = cp.cpSegmentQueryInfo()
        info_p = ct.POINTER(cp.cpSegmentQueryInfo)(info)
        _shape = cp.cpSpaceSegmentQueryFirst(self._space, start, end, radius, shape_filter, info_p)
        
        shape = self._get_shape(_shape)
        if shape != None:
            return SegmentQueryInfo(shape, info.point, info.normal, info.alpha)
        return None
    
    
    def bb_query(self, bb, shape_filter):
        """Query space to find all shapes near bb. 
        
        The filter is applied to the query and follows the same rules as the 
        collision detection. Sensor shapes are included.
        
        Returns a list of shapes hit.
        """
        
        self.__query_hits = []
        def cf(_shape, data):
            shape = self._get_shape(_shape)
            self.__query_hits.append(shape)
        f = cp.cpSpaceBBQueryFunc(cf)
        cp.cpSpaceBBQuery(self._space, bb._bb, shape_filter, f, None)
        return self.__query_hits 
    
    
    def shape_query(self, shape):
        """Query a space for any shapes overlapping the given shape
        
        Returns a list of shapes.
        """
        
        self.__query_hits = []
        def cf(_shape, points, data):
            
            shape = self._get_shape(_shape)
            self.__query_hits.append(shape)
        f = cp.cpSpaceShapeQueryFunc(cf)
        cp.cpSpaceShapeQuery(self._space, shape._shape, f, None)
        return self.__query_hits
        
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
    
    DYNAMIC = 0
    """Dynamic bodies are the default body type. 
    
    They react to collisions, 
    are affected by forces and gravity, and have a finite amount of mass. 
    These are the type of bodies that you want the physics engine to 
    simulate for you. Dynamic bodies interact with all types of bodies 
    and can generate collision callbacks.
    """
    
    KINEMATIC = 1
    """Kinematic bodies are bodies that are controlled from your code 
    instead of inside the physics engine. 
    
    They arent affected by gravity and they have an infinite amount of mass 
    so they don't react to collisions or forces with other bodies. Kinematic 
    bodies are controlled by setting their velocity, which will cause them 
    to move. Good examples of kinematic bodies might include things like 
    moving platforms. Objects that are touching or jointed to a kinematic 
    body are never allowed to fall asleep.
    """
    
    STATIC = 2
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
        gravity for you. This is probably preferred in most cases.
        
        The other option is to set the mass of the body when it's created, 
        and leave the mass of the shapes added to it as 0.0. This approach is 
        more flexible, but is not as easy to use. Don't set the mass of both 
        the body and the shapes. If you do so, it will recalculate and 
        overwite your custom mass value when the shapes are added to the body.
        """
        if body_type == Body.DYNAMIC:
            self._body = cp.cpBodyNew(mass, moment)
        elif body_type == Body.KINEMATIC:
            self._body = cp.cpBodyNewKinematic()
        elif body_type == Body.STATIC:
            self._body = cp.cpBodyNewStatic()
        
        self._bodycontents = self._body.contents 
        self._position_callback = None # To prevent the gc to collect the callbacks.
        self._velocity_callback = None # To prevent the gc to collect the callbacks.
        
        self._space = None # Weak ref to the space holding this body (if any)
        
        self._constraints = WeakSet() # weak refs to any constraints attached
        self._shapes = WeakSet() # weak refs to any shapes attached
        
    def __del__(self):
        try:
            cp.cpBodyFree(self._body)
        except: 
            pass

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
        cp.cpBodySetPosition(self._body, pos)
    def _get_position(self):
        return cp.cpBodyGetPosition(self._body)
    position = property(_get_position, _set_position,
        doc="""Position of the body. 
        
        When changing the position you may also want to call 
        Space.reindex_shapes_for_body() to update the collision detection 
        information for the attached shapes if plan to make any queries 
        against the space.""")

    def _set_center_of_gravity(self, cog):
        cp.cpBodySetCenterOfGravity(self._body, cog)
    def _get_center_of_gravity(self):
        return cp.cpBodyGetCenterOfGravity(self._body)
    center_of_gravity = property(_get_center_of_gravity, 
        _set_center_of_gravity,    
        doc="""Location of the center of gravity in body local coordinates.
        
        The default value is (0, 0), meaning the center of gravity is the 
        same as the position of the body.
        """)
    
    def _set_velocity(self, vel):
        cp.cpBodySetVelocity(self._body, vel)
    def _get_velocity(self):
        return cp.cpBodyGetVelocity(self._body)
    velocity = property(_get_velocity, _set_velocity,
        doc="""Linear velocity of the center of gravity of the body.""")
        
    def _set_force(self, f):
        cp.cpBodySetForce(self._body, f)
    def _get_force(self):
        return cp.cpBodyGetForce(self._body)
    force = property(_get_force, _set_force,
        doc="""Force applied to the center of gravity of the body. 
        
        This value is reset for every time step.""")

    def _set_angle(self, angle):
        cp.cpBodySetAngle(self._body, angle)
    def _get_angle(self):
        return cp.cpBodyGetAngle(self._body)
    angle = property(_get_angle, _set_angle, 
        doc="""Rotation of the body in radians.
        
        When changing the rotation you may also want to call 
        Space.reindex_shapes_for_body() to update the collision detection 
        information for the attached shapes if plan to make any queries 
        against the space. A body rotates around its center of gravity, not 
        its position.
        
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
        return cp.cpBodyGetRotation(self._body)
    rotation_vector = property(_get_rotation_vector,
        doc="""The rotation vector for the body.""")

    def _get_space(self):
        if self._space != None:
            return self._space._get_self() #ugly hack because of weakref
        else:
            return None
    space = property(_get_space,
        doc="""Get the cpSpace that body has been added to (or None).""")
    
    def _set_velocity_limit(self, vel):
        self._bodycontents.v_limit = vel
    def _get_velocity_limit(self):
        return self._bodycontents.v_limit
    velocity_limit = property(_get_velocity_limit, _set_velocity_limit)
    
   
    def _set_angular_velocity_limit(self, w):
        self._bodycontents.w_limit = w
    def _get_angular_velocity_limit(self):
        return self._bodycontents.w_limit
    angular_velocity_limit = property(_get_angular_velocity_limit, _set_angular_velocity_limit)
    
    def _set_velocity_func(self, func):
        """The velocity callback function. The velocity callback function 
        is called each time step, and can be used to set a body's velocity.
        
            ``func(body, gravity, damping, dt) -> None``
            
            Callback Parameters
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
        """The position callback function. The position callback function 
        is called each time step and can be used to update the body's position.
        
            ``func(body, dt) -> None``
            
            Callback Parameters
                body : `Body`
                    Body that should have its velocity calculated
                dt : float
                    Delta time since last step.
        """
        
        def _impl(_, dt):
            func(self, dt)
            return 0
        self._position_callback = cp.cpBodyPositionFunc(_impl)
        self._bodycontents.position_func = self._position_callback
    position_func = property(fset=_set_position_func, 
        doc=_set_position_func.__doc__)
    
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
        cp.cpBodyUpdateVelocity(body._body, gravity, damping, dt)

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
    
    
        
    def reset_forces(self):
        """Zero both the forces and torques accumulated on body"""
        cp.cpBodyResetForces(self._body)

    def apply_force_at_world_point(self, force, point):
        """Add the force force to body as if applied from the world point.
        
        People are sometimes confused by the difference between a force and 
        an impulse. An impulse is a very large force applied over a very 
        short period of time. Some examples are a ball hitting a wall or 
        cannon firing. Chipmunk treats impulses as if they occur 
        instantaneously by adding directly to the velocity of an object. 
        Both impulses and forces are affected the mass of an object. Doubling 
        the mass of the object will halve the effect.
        
        :Parameters:
            force : (x,y) or `Vec2d`
                Force to be applied
            point : (x,y) or `Vec2d`
                World point
        """
        cp.cpBodyApplyForceAtWorldPoint(self._body, force, point)
    
    def apply_force_at_local_point(self, force, point):
        """Add the local force force to body as if applied from the body 
        local point.
        
        :Parameters:
            force : (x,y) or `Vec2d`
                Force to be applied
            point : (x,y) or `Vec2d`
                Local point
        """
        cp.cpBodyApplyForceAtLocalPoint(self._body, force, point)
        
    def apply_impulse_at_world_point(self, impulse, point=(0, 0)):
        """Add the impulse impulse to body as if applied from the world point.
        
        :Parameters:
            impulse : (x,y) or `Vec2d`
                Impulse to be applied
            point : (x,y) or `Vec2d`
                World point
        """
        cp.cpBodyApplyImpulseAtWorldPoint(self._body, impulse, point)
    
    def apply_impulse_at_local_point(self, impulse, point=(0, 0)):
        """Add the local impulse impulse to body as if applied from the body 
        local point.
        
        :Parameters:
            impulse : (x,y) or `Vec2d`
                Impulse to be applied
            point : (x,y) or `Vec2d`
                Local point
        """
        cp.cpBodyApplyImpulseAtLocalPoint(self._body, impulse, point)
        
        
    def activate(self):
        """Reset the idle timer on a body.
        
        If it was sleeping, wake it and any other bodies it was touching.
        """
        cp.cpBodyActivate(self._body)
        
    def sleep(self):
        """Forces a body to fall asleep immediately even if it's in midair. 
        
        Cannot be called from a callback.
        """
        cp.cpBodySleep(self._body)    
        
    def sleep_with_group(self, body):
        """Force a body to fall asleep immediately along with other bodies 
        in a group.
        
        When objects in Chipmunk sleep, they sleep as a group of all objects 
        that are touching or jointed together. When an object is woken up, 
        all of the objects in its group are woken up. Body.sleep_with_group() 
        allows you group sleeping objects together. It acts identically to 
        Body.sleep() if you pass NULL as group by starting a new group. If 
        you pass a sleeping body for group, body will be awoken when group is 
        awoken. You can use this to initialize levels and start stacks of 
        objects in a pre-sleeping state.
        """
        cp.cpBodySleepWithGroup(self._body, body._body)
        
    def _is_sleeping(self):
        return cp.cpBodyIsSleeping(self._body)
    is_sleeping = property(_is_sleeping, 
        doc="""Returns true if the body is sleeping.""")
    
    
    def _set_type(self, body_type):
        cp.cpBodySetType(self._body, body_type)
    def _get_type(self):
        return cp.cpBodyGetType(self._body)
    body_type = property(_get_type
        , _set_type
        , doc="""The type of a body (DYNAMIC, KINEMATIC, STATIC).
        
        When changing an body to a dynamic body, the mass and moment of 
        inertia are recalculated from the shapes added to the body. Custom 
        calculated moments of inertia are not preseved when changing types. 
        This function cannot be called directly in a collision callback.
        """)
    
    
    def each_arbiter(self, func, *args, **kwargs):
        """Run func on each of the arbiters on this body.
        
            ``func(arbiter, *args, **kwargs) -> None``
            
            Callback Parameters
                arbiter : `Arbiter`
                    The Arbiter
                args
                    Optional parameters passed to the callback function.
                kwargs
                    Optional keyword parameters passed on to the callback function.
                    
        .. warning::
            
            Do not hold on to the Arbiter after the callback!                
        """
        
        def impl(body, _arbiter, _):
            arbiter = Arbiter(_arbiter, self._space)
            func(arbiter, *args, **kwargs)
            return 0
        f = cp.cpBodyArbiterIteratorFunc(impl)
        cp.cpBodyEachArbiter(self._body, f, None)
        
    def _get_constraints(self):
        return set(self._constraints)
    
    constraints = property(_get_constraints, 
        doc="""Get the constraints this body is attached to. 
        
        The body only keeps a weak referenece to the constraints and a 
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
        
        :Parameters:
            v : (x,y) or `Vec2d`
                Vector in body local coordinates
        """
        return cp.cpBodyLocalToWorld(self._body, v)
        
    def world_to_local(self, v):
        """Convert world space coordinates to body local coordinates
        
        :Parameters:
            v : (x,y) or `Vec2d`
                Vector in world space coordinates
        """
        return cp.cpBodyWorldToLocal(self._body, v)
        
    def velocity_at_world_point(self, point):
        """Get the absolute velocity of the rigid body at the given world 
        point
        
        It's often useful to know the absolute velocity of a point on the 
        surface of a body since the angular velocity affects everything 
        except the center of gravity.
        """
        return cp.cpBodyGetVelocityAtWorldPoint(self._body, point)
        
    def velocity_at_local_point(self, point):
        """ Get the absolute velocity of the rigid body at the given body 
        local point
        """
        return cp.cpBodyGetVelocityAtLocalPoint(self._body, point)
        
class Shape(object):
    """Base class for all the shapes. 
    
    You usually dont want to create instances of this class directly but use 
    one of the specialized shapes instead.
    """
    
    _space = None # Weak ref to the space holding this body (if any)
    
    _shapeid_counter = 1
    
    def __init__(self, shape=None):
        self._shape = shape
        self._shapecontents = self._shape.contents
        self._body = shape.body
    
    def __del__(self):
        try:
            cp.cpShapeFree(self._shape)
        except:
            pass
               
    def _get_shapeid(self):
        return cp.cpShapeGetUserData(self._shape)
    def _set_shapeid(self):
        cp.cpShapeSetUserData(self._shape, Shape._shapeid_counter)
        Shape._shapeid_counter += 1
    
    def _get_sensor(self):
        return cp.cpShapeGetSensor(self._shape)
    def _set_sensor(self, is_sensor):
        cp.cpShapeSetSensor(self._shape, is_sensor)
    sensor = property(_get_sensor, _set_sensor, 
        doc="""A boolean value if this shape is a sensor or not. 
        
        Sensors only call collision callbacks, and never generate real 
        collisions.
        """)
    
    def _get_collision_type(self):
        return cp.cpShapeGetCollisionType(self._shape)
    def _set_collision_type(self, t):
        cp.cpShapeSetCollisionType(self._shape, t)
    collision_type = property(_get_collision_type, _set_collision_type,
        doc="""User defined collision type for the shape. 
        
        See add_collisionpair_func function for more information on when to 
        use this property.
        """)

    def _get_filter(self):
        return cp.cpShapeGetFilter(self._shape)
    def _set_filter(self, f):
        cp.cpShapeSetFilter(self._shape, f)
    filter = property(_get_filter, _set_filter,
        doc="""Set the collision filter for this shape.""")    
                
    

    def _get_elasticity(self):
        return cp.cpShapeGetElasticity(self._shape)
    def _set_elasticity(self, e):
        cp.cpShapeSetElasticity(self._shape, e)
    elasticity = property(_get_elasticity, _set_elasticity, 
        doc="""Elasticity of the shape. 
        
        A value of 0.0 gives no bounce, while a value of 1.0 will give a 
        'perfect' bounce. However due to inaccuracies in the simulation 
        using 1.0 or greater is not recommended.
        """)

    def _get_friction(self):
        return cp.cpShapeGetFriction(self._shape)
    def _set_friction(self, u):
        cp.cpShapeSetFriction(self._shape, u)
    friction = property(_get_friction, _set_friction, 
        doc="""Friction coefficient. 
        
        pymunk uses the Coulomb friction model, a value of 0.0 is 
        frictionless.
        
        A value over 1.0 is perfectly fine.
        
        Some real world example values from wikipedia (Remember that 
        it is what looks good that is important, not the exact value).
        
        ==============  ======  ========
        Material        Other   Friction
        ==============  ======  ========
        Aluminium       Steel   0.61
        Copper          Steel   0.53
        Brass           Steel   0.51
        Cast iron       Copper  1.05
        Cast iron       Zinc    0.85
        Concrete (wet)  Rubber  0.30
        Concrete (dry)  Rubber  1.0 
        Concrete        Wood    0.62
        Copper          Glass   0.68
        Glass           Glass   0.94
        Metal           Wood    0.5
        Polyethene      Steel   0.2
        Steel           Steel   0.80
        Steel           Teflon  0.04
        Teflon (PTFE)   Teflon  0.04
        Wood            Wood    0.4
        ==============  ======  ========
        """)

    def _get_surface_velocity(self):
        return cp.cpShapeGetSurfaceVelocity(self._shape)
    def _set_surface_velocity(self, surface_v):
        cp.cpShapeSetSurfaceVelocity(self._shape, surface_v)
    surface_velocity = property(_get_surface_velocity, _set_surface_velocity, 
        doc="""The surface velocity of the object. 
        
        Useful for creating conveyor belts or players that move around. This 
        value is only used when calculating friction, not resolving the 
        collision.
        """)

    def _get_body(self):
        return self._body
    def _set_body(self, body):
        if self._body != None:
            self._body._shapes.remove(self)
        if body != None:
            body._shapes.add(self)
            self._shapecontents.body = body._body
        else:
            self._shapecontents.body = None
            
        self._body = body
        
    body = property(_get_body, _set_body,
        doc="""The body this shape is attached to. Can be set to None to 
        indicate that this shape doesnt belong to a body.""")

    def update(self, transform):
        """Update, cache and return the bounding box of a shape with an 
        explicit transformation.
        
        Useful if you have a shape without a body and want to use it for 
        querying.
        """
        bb = cp.cpShapeUpdate(self._shape, transform)
        return BB(bb)
        
    def cache_bb(self):
        """Update and returns the bouding box of this shape"""
        return BB(cp.cpShapeCacheBB(self._shape))

    def _get_bb(self):
        return BB(cp.cpShapeGetBB(self._shape))
        
    bb = property(_get_bb, doc="""The bounding box of the shape.
    
    Only guaranteed to be valid after Shape.cache_bb() or Space.step() is 
    called. Moving a body that a shape is connected to does not update it's 
    bounding box. For shapes used for queries that aren't attached to bodies, 
    you can also use Shape.update().
    """)
        
    def point_query(self, p):
        """Check if the given point lies within the shape."""
        info = cp.cpPointQueryInfo()
        info_p = ct.POINTER(cp.cpPointQueryInfo)(info)
        distance = cp.cpShapePointQuery(self._shape, p, info_p)
        ud = cp.cpShapeGetUserData(info.shape)
        assert ud == self._get_shapeid()
        x = PointQueryInfo(self, info.point, info.distance, info.gradient)
        return distance, x
        
        
    def segment_query(self, start, end, radius=0):
        """Check if the line segment from start to end intersects the shape. 
        """
        info = cp.cpSegmentQueryInfo()
        info_p = ct.POINTER(cp.cpSegmentQueryInfo)(info)
        r = cp.cpShapeSegmentQuery(self._shape, start, end, radius, info_p)
        if r:
            ud = cp.cpShapeGetUserData(info.shape)
            assert ud == self._get_shapeid()
            return SegmentQueryInfo(self, info.point, info.normal, info.alpha)
        else:
            return SegmentQueryInfo(None, info.point, info.normal, info.alpha)
            
    def _get_space(self):
        if self._space != None:
            return self._space._get_self() #ugly hack because of weakref
        else:
            return None
    space = property(_get_space, 
        doc="""Get the Space that shape has been added to (or None).""")
    
class Circle(Shape):
    """A circle shape defined by a radius
    
    This is the fastest and simplest collision shape
    """
    def __init__(self, body, radius, offset = (0, 0)):
        """body is the body attach the circle to, offset is the offset from the
        body's center of gravity in body local coordinates.
        
        It is legal to send in None as body argument to indicate that this 
        shape is not attached to a body.
        """
        
        self._body = body
        body_body = None if body is None else body._body
        if body != None: 
            body._shapes.add(self)
        
        self._shape = cp.cpCircleShapeNew(body_body, radius, offset)
        self._shapecontents = self._shape.contents
        self._cs = ct.cast(self._shape, ct.POINTER(cp.cpCircleShape))
        self._set_shapeid()
        
    def unsafe_set_radius(self, r):
        """Unsafe set the radius of the circle. 
    
        .. note:: 
            This change is only picked up as a change to the position 
            of the shape's surface, but not it's velocity. Changing it will 
            not result in realistic physical behavior. Only use if you know 
            what you are doing!
        """
        cp.cpCircleShapeSetRadius(self._shape, r)
        
    def _get_radius(self):
        return cp.cpCircleShapeGetRadius(self._shape)
    radius = property(_get_radius, doc="""The Radius of the circle""")

    def unsafe_set_offset(self, o):
        """Unsafe set the offset of the circle. 
    
        .. note:: 
            This change is only picked up as a change to the position 
            of the shape's surface, but not it's velocity. Changing it will 
            not result in realistic physical behavior. Only use if you know 
            what you are doing!
        """
        cp.cpCircleShapeSetOffset(self._shape, o)
    
    def _get_offset (self):
        return cp.cpCircleShapeGetOffset(self._shape)
    offset = property(_get_offset, doc="""Offset. (body space coordinates)""")

    
class Segment(Shape):
    """A line segment shape between two points
    
    Meant mainly as a static shape. Can be beveled in order to give them a 
    thickness.
    
    It is legal to send in None as body argument to indicate that this 
    shape is not attached to a body.
    """
    def __init__(self, body, a, b, radius):
        """Create a Segment
        
        :Parameters:
            body : `Body`
                The body to attach the segment to
            a : (x,y) or `Vec2d`
                The first endpoint of the segment
            b : (x,y) or `Vec2d`
                The second endpoint of the segment
            radius : float
                The thickness of the segment
        """
        self._body = body
        body_body = None if body is None else body._body
        if body != None: 
            body._shapes.add(self)
        self._shape = cp.cpSegmentShapeNew(body_body, a, b, radius)
        self._shapecontents = self._shape.contents
        self._set_shapeid()
    
    def unsafe_set_a(self, a):
        """Set the first of the two endpoints for this segment

        .. note:: 
            This change is only picked up as a change to the position 
            of the shape's surface, but not it's velocity. Changing it will 
            not result in realistic physical behavior. Only use if you know 
            what you are doing!
        """
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.a = a
    def _get_a(self):
        return cp.cpSegmentShapeGetA(self._shape)
    a = property(_get_a,  
        doc="""The first of the two endpoints for this segment""")

    def unsafe_set_b(self, b):
        """Set the second of the two endpoints for this segment

        .. note:: 
            This change is only picked up as a change to the position 
            of the shape's surface, but not it's velocity. Changing it will 
            not result in realistic physical behavior. Only use if you know 
            what you are doing!
        """
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.b = b
    def _get_b(self):
        return cp.cpSegmentShapeGetB(self._shape)
    b = property(_get_b,  
        doc="""The second of the two endpoints for this segment""")
    
    def _get_normal(self):
        return cp.cpSegmentShapeGetNormal(self._shape)
    normal = property(_get_normal,
        doc="""The normal""")
    
    def unsafe_set_radius(self, r):
        """Set the radius of the segment

        .. note:: 
            This change is only picked up as a change to the position 
            of the shape's surface, but not it's velocity. Changing it will 
            not result in realistic physical behavior. Only use if you know 
            what you are doing!
        """
        ct.cast(self._shape, ct.POINTER(cp.cpSegmentShape)).contents.r = r
    def _get_radius(self):
        return cp.cpSegmentShapeGetRadius(self._shape)
    radius = property(_get_radius,  
        doc="""The radius/thickness of the segment""")

    def set_neighbors(self, prev, next):
        """When you have a number of segment shapes that are all joined 
        together, things can still collide with the "cracks" between the 
        segments. By setting the neighbor segment endpoints you can tell 
        Chipmunk to avoid colliding with the inner parts of the crack.
        """
        cp.cpSegmentShapeSetNeighbors(self._shape, prev, next)
    
class Poly(Shape):
    """A convex polygon shape
    
    Slowest, but most flexible collision shape.

    It is legal to send in None as body argument to indicate that this 
    shape is not attached to a body.    
    """

    def _init():
        pass
    
    def __init__(self, body, vertices, transform=None, radius=0):
        """Create a polygon.
        
            A convex hull will be calculated from the vertexes automatically.
        
            body : `Body`
                The body to attach the poly to
            vertices : [(x,y)] or [`Vec2d`]
                Define a convex hull of the polygon with a counterclockwise
                winding.
            transform : `Transform`
                Transform will be applied to every vertex.
            radius : int
                Set the radius of the poly shape. Adding a small radius will 
                bevel the corners and can significantly reduce problems where 
                the poly gets stuck on seams in your geometry.
        """
        
        self._body = body
                
        body_body = None if body is None else body._body
        if body != None: 
            body._shapes.add(self)
        
        if transform == None:
            transform = Transform.identity()
        self._shape = cp.cpPolyShapeNew(body_body, len(vertices), self._to_verts(vertices), transform, radius)
        self._shapecontents = self._shape.contents
        self._set_shapeid()

    def _to_verts(self, vertices):
        verts = (Vec2d * len(vertices))
        verts = verts(Vec2d(0,0))
        for (i,v) in enumerate(vertices):
            verts[i].x = vertices[i][0]
            verts[i].y = vertices[i][1] 
        return verts
        
    def unsafe_set_radius(self, radius):
        """Unsafe set the radius of the poly.

        .. note:: 
            This change is only picked up as a change to the position 
            of the shape's surface, but not it's velocity. Changing it will 
            not result in realistic physical behavior. Only use if you know 
            what you are doing!
        """
        cp.cpPolyShapeSetRadius(self._shape, radius)    
    
    def _get_radius(self):
        return cp.cpPolyShapeGetRadius(self._shape)
    radius = property(_get_radius, 
        doc="""The radius of the poly shape. Extends the poly in all 
        directions with the given radius""")
  
    @staticmethod
    def create_box(body, size=(10,10), radius=0): 
        """Convenience function to create a box.
        
        The boxes will always be centered at the center of gravity of the 
        body you are attaching them to.  If you want to create an off-center 
        box, you will need to use the normal constructor Poly(...).

            body : `Body`
                The body to attach the poly to
            size : `(w,h)` or `Vec2d` or `BB`
                Size of the box
            radius : `float`
                Adding a small radius will bevel the corners and can 
                significantly reduce problems where the box gets stuck on 
                seams in your geometry.
        
        """
        
        self = Poly.__new__(Poly)
        
        self._body = body
                
        body_body = None if body is None else body._body
        if body != None: 
            body._shapes.add(self)
        
        if isinstance(size, BB):
            self._shape = cp.cpBoxShapeNew2(body_body, size._bb, radius)
        else:
            self._shape = cp.cpBoxShapeNew(body_body, size[0], size[1], radius)
            
        self._shapecontents = self._shape.contents
        self._set_shapeid()
        
        return self
                
    def get_vertices(self): 
        """Get the vertices in world coordinates for the polygon
        
        :return: [`Vec2d`] in world coords
        """
        verts = []
        l = cp.cpPolyShapeGetCount(self._shape)
        for i in range(l):
            verts.append(cp.cpPolyShapeGetVert(self._shape, i))
        return verts
        
    def unsafe_set_vertices(self, vertices, transform=None):
        """Unsafe set the vertices of the poly. 
    
        .. note:: 
            This change is only picked up as a change to the position 
            of the shape's surface, but not it's velocity. Changing it will 
            not result in realistic physical behavior. Only use if you know 
            what you are doing!
        """
        if transform == None:
            transform = Transform.identity()
        cp.cpPolyShapeSetVerts(self._shape, len(vertices), self._to_verts(vertices), transform)
        

class PointQueryInfo(object):
    """PointQueryInfo holds the result of a point query made on a Shape or 
    Space.
    """
    def __init__(self, shape, point, distance, gradient):
        """You shouldn't need to initialize PointQueryInfo objects 
        manually.
        """
        self._shape = shape
        self._point = point
        self._distance = distance
        self._gradient = gradient
        
    def __repr__(self):
        return 'PointQueryInfo(%s,%s,%s,%s)' % (self.shape, self.point, self.distance, self.gradient)

    shape = property(lambda self:self._shape,
        doc = """The nearest shape, None if no shape was within range.""")
        
    point = property(lambda self:self._point,
        doc = """The closest point on the shape's surface. (in world space 
        coordinates)
        """)
    
    distance = property(lambda self:self._distance,
        doc = """The distance to the point. The distance is negative if the 
        point is inside the shape.
        """)
        
    gradient = property(lambda self:self._gradient,
        doc = """The gradient of the signed distance function.
        
        The value should be similar to 
        PointQueryInfo.point/PointQueryInfo.distance, but accurate even for 
        very small values of info.distance.
        """)
       
    
class SegmentQueryInfo(object):
    """Segment queries return more information than just a simple yes or no, 
    they also return where a shape was hit and it's surface normal at the hit 
    point. This object hold that information.
    
    To test if the query hit something, check if 
    SegmentQueryInfo.shape == None or not.
    
    Segment queries are like ray casting, but because not all spatial indexes 
    allow processing infinitely long ray queries it is limited to segments. 
    In practice this is still very fast and you don't need to worry too much 
    about the performance as long as you aren't using extremely long segments 
    for your queries.

    """
    def __init__(self, shape, point, normal, alpha):
        """You shouldn't need to initialize SegmentQueryInfo objects 
        manually.
        """
        self._shape = shape
        self._point = point
        self._normal = normal
        self._alpha = alpha
        
    def __repr__(self):
        return "SegmentQueryInfo(%s, %s, %s, %s)" % (self.shape, self.point, self.normal, self.alpha)
            
    shape = property(lambda self: self._shape,
        doc = """Shape that was hit, or None if no collision occured""")
    
    point = property(lambda self: self._point,
        doc = """The point of impact.""")
    
    normal = property(lambda self: self._normal,
        doc = """The normal of the surface hit.""")
    
    alpha = property(lambda self: self._alpha,
        doc = """The normalized distance along the query segment in the 
        range [0, 1]
        """)
    
def moment_for_circle(mass, inner_radius, outer_radius, offset=(0, 0)):
    """Calculate the moment of inertia for a hollow circle
    
    inner_radius and outer_radius are the inner and outer diameters. 
    (A solid circle has an inner diameter of 0)
    """
    return cp.cpMomentForCircle(mass, inner_radius, outer_radius, offset)

def moment_for_segment(mass, a, b, radius):
    """ Calculate the moment of inertia for a line segment
    
    The endpoints a and b are relative to the body
    """
    return cp.cpMomentForSegment(mass, a, b, radius)
    
def moment_for_box(mass, width, height):
    """Calculate the moment of inertia for a solid box centered on the body"""
    return cp.cpMomentForBox(mass, width, height)
    
def moment_for_poly(mass, vertices,  offset=(0, 0), radius=0):
    """Calculate the moment of inertia for a solid polygon shape.
    
    Assumes the polygon center of gravity is at its centroid. The offset is 
    added to each vertex.
    """
    verts = (Vec2d * len(vertices))
    verts = verts(Vec2d(0, 0))
    for (i, vertex) in enumerate(vertices):
        verts[i].x = vertex[0]
        verts[i].y = vertex[1]
    return cp.cpMomentForPoly(mass, len(verts), verts, offset, radius)
    
def area_for_circle(inner_radius, outer_radius):
    """Area of a hollow circle."""
    return cp.cpAreaForCircle(inner_radius, outer_radius)

def area_for_segment(a, b, radius):
    """Area of a beveled segment. 
    
    (Will always be zero if radius is zero)
    """
    return cp.cpAreaForSegment(a, b, radius)

def area_for_poly(vertices, radius=0):
    """Signed area of a polygon shape.
    
    Returns a negative number for polygons with a clockwise winding.
    """
    verts = (Vec2d * len(vertices))
    verts = verts(Vec2d(0, 0))
    for (i, vertex) in enumerate(vertices):
        verts[i].x = vertex[0]
        verts[i].y = vertex[1]
    return cp.cpAreaForPoly(len(verts), verts, radius)


    
def reset_shapeid_counter():
    """Reset the internal shape counter
    
    pymunk keeps a counter so that every new shape is given a unique hash 
    value to be used in the spatial hash. Because this affects the order in 
    which the collisions are found and handled, you should reset the shape 
    counter every time you populate a space with new shapes. If you don't, 
    there might be (very) slight differences in the simulation.
    """
    pass
    #cp.cpResetShapeIdCounter()

    
class Contact(object):
    """Contact information"""
    def __init__(self, _contact):
        """Initialize a Contact object from the Chipmunk equivalent struct
        
        .. note:: 
            You should never need to create an instance of this class directly.
        """
        self._point = _contact.point
        self._normal = _contact.normal
        self._dist = _contact.dist
        #self._contact = contact

    def __repr__(self):
        return "Contact(p: %s, n: %s, d: %s)" % (self.position, self.normal, self.distance)
        
    def _get_position(self):
        return self._point
    position = property(_get_position, doc="""Contact position""")

    def _get_normal(self):
        return self._normal
    normal = property(_get_normal, doc="""Contact normal""")

    def _get_distance(self):
        return self._dist
    distance = property(_get_distance, doc="""Penetration distance""")
    


class Arbiter(object):
    """Arbiters are collision pairs between shapes that are used with the 
    collision callbacks.
    
    .. Warning::
        Because arbiters are handled by the space you should never 
        hold onto a reference to an arbiter as you don't know when it will be 
        destroyed! Use them within the callback where they are given to you 
        and then forget about them or copy out the information you need from 
        them.
    """
    def __init__(self, _arbiter, space):
        """Initialize an Arbiter object from the Chipmunk equivalent struct 
        and the Space.
        
        .. note::
            You should never need to create an instance of this class directly.
        """

        self._arbiter = _arbiter
        self._arbitercontents = self._arbiter.contents
        self._space = space
        self._contacts = None # keep a lazy loaded cache of converted contacts
    
    def _get_contacts(self):
        point_set = cp.cpArbiterGetContactPointSet(self._arbiter)
        
        if self._contacts is None:
            self._contacts = []
            for i in range(point_set.count):
                self.contacts.append(Contact(point_set.points[i]))
        return self._contacts
    contacts = property(_get_contacts, 
        doc="""Information on the contact points between the objects. Return [`Contact`]""")
        
    def _get_shapes(self):
        shapeA_p = ct.POINTER(cp.cpShape)()
        shapeB_p = ct.POINTER(cp.cpShape)()
        
        cpffi.cpArbiterGetShapes(self._arbiter, shapeA_p, shapeB_p)
    
        a, b = self._space._get_shape(shapeA_p), self._space._get_shape(shapeB_p)
        return a, b
        
    shapes = property(_get_shapes, 
        doc="""Get the shapes in the order that they were defined in the 
        collision handler associated with this arbiter""")
            
    def _get_elasticity(self):
        return self._arbiter.contents.e
    def _set_elasticity(self, elasticity):
        self._arbiter.contents.e = elasticity
    elasticity = property(_get_elasticity, _set_elasticity, 
        doc="""Elasticity""")

    def _get_friction(self):
        return self._arbiter.contents.u
    def _set_friction(self, friction):
        self._arbiter.contents.u = friction
    friction = property(_get_friction, _set_friction, doc="""Friction""")
    
    def _get_surface_velocity(self):
        return self._arbiter.contents.surface_vr
    surface_velocity = property(_get_surface_velocity, 
        doc="""Used for surface_v calculations, implementation may change""")

    def _get_total_impulse(self):
        return cp.cpArbiterTotalImpulse(self._arbiter)
    total_impulse = property(_get_total_impulse,
        doc="""Returns the impulse that was applied this step to resolve the 
        collision.
        
        This property should only be called from a post-solve, post-step""")
    
    def _get_total_impulse_with_friction(self):
        return cp.cpArbiterTotalImpulseWithFriction(self._arbiter)
    total_impulse_with_friction = property(_get_total_impulse_with_friction,
        doc="""Returns the impulse with friction that was applied this step to 
        resolve the collision.
        
        This property should only be called from a post-solve, post-step""")
        
    def _get_total_ke(self):
        return cp.cpArbiterTotalKE(self._arbiter)
    total_ke = property(_get_total_ke,
        doc="""The amount of energy lost in a collision including static, but 
        not dynamic friction.
        
        This property should only be called from a post-solve, post-step""")
        
    def _get_stamp(self):
        return self._arbiter.contents.stamp
    stamp = property(_get_stamp, 
        doc="""Time stamp of the arbiter. (from the space)""")
    
    def _get_is_first_contact(self):
        return bool(cpffi.cpArbiterIsFirstContact(self._arbiter))
    is_first_contact = property(_get_is_first_contact,
        doc="""Returns true if this is the first step that an arbiter existed. 
        You can use this from preSolve and postSolve to know if a collision 
        between two shapes is new without needing to flag a boolean in your 
        begin callback.""")
        
    
    
class BB(object):
    """Simple bounding box. 
    
    Stored as left, bottom, right, top values.
    """
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
            self._bb = cpffi.cpBBNew(args[0], args[1], args[2], args[3])
    
    @staticmethod
    def newForCircle(p, r):
        """Convenience constructor for making a BB fitting a circle at 
        position p with radius r.
        """
        bb_ = cpffi.cpBBNewForCircle(p, r)
        return BB(bb_)
        
    def __repr__(self):
        return 'BB(%s, %s, %s, %s)' % (self.left, self.bottom, self.right, self.top)
        
    def __eq__(self, other):
        return self.left == other.left and self.bottom == other.bottom and \
            self.right == other.right and self.top == other.top
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    left = property(lambda self: self._bb.l)
    bottom = property(lambda self: self._bb.b)
    right = property(lambda self: self._bb.r)
    top = property(lambda self: self._bb.t)
    
    def intersects(self, other):
        """Returns true if the bounding boxes intersect"""
        return bool(cpffi.cpBBIntersects(self._bb, other._bb))

    def intersects_segment(self, a, b):
        """Returns true if the segment defined by endpoints a and b 
        intersect this bb."""
        return bool(cpffi.cpBBIntersectsSegment(self._bb, a, b))
        
    def contains(self, other):
        """Returns true if bb completley contains the other bb"""
        return bool(cpffi.cpBBContainsBB(self._bb, other._bb))
        
    def contains_vect(self, v):
        """Returns true if this bb contains the vector v"""
        return bool(cpffi.cpBBContainsVect(self._bb, v))
        
    def merge(self, other):
        """Return the minimal bounding box that contains both this bb and the 
        other bb
        """
        return BB(cpffi.cpBBMerge(self._bb, other._bb))
        
    def expand(self, v):
        """Return the minimal bounding box that contans both this bounding box 
        and the vector v
        """
        return BB(cpffi.cpBBExpand(self._bb, v))
    
    def center(self):
        """Return the center"""
        return cpffi.cpBBCenter(self._bb)
    
    def area(self):
        """Return the area"""
        return cpffi.cpBBArea(self._bb)
        
    def merged_area(self, other):
        """Merges this and other then returns the area of the merged bounding 
        box.
        """
        return cpffi.cpBBMergedArea(self._bb, other._bb)
    
    def segment_query(self, a, b):
        """Returns the fraction along the segment query the BB is hit. 
        
        Returns infinity if it doesnt hit
        """
        return cpffi.cpBBSegmentQuery(self._bb, a, b)
        
    def clamp_vect(self, v):
        """Returns a copy of the vector v clamped to the bounding box"""
        return cpffi.cpBBClampVect(self._bb, v)
    
    def wrap_vect(self, v):
        """Returns a copy of v wrapped to the bounding box.
        
        That is, BB(0,0,10,10).wrap_vect((5,5)) == Vec2d(10,10)
        """
        return cpffi.cpBBWrapVect(self._bb, v)
 
        
#del cp, ct, u

