__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, List, Tuple

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
        assert len(point_a) == 2
        assert len(point_b) == 2
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
    points: List[ContactPoint]

    __slots__ = ("normal", "points")

    def __init__(self, normal: Vec2d, points: List[ContactPoint]) -> None:
        assert len(normal) == 2
        self.normal = normal
        self.points = points

    def __repr__(self) -> str:
        return "ContactPointSet(normal={}, points={})".format(self.normal, self.points)

    @classmethod
    def _from_cp(cls, _points: "ffi.CData") -> "ContactPointSet":
        normal = Vec2d(_points.normal.x, _points.normal.y)

        points = []
        for i in range(_points.count):
            _p = _points.points[i]
            p = ContactPoint(
                Vec2d(_p.pointA.x, _p.pointA.y),
                Vec2d(_p.pointB.x, _p.pointB.y),
                _p.distance,
            )
            points.append(p)

        return cls(normal, points)
