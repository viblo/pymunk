import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################

class UnitTestGeneral(unittest.TestCase):

    def testGeneral(self):
        p.version
        p.inf
        p.chipmunk_version

    def testMomentHelpers(self):
        m = p.moment_for_circle(1,2,3,(1,2))
        self.assertAlmostEqual(m, 11.5)

        m = p.moment_for_segment(1, (-10,0), (10,0), 1)
        self.assertAlmostEqual(m, 40.6666666666)

        m = p.moment_for_poly(1, [(0,0), (10,10), (10,0)], (1,2), 3)
        self.assertAlmostEqual(m, 98.3333333333)

        m = p.moment_for_box(1, 2, 3)
        self.assertAlmostEqual(m, 1.08333333333)

    def testAreaHelpers(self):
        a = p.area_for_circle(1,2)
        self.assertAlmostEqual(a, 9.4247779607)

        a = p.area_for_segment((-10,0), (10,0), 3)
        self.assertAlmostEqual(a, 148.27433388)

        a = p.area_for_poly([(0,0), (10,10), (10,0)], 3)
        self.assertAlmostEqual(a, 80.700740753)

class UnitTestBB(unittest.TestCase):
    def setUp(self):
        #print "testing pymunk version " + p.version
        pass

    def testCreation(self):
        bb_empty = p.BB()

        self.assertEqual(bb_empty.left, 0)
        self.assertEqual(bb_empty.bottom, 0)
        self.assertEqual(bb_empty.right, 0)
        self.assertEqual(bb_empty.top , 0)

        bb_defined = p.BB(-10,-5,15,20)

        self.assertEqual(bb_defined.left, -10)
        self.assertEqual(bb_defined.bottom, -5)
        self.assertEqual(bb_defined.right, 15)
        self.assertEqual(bb_defined.top, 20)

        bb_circle = p.BB.newForCircle((3,3),3)
        self.assertEqual(bb_circle.left, 0)
        self.assertEqual(bb_circle.bottom, 0)
        self.assertEqual(bb_circle.right, 6)
        self.assertEqual(bb_circle.top, 6)

    def testMethods(self):
        bb1 = p.BB(0,0,10,10)
        bb2 = p.BB(10,10,20,20)
        bb3 = p.BB(4,4,5,5)
        bb4 = p.BB(2,0,10,10)

        v1 = Vec2d(1,1)
        v2 = Vec2d(100,5)
        self.assert_(bb1.intersects(bb2))
        self.assertFalse(bb3.intersects(bb2))

        self.assert_(bb1.intersects_segment(v1,v2))
        self.assertFalse(bb3.intersects_segment(v1,v2))

        self.assert_(bb1.contains(bb3))
        self.assertFalse(bb1.contains(bb2))

        self.assert_(bb1.contains_vect(v1))
        self.assertFalse(bb1.contains_vect(v2))

        self.assertEqual(bb1.merge(bb2), p.BB(0,0,20,20))

        self.assertEqual(bb1.expand(v1), bb1)
        self.assertEqual(bb1.expand(-v2), p.BB(-100,-5,10,10))

        self.assertEqual(bb1.center(), (5,5))
        self.assertEqual(bb1.area(), 100)

        self.assertEqual(bb1.merged_area(bb2), 400)

        self.assertEqual(bb2.segment_query(v1, v2), p.inf)
        self.assertEqual(bb1.segment_query((-1,1), (99,1)), 0.01)


        self.assertEqual(bb1.clamp_vect(v2), Vec2d(10,5))

        self.assertEqual(bb1.wrap_vect((11,11)), (1,1))

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
        t = p.Transform()
        self.assertEqual(t.a, 0)
        self.assertEqual(t.b, 0)
        self.assertEqual(t.c, 0)
        self.assertEqual(t.d, 0)
        self.assertEqual(t.tx, 0)
        self.assertEqual(t.ty, 0)

        t = p.Transform(1,2,3,4,5,6)
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 2)
        self.assertEqual(t.c, 3)
        self.assertEqual(t.d, 4)
        self.assertEqual(t.tx, 5)
        self.assertEqual(t.ty, 6)
        self.assertEqual(str(t), "Transform(1.0,2.0,3.0,4.0,5.0,6.0)")

    def testIdentity(self):
        t = p.Transform.identity()
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 0)
        self.assertEqual(t.c, 0)
        self.assertEqual(t.d, 1)
        self.assertEqual(t.tx, 0)
        self.assertEqual(t.ty, 0)

class UnitTestBugs(unittest.TestCase):
    def testManyBoxCrash(self):
        space = p.Space()
        for x in [1,2]:
            for y in range(16):
                size = 10
                box_points = map(Vec2d, [(-size, -size), (-size, size), (size,size), (size, -size)])
                body = p.Body(10,20)
                shape = p.Poly(body, list(box_points))
                space.add(body, shape)
            space.step(1/50.0)


    def testNoStaticShape(self):
        space = p.Space()

        b1 = p.Body(1, p.inf)
        c1 = p.Circle(b1, 10)
        c1.name = "c1"
        c1.collision_type = 2

        b2 = p.Body(1, p.inf)
        c2 = p.Circle(b2, 10)
        c2.name = "c2"

        b3 = p.Body(1, p.inf)
        c3 = p.Circle(b3, 10)
        c3.name = "c3"

        b1.position = 0,0
        b2.position = 9,0
        b3.position = -9,0

        space.add(b1,c1,b2,c2,b3,c3)

        def remove_first(space, arbiter):
            first_shape = arbiter.shapes[0]
            #print "REMOVE FIRST", first_shape.name
            if c1 in space.shapes:
                space.remove(c1)
            #space.add_post_step_callback(space.remove, first_shape, first_shape.body)

        space.add_collision_handler(2, 0, separate = remove_first)

        space.step(1./60)
        b2.position = 22,0
        space.step(1./60)





####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()
