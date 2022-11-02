"""This module contain functions for automatic generation of geometry, for 
example from an image.

Example::

    >>> import pymunk
    >>> from pymunk.autogeometry import march_soft
    >>> img = [
    ...     "  xx   ",
    ...     "  xx   ",
    ...     "  xx   ",
    ...     "  xx   ",
    ...     "  xx   ",
    ...     "  xxxxx",
    ...     "  xxxxx",
    ... ]
    >>> def sample_func(point):
    ...     x = int(point[0])
    ...     y = int(point[1])
    ...     return 1 if img[y][x] == "x" else 0

    >>> pl_set = march_soft(pymunk.BB(0,0,6,6), 7, 7, .5, sample_func)
    >>> print(len(pl_set))
    2

The information in segments can now be used to create geometry, for example as 
a Pymunk Poly or Segment::

    >>> s = pymunk.Space()
    >>> for poly_line in pl_set:
    ...     for i in range(len(poly_line) - 1):
    ...         a = poly_line[i]
    ...         b = poly_line[i + 1]
    ...         segment = pymunk.Segment(s.static_body, a, b, 1)  
    ...         s.add(segment)


"""
__docformat__ = "reStructuredText"

from typing import TYPE_CHECKING, Callable, List, Sequence, Tuple, Union, overload

if TYPE_CHECKING:
    from .bb import BB

from . import area_for_poly
from ._chipmunk_cffi import ffi, lib
from .vec2d import Vec2d

_SegmentFunc = Callable[[Tuple[float, float], Tuple[float, float]], None]
_SampleFunc = Callable[[Tuple[float, float]], float]

_Polyline = Union[List[Tuple[float, float]], List[Vec2d]]
# Union is needed since List is invariant
# and Sequence cant be used since CFFI requires a List (or Tuple)


def _to_chipmunk(polyline: _Polyline) -> ffi.CData:
    l = len(polyline)
    _line = ffi.new("cpPolyline *", {"verts": l})
    _line.count = l
    _line.capacity = l
    _line.verts = polyline
    return _line


def _from_polyline_set(_set: ffi.CData) -> List[List[Vec2d]]:
    lines = []
    for i in range(_set.count):
        line = []
        l = _set.lines[i]
        for j in range(l.count):
            line.append(Vec2d(l.verts[j].x, l.verts[j].y))
        lines.append(line)
    return lines


def is_closed(polyline: _Polyline) -> bool:
    """Returns true if the first vertex is equal to the last.

    :param polyline: Polyline to simplify.
    :type polyline: [(float,float)]
    :rtype: `bool`
    """
    return bool(lib.cpPolylineIsClosed(_to_chipmunk(polyline)))


def simplify_curves(polyline: _Polyline, tolerance: float) -> List[Vec2d]:
    """Returns a copy of a polyline simplified by using the Douglas-Peucker
    algorithm.

    This works very well on smooth or gently curved shapes, but not well on
    straight edged or angular shapes.

    :param polyline: Polyline to simplify.
    :type polyline: [(float,float)]
    :param float tolerance: A higher value means more error is tolerated.
    :rtype: [(float,float)]
    """

    _line = lib.cpPolylineSimplifyCurves(_to_chipmunk(polyline), tolerance)
    simplified = []
    for i in range(_line.count):
        simplified.append(Vec2d(_line.verts[i].x, _line.verts[i].y))
    return simplified


def simplify_vertexes(polyline: _Polyline, tolerance: float) -> List[Vec2d]:
    """Returns a copy of a polyline simplified by discarding "flat" vertexes.

    This works well on straight edged or angular shapes, not as well on smooth
    shapes.

    :param polyline: Polyline to simplify.
    :type polyline: [(float,float)]
    :param float tolerance: A higher value means more error is tolerated.
    :rtype: [(float,float)]
    """
    _line = lib.cpPolylineSimplifyVertexes(_to_chipmunk(polyline), tolerance)
    simplified = []
    for i in range(_line.count):
        simplified.append(Vec2d(_line.verts[i].x, _line.verts[i].y))
    return simplified


def to_convex_hull(polyline: _Polyline, tolerance: float) -> List[Vec2d]:
    """Get the convex hull of a polyline as a looped polyline.

    :param polyline: Polyline to simplify.
    :type polyline: [(float,float)]
    :param float tolerance: A higher value means more error is tolerated.
    :rtype: [(float,float)]
    """
    _line = lib.cpPolylineToConvexHull(_to_chipmunk(polyline), tolerance)
    hull = []
    for i in range(_line.count):
        hull.append(Vec2d(_line.verts[i].x, _line.verts[i].y))
    return hull


def convex_decomposition(polyline: _Polyline, tolerance: float) -> List[List[Vec2d]]:
    """Get an approximate convex decomposition from a polyline.

    Returns a list of convex hulls that match the original shape to within
    tolerance.

    .. note::
        If the input is a self intersecting polygon, the output might end up
        overly simplified.

    :param polyline: Polyline to simplify.
    :type polyline: [(float,float)]
    :param float tolerance: A higher value means more error is tolerated.
    :rtype: [(float,float)]
    """

    assert is_closed(polyline), "Cannot decompose an open polygon."
    assert (
        area_for_poly(polyline) >= 0
    ), "Winding is backwards. Try to reverse the vertices. (Are you passing a hole?)"

    _line = _to_chipmunk(polyline)
    _set = lib.cpPolylineConvexDecomposition(_line, tolerance)
    return _from_polyline_set(_set)


class PolylineSet(Sequence[List[Vec2d]]):
    """A set of Polylines.

    Mainly intended to be used for its :py:meth:`collect_segment` function
    when generating geometry with the :py:func:`march_soft` and
    :py:func:`march_hard` functions.
    """

    def __init__(self) -> None:
        """Initalize a new PolylineSet"""

        def free(_set: ffi.CData) -> None:
            lib.cpPolylineSetFree(_set, True)

        self._set = ffi.gc(lib.cpPolylineSetNew(), free)

    def collect_segment(self, v0: Tuple[float, float], v1: Tuple[float, float]) -> None:
        """Add a line segment to a polyline set.

        A segment will either start a new polyline, join two others, or add to
        or loop an existing polyline. This is mostly intended to be used as a
        callback directly from :py:func:`march_soft` or :py:func:`march_hard`.

        :param v0: Start of segment
        :type v0: (float,float)
        :param v1: End of segment
        :type v1: (float,float)
        """
        assert len(v0) == 2
        assert len(v1) == 2

        lib.cpPolylineSetCollectSegment(v0, v1, self._set)

    def __len__(self) -> int:
        return self._set.count

    @overload
    def __getitem__(self, index: int) -> List[Vec2d]:
        ...

    @overload
    def __getitem__(self, index: slice) -> "PolylineSet":
        ...

    def __getitem__(self, key: Union[int, slice]) -> Union[List[Vec2d], "PolylineSet"]:
        assert not isinstance(key, slice), "Slice indexing not supported"
        if key >= self._set.count:
            raise IndexError
        line = []
        l = self._set.lines[key]
        for i in range(l.count):
            line.append(Vec2d(l.verts[i].x, l.verts[i].y))
        return line


def march_soft(
    bb: "BB",
    x_samples: int,
    y_samples: int,
    threshold: float,
    sample_func: _SampleFunc,
) -> PolylineSet:
    """Trace an *anti-aliased* contour of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding
    box area using the sampling function and context.

    :param BB bb: Bounding box of the area to sample within
    :param int x_samples: Number of samples in x
    :param int y_samples: Number of samples in y
    :param float threshold: A higher value means more error is tolerated
    :param sample_func: The sample function will be called for
        x_samples * y_samples spread across the bounding box area, and should
        return a float.
    :type sample_func: ``func(point: Tuple[float, float]) -> float``
    :return: PolylineSet with the polylines found.
    """
    pl_set = PolylineSet()

    segment_data = ffi.new_handle(pl_set)
    sample_data = ffi.new_handle(sample_func)

    lib.cpMarchSoft(
        bb,
        x_samples,
        y_samples,
        threshold,
        lib.ext_cpMarchSegmentFunc,
        segment_data,
        lib.ext_cpMarchSampleFunc,
        sample_data,
    )
    return pl_set


def march_hard(
    bb: "BB",
    x_samples: int,
    y_samples: int,
    threshold: float,
    sample_func: _SampleFunc,
) -> PolylineSet:
    """Trace an *aliased* curve of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding
    box area using the sampling function and context.

    :param BB bb: Bounding box of the area to sample within
    :param int x_samples: Number of samples in x
    :param int y_samples: Number of samples in y
    :param float threshold: A higher value means more error is tolerated
    :param sample_func: The sample function will be called for
        x_samples * y_samples spread across the bounding box area, and should
        return a float.
    :type sample_func: ``func(point: Tuple[float, float]) -> float``
    :return: PolylineSet with the polylines found.
    """

    pl_set = PolylineSet()
    segment_data = ffi.new_handle(pl_set)
    sample_data = ffi.new_handle(sample_func)

    lib.cpMarchHard(
        bb,
        x_samples,
        y_samples,
        threshold,
        lib.ext_cpMarchSegmentFunc,
        segment_data,
        lib.ext_cpMarchSampleFunc,
        sample_data,
    )

    return pl_set
