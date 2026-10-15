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

    def testNonorthogonalBasis(self) -> None:
        bases = [
            ((32, 16), (-32, 16)),
            ((2, 1), (1, 3)),
            ((1, 3), (2, 1)),
            ((-2, -1), (1, 3)),
        ]
        for x_axis, y_axis in bases:
            for expected in [(1, 0), (0, 1), (3, -2), (-0.5, 1.5)]:
                with self.subTest(basis=(x_axis, y_axis), expected=expected):
                    world = Vec2d(*x_axis) * expected[0] + Vec2d(*y_axis) * expected[1]
                    actual = world.convert_to_basis(x_axis, y_axis)
                    self.assertAlmostEqual(actual.x, expected[0])
                    self.assertAlmostEqual(actual.y, expected[1])

    def testOrthogonalBasis(self) -> None:
        for x_axis, y_axis in [((5, 0), (0, 0.5)), ((3, 4), (-4, 3))]:
            with self.subTest(basis=(x_axis, y_axis)):
                expected = Vec2d(2, -3)
                world = Vec2d(*x_axis) * expected.x + Vec2d(*y_axis) * expected.y
                self.assertEqual(world.convert_to_basis(x_axis, y_axis), expected)

    def testDependentBasis(self) -> None:
        for x_axis, y_axis in [((0, 0), (0, 1)), ((1, 2), (2, 4))]:
            with self.subTest(basis=(x_axis, y_axis)):
                with self.assertRaises(ZeroDivisionError):
                    Vec2d(3, 4).convert_to_basis(x_axis, y_axis)
