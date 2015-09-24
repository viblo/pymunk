__version__ = "$Id$"
__docformat__ = "reStructuredText"

class Contact(object):
    """Contact information"""
    def __init__(self, _contact):
        """Initialize a Contact object from the Chipmunk equivalent struct

        .. note::
            You should never need to create an instance of this class directly.
        """
        self._point = _contact.point
        self._normal = _contact.normal
        self._dist = _contact.dist
        #self._contact = contact

    def __repr__(self):
        return "Contact(p: %s, n: %s, d: %s)" % (self.position, self.normal, self.distance)

    def _get_position(self):
        return self._point
    position = property(_get_position, doc="""Contact position""")

    def _get_normal(self):
        return self._normal
    normal = property(_get_normal, doc="""Contact normal""")

    def _get_distance(self):
        return self._dist
    distance = property(_get_distance, doc="""Penetration distance""")
