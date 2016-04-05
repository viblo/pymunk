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

    def testEq(self):
        f1 = p.ShapeFilter(1,2,3)
        f2 = p.ShapeFilter(1,2,3)
        f3 = p.ShapeFilter(2,3,4)
        self.assertTrue(f1 == f2)
        self.assertTrue(f1 != f3)

class UnitTestTransform(unittest.TestCase):
    def testInit(self):
        """"
        t = p.Transform()
        self.assertEqual(t.a, 0)
        self.assertEqual(t.b, 0)
        self.assertEqual(t.c, 0)
        self.assertEqual(t.d, 0)
        self.assertEqual(t.tx, 0)
        self.assertEqual(t.ty, 0)
        """
        t = p.Transform(1,2,3,4,5,6)
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 2)
        self.assertEqual(t.c, 3)
        self.assertEqual(t.d, 4)
        self.assertEqual(t.tx, 5)
        self.assertEqual(t.ty, 6)
        self.assertEqual(str(t), "Transform(a=1, b=2, c=3, d=4, tx=5, ty=6)")

    def testIdentity(self):
        t = p.Transform.identity()
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 0)
        self.assertEqual(t.c, 0)
        self.assertEqual(t.d, 1)
        self.assertEqual(t.tx, 0)
        self.assertEqual(t.ty, 0)

class UnitTestContactPoint(unittest.TestCase):
    pass
    
class UnitTestContactPointSet(unittest.TestCase):
    pass
