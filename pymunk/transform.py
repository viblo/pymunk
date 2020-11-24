import math
from typing import NamedTuple


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

    """

    a: float = 1
    b: float = 0
    c: float = 0
    d: float = 1
    tx: float = 0
    ty: float = 0

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

        >>> Transform.rotation(1)
        Transform(a=0.5403023058681398, b=0.8414709848078965, c=-0.8414709848078965, d=0.5403023058681398, tx=0, ty=0)

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
