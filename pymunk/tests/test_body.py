import pickle
import unittest
from typing import List, Tuple

import pymunk as p
from pymunk.arbiter import Arbiter
from pymunk.constraints import *
from pymunk.shapes import Shape
from pymunk.vec2d import Vec2d

####################################################################


class UnitTestBody(unittest.TestCase):
    def testProperties(self) -> None:
        b = p.Body(10, 100)
        self.assertEqual(b.mass, 10)
        b.mass = 11
        self.assertEqual(b.mass, 11)

        self.assertEqual(b.moment, 100)
        b.moment = 101
        self.assertEqual(b.moment, 101)

        self.assertEqual(b.position, (0, 0))
        b.position = 1, 2
        self.assertEqual(b.position, (1, 2))

        self.assertEqual(b.center_of_gravity, (0, 0))
        b.center_of_gravity = 2, 3
        self.assertEqual(b.center_of_gravity, (2, 3))

        self.assertEqual(b.velocity, (0, 0))
        b.velocity = 3, 4
        self.assertEqual(b.velocity, (3, 4))

        self.assertEqual(b.force, (0, 0))
        b.force = (4, 5)
        self.assertEqual(b.force, (4, 5))

        self.assertEqual(b.angle, 0)
        b.angle = 1.2
        self.assertEqual(b.angle, 1.2)

        self.assertEqual(b.angular_velocity, 0)
        b.angular_velocity = 1.3
        self.assertEqual(b.angular_velocity, 1.3)

        self.assertEqual(b.torque, 0)
        b.torque = 1.4
        self.assertEqual(b.torque, 1.4)

        b.angle = 0
        self.assertEqual(b.rotation_vector, (1, 0))
        b.angle = Vec2d(1, 1).angle
        self.assertAlmostEqual(b.rotation_vector.angle, Vec2d(1, 1).angle)

        self.assertGreater(b._id, 0)

        self.assertEqual(b.space, None)
        s = p.Space()
        s.add(b)
        self.assertEqual(b.space, s)

    def testRepr(self) -> None:
        b = p.Body(1, 2)
        self.assertEqual(str(b), "Body(1.0, 2.0, Body.DYNAMIC)")
        b = p.Body(body_type=p.Body.KINEMATIC)
        self.assertEqual(str(b), "Body(Body.KINEMATIC)")
        b = p.Body(body_type=p.Body.STATIC)
        self.assertEqual(str(b), "Body(Body.STATIC)")

    def testCoordinateConversion(self) -> None:
        b = p.Body(body_type=p.Body.KINEMATIC)
        v = 1, 2
        self.assertEqual(b.local_to_world(v), v)
        self.assertEqual(b.world_to_local(v), v)
        b.position = 3, 4
        self.assertEqual(b.local_to_world(v), (4, 6))
        self.assertEqual(b.world_to_local(v), (-2, -2))

    def testVelocityConversion(self) -> None:
        b = p.Body(1, 2)
        self.assertEqual(b.velocity_at_world_point((1, 1)), (0, 0))
        self.assertEqual(b.velocity_at_local_point((1, 1)), (0, 0))
        b.position = 1, 2
        b.angular_velocity = 1.2
        self.assertEqual(b.velocity_at_world_point((1, 1)), (1.2, 0))
        self.assertEqual(b.velocity_at_local_point((1, 1)), (-1.2, 1.2))

    def testForce(self) -> None:
        b = p.Body(1, 2)
        b.position = 3, 4
        b.apply_force_at_world_point((10, 0), (0, 10))
        self.assertEqual(b.force, (10, 0))
        self.assertEqual(b.torque, -60)

        b = p.Body(1, 2)
        b.position = 3, 4
        b.apply_force_at_local_point((10, 0), (0, 10))
        self.assertEqual(b.force, (10, 0))
        self.assertEqual(b.torque, -100)

    def testImpulse(self) -> None:
        b = p.Body(1, 2)
        b.position = 3, 4
        b.apply_impulse_at_world_point((10, 0), (0, 10))
        self.assertEqual(b.velocity, (10, 0))
        self.assertEqual(b.angular_velocity, -30)

        b = p.Body(1, 2)
        b.position = 3, 4
        b.apply_impulse_at_local_point((10, 0), (0, 10))
        self.assertEqual(b.velocity, (10, 0))
        self.assertEqual(b.angular_velocity, -50)

    def testSleep(self) -> None:
        b = p.Body(1, 1)
        s = p.Space()
        s.sleep_time_threshold = 0.01

        self.assertFalse(b.is_sleeping)

        self.assertRaises(Exception, b.sleep)
        s.add(b)
        b.sleep()

        self.assertTrue(b.is_sleeping)

        b.activate()
        self.assertFalse(b.is_sleeping)

        b.sleep()
        s.remove(b)
        b.activate()

    def testSleepWithGroup(self) -> None:
        b1 = p.Body(1, 1)
        b2 = p.Body(2, 2)
        s = p.Space()
        s.sleep_time_threshold = 0.01
        s.add(b2)
        b2.sleep()

        with self.assertRaises(Exception):
            b1.sleep_with_group(b2)

        s.add(b1)
        b1.sleep_with_group(b2)
        self.assertTrue(b1.is_sleeping)
        b2.activate()
        self.assertFalse(b1.is_sleeping)

    def testKineticEnergy(self) -> None:
        b = p.Body(1, 10)
        self.assertEqual(b.kinetic_energy, 0)
        b.apply_impulse_at_local_point((10, 0))
        self.assertEqual(b.kinetic_energy, 100)

    def testDynamic(self) -> None:
        b1 = p.Body(1, 1)
        b2 = p.Body(1, 1, body_type=p.Body.DYNAMIC)
        self.assertEqual(b1.body_type, p.Body.DYNAMIC)
        self.assertEqual(b2.body_type, p.Body.DYNAMIC)

    def testKinematic(self) -> None:
        b = p.Body(body_type=p.Body.KINEMATIC)
        self.assertEqual(b.body_type, p.Body.KINEMATIC)

    def testStatic(self) -> None:
        b = p.Body(body_type=p.Body.STATIC)
        self.assertEqual(b.body_type, p.Body.STATIC)

    def testMassMomentFromShape(self) -> None:
        s = p.Space()

        b = p.Body()
        b.mass = 2
        c = p.Circle(b, 10, (2, 3))
        c.mass = 3

        self.assertEqual(b.mass, 0)
        s.add(b, c)
        self.assertEqual(b.mass, 3)
        c.mass = 4
        self.assertEqual(b.mass, 4)
        self.assertEqual(b.center_of_gravity.x, 2)
        self.assertEqual(b.center_of_gravity.y, 3)
        self.assertEqual(b.moment, 200)

    def testPositionFunction(self) -> None:
        s = p.Space()
        b = p.Body(1, 1)

        def f(body: p.Body, dt: float) -> None:
            body.position += 0, dt

        b.position_func = f
        s.add(b)
        s.step(10)
        self.assertEqual(b.position, (0, 10))
        s.step(1)
        s.step(1)
        self.assertEqual(b.position.y, 12)

        b.position_func = p.Body.update_position
        s.step(1)
        self.assertEqual(b.position.y, 12)

    def testVelocityFunction(self) -> None:
        s = p.Space()
        b = p.Body(1, 1)

        def f(body: p.Body, gravity: Vec2d, damping: float, dt: float) -> None:
            body.velocity += 5 * gravity

        b.velocity_func = f
        s.gravity = 1, 0
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

    def testEachArbiters(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        b2 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        c2 = p.Circle(b2, 10)
        s.add(b1, b2, c1, c2)
        s.step(1)

        shapes: List[Shape] = []

        def f(arbiter: Arbiter, shapes: List[Shape]) -> None:
            shapes += arbiter.shapes

        b1.each_arbiter(f, shapes)
        self.assertEqual(shapes[0], c1)
        self.assertEqual(shapes[1], c2)

    def testGetConstraints(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        b2 = p.Body(1, 1)
        s.add(b1)
        j1 = PivotJoint(b1, s.static_body, (0, 0))
        j2 = PivotJoint(b2, s.static_body, (0, 0))

        self.assertTrue(j1 in b1.constraints)
        self.assertTrue(j1 not in b2.constraints)
        self.assertTrue(j1 in s.static_body.constraints)
        self.assertTrue(j2 in s.static_body.constraints)

    def testGetShapes(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        s.add(b1)
        s1 = p.Circle(b1, 3)
        s2 = p.Segment(b1, (0, 0), (1, 2), 1)

        self.assertTrue(s1 in b1.shapes)
        self.assertTrue(s2 in b1.shapes)
        self.assertTrue(s1 not in s.static_body.shapes)

    def testPickle(self) -> None:
        b = p.Body(1, 2)
        b.custom = "test"
        b.position = 3, 4
        b.center_of_gravity = 5, 6
        b.velocity = 7, 8
        b.force = 9, 10
        b.angle = 11
        b.angular_velocity = 12
        b.torque = 13

        b.position_func = pf
        b.velocity_func = vf

        s = pickle.dumps(b)
        b2 = pickle.loads(s)

        self.assertEqual(b.mass, b2.mass)
        self.assertEqual(b.moment, b2.moment)
        self.assertEqual(b.body_type, b2.body_type)
        self.assertEqual(b.custom, b2.custom)
        self.assertEqual(b.position, b2.position)
        self.assertEqual(b.center_of_gravity, b2.center_of_gravity)
        self.assertEqual(b.velocity, b2.velocity)
        self.assertEqual(b.force, b2.force)
        self.assertEqual(b.angle, b2.angle)
        self.assertEqual(b.angular_velocity, b2.angular_velocity)
        self.assertEqual(b.torque, b2.torque)

        space = p.Space()
        space.add(b2)
        space.step(0.1)

        self.assertTrue(b2.pf)
        self.assertTrue(b2.vf)
        b2 = b.copy()


# Needs to be here for the lowest pickle protocol to work
def pf(body: p.Body, dt: float) -> None:
    body.pf = True


def vf(body: p.Body, gravity: Tuple[float, float], damping: float, dt: float) -> None:
    body.vf = True


####################################################################
if __name__ == "__main__":
    print("testing pymunk version " + p.version)
    unittest.main()
