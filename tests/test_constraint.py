import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################
class UnitTestConstraint(unittest.TestCase):
    def setUp(self):
        p.reset_shapeid_counter()
    
    def testProperties(self):
        a,b = p.Body(p.inf, p.inf), p.Body(10,10)
        j = p.PivotJoint(a,b,(0,0))
        
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
        j = p.PivotJoint(a,b,(0,0))
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
        
    def testGrooveJoint(self):
        a,b = p.Body(10,10), p.Body(20,20)
        a.position = 10,10
        b.position = 20,20
        j = p.GrooveJoint(a,b, (5,0), (7,7), (3,3))
        
        self.assertEqual(j.anchr2, (3,3))
        self.assertEqual(j.groove_a, (5,0))
        self.assertEqual(j.groove_b, (7,7))
        
####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()