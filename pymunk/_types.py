from typing import TYPE_CHECKING, List, Tuple, Union

if TYPE_CHECKING:
    from .vec2d import Vec2d

_Vec2dOrTuple = Union[Tuple[float, float], List[float], "Vec2d"]
_Vec2dOrFloat = Union[Tuple[float, float], List[float], "Vec2d", float]
