import unittest

import pymunk
from pymunk.vec2d import Vec2d


class UnitTestVec2d(unittest.TestCase):
    def testCreationAndAccess(self) -> None:

        v = Vec2d(111, 222)
        with self.assertRaises(TypeError):
            v[1] = 444  # type: ignore

    def testLength(self) -> None:
        v = Vec2d(3, 4)
        with self.assertRaises(AttributeError):
            v.length = 5  # type: ignore

    def testComparison(self) -> None:
        int_vec = Vec2d(3, -2)
        flt_vec = Vec2d(3.0, -2.0)
        zero_vec = Vec2d(0, 0)
        self.assertTrue(int_vec == flt_vec)
        self.assertTrue(int_vec != zero_vec)
        self.assertTrue((flt_vec == zero_vec) == False)
        self.assertTrue((flt_vec != int_vec) == False)
        self.assertTrue(int_vec == (3, -2))
        self.assertTrue(int_vec != (0, 0))
        self.assertTrue(int_vec != 5)  # type: ignore
        self.assertTrue(int_vec != (3, -2, -5))  # type: ignore
