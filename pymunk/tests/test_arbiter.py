import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

class UnitTestArbiter(unittest.TestCase):    
    def testRestitution(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        b1.position = 0, 25
        c1.collision_type = 1
        c1.elasticity = 0.6
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.elasticity = 0.3
        
        s.add(b1, c1, b2, c2)
        
        def pre_solve(arb, space, data):
            self.assertEqual(arb.restitution, 0.18)
            arb.restitution = 1
            return True
        
        s.add_collision_handler(1,2).pre_solve = pre_solve
        
        for x in range(10):
            s.step(0.1)
            
        self.assertAlmostEqual(b1.position.y, 22.42170317)
        
    def testFriction(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, p.inf)
        c1 = p.Circle(b1, 10)
        b1.position = 10, 25
        c1.collision_type = 1
        c1.friction = 0.6
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.friction = 0.3
        
        s.add(b1, c1, b2, c2)
        
        def pre_solve(arb, space, data):
            self.assertEqual(arb.friction, 0.18)
            arb.friction = 1
            return True
        
        s.add_collision_handler(1,2).pre_solve = pre_solve
        
        for x in range(10):
            s.step(0.1)
            
        self.assertAlmostEqual(b1.position.x, 10.99450928394)
            
    def testSurfaceVelocity(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, p.inf)
        c1 = p.Circle(b1, 10)
        b1.position = 10, 25
        c1.collision_type = 1
        c1.surface_velocity = (3,0)
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.surface_velocity = (5,0)
        
        s.add(b1, c1, b2, c2)
        
        def pre_solve(arb, space, data):
            self.assertAlmostEqual(arb.surface_velocity.x, 1.38461538462)
            self.assertAlmostEqual(arb.surface_velocity.y, -0.923076923077)
            
            arb.surface_velocity = (10,10)
            #TODO: add assert check that setting surface_velocity has any effect
            return True
        
        s.add_collision_handler(1,2).pre_solve = pre_solve
        
        for x in range(5):
            s.step(0.1)    
        
    def testContactPointSet(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 30)
        c1 = p.Circle(b1, 10)
        b1.position = 5, 3
        c1.collision_type = 1
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        
        s.add(b1, c1, b2, c2)
        
        def pre_solve(arb, space, data):
            # check inital values
            ps = arb.contact_point_set
            self.assertEqual(len(ps.points), 1)
            self.assertAlmostEqual(ps.normal.x, 0.8574929257)
            self.assertAlmostEqual(ps.normal.y, 0.5144957554)
            p1 = ps.points[0]
            self.assertAlmostEqual(p1.point_a.x, 8.574929257)
            self.assertAlmostEqual(p1.point_a.y, 5.144957554)
            self.assertAlmostEqual(p1.point_b.x, -3.574929257)
            self.assertAlmostEqual(p1.point_b.y, -2.144957554)
            self.assertAlmostEqual(p1.distance, -14.16904810)
            
            # check that they can be changed
            ps.normal = Vec2d(1,0)
            ps.points[0].point_a = Vec2d(9,10)
            ps.points[0].point_b = Vec2d(-2,-3)
            ps.points[0].distance = -10
            
            arb.contact_point_set = ps
            ps2 = arb.contact_point_set
            
            self.assertEqual(ps2.normal, (1,0))
            p1 = ps2.points[0]
            self.assertAlmostEqual(p1.point_a, (9,10))
            self.assertAlmostEqual(p1.point_b, (-2,-3))
            self.assertAlmostEqual(p1.distance, -11)
            
            # check for length of points
            ps2.points = []
            def f():
                arb.contact_point_set = ps2    
            self.assertRaises(Exception, f)
            
            return True
            
        s.add_default_collision_handler().pre_solve = pre_solve
        
        s.step(0.1)
        
    def testImpulse(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 30)
        c1 = p.Circle(b1, 10)
        b1.position = 5, 3
        c1.collision_type = 1
        c1.friction = 0.5
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.friction = 0.8
        
        s.add(b1, c1, b2, c2)
        
        self.post_solve_done = False
        
        def post_solve(arb, space, data):
            self.assertAlmostEqual(arb.total_impulse.x, 3.3936651583)
            self.assertAlmostEqual(arb.total_impulse.y, 4.3438914027)
            self.post_solve_done = True
            
        s.add_collision_handler(1,2).post_solve = post_solve
        
        s.step(0.1)
            
        self.assertTrue(self.post_solve_done)
    
    def testTotalKE(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 30)
        c1 = p.Circle(b1, 10)
        b1.position = 5, 3
        c1.collision_type = 1
        c1.friction = 0.5
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.friction = 0.8
        
        s.add(b1, c1, b2, c2)
        
        def post_solve(arb, space, data):
            self.assertAlmostEqual(arb.total_ke, 43.438914027)
            return True
        
        s.add_collision_handler(1,2).post_solve = post_solve
        
        s.step(0.1)
        
    def testIsFirstContact(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 30)
        c1 = p.Circle(b1, 10)
        b1.position = 5, 3
        c1.collision_type = 1
        c1.friction = 0.5
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.friction = 0.8
        
        s.add(b1, c1, b2, c2)
        
        def pre_solve1(arb, space, data):
            self.assertTrue(arb.is_first_contact)
            return True
        
        s.add_collision_handler(1,2).pre_solve = pre_solve1
        
        s.step(0.1)
        
        def pre_solve2(arb, space, data):
            self.assertFalse(arb.is_first_contact)
            return True
        
        s.add_collision_handler(1,2).pre_solve = pre_solve2
        
        s.step(0.1)

    def testNormal(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 30)
        b1.position = 5, 10
        c1 = p.Circle(b1, 10)
        c2 = p.Circle(s.static_body, 10)
        
        s.add(b1, c1, c2)
        
        def pre_solve1(arb, space, data):
            self.assertAlmostEqual(arb.normal.x, 0.44721359)
            self.assertAlmostEqual(arb.normal.y, 0.89442719)
            return True
        
        s.add_default_collision_handler().pre_solve = pre_solve1
        
        s.step(0.1)
        
    def testIsRemoval(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 30)
        c1 = p.Circle(b1, 10)
        b1.position = 5, 3
        c1.collision_type = 1
        c1.friction = 0.5
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.friction = 0.8
        
        s.add(b1, c1, b2, c2)
        
        self.called1 = False
        def separate1(arb, space, data):
            self.called1 = True
            self.assertFalse(arb.is_removal)
        
        s.add_collision_handler(1,2).separate = separate1
        
        for x in range(10):
            s.step(0.1)
        self.assertTrue(self.called1)
        
        b1.position = 5,3
        s.step(0.1) 
        
        self.called2 = False
        def separate2(arb, space, data):
            self.called2 = True
            self.assertTrue(arb.is_removal)
            return True
       
        s.add_collision_handler(1,2).separate = separate2
        s.remove(b1, c1)
        
        self.assertTrue(self.called2)
        
    def testShapes(self):
        s = p.Space()
        s.gravity = 0,-100
        
        b1 = p.Body(1, 30)
        c1 = p.Circle(b1, 10)
        b1.position = 5, 3
        c1.collision_type = 1
        c1.friction = 0.5
        
        b2 = p.Body(body_type = p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        c2.friction = 0.8
        
        s.add(b1, c1, b2, c2)
        
        self.called = False
        def pre_solve(arb, space, data):
            self.called = True
            self.assertEqual(len(arb.shapes), 2)
            self.assertEqual(arb.shapes[0], c1)
            self.assertEqual(arb.shapes[1], c2)
            return True
        
        s.add_collision_handler(1,2).pre_solve = pre_solve
        
        s.step(0.1)
        self.assertTrue(self.called)
        
            
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()        