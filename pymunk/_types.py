from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .vec2d import Vec2d

_Vec2dOrTuple = Union[tuple[float, float], list[float], "Vec2d"]
_Vec2dOrFloat = Union[tuple[float, float], list[float], "Vec2d", float]
