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
    >>> segments = []

    >>> def segment_func(v0, v1):
    ...     segments.append((tuple(v0), tuple(v1)))
    >>> def sample_func(point):
    ...     x = int(point.x)
    ...     y = int(point.y)
    ...     return 1 if img[y][x] == "x" else 0

    >>> march_soft(pymunk.BB(0,0,6,6), 7, 7, .5, segment_func, sample_func)
    >>> print(len(segments))
    13

The information in segments can now be used to create geometry, for example as 
a Pymunk Poly or Segment::

    >>> s = pymunk.Space()
    >>> for (a,b) in segments:
    ...     segment = pymunk.Segment(s.static_body, a, b, 5)  
    ...     s.add(segment)


"""
__docformat__ = "reStructuredText"

__all__ = ["is_closed", "simplify_curves", "simplify_vertexes", 
    "to_convex_hull", "convex_decomposition", "PolylineSet", "march_soft", 
    "march_hard"]

import collections

from ._chipmunk_cffi import lib, ffi
from .vec2d import Vec2d
from .bb import BB

def _to_chipmunk(polyline):
    l = len(polyline)
    _line = ffi.new("cpPolyline *", {"verts": l})
    _line.count = l
    _line.capacity = l
    _line.verts = list(map(tuple, polyline))
    return _line

def _from_polyline_set(_set):
    lines = []
    for i in range(_set.count):
        line = []
        for j in range(_set.lines[i].count):
            line.append(Vec2d._fromcffi(_set.lines[i].verts[j]))
        lines.append(line)
    return lines
    
def is_closed(polyline):
    """Returns true if the first vertex is equal to the last.
    
    :param polyline: Polyline to simplify.
    :type polyline: [(float,float)]
    :rtype: `bool`
    """
    return bool(lib.cpPolylineIsClosed(_to_chipmunk(polyline)))

def simplify_curves(polyline, tolerance):
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
        simplified.append(Vec2d._fromcffi(_line.verts[i]))
    return simplified

def simplify_vertexes(polyline, tolerance):
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
        simplified.append(Vec2d._fromcffi(_line.verts[i]))
    return simplified

def to_convex_hull(polyline, tolerance):
    """Get the convex hull of a polyline as a looped polyline.

    :param polyline: Polyline to simplify.
    :type polyline: [(float,float)]
    :param float tolerance: A higher value means more error is tolerated.
    :rtype: [(float,float)]
    """
    _line = lib.cpPolylineToConvexHull(_to_chipmunk(polyline), tolerance)
    hull = []
    for i in range(_line.count):
        hull.append(Vec2d._fromcffi(_line.verts[i]))
    return hull

def convex_decomposition(polyline, tolerance):
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
    _line = _to_chipmunk(polyline)
    _set = lib.cpPolylineConvexDecomposition(_line, tolerance)
    return _from_polyline_set(_set)


class PolylineSet(collections.Sequence):
    """A set of Polylines. 
    
    Mainly intended to be used for its :py:meth:`collect_segment` function 
    when generating geometry with the :py:func:`march_soft` and 
    :py:func:`march_hard` functions.    
    """
    def __init__(self):
        def free(_set):
            lib.cpPolylineSetFree(_set, True)
        self._set = ffi.gc(lib.cpPolylineSetNew(), free)

    def collect_segment(self, v0, v1):
        """Add a line segment to a polyline set.
        
        A segment will either start a new polyline, join two others, or add to 
        or loop an existing polyline. This is mostly intended to be used as a 
        callback directly from :py:func:`march_soft` or :py:func:`march_hard`.
        
        :param v0: Start of segment
        :type v0: (float,float)
        :param v1: End of segment
        :type v1: (float,float)
        """
        lib.cpPolylineSetCollectSegment(tuple(v0), tuple(v1), self._set)

    def __len__(self):
        return self._set.count

    def __getitem__(self, key):
        if key >= self._set.count:
            raise IndexError
        line = []
        for i in range(self._set.lines[key].count):
            line.append(Vec2d._fromcffi(self._set.lines[key].verts[i]))
        return line

def march_soft(bb, x_samples, y_samples, threshold, segment_func, sample_func):
    """Trace an *anti-aliased* contour of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding 
    box area using the sampling function and context. 

    :param BB bb: Bounding box of the area to sample within
    :param int x_samples: Number of samples in x
    :param int y_samples: Number of samples in y
    :param float threshold: A higher value means more error is tolerated
    :param segment_func: The segment function will be called for each segment 
        detected that lies along the density contour for threshold. 
    :type segment_func: ``func(v0 : Vec2d, v1 : Vec2d)``
    :param sample_func: The sample function will be called for 
        x_samples * y_samples spread across the bounding box area, and should 
        return a float. 
    :type sample_func: ``func(point: Vec2d) -> float``
    """
    
    @ffi.callback("cpMarchSegmentFunc")
    def _seg_f(v0, v1, _data):
        segment_func(Vec2d._fromcffi(v0), Vec2d._fromcffi(v1))
        
    @ffi.callback("cpMarchSampleFunc")
    def _sam_f(point, _data):
        return sample_func(Vec2d._fromcffi(point))
    
    lib.cpMarchSoft(bb._bb, x_samples, y_samples, threshold, 
        _seg_f, ffi.NULL, _sam_f, ffi.NULL)

def march_hard(bb, x_samples, y_samples, threshold, segment_func, sample_func):
    """Trace an *aliased* curve of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding 
    box area using the sampling function and context. 

    :param BB bb: Bounding box of the area to sample within
    :param int x_samples: Number of samples in x
    :param int y_samples: Number of samples in y
    :param float threshold: A higher value means more error is tolerated
    :param segment_func: The segment function will be called for each segment 
        detected that lies along the density contour for threshold. 
    :type segment_func: ``func(v0 : Vec2d, v1 : Vec2d)``
    :param sample_func: The sample function will be called for 
        x_samples * y_samples spread across the bounding box area, and should 
        return a float. 
    :type sample_func: ``func(point: Vec2d) -> float``
    """
    
    @ffi.callback("cpMarchSegmentFunc")
    def _seg_f(v0, v1, _data):
        segment_func(Vec2d._fromcffi(v0), Vec2d._fromcffi(v1))
        
    @ffi.callback("cpMarchSampleFunc")
    def _sam_f(point, _data):
        return sample_func(Vec2d._fromcffi(point))
    
    lib.cpMarchHard(bb._bb, x_samples, y_samples, threshold, 
        _seg_f, ffi.NULL, _sam_f, ffi.NULL)
