__version__ = "$Id$"
__docformat__ = "reStructuredText"

import sys
import warnings
from . import _chipmunk as cp
from ._arbiter import Arbiter

class CollisionHandler(object):
    """A collision handler is a set of 4 function callbacks for the different
    collision events that pymunk recognizes.

    Collision callbacks are closely associated with Arbiter objects. You
    should familiarize yourself with those as well.

    Note #1: Shapes tagged as sensors (Shape.sensor == true) never generate
    collisions that get processed, so collisions between sensors shapes and
    other shapes will never call the postSolve() callback. They still
    generate begin(), and separate() callbacks, and the preSolve() callback
    is also called every frame even though there is no collision response.
    Note #2: preSolve() callbacks are called before the sleeping algorithm
    runs. If an object falls asleep, its postSolve() callback won't be
    called until it's reawoken.
    """
    def __init__(self, _handler, space):
        """Initialize a CollisionHandler object from the Chipmunk equivalent
        struct and the Space.

        .. note::
            You should never need to create an instance of this class directly.
        """
        self._handler = _handler
        self._space = space
        self._begin = None
        self._pre_solve = None
        self._post_solve = None
        self._separate = None

    def _get_cf(self, func, function_type, *args, **kwargs):
        def cf(_arbiter, _space, _data):
            arbiter = Arbiter(_arbiter, self._space)
            x = func(self._space, arbiter, *args, **kwargs)

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

    def _set_begin(self, f):
        self._begin = f
        cf = self._get_cf(f, cp.cpCollisionBeginFunc)
        self._handler.contents.beginFunc = cf

    def _get_begin(self):
        return self._begin

    begin = property(_get_begin, _set_begin,
        doc="""Two shapes just started touching for the first time this step.

        ``func(space, arbiter, *args, **kwargs) -> bool``

        Return true from the callback to process the collision normally or
        false to cause pymunk to ignore the collision entirely. If you return
        false, the preSolve() and postSolve() callbacks will never be run,
        but you will still recieve a separate event when the shapes stop
        overlapping.
        """)

    def _set_pre_solve(self, f):
        self._pre_solve = f
        cf = self._get_cf(f, cp.cpCollisionPreSolveFunc)
        self._handler.contents.preSolveFunc = cf

    def _get_pre_solve(self):
        return self._pre_solve

    pre_solve = property(_get_pre_solve, _set_pre_solve,
        doc="""Two shapes are touching during this step.

        ``func(space, arbiter, *args, **kwargs) -> bool``

        Return false from the callback to make pymunk ignore the collision
        this step or true to process it normally. Additionally, you may
        override collision values using Arbiter.friction, Arbiter.elasticity
        or Arbiter.surfaceVelocity to provide custom friction, elasticity,
        or surface velocity values. See Arbiter for more info.
        """)

    def _set_post_solve(self, f):
        self._post_solve = f
        cf = self._get_cf(f, cp.cpCollisionPostSolveFunc)
        self._handler.contents.postSolveFunc = cf

    def _get_post_solve(self):
        return self._post_solve

    post_solve = property(_get_post_solve, _set_post_solve,
        doc="""Two shapes are touching and their collision response has been
        processed.

        ``func(space, arbiter, *args, **kwargs)``

        You can retrieve the collision impulse or kinetic energy at this
        time if you want to use it to calculate sound volumes or damage
        amounts. See Arbiter for more info.
        """)

    def _set_separate(self, f):
        self._separate = f
        cf = self._get_cf(f, cp.cpCollisionSeparateFunc)
        self._handler.contents.separateFunc = cf

    def _get_separate(self):
        return self._separate

    separate = property(_get_separate, _set_separate,
        doc="""Two shapes have just stopped touching for the first time this
        step.

        ``func(space, arbiter, *args, **kwargs)``

        To ensure that begin()/separate() are always called in balanced
        pairs, it will also be called when removing a shape while its in
        contact with something or when deallocating the space.
        """)
