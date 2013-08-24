import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################

class UnitTestShape(unittest.TestCase):
    def setUp(self):
        p.reset_shapeid_counter()
    
    def testShape(self):
        s = p.Space()
        b = p.Body(10,10)
        b.position = 10,0
        c = p.Circle(b,5)
        c.cache_bb()
        self.assertFalse( c.point_query((0,0)) )
        self.assert_( c.point_query((11,1)) )
        
        info = c.segment_query((0,-50),(0,50))
        self.assertEqual(info, None)
        info = c.segment_query((10,-50),(10,50))
        self.assertEqual(info.get_hit_point().x, 10)
        self.assertEqual(info.get_hit_distance(), 45)
        self.assertAlmostEqual(info.n.y, -1.0)
        
    def testCircleBB(self):
        s = p.Space()
        b = p.Body(10,10)
        c = p.Circle(b,5)
        
        c.cache_bb()
        
        self.assertEqual(c.bb, p.BB(-5.0, -5.0, 5.0, 5.0))
        
    def testSegmentBB(self):
        s = p.Space()
        b = p.Body(10,10)
        c = p.Segment(b,(2,2),(2,3),2)
        
        c.cache_bb()
        
        self.assertEqual(c.bb, p.BB(0, 0, 4.0, 5.0))
        
    def testSegmentSegmentCollision(self):
        s = p.Space()
        b1 = p.Body(10,10)
        b2 = p.Body(10,10)
        c1 = p.Segment(b1, (-1,-1), (1,1), 1)
        c2 = p.Segment(b2, (1,-1), (-1,1), 1)

        s.add(b1,b2,c1,c2)

        self.num_of_begins = 0
        def begin(space, arb):
            self.num_of_begins += 1
            return True
        s.set_default_collision_handler(begin=begin)
        s.step(.1)

        self.assertEqual(1, self.num_of_begins)

    def testPolyBB(self):
        s = p.Space()
        b = p.Body(10,10)
        c = p.Poly(b,[(2,2),(4,3),(3,5)])
        
        c.cache_bb()
        
        self.assertEqual(c.bb, p.BB(2, 2, 4, 5))
        
    def testCircleNoBody(self):
        s = p.Space()
        c = p.Circle(None,5)
        
        c.update((10,10),(1,0))
        
        self.assertEqual(c.bb, p.BB(5, 5, 15, 15))
        
    def testPolyRadius(self):
        b = p.Body(1,1)
        
        c = p.Poly(b, [(2,2), (4,3), (3,5)], radius=10)
       
        self.assertEqual(c.radius, 10)

        c.unsafe_set_radius(20)

        self.assertEqual(c.radius, 20)

    def testPolyUnsafeSet(self):
        s = p.Space()
        b = p.Body(10,10)
        c = p.Poly(b,[(2,2), (4,3), (3,5)])
        
        c.cache_bb()
        
        c.unsafe_set_vertices([(0,0), (1,0), (1,1)])
        c.cache_bb()
        
        self.assertEqual(c.bb, p.BB(0, 0, 1, 1))
        
        
    def testCreateBox(self):
        s = p.Space()
        b = p.Body(1,1)
        
        c = p.Poly.create_box(b, (4,2), (10,10))
        
        ps = c.get_vertices()
        #print help(self.assertEqual)
        self.assertEqual(ps, [(8,9), (8,11),(12,11),(12,9)])
    
    def testGroup(self):
        s = p.Space()
        b1 = p.Body(1,1)
        b2 = p.Body(1,1)
        b3 = p.Body(1,1)
        
        c1 = p.Circle(b1,2)
        c2 = p.Circle(b2,2)
        c3 = p.Circle(b3,2)
        
        c1.group = 5
        c2.group = 5
        c3.group = 6
        
        s.add(b2,b3,c2,c3)
        
        self.assertEqual(s.shape_query(c1)[0], c3)
        
    def testLayer(self):
        s = p.Space()
        b1 = p.Body(1,1)
        b2 = p.Body(1,1)
        b3 = p.Body(1,1)
        b4 = p.Body(1,1)
        
        c1 = p.Circle(b1,2)
        c2 = p.Circle(b2,2)
        c3 = p.Circle(b3,2)
        c4 = p.Circle(b4,2)
        
        c1.layers = 2 #0b10
        c2.layers = 1 #0b01
        c3.layers = 3 #0b11
        
        s.add(b2,b3,b4,c2,c3,c4)
        shapes = s.shape_query(c1)
        self.assertEqual(len(shapes), 2)
        self.assert_(c3 in shapes)
        self.assert_(c4 in shapes)
        
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
        self.assert_(c in b1.shapes)
        self.assert_(c not in b2.shapes)
        c.body = b2
        self.assert_(c not in b1.shapes)
        self.assert_(c in b2.shapes)
    
####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()