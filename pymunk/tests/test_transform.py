import pymunk as p
from pymunk.vec2d import Vec2d
import unittest
import pickle

class UnitTestTransform(unittest.TestCase):
    def testInit(self):
        
        t = p.Transform(1,2,3,4,5,6)
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 2)
        self.assertEqual(t.c, 3)
        self.assertEqual(t.d, 4)
        self.assertEqual(t.tx, 5)
        self.assertEqual(t.ty, 6)
        self.assertEqual(str(t), "Transform(a=1, b=2, c=3, d=4, tx=5, ty=6)")

        t = p.Transform(b=4, ty=2)
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 4)
        self.assertEqual(t.c, 0)
        self.assertEqual(t.d, 1)
        self.assertEqual(t.tx, 0)
        self.assertEqual(t.ty, 2)

    def testIdentity(self):
        t = p.Transform.identity()
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 0)
        self.assertEqual(t.c, 0)
        self.assertEqual(t.d, 1)
        self.assertEqual(t.tx, 0)
        self.assertEqual(t.ty, 0)

    def testPickle(self):
        x = p.Transform.identity()
        s = pickle.dumps(x, 2)
        actual = pickle.loads(s)
        self.assertEqual(x, actual)
