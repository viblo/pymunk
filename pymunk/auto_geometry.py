__docformat__ = "reStructuredText"

from ._chipmunk_cffi import lib, ffi
from .vec2d import Vec2d


def is_closed(poly_line):
    """ Returns true if the first vertex is equal to the last.
    
    :Parameters:
        poly_line : [(x,y)] or [`Vec2d`]
    """
    l = len(poly_line)
    _line = ffi.new("cpPolyline *", {"verts": l})
    _line.count = l
    _line.capacity = l
    _line.verts = poly_line

    return bool(lib.cpPolylineIsClosed(_line))


def simplify_curves(poly_line, tolerance):
    """Returns a copy of a poly_line simplified by using the Douglas-Peucker 
    algorithm.

    This works very well on smooth or gently curved shapes, but not well on 
    straight edged or angular shapes.

    :Parameters:
        poly_line : [(x,y)] or [`Vec2d`]
        tolerance : float
            A higher value means more error is tolerated.
    """
    pass

def simplify_vertexes(poly_line, tolerance):
    """Returns a copy of a polyline simplified by discarding "flat" vertexes.
        
    This works well on straigt edged or angular shapes, not as well on smooth 
    shapes.    
    """
    pass

def to_convex_hull(poly_line, tolerance):
    """Get the convex hull of a polyline as a looped polyline.
    """
    pass

def convex_decomposition(poly_line, tolerance):
    """Get an approximate convex decomposition from a polyline.

    Returns a list of convex hulls that match the original shape to within 
    tolerance.
    
    NOTE: If the input is a self intersecting polygon, the output might end up 
    overly simplified.
    """
    pass

def march_soft(bb, x_samples, y_samples, threshold, segment, 
    segment_data, sample, sample_data):
    """Trace an anti-aliased contour of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding 
    box area using the sampling function and context. The segment function will 
    be called for each segment detected that lies along the density contour for 
    threshold.
    """
    pass

def march_hard(bb, x_samples, y_samples, threshold, segment, segment_data,
    sample, sample_data):
    """Trace an aliased curve of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding 
    box area using the sampling function and context. The segment function will 
    be called for each segment detected that lies along the density contour for 
    threshold.
    """
    pass