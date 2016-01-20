import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

class UnitTestArbiter(unittest.TestCase):
    def setUp(self):
        pass
        
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
        
        def pre_solve(space, arb):
            self.assertEqual(arb.restitution, 0.18)
            arb.restitution = 1
            return True
        
        s.collision_handler(1,2).pre_solve = pre_solve
        
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
        
        def pre_solve(space, arb):
            self.assertEqual(arb.friction, 0.18)
            arb.friction = 1
            return True
        
        s.collision_handler(1,2).pre_solve = pre_solve
        
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
        
        def pre_solve(space, arb):
            self.assertAlmostEqual(arb.surface_velocity.x, 1.38461538462)
            self.assertAlmostEqual(arb.surface_velocity.y, -0.923076923077)
            
            arb.surface_velocity = (10,10)
            #TODO: add assert check that setting surface_velocity has any effect
            return True
        
        s.collision_handler(1,2).pre_solve = pre_solve
        
        for x in range(5):
            s.step(0.1)
        
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
    
    def testTotalKE(self):
        self.b1.apply_impulse((10,0))
        def post_solve(space, arb, test_self):
            self.assertAlmostEqual(arb.total_ke, 92.375)
            return True
        
        self.s.add_collision_handler(1,2, None, None, post_solve, None, self)
        for x in range(7):
            self.s.step(0.1)
            
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()        