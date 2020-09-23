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

"""This module contain the Vec2d class that is used in all of pymunk when a
vector is needed.

The Vec2d class is used almost everywhere in pymunk for 2d coordinates and
vectors, for example to define gravity vector in a space. However, pymunk is
smart enough to convert tuples or tuple like objects to Vec2ds so you usually
do not need to explicitly do conversions if you happen to have a tuple::

    >>> import pymunk
    >>> space = pymunk.Space()
    >>> space.gravity
    Vec2d(0.0, 0.0)
    >>> space.gravity = 3,5
    >>> space.gravity
    Vec2d(3.0, 5.0)
    >>> space.gravity += 2,6
    >>> space.gravity
    Vec2d(5.0, 11.0)

More examples::

    >>> from pymunk.vec2d import Vec2d
    >>> Vec2d(7.3, 4.2)
    Vec2d(7.3, 4.2)
    >>> Vec2d((7.3, 4.2))
    Vec2d(7.3, 4.2)
    >>> Vec2d(7.3, 4.2) + Vec2d((1,2))
    Vec2d(8.3, 6.2)

"""
__docformat__ = "reStructuredText"

import math
import operator
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

# from ._types import _Vec2dOrFloat, _Vec2dOrTuple
_Vec2dOrFloat = Any
_Vec2dOrTuple = Any
__all__ = ["Vec2d"]

# _T_co = TypeVar('T', Sequence[float], covariant=True)


class Vec2d(Sequence[float]):
    """2d vector class, supports vector and scalar operators, and also
    provides some high level functions.
    """

    __slots__ = ("x", "y")

    x: float
    y: float

    @staticmethod
    def _fromcffi(p: Any) -> "Vec2d":
        """Used as a speedy way to create Vec2ds internally in pymunk."""
        v = Vec2d.__new__(Vec2d)
        v.x = p.x
        v.y = p.y
        return v

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, x_or_pair: Sequence[float]) -> None:
        ...

    @overload
    def __init__(self, x_or_pair: float, y: float) -> None:
        ...

    def __init__(
        self,
        x_or_pair: Union[Sequence[float], float, None] = None,
        y: Optional[float] = None,
    ) -> None:
        if x_or_pair is not None:
            if y is None:
                if isinstance(x_or_pair, Vec2d):
                    self.x = x_or_pair.x
                    self.y = x_or_pair.y
                elif isinstance(x_or_pair, Sequence):
                    self.x = x_or_pair[0]
                    self.y = x_or_pair[1]
                else:
                    raise TypeError
            else:
                assert isinstance(x_or_pair, float)
                self.x = x_or_pair
                self.y = y
        else:
            self.x = 0
            self.y = 0

    @overload
    def __getitem__(self, s: int) -> float:
        ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[float]:
        ...

    def __getitem__(self, i: Union[int, slice]) -> Union[float, Sequence[float]]:
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        if isinstance(i, int):
            raise IndexError()
        else:
            raise TypeError()

    def __iter__(self) -> Generator[float, None, None]:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    # String representaion (for debugging)
    def __repr__(self) -> str:
        return "Vec2d(%s, %s)" % (self.x, self.y)

    # Comparison
    def __eq__(self, other: Any) -> bool:
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True

    def __nonzero__(self) -> bool:
        return self.x != 0.0 or self.y != 0.0

    # Generic operator handlers
    def _o2(
        self,
        other: Union["Vec2d", Sequence[float], float],
        f: Callable[[float, float], float],
    ) -> "Vec2d":
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x), f(self.y, other.y))
        elif isinstance(other, Sequence):
            return Vec2d(f(self.x, other[0]), f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other), f(self.y, other))

    def _r_o2(
        self, other: Union[Sequence[float], float], f: Callable[[float, float], float]
    ) -> "Vec2d":
        "Any two-operator operation where the right operand is a Vec2d"
        if isinstance(other, Sequence):
            return Vec2d(f(other[0], self.x), f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x), f(other, self.y))

    # Addition
    def __add__(self, other: _Vec2dOrFloat) -> "Vec2d":
        """Add two vectors"""
        if isinstance(other, Vec2d) or isinstance(other, Sequence):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)

    __radd__ = __add__

    # Subtraction
    def __sub__(self, other: _Vec2dOrFloat) -> "Vec2d":
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif isinstance(other, Sequence):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)

    def __rsub__(self, other: _Vec2dOrFloat) -> "Vec2d":
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if isinstance(other, Sequence):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)

    # Multiplication
    def __mul__(self, other: _Vec2dOrFloat) -> "Vec2d":
        if isinstance(other, Vec2d):
            return Vec2d(self.x * other.x, self.y * other.y)
        if isinstance(other, Sequence):
            return Vec2d(self.x * other[0], self.y * other[1])
        else:
            return Vec2d(self.x * other, self.y * other)

    __rmul__ = __mul__

    # Division
    def __floordiv__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.floordiv)

    def __rfloordiv__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._r_o2(other, operator.floordiv)

    def __truediv__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.truediv)

    def __rtruediv__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._r_o2(other, operator.truediv)

    # Modulo
    def __mod__(self, other: _Vec2dOrFloat) -> "Vec2d":
        """Elementwise modulus %.

        >>> Vec2d(20, 30) % 6
        Vec2d(2, 0)
        >>> Vec2d(20, 30) % (6, 27)
        Vec2d(2, 3)
        >>> Vec2d(20, 30) % Vec2d(6, 27)
        Vec2d(2, 3)

        """
        return self._o2(other, operator.mod)

    def __rmod__(self, other: _Vec2dOrFloat) -> "Vec2d":
        """Elementwise modulus %, accepting a Vec2d as right operand

        >>> (20, 30) % Vec2d(6, 27)
        Vec2d(2, 3)
        >>> 30 % Vec2d(27, 28)
        Vec2d(3, 2)
        """
        return self._r_o2(other, operator.mod)

    def __divmod__(
        self, other: Union[Sequence[float], float]
    ) -> Tuple["Vec2d", "Vec2d"]:
        """Elementwise divmod

        >>> divmod( Vec2d(20, 30), Vec2d(6, 27) )
        (Vec2d(3, 2), Vec2d(1, 3))
        >>> divmod( Vec2d(20, 30), (6, 27) )
        (Vec2d(3, 2), Vec2d(1, 3))
        >>> divmod( Vec2d(20, 30), 6)
        (Vec2d(3, 2), Vec2d(5, 0))

        """
        if isinstance(other, Sequence):
            return Vec2d(divmod(self.x, other[0])), Vec2d(divmod(self.y, other[1]))
        return Vec2d(divmod(self.x, other)), Vec2d(divmod(self.y, other))

    def __rdivmod__(self, other: Sequence[float]) -> Tuple["Vec2d", "Vec2d"]:
        """Elementwise divmod (with Vec2d as right hand side argument)

        >>> divmod( (20, 30), Vec2d(6, 27) )
        (Vec2d(3, 2), Vec2d(1, 3))

        """
        return Vec2d(divmod(other[0], self.x)), Vec2d(divmod(other[1], self.y))

    # Exponentation
    def __pow__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.pow)

    def __rpow__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._r_o2(other, operator.pow)

    # Bitwise operators
    def __lshift__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.lshift)

    def __rlshift__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.rshift)

    def __rrshift__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._r_o2(other, operator.rshift)

    def __and__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.and_)

    __rand__ = __and__

    def __or__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.or_)

    __ror__ = __or__

    def __xor__(self, other: _Vec2dOrFloat) -> "Vec2d":
        return self._o2(other, operator.xor)

    __rxor__ = __xor__

    # Unary operations
    def __neg__(self) -> "Vec2d":
        return Vec2d(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self) -> "Vec2d":
        return Vec2d(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self) -> "Vec2d":
        return Vec2d(abs(self.x), abs(self.y))

    def __invert__(self) -> "Vec2d":
        return Vec2d(-self.x, -self.y)

    # vectory functions
    def get_length_sqrd(self) -> float:
        """Get the squared length of the vector.
        If the squared length is enough it is more efficient to use this method
        instead of first calling get_length() or access .length and then do a
        x**2.

        >>> v = Vec2d(3,4)
        >>> v.get_length_sqrd() == v.length**2
        True

        :return: The squared length
        """
        return self.x ** 2 + self.y ** 2

    @property
    def length(self) -> float:
        """Get the length of the vector.

        >>> Vec2d(10, 0).length
        10.0
        >>> Vec2d(10, 20).length
        22.360679774997898

        :return: The length
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def scale_to_length(self, length: float) -> "Vec2d":
        """Return a copy of this vector scaled to the given length.

        >>> Vec2d(10, 20).scale_to_length(20)
        Vec2d(8.94427190999916, 17.88854381999832)
        """
        old_length = self.length
        return Vec2d(self.x * length / old_length, self.y * length / old_length)

    def rotated(self, angle_radians: float) -> "Vec2d":
        """Create and return a new vector by rotating this vector by
        angle_radians radians.

        :return: Rotated vector
        """
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec2d(x, y)

    def rotated_degrees(self, angle_degrees: float) -> "Vec2d":
        """Create and return a new vector by rotating this vector by
        angle_degrees degrees.

        :return: Rotade vector
        """
        return self.rotated(math.radians(angle_degrees))

    @property
    def angle(self) -> float:
        """The angle (in radians) of the vector"""
        if self.get_length_sqrd() == 0:
            return 0
        return math.atan2(self.y, self.x)

    @property
    def angle_degrees(self) -> float:
        """Gets the angle (in degrees) of a vector"""
        return math.degrees(self.angle)

    def get_angle_between(self, other: "Vec2d") -> float:
        """Get the angle between the vector and the other in radians

        :return: The angle
        """
        cross = self.x * other[1] - self.y * other[0]
        dot = self.x * other[0] + self.y * other[1]
        return math.atan2(cross, dot)

    def get_angle_degrees_between(self, other: "Vec2d") -> float:
        """Get the angle between the vector and the other in degrees

        :return: The angle (in degrees)
        """
        return math.degrees(self.get_angle_between(other))

    def normalized(self) -> "Vec2d":
        """Get a normalized copy of the vector
        Note: This function will return 0 if the length of the vector is 0.

        :return: A normalized vector
        """
        length = self.length
        if length != 0:
            return self / length
        return Vec2d(0, 0)

    def normalized_and_length(self) -> Tuple["Vec2d", float]:
        """Normalize the vector and return its length before the normalization

        :return: The length before the normalization
        """
        length = self.length
        if length != 0:
            return self / length, length
        return Vec2d(0, 0), 0

    def perpendicular(self) -> "Vec2d":
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self) -> "Vec2d":
        length = self.length
        if length != 0:
            return Vec2d(-self.y / length, self.x / length)
        return Vec2d(self)

    def dot(self, other: Sequence[float]) -> float:
        """The dot product between the vector and other vector
            v1.dot(v2) -> v1.x*v2.x + v1.y*v2.y

        :return: The dot product
        """
        return float(self.x * other[0] + self.y * other[1])

    def get_distance(self, other: Sequence[float]) -> float:
        """The distance between the vector and other vector

        :return: The distance
        """
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

    def get_dist_sqrd(self, other: Sequence[float]) -> float:
        """The squared distance between the vector and other vector
        It is more efficent to use this method than to call get_distance()
        first and then do a sqrt() on the result.

        :return: The squared distance
        """
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2

    def projection(self, other: Sequence[float]) -> "Vec2d":
        """Project this vector on top of other vector"""
        other_length_sqrd = other[0] * other[0] + other[1] * other[1]
        if other_length_sqrd == 0.0:
            return Vec2d(0, 0)
        projected_length_times_other_length = self.dot(other)
        new_length = projected_length_times_other_length / other_length_sqrd
        return Vec2d(other[0] * new_length, other[1] * new_length)

    def cross(self, other: Sequence[float]) -> float:
        """The cross product between the vector and other vector
            v1.cross(v2) -> v1.x*v2.y - v1.y*v2.x

        :return: The cross product
        """
        return self.x * other[1] - self.y * other[0]

    def interpolate_to(self, other: _Vec2dOrTuple, range: float) -> "Vec2d":
        return Vec2d(
            self.x + (other[0] - self.x) * range, self.y + (other[1] - self.y) * range
        )

    def convert_to_basis(self, x_vector: "Vec2d", y_vector: "Vec2d") -> "Vec2d":
        x = self.dot(x_vector) / x_vector.get_length_sqrd()
        y = self.dot(y_vector) / y_vector.get_length_sqrd()
        return Vec2d(x, y)

    @property
    def int_tuple(self) -> Tuple[int, int]:
        """The x and y values of this vector as a tuple of ints.
        Uses round() to round to closest int.

        >>> Vec2d(0.9, 2.4).int_tuple
        (1, 2)
        """
        return round(self.x), round(self.y)

    @staticmethod
    def zero() -> "Vec2d":
        """A vector of zero length.

        >>> Vec2d.zero()
        Vec2d(0, 0)
        """
        return Vec2d(0, 0)

    @staticmethod
    def unit() -> "Vec2d":
        """A unit vector pointing up

        >>> Vec2d.unit()
        Vec2d(0, 1)
        """
        return Vec2d(0, 1)

    @staticmethod
    def ones() -> "Vec2d":
        """A vector where both x and y is 1

        >>> Vec2d.ones()
        Vec2d(1, 1)
        """
        return Vec2d(1, 1)

    # Extra functions, mainly for chipmunk
    def cpvrotate(self, other: "Vec2d") -> "Vec2d":
        """Uses complex multiplication to rotate this vector by the other. """
        return Vec2d(
            self.x * other.x - self.y * other.y, self.x * other.y + self.y * other.x
        )

    def cpvunrotate(self, other: "Vec2d") -> "Vec2d":
        """The inverse of cpvrotate"""
        return Vec2d(
            self.x * other.x + self.y * other.y, self.y * other.x - self.x * other.y
        )

    # Pickle
    def __reduce__(self) -> Tuple[Type["Vec2d"], Tuple[float, float]]:
        callable = Vec2d
        args = (self.x, self.y)
        return (callable, args)
