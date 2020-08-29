__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, NamedTuple, Optional

if TYPE_CHECKING:
    from .contact_point_set import ContactPointSet
    from .shapes import Shape
    from .vec2d import Vec2d


class PointQueryInfo(NamedTuple):
    """PointQueryInfo holds the result of a point query made on a Shape or
    Space.
    """

    shape: Optional["Shape"]
    """The nearest shape, None if no shape was within range."""

    point: "Vec2d"
    """The closest point on the shape's surface. (in world space
    coordinates)
    """

    distance: float
    """The distance to the point. The distance is negative if the
    point is inside the shape.
    """

    gradient: "Vec2d"
    """The gradient of the signed distance function.

    The value should be similar to
    PointQueryInfo.point/PointQueryInfo.distance, but accurate even for
    very small values of info.distance.
    """


class SegmentQueryInfo(NamedTuple):
    """Segment queries return more information than just a simple yes or no,
    they also return where a shape was hit and it's surface normal at the hit
    point. This object hold that information.

    To test if the query hit something, check if
    SegmentQueryInfo.shape == None or not.

    Segment queries are like ray casting, but because not all spatial indexes
    allow processing infinitely long ray queries it is limited to segments.
    In practice this is still very fast and you don't need to worry too much
    about the performance as long as you aren't using extremely long segments
    for your queries.

    """

    shape: Optional["Shape"]
    """Shape that was hit, or None if no collision occured"""

    point: "Vec2d"
    """The point of impact."""

    normal: "Vec2d"
    """The normal of the surface hit."""

    alpha: float
    """The normalized distance along the query segment in the range [0, 1]"""


class ShapeQueryInfo(NamedTuple):
    """Shape queries return more information than just a simple yes or no,
    they also return where a shape was hit. This object hold that information.
    """

    shape: Optional["Shape"]
    """Shape that was hit, or None if no collision occured"""

    contact_point_set: "ContactPointSet"
