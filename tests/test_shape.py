import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################

class UnitTestShape(unittest.TestCase):
    def testPointQuery(self):
        b = p.Body(10,10)
        c = p.Circle(b, 5)
        c.cache_bb()
        
        distance, info = c.point_query((0,0))
        
        self.assertEqual(distance, -5)
        self.assertEqual(info.shape, c)
        
        self.assertEqual(str(info.point), "Vec2d(nan, nan)")
        self.assertEqual(info.distance, -5)
        self.assertEqual(info.gradient, (0,1))

        distance, info = c.point_query((11,0))
        
        self.assertEqual(distance, 6)
        self.assertEqual(info.shape, c)
        self.assertEqual(info.point, (5,0))
        self.assertEqual(info.distance, 6)
        self.assertEqual(info.gradient, (1,0))

    def testSegmentQuery(self):
        s = p.Space()
        b = p.Body(10,10)
        c = p.Circle(b, 5)
        c.cache_bb()

        info = c.segment_query((10,-50), (10,50))
        self.assertEqual(info.shape, None)
        self.assertEqual(info.point, (10,50))
        self.assertEqual(info.normal, (0,0))
        self.assertEqual(info.alpha, 1.0)

        info = c.segment_query((10,-50), (10,50), 6)
        self.assertEqual(info.shape, c)

        info = c.segment_query((0,-50), (0,50))
        self.assertEqual(info.shape, c)
        self.assertAlmostEqual(info.point.x, 0)
        self.assertAlmostEqual(info.point.y, -5)
        self.assertAlmostEqual(info.normal.x, 0)
        self.assertAlmostEqual(info.normal.y, -1)
        self.assertEqual(info.alpha, 0.45)

    def testNoBody(self):
        c = p.Circle(None, 1)
        self.assertEqual(c.body, None)

    def testRemoveBody(self):
        b = p.Body(1,1)
        c = p.Circle(b,1)
        c.body = None

        self.assertEqual(c.body, None)
        self.assertEqual(len(b.shapes), 0)

    def testSwitchBody(self):
        b1 = p.Body(1,1)
        b2 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertEqual(c.body, b1)
        self.assertTrue(c in b1.shapes)
        self.assertTrue(c not in b2.shapes)
        c.body = b2
        self.assertEqual(c.body, b2)
        self.assertTrue(c not in b1.shapes)
        self.assertTrue(c in b2.shapes)

    def testSensor(self):
        b1 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertFalse(c.sensor)
        c.sensor = True
        self.assertTrue(c.sensor)

    def testElasticity(self):
        b1 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertEqual(c.elasticity, 0)
        c.elasticity = 1
        self.assertEqual(c.elasticity, 1)

    def testFriction(self):
        b1 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertEqual(c.friction, 0)
        c.friction = 1
        self.assertEqual(c.friction, 1)

    def testSurfaceVelocity(self):
        b1 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertEqual(c.surface_velocity, (0,0))
        c.surface_velocity = (1,2)
        self.assertEqual(c.surface_velocity, (1,2))

    def testCollisionType(self):
        b1 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertEqual(c.collision_type, 0)
        c.collision_type = 1
        self.assertEqual(c.collision_type, 1)

    def testFilter(self):
        b1 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertEqual(c.filter, p.ShapeFilter(0, 0xffffffff, 0xffffffff))
        c.filter = p.ShapeFilter(1, 0xfffffff2, 0xfffffff3)
        self.assertEqual(c.filter, p.ShapeFilter(1, 0xfffffff2, 0xfffffff3))

    def testSpace(self):
        b1 = p.Body(1,1)
        c = p.Circle(b1,1)
        self.assertEqual(c.space, None)
        s = p.Space()
        s.add(c)
        self.assertEqual(c.space, s)
        
    def testShapesCollide(self):
        b1 = p.Body(1,1)
        s1 = p.Circle(b1, 10)
        
        b2 = p.Body(1,1)
        b2.position = 30,30
        s2 = p.Circle(b2, 10)
        
        c = s1.shapes_collide(s2)
        self.assertEqual(c.normal, (1, 0))
        self.assertEqual(len(c.points), 1)
        point = c.points[0]
        self.assertEqual(point.point_a, (10,0))
        self.assertEqual(point.point_b, (-10,0))
        self.assertEqual(point.distance, -20) 


class UnitTestCircle(unittest.TestCase):
    def testCircleBB(self):
        s = p.Space()
        b = p.Body(10,10)
        c = p.Circle(b,5)

        c.cache_bb()

        self.assertEqual(c.bb, p.BB(-5.0, -5.0, 5.0, 5.0))

    def testCircleNoBody(self):
        s = p.Space()
        c = p.Circle(None,5)

        bb = c.update(p.Transform(1, 2, 3, 4, 5, 6))
        self.assertEqual(c.bb, bb)
        self.assertEqual(c.bb, p.BB(0, 1, 10, 11))

    def testOffset(self):
        c = p.Circle(None, 5, (1,2))

        self.assertEqual(c.offset, (1,2))

    def testOffsetUnsafe(self):
        c = p.Circle(None, 5, (1,2))

        c.unsafe_set_offset((3,4))

        self.assertEqual(c.offset, (3,4))

    def testRadius(self):
        c = p.Circle(None, 5)

        self.assertEqual(c.radius, 5)

    def testRadiusUnsafe(self):
        c = p.Circle(None, 5)
        
        c.unsafe_set_radius(3)
        
        self.assertEqual(c.radius, 3)

class UnitTestSegment(unittest.TestCase):
    def testBB(self):
        s = p.Space()
        b = p.Body(10,10)
        c = p.Segment(b,(2,2),(2,3),2)

        c.cache_bb()

        self.assertEqual(c.bb, p.BB(0, 0, 4.0, 5.0))

    def testProperties(self):
        c = p.Segment(None, (2,2), (2,3), 4)

        self.assertEqual(c.a, (2,2))
        self.assertEqual(c.b, (2,3))
        self.assertEqual(c.normal, (1,0))
        self.assertEqual(c.radius, 4)

    def testPropertiesUnsafe(self):
        c = p.Segment(None, (2,2), (2,3), 4)
        
        c.unsafe_set_endpoints((3,4), (5,6))
        self.assertEqual(c.a, (3,4))
        self.assertEqual(c.b, (5,6))
        
        c.unsafe_set_radius(5)
        self.assertEqual(c.radius, 5)

    def testSetNeighbors(self):
        c = p.Segment(None, (2,2), (2,3), 1)
        c.set_neighbors((2,2),(2,3))

    def testSegmentSegmentCollision(self):
        s = p.Space()
        b1 = p.Body(10,10)
        c1 = p.Segment(b1, (-1,-1), (1,1), 1)
        b2 = p.Body(10,10)
        c2 = p.Segment(b2, (1,-1), (-1,1), 1)

        s.add(b1,b2,c1,c2)

        self.num_of_begins = 0
        def begin(arb, space, data):
            self.num_of_begins += 1
            return True
            
        s.add_default_collision_handler().begin=begin
        s.step(.1)

        self.assertEqual(1, self.num_of_begins)

class UnitTestPoly(unittest.TestCase):
    def testInit(self):
        c = p.Poly(None, [(0,0),(10,10),(20,0),(-10,10)], None, 0)

        b = p.Body(1,2)
        c = p.Poly(b, [(0,0),(10,10),(20,0),(-10,10)], p.Transform.identity(), 6)

    def testVertices(self):
        vs = [(-10,10), (0,0),(20,0),(10,10)]
        c = p.Poly(None, vs, None, 0)

        self.assertEqual(c.get_vertices(), vs)
        
        c = p.Poly(None, vs, p.Transform(1,2,3,4,5,6), 0)
        
        vs2 = [(5.0, 6.0), (25.0, 26.0), (45.0, 66.0), (25.0, 46.0)]
        self.assertEqual(c.get_vertices(), vs2)

    def testVerticesUnsafe(self):
        vs = [(-10,10), (0,0),(20,0),(10,10)]
        c = p.Poly(None, vs, None, 0)

        vs2 = [(-3,3), (0,0), (3,0)]
        c.unsafe_set_vertices(vs2)
        self.assertEqual(c.get_vertices(), vs2)
        
        vs3 = [(-4,4), (0,0), (4,0)]
        c.unsafe_set_vertices(vs3, p.Transform.identity())
        self.assertEqual(c.get_vertices(), vs3)
        
    def testBB(self):
        c = p.Poly(None, [(2,2),(4,3),(3,5)])
        bb = c.update(p.Transform.identity())
        self.assertEqual(bb, c.bb)
        self.assertEqual(c.bb, p.BB(2, 2, 4, 5))

        b = p.Body(1,2)
        c = p.Poly(b, [(2,2),(4,3),(3,5)])
        c.cache_bb()
        self.assertEqual(c.bb, p.BB(2, 2, 4, 5))

        s = p.Space()
        b = p.Body(1,2)
        c = p.Poly(b, [(2,2),(4,3),(3,5)])
        s.add(b,c)
        self.assertEqual(c.bb, p.BB(2, 2, 4, 5))

    def testRadius(self):
        c = p.Poly(None, [(2,2), (4,3), (3,5)], radius=10)
        self.assertEqual(c.radius, 10)
        
    def testRadiusUnsafe(self):
        c = p.Poly(None, [(2,2), (4,3), (3,5)], radius=10)

        c.unsafe_set_radius(20)

        self.assertEqual(c.radius, 20)        

    def testCreateBox(self):
        c = p.Poly.create_box(None, (4,2), 3)
        self.assertEqual(c.get_vertices(), [(2,-1), (2,1), (-2,1), (-2,-1)])

        c = p.Poly.create_box_bb(None, p.BB(1,2,3,4), 3)
        self.assertEqual(c.get_vertices(), [(3,2), (3,4), (1,4), (1,2)])


####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()
