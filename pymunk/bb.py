__docformat__ = "reStructuredText"

from typing import NamedTuple, Tuple

from . import _chipmunk_cffi

lib = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi
from .vec2d import Vec2d


class BB(NamedTuple):
    """Simple axis-aligned 2D bounding box.

    Stored as left, bottom, right, top values.

    An instance can be created in this way:
        >>> BB(left=1, bottom=5, right=20, top=10)
        BB(left=1, bottom=5, right=20, top=10)

    Or partially, for example like this:
        >>> BB(right=5, top=10)
        BB(left=0, bottom=0, right=5, top=10)
    """

    left: float = 0
    bottom: float = 0
    right: float = 0
    top: float = 0

    @staticmethod
    def newForCircle(p: Tuple[float, float], r: float) -> "BB":
        """Convenience constructor for making a BB fitting a circle at
        position p with radius r.
        """

        bb_ = lib.cpBBNewForCircle(p, r)
        return BB(bb_.l, bb_.b, bb_.r, bb_.t)

    def intersects(self, other: "BB") -> bool:
        """Returns true if the bounding boxes intersect"""
        return bool(lib.cpBBIntersects(self, other))

    def intersects_segment(
        self, a: Tuple[float, float], b: Tuple[float, float]
    ) -> bool:
        """Returns true if the segment defined by endpoints a and b
        intersect this bb."""
        assert len(a) == 2
        assert len(b) == 2
        return bool(lib.cpBBIntersectsSegment(self, a, b))

    def contains(self, other: "BB") -> bool:
        """Returns true if bb completley contains the other bb"""
        return bool(lib.cpBBContainsBB(self, other))

    def contains_vect(self, v: Tuple[float, float]) -> bool:
        """Returns true if this bb contains the vector v"""
        assert len(v) == 2
        return bool(lib.cpBBContainsVect(self, v))

    def merge(self, other: "BB") -> "BB":
        """Return the minimal bounding box that contains both this bb and the
        other bb
        """
        cp_bb = lib.cpBBMerge(self, other)
        return BB(cp_bb.l, cp_bb.b, cp_bb.r, cp_bb.t)

    def expand(self, v: Tuple[float, float]) -> "BB":
        """Return the minimal bounding box that contans both this bounding box
        and the vector v
        """
        cp_bb = lib.cpBBExpand(self, tuple(v))
        return BB(cp_bb.l, cp_bb.b, cp_bb.r, cp_bb.t)

    def center(self) -> Vec2d:
        """Return the center"""
        v = lib.cpBBCenter(self)
        return Vec2d(v.x, v.y)

    def area(self) -> float:
        """Return the area"""
        return lib.cpBBArea(self)

    def merged_area(self, other: "BB") -> float:
        """Merges this and other then returns the area of the merged bounding
        box.
        """
        return lib.cpBBMergedArea(self, other)

    def segment_query(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """Returns the fraction along the segment query the BB is hit.

        Returns infinity if it doesnt hit
        """
        assert len(a) == 2
        assert len(b) == 2
        return lib.cpBBSegmentQuery(self, a, b)

    def clamp_vect(self, v: Tuple[float, float]) -> Vec2d:
        """Returns a copy of the vector v clamped to the bounding box"""
        assert len(v) == 2
        v2 = lib.cpBBClampVect(self, v)
        return Vec2d(v2.x, v2.y)

    '''
    def wrap_vect(self, v):
        """Returns a copy of v wrapped to the bounding box.

        That is, BB(0,0,10,10).wrap_vect((5,5)) == Vec2d._fromcffi(10,10)
        """
        return lib._cpBBWrapVect(self.cp_bb[0], v)
    '''
