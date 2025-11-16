# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2025 Victor Blomqvist
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

"""This module contains the Vec2d class that is used in all of Pymunk when a
2d vector is needed.

It is easy to create Vec2ds::

    >>> from pymunk.vec2d import Vec2d
    >>> Vec2d(1, 2)
    Vec2d(1, 2)
    >>> xy = (1, 2)
    >>> Vec2d(*xy)
    Vec2d(1, 2)
    >>> '%.2f, %.2f' % Vec2d.from_polar(3, math.pi/4)
    '2.12, 2.12'

You can index into Vec2ds with both positional and attribute access::

    >>> v = Vec2d(1, 2)
    >>> v.x, v.y
    (1, 2)
    >>> v[0], v[1]
    (1, 2)

Vec2ds can be converted to lists or tuples, and they are of length 2::

    >>> list(Vec2d(1, 2))
    [1, 2]
    >>> tuple(Vec2d(1, 2))
    (1, 2)
    >>> len(Vec2d(1, 2))
    2

The Vec2d supports many common opertions, for example addition and
multiplication::

    >>> Vec2d(7.3, 4.2) + Vec2d(1, 2)
    Vec2d(8.3, 6.2)
    >>> Vec2d(7.3, 4.2) * 2
    Vec2d(14.6, 8.4)

Vec2ds are immutable, meaning you cannot update them. But you can replace
them::

    >>> v = Vec2d(1, 2)
    >>> v.x = 4
    Traceback (most recent call last):
    ...
    AttributeError: can't set attribute
    >>> v += (3, 4)
    >>> v
    Vec2d(4, 6)

Vec2ds can be compared::

    >>> Vec2d(7.3, 4.2) == Vec2d(7.3, 4.2)
    True
    >>> Vec2d(7.3, 4.2) == Vec2d(0, 0)
    False

The Vec2d class is used almost everywhere in pymunk for 2d coordinates and
vectors, for example to define gravity vector in a space. However, Pymunk is
smart enough to convert tuples or tuple like objects to Vec2ds so you usually
do not need to explicitly do conversions if you happen to have a tuple::

    >>> import pymunk
    >>> space = pymunk.Space()
    >>> space.gravity
    Vec2d(0.0, 0.0)
    >>> space.gravity = 3, 5
    >>> space.gravity
    Vec2d(3.0, 5.0)
    >>> space.gravity += 2, 6
    >>> space.gravity
    Vec2d(5.0, 11.0)

Finally, Vec2ds can be pickled and unpickled::

    >>> import pickle
    >>> data = pickle.dumps(Vec2d(5, 0.3))
    >>> pickle.loads(data)
    Vec2d(5, 0.3)

"""
__docformat__ = "reStructuredText"

import math
import numbers
import operator
import warnings
from typing import NamedTuple

__all__ = ["Vec2d"]


class Vec2d(NamedTuple):
    """2d vector class, supports vector and scalar operators, and also
    provides some high level functions.
    """

    x: float
    y: float

    def __repr__(self) -> str:
        """String representaion of Vec2d (for debugging)

        >>> repr(Vec2d(1, 2.3))
        'Vec2d(1, 2.3)'
        """
        return "Vec2d(%s, %s)" % (self.x, self.y)

    # Addition
    def __add__(self, other: tuple[float, float]) -> "Vec2d":  # type: ignore[override]
        """Add a Vec2d with another Vec2d or tuple of size 2.

        >>> Vec2d(3, 4) + Vec2d(1, 2)
        Vec2d(4, 6)
        >>> Vec2d(3, 4) + (1, 2)
        Vec2d(4, 6)
        """
        assert (
            len(other) == 2
        ), f"{other} not supported. Only Vec2d and Sequence of length 2 is supported."

        return Vec2d(self.x + other[0], self.y + other[1])

    def __radd__(self, other: tuple[float, float]) -> "Vec2d":
        """Add a tuple of size 2 with a Vec2d.

        >>> (1, 2) + Vec2d(3, 4)
        Vec2d(4, 6)
        """
        return self.__add__(other)

    # Subtraction
    def __sub__(self, other: tuple[float, float]) -> "Vec2d":
        """Subtract a Vec2d with another Vec2d or tuple of size 2.

        >>> Vec2d(3, 4) - Vec2d(1, 2)
        Vec2d(2, 2)
        >>> Vec2d(3, 4) - (1, 2)
        Vec2d(2, 2)
        """
        return Vec2d(self.x - other[0], self.y - other[1])

    def __rsub__(self, other: tuple[float, float]) -> "Vec2d":
        """Subtract a tuple of size 2 with a Vec2d.

        >>> (1, 2) - Vec2d(3, 4)
        Vec2d(-2, -2)
        """
        assert (
            len(other) == 2
        ), f"{other} not supported. Only Vec2d and Sequence of length 2 is supported."
        return Vec2d(other[0] - self.x, other[1] - self.y)

    # Multiplication
    def __mul__(self, other: float) -> "Vec2d":  # type: ignore[override]
        """Multiply a Vec2d with a float.

        >>> Vec2d(3, 6) * 2.5
        Vec2d(7.5, 15.0)
        """
        assert isinstance(other, numbers.Real)
        return Vec2d(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> "Vec2d":  # type: ignore[override]
        """Multiply a float with a Vec2d.

        >>> 2.5 * Vec2d(3, 6)
        Vec2d(7.5, 15.0)
        """
        return self.__mul__(other)

    # Division
    def __floordiv__(self, other: float) -> "Vec2d":
        """Floor division by a float (also known as integer division).

        >>> Vec2d(3, 6) // 2.0
        Vec2d(1.0, 3.0)
        >>> Vec2d(0, 0) // 2.0
        Vec2d(0.0, 0.0)
        """
        assert isinstance(other, numbers.Real)
        return Vec2d(self.x // other, self.y // other)

    def __truediv__(self, other: float) -> "Vec2d":
        """Division by a float.

        >>> Vec2d(3, 6) / 2.0
        Vec2d(1.5, 3.0)
        >>> Vec2d(0,0) / 2.0
        Vec2d(0.0, 0.0)
        """
        assert isinstance(other, numbers.Real)
        return Vec2d(self.x / other, self.y / other)

    # Unary operations
    def __neg__(self) -> "Vec2d":
        """Return the negated version of the Vec2d.

        >>> -Vec2d(1, -2)
        Vec2d(-1, 2)
        >>> -Vec2d(0, 0)
        Vec2d(0, 0)
        """
        return Vec2d(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self) -> "Vec2d":
        """Return the unary pos of the Vec2d.

        >>> +Vec2d(1, -2)
        Vec2d(1, -2)
        """
        return Vec2d(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self) -> float:
        """Return the length of the Vec2d.

        >>> abs(Vec2d(3, 4))
        5.0
        >>> abs(Vec2d(3, 4)) == Vec2d(3, 4).length
        True
        """
        return self.length

    def __bool__(self) -> bool:
        """Return true if both x and y are nonzero.

        >>> bool(Vec2d(1, 0))
        True
        >>> bool(Vec2d(-1, -2))
        True
        >>> bool(Vec2d(0, 0))
        False
        """
        return self.x != 0 or self.y != 0

    @property
    def length_squared(self) -> float:
        """Get the squared length of the vector.
        If the squared length is enough, it is more efficient to use this method
        instead of first access .length and then do a x**2.

        >>> v = Vec2d(3, 4)
        >>> v.length_squared == v.length**2
        True
        >>> Vec2d(0, 0).length_squared
        0
        """
        return self.x**2 + self.y**2

    # vectory functions

    def get_length_sqrd(self) -> float:
        """Get the squared length of the vector.
        If the squared length is enough, it is more efficient to use this method
        instead of first accessing .length and then do a x**2.

        .. deprecated:: 7.0.0
            Please use :py:attr:`length_squared` instead.

        >>> v = Vec2d(3, 4)
        >>> v.get_length_sqrd() == v.length**2
        True
        >>> Vec2d(0, 0).get_length_sqrd()
        0
        """
        warnings.warn(
            "Vec2d.get_length_sqrd() is deprecated. Use Vec2d.length_squared instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.x**2 + self.y**2

    @property
    def length(self) -> float:
        """Get the length of the vector.

        >>> Vec2d(10, 0).length
        10.0
        >>> '%.2f' % Vec2d(10, 20).length
        '22.36'
        >>> Vec2d(0, 0).length
        0.0
        """
        return math.sqrt(self.x**2 + self.y**2)

    def scale_to_length(self, length: float) -> "Vec2d":
        """Return a copy of this vector scaled to the given length.

        Note that a zero length Vec2d cannot be scaled but will raise an
        exception.

        >>> Vec2d(1, 0).scale_to_length(10)
        Vec2d(10.0, 0.0)
        >>> '%.2f, %.2f' % Vec2d(10, 20).scale_to_length(20)
        '8.94, 17.89'
        >>> Vec2d(1, 0).scale_to_length(0)
        Vec2d(0.0, 0.0)
        >>> Vec2d(0, 0).scale_to_length(1)
        Traceback (most recent call last):
        ...
        ZeroDivisionError: float division by zero
        """
        old_length = self.length
        return Vec2d(self.x * length / old_length, self.y * length / old_length)

    def rotated(self, angle_radians: float) -> "Vec2d":
        """Create and return a new vector by rotating this vector by
        angle_radians radians.

        >>> '%.2f' % Vec2d(2,0).rotated(math.pi).angle
        '3.14'
        >>> Vec2d(0,0).rotated(1)
        Vec2d(0.0, 0.0)
        """
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec2d(x, y)

    def rotated_degrees(self, angle_degrees: float) -> "Vec2d":
        """Create and return a new vector by rotating this vector by
                angle_degrees degrees.

        >>> Vec2d(2,0).rotated_degrees(90.0).angle_degrees
        90.0
        >>> Vec2d(0, 0).rotated_degrees(90.0)
        Vec2d(0.0, 0.0)
        """
        return self.rotated(math.radians(angle_degrees))

    @property
    def angle(self) -> float:
        """The angle (in radians) of the vector.

        Angle calculated with atan2(y, x).

        >>> '%.2f' % Vec2d(-1, 0).angle
        '3.14'
        >>> Vec2d(0, 0).angle
        0.0
        """
        return math.atan2(self.y, self.x)

    @property
    def angle_degrees(self) -> float:
        """Get the angle (in degrees) of a vector.

        >>> Vec2d(0, 1).angle_degrees
        90.0
        >>> Vec2d(0, 0).angle_degrees
        0.0
        """
        return math.degrees(self.angle)

    def get_angle_between(self, other: tuple[float, float]) -> float:
        """Get the angle between the vector and the other in radians.

        >>> '%.2f' % Vec2d(3, 0).get_angle_between(Vec2d(-1, 0))
        '3.14'
        >>> Vec2d(3, 0).get_angle_between(Vec2d(0, 0))
        0.0
        >>> Vec2d(0, 0).get_angle_between(Vec2d(0, 0))
        0.0
        """
        assert len(other) == 2
        cross = self.x * other[1] - self.y * other[0]
        dot = self.x * other[0] + self.y * other[1]
        return math.atan2(cross, dot)

    def get_angle_degrees_between(self, other: "Vec2d") -> float:
        """Get the angle between the vector and the other in degrees.

        >>> Vec2d(3, 0).get_angle_degrees_between(Vec2d(-1, 0))
        180.0
        >>> Vec2d(3, 0).get_angle_degrees_between(Vec2d(0, 0))
        0.0
        >>> Vec2d(0, 0).get_angle_degrees_between(Vec2d(0, 0))
        0.0
        """
        return math.degrees(self.get_angle_between(other))

    def normalized(self) -> "Vec2d":
        """Get a normalized copy of the vector.
        Note: This function will return a Vec2d(0.0, 0.0) if the length of the vector is 0.

        >>> Vec2d(3, 0).normalized()
        Vec2d(1.0, 0.0)
        >>> Vec2d(3, 4).normalized()
        Vec2d(0.6, 0.8)
        >>> Vec2d(0, 0).normalized()
        Vec2d(0.0, 0.0)
        """
        length = self.length
        if length != 0:
            return self / length
        return Vec2d(0.0, 0.0)

    def normalized_and_length(self) -> tuple["Vec2d", float]:
        """Normalize the vector and return its length before the normalization.

        >>> Vec2d(3, 0).normalized_and_length()
        (Vec2d(1.0, 0.0), 3.0)
        >>> Vec2d(3, 4).normalized_and_length()
        (Vec2d(0.6, 0.8), 5.0)
        >>> Vec2d(0, 0).normalized_and_length()
        (Vec2d(0.0, 0.0), 0.0)
        """
        length = self.length
        if length != 0:
            return self / length, length
        return Vec2d(0.0, 0.0), 0.0

    def perpendicular(self) -> "Vec2d":
        """Get a vertical vector rotated 90 degrees counterclockwise from the original vector.

        >>> Vec2d(1, 2).perpendicular()
        Vec2d(-2, 1)
        """
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self) -> "Vec2d":
        """Get a vertical normalized vector rotated 90 degrees counterclockwise from the original vector.

        >>> Vec2d(1, 0).perpendicular_normal()
        Vec2d(0.0, 1.0)
        >>> Vec2d(2, 0).perpendicular_normal()
        Vec2d(0.0, 1.0)
        >>> Vec2d(1, 1).perpendicular_normal().angle_degrees
        135.0
        >>> Vec2d(1, 1).angle_degrees + 90
        135.0
        >>> Vec2d(0, 0).perpendicular_normal()
        Vec2d(0, 0)
        """
        length = self.length
        if length != 0:
            return Vec2d(-self.y / length, self.x / length)
        return Vec2d(self.x, self.y)

    def dot(self, other: tuple[float, float]) -> float:
        """The dot product between the vector and other vector.
        v1.dot(v2) -> v1.x*v2.x + v1.y*v2.y

        >>> Vec2d(5, 0).dot((0, 5))
        0.0
        >>> Vec2d(1, 2).dot((3, 4))
        11.0
        """
        assert len(other) == 2
        return float(self.x * other[0] + self.y * other[1])

    def get_distance(self, other: tuple[float, float]) -> float:
        """The distance between the vector and other vector.

        >>> Vec2d(0, 2).get_distance((0, -3))
        5.0
        >>> a, b = Vec2d(3, 2), Vec2d(4,3)
        >>> a.get_distance(b) == (a - b).length == (b - a).length
        True
        """
        assert len(other) == 2
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

    def get_distance_squared(self, other: tuple[float, float]) -> float:
        """The squared distance between the vector and other vector.
        It is more efficent to use this method than to call get_distance()
        first and then do a square() on the result.

        >>> Vec2d(1, 0).get_distance_squared((1, 10))
        100
        >>> Vec2d(1, 2).get_distance_squared((10, 11))
        162
        >>> Vec2d(1, 2).get_distance((10, 11))**2
        162.0
        """
        assert len(other) == 2
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2

    def get_dist_sqrd(self, other: tuple[float, float]) -> float:
        """The squared distance between the vector and other vector.
        It is more efficent to use this method than to call get_distance()
        first and then do a square() on the result.

        .. deprecated:: 7.0.0
            Please use :py:func:`get_distance_squared` instead.

        >>> Vec2d(1, 0).get_dist_sqrd((1, 10))
        100
        >>> Vec2d(1, 2).get_dist_sqrd((10, 11))
        162
        >>> Vec2d(1, 2).get_distance((10, 11))**2
        162.0
        """
        warnings.warn(
            "get_dist_sqrd() is deprecated. Use get_distance_squared() instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        assert len(other) == 2
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2

    def projection(self, other: tuple[float, float]) -> "Vec2d":
        """Project this vector on top of other vector.

        >>> Vec2d(10, 1).projection((5.0, 0))
        Vec2d(10.0, 0.0)
        >>> Vec2d(10, 1).projection((10, 5))
        Vec2d(8.4, 4.2)
        >>> Vec2d(10, 1).projection((0, 0))
        Vec2d(0.0, 0.0)
        """
        assert len(other) == 2
        other_length_sqrd = other[0] * other[0] + other[1] * other[1]
        if other_length_sqrd == 0.0:
            return Vec2d(0.0, 0.0)
        # projected_length_times_other_length = self.dot(other)
        # new_length = projected_length_times_other_length / other_length_sqrd
        new_length = self.dot(other) / other_length_sqrd
        return Vec2d(other[0] * new_length, other[1] * new_length)

    def cross(self, other: tuple[float, float]) -> float:
        """The cross product between the vector and the other.

        v1.cross(v2) -> v1.x*v2.y - v1.y*v2.x

        >>> Vec2d(1, 0.5).cross((4, 6))
        4.0
        """
        assert len(other) == 2
        return self.x * other[1] - self.y * other[0]

    def interpolate_to(self, other: tuple[float, float], range: float) -> "Vec2d":
        """Vector interpolation between the current vector and another vector.

        >>> Vec2d(10,20).interpolate_to((20,-20), 0.1)
        Vec2d(11.0, 16.0)
        """
        assert len(other) == 2
        return Vec2d(
            self.x + (other[0] - self.x) * range, self.y + (other[1] - self.y) * range
        )

    def convert_to_basis(
        self, x_vector: tuple[float, float], y_vector: tuple[float, float]
    ) -> "Vec2d":
        """Convert the vector to a new basis defined by the given x and y vectors.

        >>> Vec2d(10, 1).convert_to_basis((5, 0), (0, 0.5))
        Vec2d(2.0, 2.0)
        """
        assert len(x_vector) == 2
        assert len(y_vector) == 2
        x = self.dot(x_vector) / Vec2d(*x_vector).length_squared
        y = self.dot(y_vector) / Vec2d(*y_vector).length_squared
        return Vec2d(x, y)

    @property
    def int_tuple(self) -> tuple[int, int]:
        """The x and y values of this vector as a tuple of ints.
        Uses `round()` to round to closest int.

        >>> Vec2d(0.9, 2.4).int_tuple
        (1, 2)
        """
        return round(self.x), round(self.y)

    @property
    def polar_tuple(self) -> tuple[float, float]:
        """Return this vector as polar coordinates (length, angle)

        See Vec2d.from_polar() for the inverse.

        >>> Vec2d(2, 0).polar_tuple
        (2.0, 0.0)
        >>> Vec2d(2, 0).rotated(0.5).polar_tuple
        (2.0, 0.5)
        >>> Vec2d.from_polar(2, 0.5).polar_tuple
        (2.0, 0.5)

        """
        return self.length, self.angle

    @staticmethod
    def zero() -> "Vec2d":
        """A vector of zero length.

        >>> Vec2d.zero()
        Vec2d(0.0, 0.0)
        """
        return Vec2d(0.0, 0.0)

    @staticmethod
    def unit() -> "Vec2d":
        """A unit vector pointing up.

        >>> Vec2d.unit()
        Vec2d(0.0, 1.0)
        """
        return Vec2d(0.0, 1.0)

    @staticmethod
    def ones() -> "Vec2d":
        """A vector where both x and y is 1.

        >>> Vec2d.ones()
        Vec2d(1.0, 1.0)
        """
        return Vec2d(1.0, 1.0)

    @staticmethod
    def from_polar(length: float, angle: float) -> "Vec2d":
        """Create a new Vec2d from a length and an angle (in radians).

        See Vec2d.polar_tuple for the inverse.

        >>> Vec2d.from_polar(2, 0)
        Vec2d(2.0, 0.0)
        >>> Vec2d(2, 0).rotated(0.5) == Vec2d.from_polar(2, 0.5)
        True
        >>> v = Vec2d.from_polar(2, 0.5)
        >>> v.length, v.angle
        (2.0, 0.5)
        """
        return Vec2d(math.cos(angle) * length, math.sin(angle) * length)

    # Extra functions, mainly for chipmunk
    def cpvrotate(self, other: tuple[float, float]) -> "Vec2d":
        """Use complex multiplication to rotate this vector by the other."""
        assert len(other) == 2
        return Vec2d(
            self.x * other[0] - self.y * other[1], self.x * other[1] + self.y * other[0]
        )

    def cpvunrotate(self, other: tuple[float, float]) -> "Vec2d":
        """The inverse of cpvrotate."""
        assert len(other) == 2
        return Vec2d(
            self.x * other[0] + self.y * other[1], self.y * other[0] - self.x * other[1]
        )
