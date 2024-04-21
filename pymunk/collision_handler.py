__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

if TYPE_CHECKING:
    from .space import Space

from ._chipmunk_cffi import ffi, lib
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
        self._userData = ffi.new_handle(self)

        self._handler = _handler
        self._handler.userData = self._userData

        self._space = space
        self._begin: Optional[_CollisionCallbackBool] = None
        self._pre_solve: Optional[_CollisionCallbackBool] = None
        self._post_solve: Optional[_CollisionCallbackNoReturn] = None
        self._separate: Optional[_CollisionCallbackNoReturn] = None

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
        self._begin = func
        self._handler.beginFunc = lib.ext_cpCollisionBeginFunc

    def _get_begin(self) -> Optional[_CollisionCallbackBool]:
        return self._begin

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
        self._pre_solve = func
        self._handler.preSolveFunc = lib.ext_cpCollisionPreSolveFunc

    def _get_pre_solve(self) -> Optional[Callable[[Arbiter, "Space", Any], bool]]:
        return self._pre_solve

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

        self._post_solve = func
        self._handler.postSolveFunc = lib.ext_cpCollisionPostSolveFunc

    def _get_post_solve(self) -> Optional[_CollisionCallbackNoReturn]:
        return self._post_solve

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
        self._separate = func
        self._handler.separateFunc = lib.ext_cpCollisionSeparateFunc

    def _get_separate(self) -> Optional[_CollisionCallbackNoReturn]:
        return self._separate

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
