from __future__ import with_statement
import sys
import unittest
import warnings

import pymunk as p
from pymunk import *
from pymunk.vec2d import Vec2d

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
        s = p.Space()
        
        self.assertEqual(s.iterations, 10)
        s.iterations = 15
        self.assertEqual(s.iterations, 15)
        
        self.assertEqual(s.gravity, (0,0))
        s.gravity = 10,2
        self.assertEqual(s.gravity, (10,2))
        self.assertEqual(s.gravity.x, 10)
        
        self.assertEqual(s.damping, 1)
        s.damping = 3
        self.assertEqual(s.damping, 3)
        
        self.assertEqual(s.idle_speed_threshold, 0)
        s.idle_speed_threshold = 4
        self.assertEqual(s.idle_speed_threshold, 4)
        
        self.assertEqual(str(s.sleep_time_threshold), 'inf')
        s.sleep_time_threshold = 5
        self.assertEqual(s.sleep_time_threshold, 5)
        
        self.assertAlmostEqual(s.collision_slop, 0.1)
        s.collision_slop = 6
        self.assertEqual(s.collision_slop, 6)
        
        self.assertAlmostEqual(s.collision_bias, 0.0017970074436)
        s.collision_bias = 0.2
        self.assertEqual(s.collision_bias, 0.2)
        
        self.assertEqual(s.collision_persistence, 3)
        s.collision_persistence = 9
        self.assertEqual(s.collision_persistence, 9)
        
        self.assertEqual(s.current_time_step, 0)
        s.step(0.1)
        self.assertEqual(s.current_time_step, 0.1)
        
        self.assertTrue(s.static_body != None)
        self.assertEqual(s.static_body.body_type, p.Body.STATIC)
    
    def testAddRemove(self):
        s = p.Space()
        
        self.assertEqual(s.bodies, [])
        self.assertEqual(s.shapes, [])
        
        b = p.Body(1,2)
        s.add(b)
        self.assertEqual(s.bodies, [b])
        self.assertEqual(s.shapes, [])
        
        c1 = p.Circle(b, 10)
        s.add(c1)
        self.assertEqual(s.bodies, [b])
        self.assertEqual(s.shapes, [c1])
        
        c2 = p.Circle(b, 15)
        s.add(c2)
        self.assertEqual(s.shapes, [c1,c2])
        
        s.remove(c1)
        self.assertEqual(s.shapes, [c2])
        
        s.remove(c2, b)
        self.assertEqual(s.bodies, [])
        self.assertEqual(s.shapes, [])
        
        s.add(c2, b)
        self.assertEqual(s.bodies, [b])
        self.assertEqual(s.shapes, [c2])
                        
    def testAddRemoveInStep(self):
        s = p.Space()
        
        b1 = p.Body(1, 2)
        c1 = p.Circle(b1, 2)
        
        b2 = p.Body(1, 2)
        c2 = p.Circle(b2, 2)
        
        s.add(b1, b2, c1, c2)
        
        b = p.Body(1, 2)
        c = p.Circle(b, 2)
        def pre_solve(space, arbiter):
            print "XXX"
            space.add(b, c)
            self.assertTrue(b in s.bodies)
            self.assertTrue(c in s.shapes)
            
            space.remove(b, c)
            self.assertTrue(b not in s.bodies)
            self.assertTrue(c not in s.shapes)
            
            space.add(b, c)
            return True
        
        s.add_collision_handler(0, 0, pre_solve = pre_solve)
        
        s.step(.1)
        
        self.assert_(b in s.bodies)
        self.assert_(c in s.shapes)
    
    def testRemoveInStep(self):
        s = self.s
        
        def pre_solve(space, arbiter):
            space.remove(arbiter.shapes)
            return True
        
        s.add_collision_handler(0, 0, pre_solve = pre_solve)
        
        s.step(.1)
        
        self.assert_(self.s1 not in s.bodies)
        self.assert_(self.s2 not in s.shapes)
                
    def testPointQuery(self):       
        s = p.Space()       
        b1 = p.Body(1, 1)
        b1.position = 19, 0
        s1 = p.Circle(b1, 10)
        s.add(s1)
        
        b2 = p.Body(1, 1)
        b2.position = 0, 0
        s2 = p.Circle(b2, 10)
        s.add(s2)
        
        hits = s.point_query((23,0), 0, p.ShapeFilter())
        
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].shape, s1)
        self.assertEqual(hits[0].point, (29,0))
        self.assertEqual(hits[0].distance, -6)
        self.assertEqual(hits[0].gradient, (1,0))
        
        hits = s.point_query((30,0), 0, p.ShapeFilter())
        self.assertEqual(len(hits), 0)
        
        hits = s.point_query((30,0), 30, p.ShapeFilter())
        self.assertEqual(len(hits), 2)
        self.assertEqual(hits[0].shape, s2)
        self.assertEqual(hits[0].point, (10,0))
        self.assertEqual(hits[0].distance, 20)
        self.assertEqual(hits[0].gradient, (1,0))
        
        self.assertEqual(hits[1].shape, s1)
        self.assertEqual(hits[1].point, (29,0))
        self.assertEqual(hits[1].distance, 1)
        self.assertEqual(hits[1].gradient, (1,0))
        
    def testPointQueryNearest(self):
        s = p.Space()       
        b1 = p.Body(1,1)
        b1.position = 19,0
        s1 = p.Circle(b1, 10)
        s.add(s1)
        
        hit = s.point_query_nearest((23,0), 0, p.ShapeFilter())
        self.assertEqual(hit.shape, s1)
        self.assertEqual(hit.point, (29,0))
        self.assertEqual(hit.distance, -6)
        self.assertEqual(hit.gradient, (1,0))
        
        hit = s.point_query_nearest((30,0), 0, p.ShapeFilter())
        self.assertEqual(hit.shape, None)
        
        hit = s.point_query_nearest((30,0), 10, p.ShapeFilter())
        self.assertEqual(hit.shape, s1)
        self.assertEqual(hit.point, (29,0))
        self.assertEqual(hit.distance, 1)
        self.assertEqual(hit.gradient, (1,0))
        
    def testBBQuery(self):
        s = p.Space()     
        
        b1 = p.Body(1,1)
        b1.position = 19,0
        s1 = p.Circle(b1, 10)
        s.add(s1)
        
        b2 = p.Body(1, 1)
        b2.position = 0, 0
        s2 = p.Circle(b2, 10)
        s.add(s2)
        
        bb = p.BB(-7, -7, 7, 7)
        
        hits = s.bb_query(bb, p.ShapeFilter()) 
        self.assertEqual(len(hits), 1)
        self.assert_(s2 in hits)
        self.assert_(s1 not in hits)
    
    def testShapeQuery(self):
        
        b = p.Body()
        s = p.Circle(b, 2)
        b.position = 20,1
        
        hits = self.s.shape_query(s)        
        self.assert_(self.s1 not in hits)
        self.assert_(self.s2 in hits)
        
        
    def testStaticPointQueries(self):
        b = p.Body()
        c = p.Circle(b, 10)
        b.position = -50,-50
        
        self.s.add(c)
        
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, c)
        hits = self.s.point_query( (-50,-55) )
        self.assertEqual(hits[0], c)
    
    def testReindexStatic(self):
        b = p.Body()
        c = p.Circle(b, 10)
        
        self.s.add(c)
        
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
        
        b2 = p.Body()
        s2 = p.Segment(b2, (-10,0), (10,0),1)
        
        self.s.add(b1,c1)
        self.s.add(s2)

        s2.unsafe_set_b((100,0))
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
        b = p.Body()
        c = p.Circle(b, 10)
        
        self.s.add(c)
        
        b.position = -50,-50
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, None)
        self.s.reindex_shape(c)
        hit = self.s.point_query_first( (-50,-55) )
        self.assertEqual(hit, c)
    
    def testSegmentQueries(self):
        
        self.assertEqual(self.s.segment_query_first( (13,11), (131.01,12) ), None)
        self.assertEqual(self.s.segment_query_first( (13,-11),(131.01,-11) ), None)
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
        b = p.Body()
        c = p.Circle(b, 10)
        b.position = -50,-50
        
        self.s.add(c)
        
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

    def testCollisionHandlerBeginNoReturn(self):
        if sys.version_info < (2, 6): return
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            def begin(space, arb, data):
                return
                
            self.b1.position = self.b2.position
            self.s.add_collision_handler(0,0, begin, None, None, None, None)
            self.s.step(0.1)
            self.s.step(0.1)
            
            self.assertEqual(len(w),1)
            self.assertTrue(issubclass(w[-1].category,UserWarning))
    
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
        
    def testCollisionHandlerPreSolveNoReturn(self):
        if sys.version_info < (2, 6): return
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
        
            def pre_solve(space, arb, test_self):
                return
            
            self.s.add_collision_handler(0,0, None, pre_solve, None, None, self)
            self.s.step(0.1)
            
            self.assertEqual(len(w),1)
            self.assertTrue(issubclass(w[-1].category,UserWarning))
            
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