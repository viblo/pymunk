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
        
        ps = c.get_points()
        print help(self.assertEqual)
        self.assertEqual(ps, [(8,9), (8,11),(12,11),(12,9)])
    
####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()