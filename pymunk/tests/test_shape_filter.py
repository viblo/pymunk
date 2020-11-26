import pickle
import unittest

import pymunk as p


class UnitTestShapeFilter(unittest.TestCase):
    def testInit(self) -> None:
        f = p.ShapeFilter()
        self.assertEqual(f.group, 0)
        self.assertEqual(f.categories, 0xFFFFFFFF)
        self.assertEqual(f.mask, 0xFFFFFFFF)

        f = p.ShapeFilter(1, 2, 3)
        self.assertEqual(f.group, 1)
        self.assertEqual(f.categories, 2)
        self.assertEqual(f.mask, 3)

    def testConstants(self) -> None:
        self.assertEqual(p.ShapeFilter.ALL_MASKS(), 0xFFFFFFFF)
        self.assertEqual(p.ShapeFilter.ALL_CATEGORIES(), 0xFFFFFFFF)

    def testEq(self) -> None:
        f1 = p.ShapeFilter(1, 2, 3)
        f2 = p.ShapeFilter(1, 2, 3)
        f3 = p.ShapeFilter(2, 3, 4)
        self.assertTrue(f1 == f2)
        self.assertTrue(f1 != f3)

    def testPickle(self) -> None:
        x = p.ShapeFilter(1, 2, 3)
        s = pickle.dumps(x, 2)
        actual = pickle.loads(s)
        self.assertEqual(x, actual)


class UnitTestContactPoint(unittest.TestCase):
    pass


class UnitTestContactPointSet(unittest.TestCase):
    pass
