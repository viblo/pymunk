import math
import pickle
import unittest

import pymunk
from pymunk.vec2d import Vec2d


class UnitTestVec2d(unittest.TestCase):
    def testCreationAndAccess(self) -> None:
        v = Vec2d(*(0, 0))
        self.assertEqual(v.x, 0)
        self.assertEqual(v[0], 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v[1], 0)

        v = Vec2d(3, 5)
        self.assertEqual(v.x, 3)
        self.assertEqual(v[0], 3)
        self.assertEqual(v.y, 5)
        self.assertEqual(v[1], 5)

        v = Vec2d(111, 222)
        self.assertTrue(v.x == 111 and v.y == 222)
        with self.assertRaises(AttributeError):
            v.x = 333  # type: ignore
        with self.assertRaises(TypeError):
            v[1] = 444  # type: ignore

        v = Vec2d(3, 5)
        self.assertEqual(len(v), 2)
        self.assertEqual(list(v), [3, 5])
        self.assertEqual(tuple(v), (3, 5))

    def testMath(self) -> None:
        v = Vec2d(111, 222)
        self.assertEqual(v + Vec2d(1, 2), Vec2d(112, 224))
        self.assertEqual(v + (1, 2), Vec2d(112, 224))
        self.assertEqual((1, 2) + v, Vec2d(112, 224))

        self.assertEqual(v - Vec2d(1, 2), Vec2d(110, 220))
        self.assertEqual(v - (1, 2), Vec2d(110, 220))
        self.assertEqual((1, 2) - v, Vec2d(-110, -220))

        self.assertEqual(v * 3, Vec2d(333, 666))
        self.assertEqual(3 * v, Vec2d(333, 666))

        self.assertEqual(v / 2, Vec2d(55.5, 111))
        self.assertEqual(v // 2, Vec2d(55, 111))

    def testUnary(self) -> None:
        v = Vec2d(111, 222)
        self.assertEqual(+v, v)
        self.assertEqual(-v, Vec2d(-111, -222))
        self.assertAlmostEqual(abs(v), 248.20354550247666)

    def testLength(self) -> None:
        v = Vec2d(3, 4)
        self.assertTrue(v.length == 5)
        self.assertTrue(v.get_length_sqrd() == 25)
        normalized, length = v.normalized_and_length()
        self.assertEqual(normalized, Vec2d(0.6, 0.8))
        self.assertEqual(length, 5)
        normalized, length = Vec2d(0, 0).normalized_and_length()
        self.assertEqual(normalized, Vec2d(0, 0))
        self.assertEqual(length, 0)
        with self.assertRaises(AttributeError):
            v.length = 5  # type: ignore
        v2 = Vec2d(10, -2)
        self.assertEqual(v.get_distance(v2), (v - v2).length)

    def testAnglesDegrees(self) -> None:
        v = Vec2d(0, 3)
        self.assertEqual(v.angle_degrees, 90)
        v2 = Vec2d(*v)
        v = v.rotated_degrees(-90)
        self.assertEqual(v.get_angle_degrees_between(v2), 90)
        v2 = v2.rotated_degrees(-90)
        self.assertEqual(v.length, v2.length)
        self.assertAlmostEqual(v2.angle_degrees, 0, 10)
        self.assertAlmostEqual(v2.x, 3)
        self.assertAlmostEqual(v2.y, 0)
        self.assertTrue((v - v2).length < 0.00001)
        self.assertEqual(v.length, v2.length)
        v2 = v2.rotated_degrees(300)
        self.assertAlmostEqual(
            v.get_angle_degrees_between(v2), -60
        )  # Allow a little more error than usual (floats..)
        v2 = v2.rotated_degrees(v2.get_angle_degrees_between(v))
        self.assertAlmostEqual(v.get_angle_degrees_between(v2), 0)

    def testAnglesRadians(self) -> None:
        v = Vec2d(0, 3)
        self.assertEqual(v.angle, math.pi / 2.0)
        v2 = Vec2d(*v)
        v = v.rotated(-math.pi / 2.0)
        self.assertEqual(v.get_angle_between(v2), math.pi / 2.0)
        v2 = v2.rotated(-math.pi / 2.0)
        self.assertEqual(v.length, v2.length)
        self.assertAlmostEqual(v2.angle, 0)
        self.assertEqual(v2.x, 3)
        self.assertAlmostEqual(v2.y, 0)
        self.assertTrue((v - v2).length < 0.00001)
        self.assertEqual(v.length, v2.length)
        v2 = v2.rotated(math.pi / 3.0 * 5.0)
        self.assertAlmostEqual(
            v.get_angle_between(v2), -math.pi / 3.0
        )  # Allow a little more error than usual (floats..)
        v2 = v2.rotated(v2.get_angle_between(v))
        self.assertAlmostEqual(v.get_angle_between(v2), 0)

    def testHighLevel(self) -> None:
        basis0 = Vec2d(5.0, 0)
        basis1 = Vec2d(0, 0.5)
        v = Vec2d(10, 1)
        self.assertEqual(v.convert_to_basis(basis0, basis1), (2, 2))
        self.assertEqual(v.projection(basis0), (10, 0))
        self.assertEqual(v.projection(Vec2d(0, 0)), (0, 0))
        self.assertEqual(v.projection((0, 0)), (0, 0))
        self.assertEqual(basis0.dot(basis1), 0)

    def testCross(self) -> None:
        lhs = Vec2d(1, 0.5)
        rhs = Vec2d(4, 6)
        self.assertEqual(lhs.cross(rhs), 4)

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

    def testImmuatable(self) -> None:
        inplace_vec = Vec2d(5, 13)
        inplace_ref = inplace_vec
        inplace_vec *= 0.5
        inplace_vec += Vec2d(0.5, 0.5)
        inplace_vec -= Vec2d(3.5, 3.5)
        inplace_vec /= 5
        self.assertEqual(inplace_ref, Vec2d(5, 13))
        self.assertEqual(inplace_vec, Vec2d(-0.1, 0.7))

    def testPickle(self) -> None:
        testvec = Vec2d(5, 0.3)
        testvec_str = pickle.dumps(testvec)
        loaded_vec = pickle.loads(testvec_str)
        self.assertEqual(testvec, loaded_vec)
