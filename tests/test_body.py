import pymunk as p
from pymunk.vec2d import Vec2d
import unittest

####################################################################

class UnitTestBody(unittest.TestCase):
    def testProperties(self):
        b = p.Body(10,100)
        self.assertEqual(b.mass, 10)
        b.mass = 11
        self.assertEqual(b.mass, 11)

        self.assertEqual(b.moment, 100)
        b.moment = 101
        self.assertEqual(b.moment, 101)

        self.assertEqual(b.position, (0,0))
        b.position = 1,2
        self.assertEqual(b.position, (1,2))

        self.assertEqual(b.center_of_gravity, (0,0))
        b.center_of_gravity = 2,3
        self.assertEqual(b.center_of_gravity, (2,3))

        self.assertEqual(b.velocity, (0,0))
        b.velocity = 3,4
        self.assertEqual(b.velocity, (3,4))

        self.assertEqual(b.force, (0,0))
        b.force = (4,5)
        self.assertEqual(b.force, (4,5))

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
        self.assertEqual(b.rotation_vector, (1,0))
        b.angle = Vec2d(1,1).get_angle()
        self.assertAlmostEqual(b.rotation_vector.get_angle(), Vec2d(1,1).get_angle())

        self.assertEqual(b.space, None)
        s = p.Space()
        s.add(b)
        self.assertEqual(b.space, s)

    def testRepr(self):
        b = p.Body(1,2)
        self.assertEqual(str(b), "Body(1.0, 2.0, Body.DYNAMIC)")
        b = p.Body(body_type = p.Body.KINEMATIC)
        self.assertEqual(str(b), "Body(Body.KINEMATIC)")
        b = p.Body(body_type = p.Body.STATIC)
        self.assertEqual(str(b), "Body(Body.STATIC)")

    def testCoordinateConversion(self):
        b = p.Body(body_type=p.Body.KINEMATIC)
        v = 1,2
        self.assertEqual(b.local_to_world(v), v)
        self.assertEqual(b.world_to_local(v), v)
        b.position = 3,4
        self.assertEqual(b.local_to_world(v), (4,6))
        self.assertEqual(b.world_to_local(v), (-2,-2))

    def testVelocityConversion(self):
        b = p.Body(1,2)
        self.assertEqual(b.velocity_at_world_point((1,1)), (0,0))
        self.assertEqual(b.velocity_at_local_point((1,1)), (0,0))
        b.position = 1,2
        b.angular_velocity = 1.2
        self.assertEqual(b.velocity_at_world_point((1,1)), (1.2, 0))
        self.assertEqual(b.velocity_at_local_point((1,1)), (-1.2, 1.2))

    def testForce(self):
        b = p.Body(1,2)
        b.position = 3,4
        b.apply_force_at_world_point((10,0), (0,10))
        self.assertEqual(b.force, (10,0))
        self.assertEqual(b.torque, -60)

        b = p.Body(1,2)
        b.position = 3,4
        b.apply_force_at_local_point((10,0), (0,10))
        self.assertEqual(b.force, (10,0))
        self.assertEqual(b.torque, -100)

    def testImpulse(self):
        b = p.Body(1,2)
        b.position = 3,4
        b.apply_impulse_at_world_point((10,0), (0,10))
        self.assertEqual(b.velocity, (10,0))
        self.assertEqual(b.angular_velocity, -30)

        b = p.Body(1,2)
        b.position = 3,4
        b.apply_impulse_at_local_point((10,0), (0,10))
        self.assertEqual(b.velocity, (10,0))
        self.assertEqual(b.angular_velocity, -50)

    def testSleep(self):
        b = p.Body(1,1)
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
        

    def testSleepWithGroup(self):
        b1 = p.Body(1,1)
        b2 = p.Body(2,2)
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


    def testKineticEnergy(self):
        b = p.Body(1,10)
        self.assertEqual(b.kinetic_energy, 0)
        b.apply_impulse_at_local_point((10,0))
        self.assertEqual(b.kinetic_energy, 100)

    def testDynamic(self):
        b1 = p.Body(1,1)
        b2 = p.Body(1,1, body_type=p.Body.DYNAMIC)
        self.assertEqual(b1.body_type, p.Body.DYNAMIC)
        self.assertEqual(b2.body_type, p.Body.DYNAMIC)


    def testKinematic(self):
        b = p.Body(body_type=p.Body.KINEMATIC)
        self.assertEqual(b.body_type, p.Body.KINEMATIC)

    def testStatic(self):
        b = p.Body(body_type=p.Body.STATIC)
        self.assertEqual(b.body_type, p.Body.STATIC)



    def testPositionFunction(self):
        s = p.Space()
        b = p.Body(1,1)
        def f(body, dt):
            body.position += 0,dt

        b.position_func=f
        s.add(b)
        s.step(10)
        self.assertEqual(b.position, (0,10))
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

    def testEachArbiters(self):
        s = p.Space()
        b1 = p.Body(1,1)
        b2 = p.Body(1,1)
        c1 = p.Circle(b1,10)
        c2 = p.Circle(b2,10)
        s.add(b1,b2,c1,c2)
        s.step(1)

        shapes = []
        def f(arbiter, shapes):
            shapes += arbiter.shapes
        arbs = b1.each_arbiter(f, shapes)
        self.assertEqual(shapes[0], c1)
        self.assertEqual(shapes[1], c2)

    def testGetConstraints(self):
        s = p.Space()
        b1 = p.Body(1,1)
        b2 = p.Body(1,1)
        s.add(b1)
        j1 = p.PivotJoint(b1,s.static_body,(0,0))
        j2 = p.PivotJoint(b2,s.static_body,(0,0))

        self.assertTrue(j1 in b1.constraints)
        self.assertTrue(j1 not in b2.constraints)
        self.assertTrue(j1 in s.static_body.constraints)
        self.assertTrue(j2 in s.static_body.constraints)

    def testGetShapes(self):
        s = p.Space()
        b1 = p.Body(1,1)
        s.add(b1)
        s1 = p.Circle(b1,3)
        s2 = p.Segment(b1,(0,0), (1,2),1)

        self.assertTrue(s1 in b1.shapes)
        self.assertTrue(s2 in b1.shapes)
        self.assertTrue(s1 not in s.static_body.shapes)

####################################################################
if __name__ == "__main__":
    print ("testing pymunk version " + p.version)
    unittest.main()
