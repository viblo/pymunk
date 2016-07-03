__docformat__ = "reStructuredText"

from ._chipmunk_cffi import lib, ffi
from .vec2d import Vec2d
from .bb import BB


def _to_chipmunk(polyline):
    l = len(polyline)
    _line = ffi.new("cpPolyline *", {"verts": l})
    _line.count = l
    _line.capacity = l
    _line.verts = polyline
    return _line

def _from_polyline_set(_set):
    lines = []
    for i in range(_set.count):
        line = []
        for j in range(_set.lines[i].count):
            line.append(Vec2d(_set.lines[i].verts[j]))
        lines.append(line)
    return lines
    
def is_closed(polyline):
    """Returns true if the first vertex is equal to the last.
    
    :Parameters:
        polyline : [(x,y)] or [`Vec2d`]
            Polyline to simplify.
    """
    return bool(lib.cpPolylineIsClosed(_to_chipmunk(polyline)))

def simplify_curves(polyline, tolerance):
    """Returns a copy of a polyline simplified by using the Douglas-Peucker 
    algorithm.

    This works very well on smooth or gently curved shapes, but not well on 
    straight edged or angular shapes.

    :Parameters:
        polyline : [(x,y)] or [`Vec2d`]
            Polyline to simplify.
        tolerance : float
            A higher value means more error is tolerated.
    """

    _line = lib.cpPolylineSimplifyCurves(_to_chipmunk(polyline), tolerance)
    simplified = []
    for i in range(_line.count):
        simplified.append(Vec2d(_line.verts[i]))
    return simplified

def simplify_vertexes(polyline, tolerance):
    """Returns a copy of a polyline simplified by discarding "flat" vertexes.
        
    This works well on straigt edged or angular shapes, not as well on smooth 
    shapes.    

    :Parameters:
        polyline : [(x,y)] or [`Vec2d`]
            Polyline to simplify.
        tolerance : float
            A higher value means more error is tolerated.
    """
    _line = lib.cpPolylineSimplifyVertexes(_to_chipmunk(polyline), tolerance)
    simplified = []
    for i in range(_line.count):
        simplified.append(Vec2d(_line.verts[i]))
    return simplified

def to_convex_hull(polyline, tolerance):
    """Get the convex hull of a polyline as a looped polyline.

    :Parameters:
        polyline : [(x,y)] or [`Vec2d`]
            The polyline to generate the hull for.
        tolerance : float
            A higher value means more error is tolerated.
    """
    _line = lib.cpPolylineToConvexHull(_to_chipmunk(polyline), tolerance)
    hull = []
    for i in range(_line.count):
        hull.append(Vec2d(_line.verts[i]))
    return hull

def convex_decomposition(polyline, tolerance):
    """Get an approximate convex decomposition from a polyline.

    Returns a list of convex hulls that match the original shape to within 
    tolerance.
    
    NOTE: If the input is a self intersecting polygon, the output might end up 
    overly simplified.

    :Parameters:
        polyline : [(x,y)] or [`Vec2d`]
            The polyline to get the convex hulls for.
        tolerance : float
            A higher value means more error is tolerated.
        
    """
    _line = _to_chipmunk(polyline)
    _set = lib.cpPolylineConvexDecomposition(_line, tolerance)
    return _from_polyline_set(_set)

import collections
class PolylineSet(collections.Sequence):
    """A set of Polylines. 
    
    Mainly intended to be used for its `collect_segment()` function when generating
    geometry with the `march_soft()` and `march_hard()` functions.    
    """
    def __init__(self):
        self._set = lib.cpPolylineSetNew()

    def collect_segment(self, v0, v1):
        """Add a line segment to a polyline set.
        
        A segment will either start a new polyline, join two others, or add to 
        or loop an existing polyline. This is mostly intended to be used as a 
        callback directly from `march_soft()` or `march_hard()`.
        
        """
        lib.cpPolylineSetCollectSegment(v0, v1, self._set)

    def __len__(self):
        return self._set.count

    def __getitem__(self, key):
        if key >= self._set.count:
            raise IndexError
        line = []
        for i in range(self._set.lines[key].count):
            line.append(Vec2d(self._set.lines[key].verts[i]))
        return line

def march_soft(bb, x_samples, y_samples, threshold, segment_func, sample_func):
    """Trace an anti-aliased contour of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding 
    box area using the sampling function and context. 

    :Parameters:
        bb : `BB`
            bounding box of the area to sample within.
        x_samples : int
            Number of samples in x
        y_samples : int 
            Number of samples in y
        threshold : float
            A higher value means more error is tolerated
        segment_func : ``func(v0, v1)``
            The segment function will be called for each segment detected that 
            lies along the density contour for threshold. v0 and v1 are `Vec2d`.
        sample_func : ``func(point) -> float``
            The sample function will be called for x_samples * y_samples spread
            across the bounding box area, and should return a float. point is 
            a `Vec2d`.
    """
    
    @ffi.callback("typedef void (*cpMarchSegmentFunc)"
        "(cpVect v0, cpVect v1, void *data)")
    def _seg_f(v0, v1, _data):
        segment_func(Vec2d(v0), Vec2d(v1))
        
    @ffi.callback("typedef cpFloat (*cpMarchSampleFunc)"
        "(cpVect point, void *data)")
    def _sam_f(point, _data):
        return sample_func(Vec2d(point))
    
    lib.cpMarchSoft(bb._bb[0], x_samples, y_samples, threshold, 
        _seg_f, ffi.NULL, _sam_f, ffi.NULL)

def march_hard(bb, x_samples, y_samples, threshold, segment_func, sample_func):
    """Trace an aliased curve of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding 
    box area using the sampling function and context. 

     :Parameters:
        bb : `BB`
            bounding box of the area to sample within.
        x_samples : int
            Number of samples in x
        y_samples : int 
            Number of samples in y
        threshold : float
            A higher value means more error is tolerated
        segment_func : ``func(v0, v1)``
            The segment function will be called for each segment detected that 
            lies along the density contour for threshold. v0 and v1 are `Vec2d`.
        sample_func : ``func(point) -> float``
            The sample function will be called for x_samples * y_samples spread
            across the bounding box area, and should return a float. point is 
            a `Vec2d`.
    """
    @ffi.callback("typedef void (*cpMarchSegmentFunc)"
        "(cpVect v0, cpVect v1, void *data)")
    def _seg_f(v0, v1, _data):
        segment_func(Vec2d(v0), Vec2d(v1))
        
    @ffi.callback("typedef cpFloat (*cpMarchSampleFunc)"
        "(cpVect point, void *data)")
    def _sam_f(point, _data):
        return sample_func(Vec2d(point))
    
    lib.cpMarchHard(bb._bb[0], x_samples, y_samples, threshold, 
        _seg_f, ffi.NULL, _sam_f, ffi.NULL)
