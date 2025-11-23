import gc
import pickle
import unittest

import pymunk as p
from pymunk.constraints import *


class UnitTestConstraint(unittest.TestCase):
    def testA(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = PivotJoint(a, b, (0, 0))
        self.assertEqual(j.a, a)

    def testB(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = PivotJoint(a, b, (0, 0))
        self.assertEqual(j.b, b)

    def testMaxForce(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = PivotJoint(a, b, (0, 0))
        self.assertEqual(j.max_force, float("inf"))
        j.max_force = 10
        self.assertEqual(j.max_force, 10)

    def testErrorBias(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = PivotJoint(a, b, (0, 0))
        self.assertAlmostEqual(j.error_bias, pow(1.0 - 0.1, 60.0))
        j.error_bias = 0.3
        self.assertEqual(j.error_bias, 0.3)

    def testMaxBias(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = PivotJoint(a, b, (0, 0))
        self.assertEqual(j.max_bias, float("inf"))
        j.max_bias = 10
        self.assertEqual(j.max_bias, 10)

    def testCollideBodies(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = PivotJoint(a, b, (0, 0))
        self.assertEqual(j.collide_bodies, True)
        j.collide_bodies = False
        self.assertEqual(j.collide_bodies, False)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        b.position = 0, 10
        j = PivotJoint(a, b, (0, 0))

        s = p.Space()
        s.gravity = 0, 10
        s.add(b, j)
        self.assertEqual(j.impulse, 0)
        s.step(1)
        self.assertAlmostEqual(j.impulse, 50)

    def testActivate(self) -> None:
        a, b = p.Body(4, 5), p.Body(10, 10)
        j = PivotJoint(a, b, (0, 0))
        s = p.Space()
        s.sleep_time_threshold = 0.01
        s.add(a, b)
        a.sleep()
        b.sleep()

        j.activate_bodies()
        self.assertFalse(a.is_sleeping)
        self.assertFalse(b.is_sleeping)

    def testPreSolve(self) -> None:
        b = p.Body(1, 2)
        s = p.Space()
        j = PivotJoint(s.static_body, b, (0, 0))

        s.add(b, j)
        self.assertIsNone(j.pre_solve)
        s.step(1)

        actual_constraint = None
        actual_space = None

        def pre_solve(constraint: Constraint, space: p.Space) -> None:
            nonlocal actual_constraint
            nonlocal actual_space
            actual_constraint = constraint
            actual_space = space

        j.pre_solve = pre_solve
        s.step(1)

        self.assertEqual(actual_constraint, j)
        self.assertEqual(actual_space, s)

    def testPostSolve(self) -> None:
        b = p.Body(1, 2)
        s = p.Space()
        j = PivotJoint(s.static_body, b, (0, 0))

        s.add(b, j)
        self.assertIsNone(j.pre_solve)
        s.step(1)

        actual_constraint = None
        actual_space = None

        def post_solve(constraint: Constraint, space: p.Space) -> None:
            nonlocal actual_constraint
            nonlocal actual_space
            actual_constraint = constraint
            actual_space = space

        j.post_solve = post_solve
        s.step(1)

        self.assertEqual(actual_constraint, j)
        self.assertEqual(actual_space, s)

    def testPrePostSolveOrder(self) -> None:
        s = p.Space()
        b = p.Body(1, 2)
        j = PivotJoint(s.static_body, b, (0, 0))

        s.add(b, j)

        actual_order = []

        def pre_solve(c: Constraint, s: p.Space) -> None:
            nonlocal actual_order
            actual_order.append(1)

        def post_solve(c: Constraint, s: p.Space) -> None:
            nonlocal actual_order
            actual_order.append(2)

        j.pre_solve = pre_solve
        j.post_solve = post_solve
        s.step(1)

        self.assertEqual(actual_order, [1, 2])

    def testPickle(self) -> None:
        a, b = p.Body(4, 5), p.Body(10, 10)
        a.custom = "a"
        b.custom = "b"
        j = PivotJoint(a, b, (1, 2))
        j.custom = "test"
        j.max_force = 2
        j.error_bias = 3
        j.max_bias = 4
        j.collide_bodies = False

        j.pre_solve = pre_solve

        j.post_solve = post_solve

        s = pickle.dumps(j)
        j2 = pickle.loads(s)
        self.assertEqual(j.custom, j2.custom)
        self.assertEqual(j.max_force, j2.max_force)
        self.assertEqual(j.error_bias, j2.error_bias)
        self.assertEqual(j.max_bias, j2.max_bias)
        self.assertEqual(j.collide_bodies, j2.collide_bodies)
        self.assertEqual(j.a.custom, j2.a.custom)
        self.assertEqual(j.b.custom, j2.b.custom)

        self.assertEqual(j.pre_solve, j2.pre_solve)
        self.assertEqual(j.post_solve, j2.post_solve)

        j2 = j.copy()

    def test_body_types(self) -> None:
        supported = [
            (p.Body.DYNAMIC, p.Body.DYNAMIC),
            (p.Body.DYNAMIC, p.Body.KINEMATIC),
            (p.Body.DYNAMIC, p.Body.STATIC),
            (p.Body.KINEMATIC, p.Body.DYNAMIC),
            (p.Body.STATIC, p.Body.DYNAMIC),
        ]
        non_supported = [
            (p.Body.KINEMATIC, p.Body.KINEMATIC),
            (p.Body.KINEMATIC, p.Body.STATIC),
            (p.Body.STATIC, p.Body.KINEMATIC),
            (p.Body.STATIC, p.Body.STATIC),
        ]

        for type1, type2 in supported:
            a, b = p.Body(4, 5, body_type=type1), p.Body(10, 10, body_type=type2)
            _ = PivotJoint(a, b, (1, 2))

            for type3, type4 in non_supported:
                with self.assertRaises(AssertionError):
                    a.body_type = type3
                    a.body_type = type4

        for type1, type2 in non_supported:
            a, b = p.Body(4, 5, body_type=type1), p.Body(10, 10, body_type=type2)
            with self.assertRaises(AssertionError):
                _ = PivotJoint(a, b, (1, 2))

    def test_delete(self) -> None:
        a, b = p.Body(1), p.Body(2)
        j1 = PivotJoint(a, b, (0, 0))
        j2 = PivotJoint(a, b, (0, 0))

        del j1
        gc.collect()

        self.assertListEqual(list(a.constraints), [j2])
        self.assertListEqual(list(b.constraints), [j2])


class UnitTestPinJoint(unittest.TestCase):
    def testAnchor(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = PinJoint(a, b, (1, 2), (3, 4))
        self.assertEqual(j.anchor_a, (1, 2))
        self.assertEqual(j.anchor_b, (3, 4))
        j.anchor_a = (5, 6)
        j.anchor_b = (7, 8)
        self.assertEqual(j.anchor_a, (5, 6))
        self.assertEqual(j.anchor_b, (7, 8))

    def testDistance(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = PinJoint(a, b, (0, 0), (10, 0))
        self.assertEqual(j.distance, 10)
        j.distance = 20
        self.assertEqual(j.distance, 20)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        a.position = 0, 10
        j = PinJoint(a, b, (0, 0), (0, 0))
        s = p.Space()
        s.add(a, b, j)
        s.step(0.1)
        self.assertEqual(j.impulse_signed, 0)
        self.assertEqual(j.impulse, 0)
        a.position = 0, 0
        s.step(0.1)
        self.assertAlmostEqual(j.impulse_signed, 2343, 0)
        self.assertAlmostEqual(j.impulse, 2343,0)
        a.position = 0, 20
        s.step(0.1)
        self.assertAlmostEqual(j.impulse_signed, -234, 0)
        self.assertAlmostEqual(j.impulse, 234, 0)

    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = PinJoint(a, b, (1, 2), (3, 4))

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.anchor_a, j2.anchor_a)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.distance, j2.distance)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


class UnitTestSlideJoint(unittest.TestCase):
    def testAnchor(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = SlideJoint(a, b, (1, 2), (3, 4), 0, 10)
        self.assertEqual(j.anchor_a, (1, 2))
        self.assertEqual(j.anchor_b, (3, 4))
        j.anchor_a = (5, 6)
        j.anchor_b = (7, 8)
        self.assertEqual(j.anchor_a, (5, 6))
        self.assertEqual(j.anchor_b, (7, 8))

    def testMin(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = SlideJoint(a, b, (0, 0), (0, 0), 1, 0)
        self.assertEqual(j.min, 1)
        j.min = 2
        self.assertEqual(j.min, 2)

    def testMax(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = SlideJoint(a, b, (0, 0), (0, 0), 0, 1)
        self.assertEqual(j.max, 1)
        j.max = 2
        self.assertEqual(j.max, 2)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        a.position = 0, 20
        j = SlideJoint(a, b, (0, 0), (0, 0), 20, 30)
        s = p.Space()
        s.add(a, b, j)
        s.step(0.1)
        self.assertEqual(j.impulse_signed, 0)
        self.assertEqual(j.impulse, 0)
        a.position = 0, 40
        s.step(0.1)
        self.assertAlmostEqual(j.impulse_signed, -234, 0)
        self.assertAlmostEqual(j.impulse, 234,0)
        # TODO: FIX ME when SlideJoint jnAcc is fixed.
        # a.position = 0,0
        # s.step(0.1)
        # self.assertAlmostEqual(j.impulse_signed, 234, 0)
        # self.assertAlmostEqual(j.impulse, 234, 0)


    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = SlideJoint(a, b, (1, 2), (3, 4), 5, 6)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.anchor_a, j2.anchor_a)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.min, j2.min)
        self.assertEqual(j.max, j2.max)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


class UnitTestPivotJoint(unittest.TestCase):
    def testAnchorByPivot(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        a.position = (5, 7)
        j = PivotJoint(a, b, (1, 2))
        self.assertEqual(j.anchor_a, (-4, -5))
        self.assertEqual(j.anchor_b, (1, 2))

    def testAnchorByAnchor(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = PivotJoint(a, b, (1, 2), (3, 4))
        self.assertEqual(j.anchor_a, (1, 2))
        self.assertEqual(j.anchor_b, (3, 4))
        j.anchor_a = (5, 6)
        j.anchor_b = (7, 8)
        self.assertEqual(j.anchor_a, (5, 6))
        self.assertEqual(j.anchor_b, (7, 8))

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        a.position = 0, 10
        j = PivotJoint(a, b, (10,0))
        s = p.Space()
        s.add(a, b, j)
        s.step(0.1)
        almostEqualVector(self, j.impulse_vector, p.Vec2d(0,0), 0)
        self.assertEqual(j.impulse, 0)
        a.position = 0, 0
        s.step(0.1)
        almostEqualVector(self, j.impulse_vector, p.Vec2d(4,-5), 0)
        self.assertAlmostEqual(j.impulse, 6,0)

    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = PivotJoint(a, b, (1, 2), (3, 4))

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.anchor_a, j2.anchor_a)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


class UnitTestGrooveJoint(unittest.TestCase):
    def testAnchor(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = GrooveJoint(a, b, (0, 0), (0, 0), (1, 2))
        self.assertEqual(j.anchor_b, (1, 2))
        j.anchor_b = (3, 4)
        self.assertEqual(j.anchor_b, (3, 4))

    def testGroove(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = GrooveJoint(a, b, (1, 2), (3, 4), (0, 0))
        self.assertEqual(j.groove_a, (1, 2))
        self.assertEqual(j.groove_b, (3, 4))
        j.groove_a = (5, 6)
        j.groove_b = (7, 8)
        self.assertEqual(j.groove_a, (5, 6))
        self.assertEqual(j.groove_b, (7, 8))

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        a.position = 0, 2.5
        b.position = 0, 2.5
        j = GrooveJoint(a, b, (0,0), (10, 0), (0,0))
        s = p.Space()
        s.add(a, b, j)
        almostEqualVector(self, j.impulse_vector, p.Vec2d(0,0))
        self.assertAlmostEqual(j.impulse, 0)
        
        a.position = 0, 0
        s.step(0.1)
        almostEqualVector(self, j.impulse_vector, p.Vec2d(0, -59), 0)
        self.assertAlmostEqual(j.impulse, 59,0)


    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = GrooveJoint(a, b, (1, 2), (3, 4), (5, 6))

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.groove_a, j2.groove_a)
        self.assertEqual(j.groove_b, j2.groove_b)
        self.assertEqual(j.anchor_b, j2.anchor_b)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


class UnitTestDampedSpring(unittest.TestCase):
    def testAnchor(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedSpring(a, b, (1, 2), (3, 4), 0, 0, 0)
        self.assertEqual(j.anchor_a, (1, 2))
        self.assertEqual(j.anchor_b, (3, 4))
        j.anchor_a = (5, 6)
        j.anchor_b = (7, 8)
        self.assertEqual(j.anchor_a, (5, 6))
        self.assertEqual(j.anchor_b, (7, 8))

    def testRestLength(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedSpring(a, b, (0, 0), (0, 0), 1, 0, 0)
        self.assertEqual(j.rest_length, 1)
        j.rest_length = 2
        self.assertEqual(j.rest_length, 2)

    def testStiffness(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedSpring(a, b, (0, 0), (0, 0), 0, 1, 0)
        self.assertEqual(j.stiffness, 1)
        j.stiffness = 2
        self.assertEqual(j.stiffness, 2)

    def testDamping(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedSpring(a, b, (0, 0), (0, 0), 0, 0, 1)
        self.assertEqual(j.damping, 1)
        j.damping = 2
        self.assertEqual(j.damping, 2)

    def testForceFunc(self) -> None:
        s = p.Space()
        a, b = p.Body(10, 10), p.Body(20, 20)
        b.position = 0, 100
        j = DampedSpring(a, b, (0, 0), (0, 0), 0, 1, 0)
        s.add(a, b, j)

        def f(spring: p.DampedSpring, dist: float) -> float:
            self.assertEqual(spring, j)
            self.assertEqual(dist, 100)

            return 1

        self.assertEqual(j.force_func, DampedSpring.spring_force)

        j.force_func = f
        self.assertEqual(f, j.force_func)
        s.step(1)
        self.assertEqual(j.impulse, 1)

        j.force_func = DampedSpring.spring_force
        s.step(1)
        self.assertAlmostEqual(j.impulse, -100.15)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        a.position = 0, 0
        b.position = 0, 10
        j = DampedSpring(a, b, (0,0), (0,0), 10, 9, 0.01)
        s = p.Space()
        s.add(a, b, j)
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 0)
        b.position = 0,25
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, -13.497300269982)


    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedSpring(a, b, (1, 2), (3, 4), 5, 6, 7)

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
    def testRestAngle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedRotarySpring(a, b, 1, 0, 0)
        self.assertEqual(j.rest_angle, 1)
        j.rest_angle = 2
        self.assertEqual(j.rest_angle, 2)

    def testStiffness(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedRotarySpring(a, b, 0, 1, 0)
        self.assertEqual(j.stiffness, 1)
        j.stiffness = 2
        self.assertEqual(j.stiffness, 2)

    def testDamping(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedRotarySpring(a, b, 0, 0, 1)
        self.assertEqual(j.damping, 1)
        j.damping = 2
        self.assertEqual(j.damping, 2)

    def testTorqueFunc(self) -> None:
        s = p.Space()
        a, b = p.Body(10, 10), p.Body(20, 20)
        b.angle = 2
        j = DampedRotarySpring(a, b, 0, 10, 0)
        s.add(a, b, j)

        def f(spring: p.DampedRotarySpring, relative_angle: float) -> float:
            self.assertEqual(spring, j)
            self.assertEqual(relative_angle, -2)

            return 1

        self.assertEqual(j.torque_func, DampedRotarySpring.spring_torque)

        j.torque_func = f
        self.assertEqual(f, j.torque_func)
        s.step(1)
        self.assertEqual(j.impulse, 1)

        j.torque_func = DampedRotarySpring.spring_torque
        s.step(1)
        self.assertAlmostEqual(j.impulse, -21.5)
    
    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        a.angle = 1
        j = DampedRotarySpring(a, b, 1, 9, 0.01)
        s = p.Space()
        s.add(a, b, j)
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 0)
        a.angle = 2
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 0.89982001)

    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = DampedRotarySpring(a, b, 1, 2, 3)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.rest_angle, j2.rest_angle)
        self.assertEqual(j.stiffness, j2.stiffness)
        self.assertEqual(j.damping, j2.damping)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


class UnitTestRotaryLimitJoint(unittest.TestCase):
    def testMin(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = RotaryLimitJoint(a, b, 1, 0)
        self.assertEqual(j.min, 1)
        j.min = 2
        self.assertEqual(j.min, 2)

    def testMax(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = RotaryLimitJoint(a, b, 0, 1)
        self.assertEqual(j.max, 1)
        j.max = 2
        self.assertEqual(j.max, 2)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = RotaryLimitJoint(a, b, 0, 1)
        s = p.Space()
        s.add(a, b, j)
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 0)
        self.assertAlmostEqual(j.impulse_signed, 0)
        a.angle = 2
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 46.855908447)
        self.assertAlmostEqual(j.impulse_signed, 46.855908447)

    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = RotaryLimitJoint(a, b, 1, 2)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.min, j2.min)
        self.assertEqual(j.max, j2.max)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


class UnitTestRatchetJoint(unittest.TestCase):
    def testAngle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = RatchetJoint(a, b, 0, 0)
        self.assertEqual(j.angle, 0)
        j.angle = 1
        self.assertEqual(j.angle, 1)

    def testPhase(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = RatchetJoint(a, b, 1, 0)
        self.assertEqual(j.phase, 1)
        j.phase = 2
        self.assertEqual(j.phase, 2)

    def testRatchet(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = RatchetJoint(a, b, 0, 1)
        self.assertEqual(j.ratchet, 1)
        j.ratchet = 2
        self.assertEqual(j.ratchet, 2)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        j = RatchetJoint(a, b, 0.1, 0.1)
        s = p.Space()
        s.add(a, b, j)
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 0)
        self.assertAlmostEqual(j.impulse_signed, 0)
        a.angle = 2
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 46.855908447)
        self.assertAlmostEqual(j.impulse_signed, 46.855908447)

    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = RatchetJoint(a, b, 1, 2)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.phase, j2.phase)
        self.assertEqual(j.ratchet, j2.ratchet)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


class UnitTestGearJoint(unittest.TestCase):
    def testPhase(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = GearJoint(a, b, 1, 0)
        self.assertEqual(j.phase, 1)
        j.phase = 2
        self.assertEqual(j.phase, 2)

    def testRatio(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = GearJoint(a, b, 0, 1)
        self.assertEqual(j.ratio, 1)
        j.ratio = 2
        self.assertEqual(j.ratio, 2)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        b.angle = 0.03
        j = GearJoint(a, b, 0.1, 3)
        s = p.Space()
        s.add(a, b, j)
        self.assertAlmostEqual(j.impulse, 0)
        self.assertAlmostEqual(j.impulse_signed, 0)
        a.angle = 2
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 28.25411279)
        self.assertAlmostEqual(j.impulse_signed, 28.25411279)
        a.angular_velocity = -0.1
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 9.5300055)
        self.assertAlmostEqual(j.impulse_signed, -9.5300055)


    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = GearJoint(a, b, 1, 2)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.phase, j2.phase)
        self.assertEqual(j.ratio, j2.ratio)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)



class UnitTestSimleMotor(unittest.TestCase):
    def testSimpleMotor(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = SimpleMotor(a, b, 0.3)
        self.assertEqual(j.rate, 0.3)
        j.rate = 0.4
        self.assertEqual(j.rate, 0.4)

    def testImpulse(self) -> None:
        a, b = p.Body(10, 10), p.Body(10, 10)
        a.angular_velocity = .3
        j = SimpleMotor(a, b, .3)
        s = p.Space()
        s.add(a, b, j)
        self.assertAlmostEqual(j.impulse, 0)
        self.assertAlmostEqual(j.impulse_signed, 0)
        a.angular_velocity = 1
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 3.5)
        self.assertAlmostEqual(j.impulse_signed, 3.5)
        a.angular_velocity = -0.1
        s.step(0.1)
        self.assertAlmostEqual(j.impulse, 3.75)
        self.assertAlmostEqual(j.impulse_signed, -3.75)

    def testPickle(self) -> None:
        a, b = p.Body(10, 10), p.Body(20, 20)
        j = SimpleMotor(a, b, 1)

        s = pickle.dumps(j)
        j2 = pickle.loads(s)

        self.assertEqual(j.rate, j2.rate)
        self.assertEqual(j.a.mass, j2.a.mass)
        self.assertEqual(j.b.mass, j2.b.mass)


# Needed to be able to pickle
def pre_solve(c: Constraint, s: p.Space) -> None:
    pass


def post_solve(c: Constraint, s: p.Space) -> None:
    pass

def almostEqualVector(self, first:p.Vec2d, second:p.Vec2d, places:int=7) -> None:
    self.assertAlmostEqual(first.x, second.x, places)
    self.assertAlmostEqual(first.y, second.y, places)
