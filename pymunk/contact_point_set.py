__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from ._chipmunk_cffi import ffi

from .vec2d import Vec2d


class ContactPoint(object):
    """Contains information about a contact point.

    point_a and point_b are the contact position on the surface of each shape.

    distance is the penetration distance of the two shapes. Overlapping
    means it will be negative. This value is calculated as
    dot(point2 - point1), normal) and is ignored when you set the
    Arbiter.contact_point_set.
    """

    point_a: Vec2d
    point_b: Vec2d
    distance: float

    __slots__ = ("point_a", "point_b", "distance")

    def __init__(
        self,
        point_a: Vec2d,
        point_b: Vec2d,
        distance: float,
    ) -> None:
        self.point_a = point_a
        self.point_b = point_b
        self.distance = distance

    def __repr__(self) -> str:
        return "ContactPoint(point_a={}, point_b={}, distance={})".format(
            self.point_a, self.point_b, self.distance
        )


class ContactPointSet(object):
    """Contact point sets make getting contact information simpler.

    normal is the normal of the collision

    points is the array of contact points. Can be at most 2 points.
    """

    normal: Vec2d
    points: Tuple[ContactPoint, ...]

    __slots__ = ("normal", "points")

    def __init__(self, normal: Vec2d, points: Tuple[ContactPoint, ...]) -> None:
        self.normal = normal
        self.points = points

    def __repr__(self) -> str:
        return "ContactPointSet(normal={}, points={})".format(self.normal, self.points)

    @classmethod
    def _from_cp(cls, _points: "ffi.CData") -> "ContactPointSet":
        normal = Vec2d(_points.normal.x, _points.normal.y)

        assert _points.count in (1, 2), "This is likely a bug in Pymunk, please report."

        _p1 = _points.points[0]
        p1 = ContactPoint(
            Vec2d(_p1.pointA.x, _p1.pointA.y),
            Vec2d(_p1.pointB.x, _p1.pointB.y),
            _p1.distance,
        )
        if _points.count == 1:
            return cls(normal, (p1,))

        _p2 = _points.points[1]
        p2 = ContactPoint(
            Vec2d(_p2.pointA.x, _p2.pointA.y),
            Vec2d(_p2.pointB.x, _p2.pointB.y),
            _p2.distance,
        )
        return cls(normal, (p1, p2))
