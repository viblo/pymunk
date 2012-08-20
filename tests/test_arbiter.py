import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

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