__docformat__ = "reStructuredText"

import copy

from . import _chipmunk_cffi
lib = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi
from .vec2d import Vec2d
from ._pickle import PickleMixin

class BB(PickleMixin, object):
    """Simple bounding box.

    Stored as left, bottom, right, top values.
    """

    _pickle_attrs_init = ['left', 'bottom', 'right', 'top']

    def __init__(self, *args):
        """Create a new instance of a bounding box. 
        
        Can be created with zero size with bb = BB() or with four args defining 
        left, bottom, right and top: bb = BB(left, bottom, right, top)
        """
        if len(args) == 0:
            self._bbp = ffi.new("cpBB *")
            self._bb = self._bbp[0]
        elif len(args) == 1:
            self._bb = args[0]
        else:
            self._bbp = ffi.new("cpBB *", args)
            self._bb = self._bbp[0]

    @staticmethod
    def newForCircle(p, r):
        """Convenience constructor for making a BB fitting a circle at
        position p with radius r.
        """
        
        bb_ = lib._cpBBNewForCircle(p, r)
        return BB(bb_)

    def __repr__(self):
        return 'BB(%s, %s, %s, %s)' % (self.left, self.bottom, self.right, self.top)

    def __eq__(self, other):
        return self.left == other.left and self.bottom == other.bottom and \
            self.right == other.right and self.top == other.top

    def __ne__(self, other):
        return not self.__eq__(other)

    left = property(lambda self: self._bb.l)
    bottom = property(lambda self: self._bb.b)
    right = property(lambda self: self._bb.r)
    top = property(lambda self: self._bb.t)

    def intersects(self, other):
        """Returns true if the bounding boxes intersect"""
        return bool(lib._cpBBIntersects(self._bb, other._bb))

    def intersects_segment(self, a, b):
        """Returns true if the segment defined by endpoints a and b
        intersect this bb."""
        return bool(lib._cpBBIntersectsSegment(self._bb, tuple(a), tuple(b)))

    def contains(self, other):
        """Returns true if bb completley contains the other bb"""
        return bool(lib._cpBBContainsBB(self._bb, other._bb))

    def contains_vect(self, v):
        """Returns true if this bb contains the vector v"""
        return bool(lib._cpBBContainsVect(self._bb, tuple(v)))

    def merge(self, other):
        """Return the minimal bounding box that contains both this bb and the
        other bb
        """
        return BB(lib._cpBBMerge(self._bb, other._bb))

    def expand(self, v):
        """Return the minimal bounding box that contans both this bounding box
        and the vector v
        """
        return BB(lib._cpBBExpand(self._bb, tuple(v)))

    def center(self):
        """Return the center"""
        return Vec2d._fromcffi(lib._cpBBCenter(self._bb))

    def area(self):
        """Return the area"""
        return lib._cpBBArea(self._bb)

    def merged_area(self, other):
        """Merges this and other then returns the area of the merged bounding
        box.
        """
        return lib._cpBBMergedArea(self._bb, other._bb)

    def segment_query(self, a, b):
        """Returns the fraction along the segment query the BB is hit.

        Returns infinity if it doesnt hit
        """
        return lib._cpBBSegmentQuery(self._bb, tuple(a), tuple(b))

    def clamp_vect(self, v):
        """Returns a copy of the vector v clamped to the bounding box"""
        return Vec2d._fromcffi(lib._cpBBClampVect(self._bb, tuple(v)))

    '''
    def wrap_vect(self, v):
        """Returns a copy of v wrapped to the bounding box.

        That is, BB(0,0,10,10).wrap_vect((5,5)) == Vec2d._fromcffi(10,10)
        """
        return lib._cpBBWrapVect(self._bb[0], v)
    '''

    def copy(self):
        """Create a deep copy of this BB."""
        return copy.deepcopy(self)
