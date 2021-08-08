import math
from typing import NamedTuple, Tuple, Union, cast, overload

from .vec2d import Vec2d


class Transform(NamedTuple):
    """Type used for 2x3 affine transforms.

    See wikipedia for details:
    http://en.wikipedia.org/wiki/Affine_transformation

    The properties map to the matrix in this way:

    = = ==
    a c tx
    b d ty
    0 0  1
    = = ==

    An instance can be created in this way:

        >>> Transform(1,2,3,4,5,6)
        Transform(a=1, b=2, c=3, d=4, tx=5, ty=6)

    Or overriding only some of the values (on a identity matrix):

        >>> Transform(b=3,ty=5)
        Transform(a=1, b=3, c=0, d=1, tx=0, ty=5)

    Or using one of the static methods like identity or translation (see each
    method for details).

    The Transform supports the matrix multiplicaiton operator (@) with a
    Transform, Vec2d or tuple as second operand, which produces a transformed
    Transform or Vec2d as result:

        >>> Transform.scaling(2) @ Transform.scaling(3)
        Transform(a=6, b=0, c=0, d=6, tx=0, ty=0)
        >>> Transform.scaling(2) @ Vec2d(1, 2)
        Vec2d(2, 4)

    """

    a: float = 1
    b: float = 0
    c: float = 0
    d: float = 1
    tx: float = 0
    ty: float = 0

    @overload
    def __matmul__(self, other: Tuple[float, float]) -> Vec2d:
        ...

    @overload
    def __matmul__(
        self, other: Tuple[float, float, float, float, float, float]
    ) -> "Transform":
        ...

    def __matmul__(
        self,
        other: Union[
            Tuple[float, float], Tuple[float, float, float, float, float, float]
        ],
    ) -> Union[Vec2d, "Transform"]:

        """Multiply this transform with a Transform, Vec2d or Tuple of size 2
        or 6.


        Examples (Transform @ Transform):

        >>> Transform() @ Transform() == Transform.identity()
        True
        >>> Transform.translation(2,3) @ Transform.translation(4,5)
        Transform(a=1, b=0, c=0, d=1, tx=6, ty=8)
        >>> Transform.scaling(2) @ Transform.scaling(3)
        Transform(a=6, b=0, c=0, d=6, tx=0, ty=0)
        >>> Transform.scaling(2) @ Transform.translation(3,4)
        Transform(a=2, b=0, c=0, d=2, tx=6, ty=8)
        >>> Transform.translation(3,4) @ Transform.scaling(2)
        Transform(a=2, b=0, c=0, d=2, tx=3, ty=4)


        Examples (Transform @ Vec2d):

        >>> Transform.identity() @ Vec2d(1, 2)
        Vec2d(1, 2)
        >>> Transform.scaling(2) @ Vec2d(1, 2)
        Vec2d(2, 4)
        >>> Transform.translation(3,5) @ Vec2d(1, 2)
        Vec2d(4, 7)
        >>> Transform.rotation(1) @ Vec2d(1, 2) == Vec2d(1, 2).rotated(1)
        True

        """
        assert (
            len(other) == 2 or len(other) == 6
        ), f"{other} not supported. Only Vec2d, Transform and Sequence of length 2 or 6 are supported."

        if len(other) == 2:
            assert len(other) == 2
            x, y = cast(Tuple[float, float], other)
            return Vec2d(
                self.a * x + self.c * y + self.tx, self.b * x + self.d * y + self.ty
            )
        else:
            a, b, c, d, tx, ty = cast(Tuple[float, float, float, float, float, float], other)
            return Transform(
                a=self.a * a + self.c * b + self.tx * 0,
                b=self.b * a + self.d * b + self.ty * 0,
                c=self.a * c + self.c * d + self.tx * 0,
                d=self.b * c + self.d * d + self.ty * 0,
                tx=self.a * tx + self.c * ty + self.tx * 1,
                ty=self.b * tx + self.d * ty + self.ty * 1,
            )

    @staticmethod
    def identity() -> "Transform":
        """The identity transform

        Example:

        >>> Transform.identity()
        Transform(a=1, b=0, c=0, d=1, tx=0, ty=0)

        Returns a Transform with this matrix:

        = = =
        1 0 0
        0 1 0
        0 0 1
        = = =

        """
        return Transform(1, 0, 0, 1, 0, 0)

    def translated(self, x: float, y: float) -> "Transform":
        """Translate this Transform and return the result.

        Example:
        >>> Transform.scaling(2).translated(3,4)
        Transform(a=2, b=0, c=0, d=2, tx=6, ty=8)

        """
        return self @ Transform.translation(x, y)

    def scaled(self, s: float) -> "Transform":
        """Scale this Transform and return the result.

        Example:

        >>> Transform.translation(3,4).scaled(2)
        Transform(a=2, b=0, c=0, d=2, tx=3, ty=4)
        """
        return self @ Transform.scaling(s)

    def rotated(self, t: float) -> "Transform":
        """Rotate this Transform and return the result.

        >>> '%.2f, %.2f, %.2f, %.2f, %.2f, %.2f' % Transform.rotation(1).rotated(0.5)
        '0.07, 1.00, -1.00, 0.07, 0.00, 0.00'
        >>> '%.2f, %.2f, %.2f, %.2f, %.2f, %.2f' % Transform.rotation(1.5)
        '0.07, 1.00, -1.00, 0.07, 0.00, 0.00'
        """
        return self @ Transform.rotation(t)

    @staticmethod
    def translation(x: float, y: float) -> "Transform":
        """A translation transform

        Example to translate (move) by 3 on x and 5 in y axis:

        >>> Transform.translation(3, 5)
        Transform(a=1, b=0, c=0, d=1, tx=3, ty=5)

        Returns a Transform with this matrix:

        = = =
        1 0 x
        0 1 y
        0 0 1
        = = =

        """
        return Transform(tx=x, ty=y)

    # split into scale and scale_non-uniform
    @staticmethod
    def scaling(s: float) -> "Transform":
        """A scaling transform

        Example to scale 4x:

        >>> Transform.scaling(4)
        Transform(a=4, b=0, c=0, d=4, tx=0, ty=0)

        Returns a Transform with this matrix:

        = = =
        s 0 0
        0 s 0
        0 0 1
        = = =

        """
        return Transform(a=s, d=s)

    @staticmethod
    def rotation(t: float) -> "Transform":
        """A rotation transform

        Example to rotate by 1 rad:

        >>> '%.2f, %.2f, %.2f, %.2f, %.2f, %.2f' % Transform.rotation(1)
        '0.54, 0.84, -0.84, 0.54, 0.00, 0.00'

        Returns a Transform with this matrix:

        ====== ======= =
        cos(t) -sin(t) 0
        sin(t) cos(t)  0
        0      0       1
        ====== ======= =

        """
        c = math.cos(t)
        s = math.sin(t)
        return Transform(a=c, b=s, c=-s, d=c)
