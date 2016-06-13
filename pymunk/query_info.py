__docformat__ = "reStructuredText"

from collections import namedtuple

class PointQueryInfo(
    namedtuple('PointQueryInfo', ['shape', 'point', 'distance', 'gradient'])):
    """PointQueryInfo holds the result of a point query made on a Shape or
    Space.
    
    The properties are as follows
    
    shape 
    The nearest shape, None if no shape was within range.
    
    point
    The closest point on the shape's surface. (in world space
    coordinates)
    
    distance
    The distance to the point. The distance is negative if the
    point is inside the shape.
        
    gradient
    The gradient of the signed distance function.

        The value should be similar to
        PointQueryInfo.point/PointQueryInfo.distance, but accurate even for
        very small values of info.distance.
    """
    __slots__ = ()

class SegmentQueryInfo(
    namedtuple('SegmentQueryInfo', ['shape', 'point', 'normal', 'alpha'])):
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

    The properties are as follows

    shape
    Shape that was hit, or None if no collision occured
    
    point 
    The point of impact.

    normal
    The normal of the surface hit.
    
    alpha
    The normalized distance along the query segment in the range [0, 1]

    """
    __slots__ = ()
    
class ShapeQueryInfo(
    namedtuple('ShapeQueryInfo', ['shape', 'contact_point_set'])):
    """Shape queries return more information than just a simple yes or no,
    they also return where a shape was hit. This object hold that information.
    """
    __slots__ = ()
