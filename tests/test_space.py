import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################
 
class UnitTestSpace(unittest.TestCase):
    def setUp(self):
        p.reset_shapeid_counter()
    
        self.s = p.Space()
        
        self.b1, self.b2 = p.Body(1,3),p.Body(10,100)
        self.s.add(self.b1,self.b2)
        self.b1.position = 10,0
        self.b2.position = 20,0
        
        self.s1,self.s2 = p.Circle(self.b1,5), p.Circle(self.b2,10)
        self.s.add(self.s1,self.s2)
    
    def tearDown(self):
        del self.s
        del self.b1, self.b2
        del self.s1, self.s2
    
    
    def testProperties(self):
        s = p.Space(15)
        self.assertEqual(s.iterations, 15)
        s.gravity = 10,2
        self.assertEqual(s.gravity.x, 10)
        s.damping = 3
        self.assertEqual(s.damping, 3)
        
        s.idle_speed_threshold = 4
        self.assertEqual(s.idle_speed_threshold, 4)
        s.sleep_time_threshold = 5
        self.assertEqual(s.sleep_time_threshold, 5)
        s.collision_slop = 6
        self.assertEqual(s.collision_slop, 6)
        
        
        s.collision_bias = 8
        self.assertEqual(s.collision_bias, 8)
        s.collision_persistence = 9
        self.assertEqual(s.collision_persistence, 9)
        
        s.enable_contact_graph = True
        self.assertEqual(s.enable_contact_graph, True)
    
    def testAddRemove(self):
        
        self.s.remove(self.b1)
        self.s.add(self.b1)
        b = p.Body()
        s3 = p.Circle(b,2)
        self.s.add_static(s3)
        b3 = p.Body(1,1)
        self.s.add(b3)
        
        self.assertEqual(len(self.s.bodies), 3)
        self.assertEqual(len(self.s.shapes), 2)
        self.assertEqual(len(self.s.static_shapes), 1)
        
        self.s.remove(self.s2,self.b1,self.s1)
        self.s.remove_static(s3)
        self.assertEqual(len(self.s.bodies), 2)
        self.assertEqual(len(self.s.shapes), 0)
        self.assertEqual(len(self.s.static_shapes), 0)
        
    def testPointQueries(self):
        
        self.assertEqual(self.s.point_query_first((31,0)), None)
        self.assertEqual(self.s.point_query_first((10,0)), self.s1)
        
        b3 = p.Body(1,1)
        b3.position = 19,1
        s3 = p.Circle(b3, 10)
        self.s.add(s3)
        hits = self.s.point_query((23,0))
        self.assert_(self.s1 not in hits)
        self.assert_(self.s2 in hits)
        self.assert_(s3 in hits)
        
    def testBBQuery(self):
        bb = p.BB(-7,-7,7,7)
        
        hits = self.s.bb_query(bb)        
        self.assert_(self.s1 in hits)
        self.assert_(self.s2 not in hits)
    
    def testShapeQuery(self):
        
        b = p.Body()
        s = p.Circle(b, 2)
        b.position = 20,1
        
        hits = self.s.shape_query(s)        
        self.assert_(self.s1 not in hits)
        self.assert_(self.s2 in hits)
        
        
    def testStaticPointQueries(self):
        b = p.Body(p.inf, p.inf)
        c = p.Circle(b, 10)
        b.position = -50,-50
        
        self.s.add_static(c)
        
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, c)
        hits = self.s.point_query( (-50,-55) )
        self.assertEqual(hits[0], c)
    
    def testReindexStatic(self):
        b = p.Body(p.inf, p.inf)
        c = p.Circle(b, 10)
        
        self.s.add_static(c)
        
        b.position = -50,-50
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, None)
        self.s.reindex_static()
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, c)
        b.position = 50,50
        self.s.reindex_shape(c)
        hit = self.s.point_query_first( (50,50) )
        self.assertEqual(hit, c)
    
    def testReindexStaticCollision(self):
        b1 = p.Body(10, p.inf)
        c1 = p.Circle(b1, 10)
        b1.position = 20, 20
        
        b2 = p.Body(p.inf, p.inf)
        s2 = p.Segment(b2, (-10,0), (10,0),1)
        
        self.s.add(b1,c1)
        self.s.add_static(s2)

        s2.b = (100,0)
        self.s.gravity = 0, -100
        
        for x in range(10):
            self.s.step(.1)
        
        self.assert_(b1.position.y < 0)
        
        b1.position = 20,20
        b1.velocity = 0,0
        self.s.reindex_static()
        
        for x in range(10):
            self.s.step(.1)
        
        self.assert_(b1.position.y > 10)
    
    def testReindexShape(self):
        b = p.Body(p.inf, p.inf)
        c = p.Circle(b, 10)
        
        self.s.add_static(c)
        
        b.position = -50,-50
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, None)
        self.s.reindex_shape(c)
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, c)
    
    def testSegmentQueries(self):
        
        self.assertEqual(self.s.segment_query_first( (13,1), (131.01,2) ), None)
        self.assertEqual(self.s.segment_query_first( (13,0),(131.01,0) ), None)
        r = self.s.segment_query_first( (10,-100), (10,100) )
        
        self.assertEqual(r.shape, self.s1)
        self.assertEqual(r.t, 0.475)
        self.assertEqual(r.n, Vec2d(0,-1))
        
        b3 = p.Body(1,1)
        b3.position = 19,1
        s3 = p.Circle(b3, 10)
        self.s.add(s3)
        hits = self.s.segment_query((16,-100), (16,100))
        
        hit_shapes = [hit.shape for hit in hits]
        self.assert_(self.s1 not in hit_shapes)
        self.assert_(self.s2 in hit_shapes)
        self.assert_(s3 in hit_shapes)

    def testStaticSegmentQueries(self):
        b = p.Body(p.inf, p.inf)
        c = p.Circle(b, 10)
        b.position = -50,-50
        
        self.s.add_static(c)
        
        hit = self.s.segment_query_first( (-70,-50), (-30, -50) )
        self.assertEqual(hit.shape, c)
        hits = self.s.segment_query( (-70,-50), (-30, -50) )
        self.assertEqual(hits[0].shape, c)
    
    def testCollisionHandlerBegin(self):
        self.num_of_begins = 0
        def begin(space, arb, data):
            self.num_of_begins += 1
            return True
            
        self.b1.position = self.b2.position
        self.s.add_collision_handler(0,0, begin, None, None, None, None)
        self.s.step(0.1)
        self.s.step(0.1)
        self.assertEqual(self.num_of_begins, 1)
        
    def testCollisionHandlerPreSolve(self):
    
        self.begin_shapes = None
        self.begin_contacts = None
        self.begin_space = None
        
        self.s1.collision_type = 1
        self.s2.collision_type = 2
        
        def pre_solve(space, arb, test_self):
            test_self.begin_shapes = arb.shapes
            test_self.begin_contacts = arb.contacts
            test_self.begin_space = space
            return True
            
        for x in range(100): 
            self.s.step(0.1)
        
        self.s.add_collision_handler(1,2, None, pre_solve, None, None, self)
        self.s.step(0.1)
        self.assertEqual(self.s1, self.begin_shapes[0])
        self.assertEqual(self.s2, self.begin_shapes[1])
        self.assertEqual(self.begin_space, self.s)
        
    def testCollisionHandlerPostSolve(self):  
        self.first_contact = None
        def post_solve(space, arb, test_self):
            self.first_contact = arb.is_first_contact
            return True
            
        self.s.add_collision_handler(0,0, None, None, post_solve, None, self)
        self.s.step(0.1)
        self.assert_(self.first_contact)
        self.s.step(0.1)
        self.assertFalse(self.first_contact)
        
    def testPostStepCallback(self):
        self.number_of_calls = 0
        def f(obj, shapes, test_self):
            for shape in shapes:
                self.s.remove(shape)
            test_self.number_of_calls += 1
        def pre_solve(space, arb):
            space.add_post_step_callback(f, arb.shapes[0], arb.shapes, test_self = self)
            return True
            
        self.s.add_collision_handler(0, 0, None, pre_solve, None, None)
        self.s.step(0.1)
        self.assertEqual(self.s.shapes, [])
        self.s.add(self.s1, self.s2)
        self.s.step(0.1)
        self.assertEqual(self.s.shapes, [])
        self.s.add(self.s1, self.s2)
        self.s.add_collision_handler(0, 0, None, None, None, None)
        self.s.step(0.1)
        self.assertEqual(self.number_of_calls, 2)

####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()