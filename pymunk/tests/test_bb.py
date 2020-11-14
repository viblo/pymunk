import pickle
import unittest

import pymunk as p
from pymunk.vec2d import Vec2d


class UnitTestBB(unittest.TestCase):
    def setUp(self) -> None:
        # print "testing pymunk version " + p.version
        pass

    def testCreation(self) -> None:
        bb_empty = p.BB()

        self.assertEqual(bb_empty.left, 0)
        self.assertEqual(bb_empty.bottom, 0)
        self.assertEqual(bb_empty.right, 0)
        self.assertEqual(bb_empty.top, 0)

        bb_defined = p.BB(-10, -5, 15, 20)

        self.assertEqual(bb_defined.left, -10)
        self.assertEqual(bb_defined.bottom, -5)
        self.assertEqual(bb_defined.right, 15)
        self.assertEqual(bb_defined.top, 20)

        bb_circle = p.BB.newForCircle((3, 3), 3)
        self.assertEqual(bb_circle.left, 0)
        self.assertEqual(bb_circle.bottom, 0)
        self.assertEqual(bb_circle.right, 6)
        self.assertEqual(bb_circle.top, 6)

    def testMerge(self) -> None:
        bb1 = p.BB(0, 0, 10, 10)
        bb2 = p.BB(2, 0, 10, 10)
        bb3 = p.BB(10, 10, 15, 15)

        self.assertEqual(bb1.merge(bb2), p.BB(0, 0, 10, 10))
        self.assertEqual(bb2.merge(bb3).merge(bb1), p.BB(0, 0, 15, 15))

    def testMethods(self) -> None:
        bb1 = p.BB(0, 0, 10, 10)
        bb2 = p.BB(10, 10, 20, 20)
        bb3 = p.BB(4, 4, 5, 5)
        bb4 = p.BB(2, 0, 10, 10)

        v1 = Vec2d(1, 1)
        v2 = Vec2d(100, 3)
        self.assertTrue(bb1.intersects(bb2))
        self.assertFalse(bb3.intersects(bb2))

        self.assertTrue(bb1.intersects_segment(v1, v2))
        self.assertFalse(bb3.intersects_segment(v1, v2))

        self.assertTrue(bb1.contains(bb3))
        self.assertFalse(bb1.contains(bb2))

        self.assertTrue(bb1.contains_vect(v1))
        self.assertFalse(bb1.contains_vect(v2))

        self.assertEqual(bb1.expand(v1), bb1)
        self.assertEqual(bb1.expand(-v2), p.BB(-100, -3, 10, 10))

        self.assertEqual(bb1.center(), (5, 5))
        self.assertEqual(bb1.area(), 100)

        self.assertEqual(bb1.merged_area(bb2), 400)

        self.assertEqual(bb2.segment_query(v1, v2), float("inf"))
        self.assertEqual(bb1.segment_query((-1, 1), (99, 1)), 0.01)

        self.assertEqual(bb1.clamp_vect(v2), Vec2d(10, 3))

        # self.assertEqual(bb1.wrap_vect((11,11)), (1,1))

    def testPickle(self) -> None:
        x = p.BB(4, 4, 5, 5)

        s = pickle.dumps(x, 2)
        actual = pickle.loads(s)

        self.assertEqual(x, actual)

        self.assertEqual(p.BB(*x), x)
