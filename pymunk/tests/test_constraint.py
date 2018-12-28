import pymunk as p
from pymunk.vec2d import Vec2d
import unittest
import pickle

####################################################################
class UnitTestConstraint(unittest.TestCase):
    def testA(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.a, a)

    def testB(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.b, b)

    def testMaxForce(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.max_force, p.inf)
        j.max_force = 10
        self.assertEqual(j.max_force, 10)

    def testErrorBias(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertAlmostEqual(j.error_bias, pow(1.0 - 0.1, 60.0))
        j.error_bias = 0.3
        self.assertEqual(j.error_bias, 0.3)

    def testMaxBias(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.max_bias, p.inf)
        j.max_bias = 10
        self.assertEqual(j.max_bias, 10)

    def testCollideBodies(self):
        a,b = p.Body(10,10), p.Body(10,10)
        j = p.PivotJoint(a, b, (0,0))
        self.assertEqual(j.collide_bodies, True)
        j.collide_bodies = False
        self.assertEqual(j.collide_bodies, False)

    def testImpulse(self):
        a,b = p.Body(10,10), p.Body(10,10)
        b.position = 0,10
        j = p.PivotJoint(a, b, (0,0))

        s = p.Space()
        s.gravity = 0,10
        s.add(b, j)
        self.assertEqual(j.impulse, 0)
        s.step(1)
        self.assertAlmostEqual(j.impulse, 50)

    def testActivate(self):
        a,b = p.Body(4,5), p.Body(10,10)
        j = p.PivotJoint(a,b,(0,0))
        s = p.Space()
        s.sleep_time_threshold = 0.01
        s.add(a,b)
        a.sleep()
        b.sleep()

        j.activate_bodies()
        self.assertFalse(a.is_sleeping)
        self.assertFalse(b.is_sleeping)

    def testPickle(self):
        a,b = p.Body(4,5), p.Body(10,10)
        a.custom = "a"
        b.custom = "b"
        j = p.PivotJoint(a,b,(1,2))
        j.custom = "test"
        j.max_force = 2
        j.error_bias = 3
        j.max_bias = 4
        j.collide_bodies = False

        s = pickle.dumps(j)
        j2 = pickle.loads(s)
        self.assertEqual(j.custom, j2.custom)
        self.assertEqual(j.max_force, j2.max_force)
        self.assertEqual(j.error_bias, j2.error_bias)
        self.assertEqual(j.max_bias, j2.max_bias)
        self.assertEqual(j.collide_bodies, j2.collide_bodies)
        self.assertEqual(j.a.custom, j2.a.custom)
        self.assertEqual(j.b.custom, j2.b.custom)

        j2 = j.copy()

class UnitTestPinJoint(unittest.TestCase):
    def testAnchor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PinJoint(a, b, (1,2), (3,4))
        self.assertEqual(j.anchor_a, (1,2))
        self.assertEqual(j.anchor_b, (3,4))
        j.anchor_a = (5,6)
        j.anchor_b = (7,8)
        self.assertEqual(j.anchor_a, (5,6))
        self.assertEqual(j.anchor_b, (7,8))

    def testDistane(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PinJoint(a, b, (0,0), (10,0))
        self.assertEqual(j.distance, 10)
        j.distance = 20
        self.assertEqual(j.distance, 20)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PinJoint(a, b, (1,2), (3,4))

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.anchor_a, j2.anchor_a)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.distance, j2.distance)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestSlideJoint(unittest.TestCase):
    def testAnchor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a, b, (1,2), (3,4), 0, 10)
        self.assertEqual(j.anchor_a, (1,2))
        self.assertEqual(j.anchor_b, (3,4))
        j.anchor_a = (5,6)
        j.anchor_b = (7,8)
        self.assertEqual(j.anchor_a, (5,6))
        self.assertEqual(j.anchor_b, (7,8))

    def testMin(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a, b, (0,0), (0,0), 1, 0)
        self.assertEqual(j.min, 1)
        j.min = 2
        self.assertEqual(j.min, 2)

    def testMax(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a, b, (0,0), (0,0), 0, 1)
        self.assertEqual(j.max, 1)
        j.max = 2
        self.assertEqual(j.max, 2)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SlideJoint(a, b, (1,2), (3,4), 5, 6)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.anchor_a, j2.anchor_a)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.min, j2.min)
        self.assertEqual(j.max, j2.max)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestPivotJoint(unittest.TestCase):
    def testAnchorByPivot(self):
        a,b = p.Body(10,10), p.Body(20,20)
        a.position = (5,7)
        j = p.PivotJoint(a, b, (1,2))
        self.assertEqual(j.anchor_a, (-4,-5))
        self.assertEqual(j.anchor_b, (1,2))

    def testAnchorByAnchor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PivotJoint(a, b, (1,2), (3,4))
        self.assertEqual(j.anchor_a, (1,2))
        self.assertEqual(j.anchor_b, (3,4))
        j.anchor_a = (5,6)
        j.anchor_b = (7,8)
        self.assertEqual(j.anchor_a, (5,6))
        self.assertEqual(j.anchor_b, (7,8))

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.PivotJoint(a, b, (1,2), (3,4))

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.anchor_a, j2.anchor_a)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestGrooveJoint(unittest.TestCase):
    def testAnchor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GrooveJoint(a, b, (0,0), (0,0), (1,2))
        self.assertEqual(j.anchor_b, (1,2))
        j.anchor_b = (3,4)
        self.assertEqual(j.anchor_b, (3,4))

    def testGroove(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GrooveJoint(a, b, (1,2), (3,4), (0,0))
        self.assertEqual(j.groove_a, (1,2))
        self.assertEqual(j.groove_b, (3,4))
        j.groove_a = (5,6)
        j.groove_b = (7,8)
        self.assertEqual(j.groove_a, (5,6))
        self.assertEqual(j.groove_b, (7,8))

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GrooveJoint(a, b, (1,2), (3,4), (5,6))

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.groove_a, j2.groove_a)
        self.assertEqual(j.groove_b, j2.groove_b)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestDampedSpring(unittest.TestCase):
    def testAnchor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedSpring(a, b, (1,2), (3,4), 0, 0, 0)
        self.assertEqual(j.anchor_a, (1,2))
        self.assertEqual(j.anchor_b, (3,4))
        j.anchor_a = (5,6)
        j.anchor_b = (7,8)
        self.assertEqual(j.anchor_a, (5,6))
        self.assertEqual(j.anchor_b, (7,8))

    def testRestLength(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedSpring(a, b, (0,0), (0,0), 1, 0, 0)
        self.assertEqual(j.rest_length, 1)
        j.rest_length = 2
        self.assertEqual(j.rest_length, 2)

    def testStiffness(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedSpring(a, b, (0,0), (0,0), 0, 1, 0)
        self.assertEqual(j.stiffness, 1)
        j.stiffness = 2
        self.assertEqual(j.stiffness, 2)

    def testDamping(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedSpring(a, b, (0,0), (0,0), 0, 0, 1)
        self.assertEqual(j.damping, 1)
        j.damping = 2
        self.assertEqual(j.damping, 2)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedSpring(a, b, (1,2), (3,4), 5, 6, 7)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.anchor_a, j2.anchor_a)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.rest_length, j2.rest_length)
        self.assertEqual(j.stiffness, j2.stiffness)
        self.assertEqual(j.damping, j2.damping)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestDampedRotarySpring(unittest.TestCase):
    def testRestAngle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a, b, 1, 0, 0)
        self.assertEqual(j.rest_angle, 1)
        j.rest_angle = 2
        self.assertEqual(j.rest_angle, 2)

    def testStiffness(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a, b, 0, 1, 0)
        self.assertEqual(j.stiffness, 1)
        j.stiffness = 2
        self.assertEqual(j.stiffness, 2)

    def testDamping(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a, b,  0, 0, 1)
        self.assertEqual(j.damping, 1)
        j.damping = 2
        self.assertEqual(j.damping, 2)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.DampedRotarySpring(a, b, 1, 2, 3)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.rest_angle, j2.rest_angle)
        self.assertEqual(j.stiffness, j2.stiffness)
        self.assertEqual(j.damping, j2.damping)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestRotaryLimitJoint(unittest.TestCase):
    def testMin(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RotaryLimitJoint(a, b, 1, 0)
        self.assertEqual(j.min, 1)
        j.min = 2
        self.assertEqual(j.min, 2)

    def testMax(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RotaryLimitJoint(a, b, 0, 1)
        self.assertEqual(j.max, 1)
        j.max = 2
        self.assertEqual(j.max, 2)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RotaryLimitJoint(a, b, 1, 2)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.min, j2.min)
        self.assertEqual(j.max, j2.max)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestRatchetJoint(unittest.TestCase):
    def testAngle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RatchetJoint(a, b, 0, 0)
        self.assertEqual(j.angle, 0)
        j.angle = 1
        self.assertEqual(j.angle, 1)

    def testPhase(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RatchetJoint(a, b, 1, 0)
        self.assertEqual(j.phase, 1)
        j.phase = 2
        self.assertEqual(j.phase, 2)

    def testRatchet(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RatchetJoint(a, b, 0, 1)
        self.assertEqual(j.ratchet, 1)
        j.ratchet = 2
        self.assertEqual(j.ratchet, 2)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.RatchetJoint(a, b, 1, 2)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.phase, j2.phase)
        self.assertEqual(j.ratchet, j2.ratchet)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestGearJoint(unittest.TestCase):
    def testPhase(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GearJoint(a, b, 1, 0)
        self.assertEqual(j.phase, 1)
        j.phase = 2
        self.assertEqual(j.phase, 2)

    def testRatio(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GearJoint(a, b, 0, 1)
        self.assertEqual(j.ratio, 1)
        j.ratio = 2
        self.assertEqual(j.ratio, 2)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.GearJoint(a, b, 1, 2)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.phase, j2.phase)
        self.assertEqual(j.ratio, j2.ratio)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

class UnitTestSimleMotor(unittest.TestCase):
    def testSimpleMotor(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SimpleMotor(a, b, 0.3)
        self.assertEqual(j.rate, 0.3)
        j.rate = 0.4
        self.assertEqual(j.rate, 0.4)

    def testPickle(self):
        a,b = p.Body(10,10), p.Body(20,20)
        j = p.SimpleMotor(a, b, 1)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.rate, j2.rate)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)

####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()
