
import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################

class UnitTestGeneral(unittest.TestCase):
    
    def testGeneral(self):
        p.version
        p.inf
        p.chipmunk_version
        
        m = p.moment_for_box(1, 2, 3)
        self.assertAlmostEqual(m, 1.08333333333)
        
        m = p.moment_for_segment(1, Vec2d(-1,0), Vec2d(1,0))
        self.assertAlmostEqual(m, 0.33333333333)
        
class UnitTestBody(unittest.TestCase):
    def setUp(self):
        p.reset_shapeid_counter()
        
    def test(self):
        b = p.Body(10,100)
        self.assertEqual(b.mass, 10)
        self.assertEqual(b.moment, 100)
        b.reset_forces()
        b.apply_force((10,10))
        
    def testSleep(self):
        b = p.Body(1,1)
        s = p.Space()
        s.add(b)
        
        self.assertFalse(b.is_sleeping)
        
        b.sleep()
        self.assert_(b.is_sleeping)
        
        b.activate()
        self.assertFalse(b.is_sleeping)
        
    def testSleepWithGroup(self):
        b1 = p.Body(1,1)
        b2 = p.Body(2,2)
        s = p.Space()
        s.add(b1,b2)
        b2.sleep()
        b1.sleep_with_group(b2)
        self.assert_(b1.is_sleeping)
        b2.activate()
        self.assertFalse(b1.is_sleeping)
        
        
    def testKineticEnergy(self):
        b = p.Body(1,10)
        self.assertEqual(b.kinetic_energy, 0)
        b.apply_impulse((10,0))
        self.assertEqual(b.kinetic_energy, 100)
        
    def testIsRogue(self):
        b = p.Body(1,1)
        self.assert_(b.is_rogue)
        s = p.Space()
        s.add(b)
        self.assertFalse(b.is_rogue)
        
    def testStatic(self):
        bd = p.Body(1,1)
        bs = p.Body()
        self.assertFalse(bd.is_static)
        self.assert_(bs.is_static)
        
    def testConversion(self):
        b = p.Body(1,1)
        b.position = 10,20
        self.assertEqual(b.local_to_world((1,1)), Vec2d(11,21))
        self.assertEqual(b.world_to_local((1,1)), Vec2d(-9,-19))
        
    def testPositonFunction(self):
        s = p.Space()
        b = p.Body(1,1)
        def f(body, dt):
            body.position += 0,dt
        
        b.position_func=f
        s.add(b)
        s.step(10)
        self.assertEqual(b.position.y, 10)
        s.step(1)
        s.step(1)
        self.assertEqual(b.position.y, 12)
        
        b.position_func = p.Body.update_position
        s.step(1)
        self.assertEqual(b.position.y, 12)
        
    def testVelocityFunction(self):
        s = p.Space()
        b = p.Body(1,1)
        def f(body, gravity, damping, dt):
            body.velocity += 5*gravity
        
        b.velocity_func=f
        s.gravity = 1,0
        s.add(b)
        s.step(10)
        return
        self.assertEqual(b.velocity.x, 5)
        s.step(0.1)
        s.step(0.1)
        self.assertEqual(b.velocity.x, 15)
        
        b.velocity_func = b.update_velocity
        s.step(1)
        self.assertEqual(b.velocity.x, 16)
        
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
        
class UnitTestConstraint(unittest.TestCase):
    def setUp(self):
        p.reset_shapeid_counter()
    
    def testProperties(self):
        a,b = p.Body(p.inf, p.inf), p.Body(10,10)
        j = p.PinJoint(a,b)
        
        self.assertEqual(j.a, a)
        self.assertEqual(j.b, b)
        
        j.max_force = 10
        j.error_bias = 20
        j.max_bias = 30
        self.assertEqual(j.max_force, 10)
        self.assertEqual(j.error_bias, 20)
        self.assertEqual(j.max_bias, 30)
    
    def testActivate(self):
        a,b = p.Body(p.inf, p.inf), p.Body(10,10)
        j = p.PinJoint(a,b)
        s = p.Space()
        s.add(a,b)
        a.sleep()
        b.sleep()
        
        j.activate_bodies()
        self.assertFalse(a.is_sleeping)
        self.assertFalse(b.is_sleeping)
        
    def testImpulse(self):
        a,b = p.Body(p.inf, p.inf), p.Body(10,10)
        b.position = 0,10
        j = p.PinJoint(a,b)
        
        s = p.Space()
        s.gravity = 0,10
        s.add(b,j)
        self.assertEqual(j.impulse, 0)
        s.step(1)
        self.assertEqual(j.impulse, 100)
        
    def testPinJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PinJoint(a,b,(0,0), (10,0))
        self.assertEqual(j.distance, 10)
        
    def testSlideJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a,b,(1,0), (10,0), 7, 12)
        self.assertEqual(j.max, 12)
        self.assertEqual(j.anchr1, (1,0))
        
    def testPivotjoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        a.position = (-10,0)
        b.position = (10,0)
        s = p.Space()
        j1 = p.PivotJoint(a, b, (0,0))
        j2 = p.PivotJoint(a, b, (-10,0), (10,0))
        s.add(a,b,j1,j2)
        s.step(1)
        self.assertEqual(j1.anchr1, j2.anchr2)
        self.assertEqual(j2.anchr1, j1.anchr2)
        
    def testDampedSpring(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedSpring(a,b,(1,0), (10,0), 7, 12,5)
        self.assertEqual(j.rest_length, 7)
        self.assertEqual(j.stiffness, 12)
        self.assertEqual(j.damping, 5)
    
    def testDampedRotarySpring(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a,b, 0.4, 12,5)
        self.assertEqual(j.rest_angle, 0.4)
        self.assertEqual(j.stiffness, 12)
        self.assertEqual(j.damping, 5)
        
    def testDampedRotarySpringCallback(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a,b, 0.4, 12,5)
        def f(self, relative_angle):
            return 1
        j.torque_func = f
        s = p.Space()
        s.add(a,b,j)
        a.apply_impulse((10,0), (0,10))
        a.apply_impulse((-10,0), (0,-10))
        for x in range(100):
            s.step(0.1)
        self.assertAlmostEqual(a.angle-b.angle,-29.3233997)
        
    def testRotaryLimitJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RotaryLimitJoint(a, b, 0.1, 0.2)
        self.assertEqual(j.max, 0.2)
        self.assertEqual(j.min, 0.1)
        
    def testRatchetJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RatchetJoint(a, b, 0.3, 0.2)
        self.assertEqual(j.angle, 0.0)
        self.assertEqual(j.phase, 0.3)
        self.assertEqual(j.ratchet, 0.2)
        
    def testGearJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GearJoint(a, b, 0.3, 0.2)
        self.assertEqual(j.phase, 0.3)
        self.assertEqual(j.ratio, 0.2)
        
    def testSimpleMotor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SimpleMotor(a, b, 0.3)
        self.assertEqual(j.rate, 0.3)
        j.rate = 0.4
        self.assertEqual(j.rate, 0.4)
        j.max_bias = 30
        j.bias_coef = 40
        j.max_force = 50
        self.assertEqual(j.max_bias, 30)
        self.assertEqual(j.bias_coef, 40)
        self.assertEqual(j.max_force, 50)
        
class UnitTestArbiter(unittest.TestCase):
    def setUp(self):
        p.reset_shapeid_counter()
        self.s = p.Space()
        
        self.b1, self.b2 = p.Body(1,10),p.Body(p.inf,p.inf)
        self.s.add(self.b1)
        self.b1.position = -10,1
        self.b2.position = 0,0
        
        self.s1, self.s2 = p.Circle(self.b1,2), p.Circle(self.b2,2)
        self.s.add(self.s1, self.s2)
        
        self.s1.collision_type = 1
        self.s2.collision_type = 2  

        self.s1.elasticity = 0.5
        self.s2.elasticity = 0.5
        self.s1.friction = 0.8
        self.s2.friction = 0.7

    def testImpulse(self):
        self.post_solve_done = False
        self.b1.apply_impulse((10,0))
        def post_solve(space, arb, test_self):
            self.assertAlmostEqual(arb.total_impulse.x, -11.25)
            self.assertAlmostEqual(arb.total_impulse.y, 3.75)
            self.assertAlmostEqual(arb.total_impulse_with_friction.x, -12.05)
            self.assertAlmostEqual(arb.total_impulse_with_friction.y, 1.35)
            self.post_solve_done = True
            return True
        
        self.s.add_collision_handler(1,2, None, None, post_solve, None, self)
        
        for x in range(7):
            self.s.step(0.1)
        self.assert_(self.post_solve_done)
        
        
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
            
    def testMethods(self):
        bb1 = p.BB(0,0,10,10)
        bb2 = p.BB(10,10,20,20)
        bb3 = p.BB(4,4,5,5)
        v1 = Vec2d(1,1)
        v2 = Vec2d(100,5)
        self.assert_(bb1.intersects(bb2))

        self.assertFalse(bb1.contains(bb2))
        self.assert_(bb1.contains(bb3))
        
        self.assert_(bb1.contains_vect(v1))
        self.assertFalse(bb1.contains_vect(v2))
        
        self.assertEqual(bb1.merge(bb2), p.BB(0,0,20,20))
        
        self.assertEqual(bb1.expand(v1), bb1)
        self.assertEqual(bb1.expand(-v2), p.BB(-100,-5,10,10))
        
        self.assertEqual(bb1.clamp_vect(v2), Vec2d(10,5))
        
        self.assertEqual(bb1.wrap_vect((11,11)), (1,1))

class UnitTestBugs(unittest.TestCase):
    def testManyBoxCrash(self):
        space = p.Space()
        for x in [1,2]:
            for y in range(16):
                size = 10
                box_points = map(Vec2d, [(-size, -size), (-size, size), (size,size), (size, -size)])
                body = p.Body(10,20)
                shape = p.Poly(body, list(box_points), Vec2d(0,0))
                space.add(body, shape)
            space.step(1/50.0)
####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()