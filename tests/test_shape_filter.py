import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

class UnitTestShapeFilter(unittest.TestCase):
    def testInit(self):
        f = p.ShapeFilter()
        self.assertEqual(f.group, 0)
        self.assertEqual(f.categories, 0xffffffff)
        self.assertEqual(f.mask, 0xffffffff)

        f = p.ShapeFilter(1,2,3)
        self.assertEqual(f.group, 1)
        self.assertEqual(f.categories, 2)
        self.assertEqual(f.mask, 3)

    def testConstants(self):
        self.assertEqual(p.ShapeFilter.ALL_MASKS, 0xffffffff)
        self.assertEqual(p.ShapeFilter.ALL_CATEGORIES, 0xffffffff)

    def testEq(self):
        f1 = p.ShapeFilter(1,2,3)
        f2 = p.ShapeFilter(1,2,3)
        f3 = p.ShapeFilter(2,3,4)
        self.assertTrue(f1 == f2)
        self.assertTrue(f1 != f3)

class UnitTestContactPoint(unittest.TestCase):
    pass
    
class UnitTestContactPointSet(unittest.TestCase):
    pass
