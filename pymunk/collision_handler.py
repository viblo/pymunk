__version__ = "$Id$"
__docformat__ = "reStructuredText"

import warnings
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

if TYPE_CHECKING:
    from .space import Space

from ._chipmunk_cffi import ffi
from .arbiter import Arbiter

_CollisionCallbackBool = Callable[[Arbiter, "Space", Any], bool]
_CollisionCallbackNoReturn = Callable[[Arbiter, "Space", Any], None]


class CollisionHandler(object):
    """A collision handler is a set of 4 function callbacks for the different
    collision events that Pymunk recognizes.

    Collision callbacks are closely associated with Arbiter objects. You
    should familiarize yourself with those as well.

    Note #1: Shapes tagged as sensors (Shape.sensor == true) never generate
    collisions that get processed, so collisions between sensors shapes and
    other shapes will never call the post_solve() callback. They still
    generate begin(), and separate() callbacks, and the pre_solve() callback
    is also called every frame even though there is no collision response.
    Note #2: pre_solve() callbacks are called before the sleeping algorithm
    runs. If an object falls asleep, its post_solve() callback won't be
    called until it's re-awoken.
    """

    def __init__(self, _handler: Any, space: "Space") -> None:
        """Initialize a CollisionHandler object from the Chipmunk equivalent
        struct and the Space.

        .. note::
            You should never need to create an instance of this class directly.
        """
        self._handler = _handler
        self._space = space
        self._begin = None
        self._begin_base: Optional[_CollisionCallbackBool] = None  # For pickle
        self._pre_solve = None
        self._pre_solve_base: Optional[_CollisionCallbackBool] = None  # For pickle
        self._post_solve = None
        self._post_solve_base: Optional[_CollisionCallbackNoReturn] = None  # For pickle
        self._separate = None
        self._separate_base: Optional[_CollisionCallbackNoReturn] = None  # For pickle

        self._data: Dict[Any, Any] = {}

    def _reset(self) -> None:
        def allways_collide(arb: Arbiter, space: "Space", data: Any) -> bool:
            return True

        def do_nothing(arb: Arbiter, space: "Space", data: Any) -> None:
            return

        self.begin = allways_collide
        self.pre_solve = allways_collide
        self.post_solve = do_nothing
        self.separate = do_nothing

    @property
    def data(self) -> Dict[Any, Any]:
        """Data property that get passed on into the
        callbacks.

        data is a dictionary and you can not replace it, only fill it with data.

        Usefull if the callback needs some extra data to perform its function.
        """
        return self._data

    def _set_begin(self, func: Callable[[Arbiter, "Space", Any], bool]) -> None:
        @ffi.callback("cpCollisionBeginFunc")
        def cf(_arb: ffi.CData, _space: ffi.CData, _: ffi.CData) -> bool:
            x = func(Arbiter(_arb, self._space), self._space, self._data)
            if isinstance(x, bool):
                return x

            func_name = func.__code__.co_name
            filename = func.__code__.co_filename
            lineno = func.__code__.co_firstlineno

            warnings.warn_explicit(
                "Function '" + func_name + "' should return a bool to"
                " indicate if the collision should be processed or not when"
                " used as 'begin' or 'pre_solve' collision callback.",
                UserWarning,
                filename,
                lineno,
                func.__module__,
            )
            return True

        self._begin = cf
        self._begin_base = func
        self._handler.beginFunc = cf

    def _get_begin(self) -> Optional[_CollisionCallbackBool]:
        return self._begin_base

    begin = property(
        _get_begin,
        _set_begin,
        doc="""Two shapes just started touching for the first time this step.

        ``func(arbiter, space, data) -> bool``

        Return true from the callback to process the collision normally or
        false to cause pymunk to ignore the collision entirely. If you return
        false, the `pre_solve` and `post_solve` callbacks will never be run,
        but you will still recieve a separate event when the shapes stop
        overlapping.
        """,
    )

    def _set_pre_solve(self, func: _CollisionCallbackBool) -> None:
        @ffi.callback("cpCollisionPreSolveFunc")
        def cf(_arb: ffi.CData, _space: ffi.CData, _: ffi.CData) -> bool:
            x = func(Arbiter(_arb, self._space), self._space, self._data)
            if isinstance(x, int):
                return x

            func_name = func.__code__.co_name
            filename = func.__code__.co_filename
            lineno = func.__code__.co_firstlineno

            warnings.warn_explicit(
                "Function '" + func_name + "' should return a bool to"
                " indicate if the collision should be processed or not when"
                " used as 'begin' or 'pre_solve' collision callback.",
                UserWarning,
                filename,
                lineno,
                func.__module__,
            )
            return True

        self._pre_solve = cf
        self._pre_solve_base = func
        self._handler.preSolveFunc = cf

    def _get_pre_solve(self) -> Optional[Callable[[Arbiter, "Space", Any], bool]]:
        return self._pre_solve_base

    pre_solve = property(
        _get_pre_solve,
        _set_pre_solve,
        doc="""Two shapes are touching during this step.

        ``func(arbiter, space, data) -> bool``

        Return false from the callback to make pymunk ignore the collision
        this step or true to process it normally. Additionally, you may
        override collision values using Arbiter.friction, Arbiter.elasticity
        or Arbiter.surfaceVelocity to provide custom friction, elasticity,
        or surface velocity values. See Arbiter for more info.
        """,
    )

    def _set_post_solve(self, func: _CollisionCallbackNoReturn) -> None:
        @ffi.callback("cpCollisionPostSolveFunc")
        def cf(_arb: ffi.CData, _space: ffi.CData, _: ffi.CData) -> None:
            func(Arbiter(_arb, self._space), self._space, self._data)

        self._post_solve = cf
        self._post_solve_base = func
        self._handler.postSolveFunc = cf

    def _get_post_solve(self) -> Optional[_CollisionCallbackNoReturn]:
        return self._post_solve_base

    post_solve = property(
        _get_post_solve,
        _set_post_solve,
        doc="""Two shapes are touching and their collision response has been
        processed.

        ``func(arbiter, space, data)``

        You can retrieve the collision impulse or kinetic energy at this
        time if you want to use it to calculate sound volumes or damage
        amounts. See Arbiter for more info.
        """,
    )

    def _set_separate(self, func: _CollisionCallbackNoReturn) -> None:
        @ffi.callback("cpCollisionSeparateFunc")
        def cf(_arb: ffi.CData, _space: ffi.CData, _: ffi.CData) -> None:
            try:
                # this try is needed since a separate callback will be called
                # if a colliding object is removed, regardless if its in a
                # step or not.
                self._space._locked = True
                func(Arbiter(_arb, self._space), self._space, self._data)
            finally:
                self._space._locked = False

        self._separate = cf
        self._separate_base = func
        self._handler.separateFunc = cf

    def _get_separate(self) -> Optional[_CollisionCallbackNoReturn]:
        return self._separate_base

    separate = property(
        _get_separate,
        _set_separate,
        doc="""Two shapes have just stopped touching for the first time this
        step.

        ``func(arbiter, space, data)``

        To ensure that begin()/separate() are always called in balanced
        pairs, it will also be called when removing a shape while its in
        contact with something or when de-allocating the space.
        """,
    )
