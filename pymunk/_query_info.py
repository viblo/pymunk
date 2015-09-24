__version__ = "$Id$"
__docformat__ = "reStructuredText"

class PointQueryInfo(object):
    """PointQueryInfo holds the result of a point query made on a Shape or
    Space.
    """
    def __init__(self, shape, point, distance, gradient):
        """You shouldn't need to initialize PointQueryInfo objects
        manually.
        """
        self._shape = shape
        self._point = point
        self._distance = distance
        self._gradient = gradient

    def __repr__(self):
        return 'PointQueryInfo(%s,%s,%s,%s)' % (self.shape, self.point, self.distance, self.gradient)

    shape = property(lambda self:self._shape,
        doc = """The nearest shape, None if no shape was within range.""")

    point = property(lambda self:self._point,
        doc = """The closest point on the shape's surface. (in world space
        coordinates)
        """)

    distance = property(lambda self:self._distance,
        doc = """The distance to the point. The distance is negative if the
        point is inside the shape.
        """)

    gradient = property(lambda self:self._gradient,
        doc = """The gradient of the signed distance function.

        The value should be similar to
        PointQueryInfo.point/PointQueryInfo.distance, but accurate even for
        very small values of info.distance.
        """)


class SegmentQueryInfo(object):
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
    def __init__(self, shape, point, normal, alpha):
        """You shouldn't need to initialize SegmentQueryInfo objects
        manually.
        """
        self._shape = shape
        self._point = point
        self._normal = normal
        self._alpha = alpha

    def __repr__(self):
        return "SegmentQueryInfo(%s, %s, %s, %s)" % (self.shape, self.point, self.normal, self.alpha)

    shape = property(lambda self: self._shape,
        doc = """Shape that was hit, or None if no collision occured""")

    point = property(lambda self: self._point,
        doc = """The point of impact.""")

    normal = property(lambda self: self._normal,
        doc = """The normal of the surface hit.""")

    alpha = property(lambda self: self._alpha,
        doc = """The normalized distance along the query segment in the
        range [0, 1]
        """)
