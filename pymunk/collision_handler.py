__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from .space import Space

from ._chipmunk_cffi import ffi, lib
from .arbiter import Arbiter

_CollisionCallback = Callable[[Arbiter, "Space", dict[Any, Any]], None]


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
        self._userData = ffi.new_handle(self)

        self._handler = _handler
        self._handler.userData = self._userData

        self._space = space
        self._begin: _CollisionCallback = CollisionHandler.do_nothing
        self._pre_solve: _CollisionCallback = CollisionHandler.do_nothing
        self._post_solve: _CollisionCallback = CollisionHandler.do_nothing
        self._separate: _CollisionCallback = CollisionHandler.do_nothing

        self._data: dict[Any, Any] = {}

    @property
    def data(self) -> dict[Any, Any]:
        """Data property that get passed on into the
        callbacks.

        data is a dictionary and you can not replace it, only fill it with data.

        Usefull if the callback needs some extra data to perform its function.
        """
        return self._data

    @property
    def begin(self) -> _CollisionCallback:
        """Two shapes just started touching for the first time this step.

        ``func(arbiter, space, data)``

        Return true from the callback to process the collision normally or
        false to cause pymunk to ignore the collision entirely. If you return
        false, the `pre_solve` and `post_solve` callbacks will never be run,
        but you will still recieve a separate event when the shapes stop
        overlapping.
        """
        return self._begin

    @begin.setter
    def begin(self, func: _CollisionCallback) -> None:
        self._begin = func

        if self._begin == CollisionHandler.do_nothing:
            self._handler.beginFunc = ffi.addressof(lib, "DoNothing")
        else:
            self._handler.beginFunc = lib.ext_cpCollisionBeginFunc

    @property
    def pre_solve(self) -> _CollisionCallback:
        """Two shapes are touching during this step.

        ``func(arbiter, space, data)``

        Additionally, you may
        override collision values using Arbiter.friction, Arbiter.elasticity
        or Arbiter.surfaceVelocity to provide custom friction, elasticity,
        or surface velocity values. See Arbiter for more info.
        """
        return self._pre_solve

    @pre_solve.setter
    def pre_solve(self, func: _CollisionCallback) -> None:
        self._pre_solve = func

        if self._pre_solve == CollisionHandler.do_nothing:
            self._handler.preSolveFunc = ffi.addressof(lib, "DoNothing")
        else:
            self._handler.preSolveFunc = lib.ext_cpCollisionPreSolveFunc

    @property
    def post_solve(self) -> _CollisionCallback:
        """Two shapes are touching and their collision response has been
        processed.

        ``func(arbiter, space, data)``

        You can retrieve the collision impulse or kinetic energy at this
        time if you want to use it to calculate sound volumes or damage
        amounts. See Arbiter for more info.
        """
        return self._post_solve

    @post_solve.setter
    def post_solve(self, func: _CollisionCallback) -> None:
        self._post_solve = func

        if self._post_solve == CollisionHandler.do_nothing:
            self._handler.postSolveFunc = ffi.addressof(lib, "DoNothing")
        else:
            self._handler.postSolveFunc = lib.ext_cpCollisionPostSolveFunc

    @property
    def separate(self) -> _CollisionCallback:
        """Two shapes have just stopped touching for the first time this
        step.

        ``func(arbiter, space, data)``

        To ensure that begin()/separate() are always called in balanced
        pairs, it will also be called when removing a shape while its in
        contact with something or when de-allocating the space.
        """
        return self._separate

    @separate.setter
    def separate(self, func: _CollisionCallback) -> None:
        self._separate = func

        if self._separate == CollisionHandler.do_nothing:
            self._handler.separateFunc = ffi.addressof(lib, "DoNothing")
        else:
            self._handler.separateFunc = lib.ext_cpCollisionSeparateFunc

    @staticmethod
    def do_nothing(arbiter: Arbiter, space: "Space", data: dict[Any, Any]) -> None:
        """The default do nothing method used for the post_solve and seprate
        callbacks.

        Note that its more efficient to set this method than to define your own
        do nothing method.
        """
        return
