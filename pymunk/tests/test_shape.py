import pickle
import unittest
from typing import Any

import pymunk as p


class UnitTestShape(unittest.TestCase):
    def test_point_query(self) -> None:
        b = p.Body(10, 10)
        c = p.Circle(b, 5)
        c.cache_bb()

        info = c.point_query((0, 0))

        self.assertEqual(info.shape, c)
        self.assertEqual(info.point, (0, 0))
        self.assertEqual(info.distance, -5)
        self.assertEqual(info.gradient, (0, 1))

        info = c.point_query((11, 0))

        self.assertEqual(info.shape, c)
        self.assertEqual(info.point, (5, 0))
        self.assertEqual(info.distance, 6)
        self.assertEqual(info.gradient, (1, 0))

    def test_segment_query(self) -> None:
        b = p.Body(10, 10)
        c = p.Circle(b, 5)
        c.cache_bb()

        info = c.segment_query((10, -50), (10, 50))
        self.assertEqual(info, None)

        info = c.segment_query((10, -50), (10, 50), 6)
        assert info != None
        self.assertEqual(info.shape, c)

        info = c.segment_query((0, -50), (0, 50))
        assert info != None
        self.assertEqual(info.shape, c)
        self.assertAlmostEqual(info.point.x, 0)
        self.assertAlmostEqual(info.point.y, -5)
        self.assertAlmostEqual(info.normal.x, 0)
        self.assertAlmostEqual(info.normal.y, -1)
        self.assertEqual(info.alpha, 0.45)

    def test_mass(self) -> None:
        c = p.Circle(None, 1)
        self.assertEqual(c.mass, 0)
        c.mass = 2
        self.assertEqual(c.mass, 2)

    def test_density(self) -> None:
        c = p.Circle(None, 1)
        self.assertEqual(c.density, 0)
        c.density = 2
        self.assertEqual(c.density, 2)

    def test_moment(self) -> None:
        c = p.Circle(None, 5)
        self.assertEqual(c.moment, 0)
        c.density = 2
        self.assertAlmostEqual(c.moment, 1963.4954084936207)
        c.density = 0
        c.mass = 2
        self.assertAlmostEqual(c.moment, 25)

    def test_area(self) -> None:
        c = p.Circle(None, 5)
        self.assertEqual(c.area, 78.53981633974483)

    def test_center_of_gravity(self) -> None:
        c = p.Circle(None, 5)
        self.assertEqual(c.center_of_gravity, (0, 0))
        c = p.Circle(None, 5, (10, 5))
        self.assertEqual(c.center_of_gravity.x, 10)
        self.assertEqual(c.center_of_gravity.y, 5)

    def test_no_body(self) -> None:
        c = p.Circle(None, 1)
        self.assertEqual(c.body, None)

    def test_remove_body(self) -> None:
        b = p.Body(1, 1)
        c = p.Circle(b, 1)
        c.body = None

        self.assertEqual(c.body, None)
        self.assertEqual(len(b.shapes), 0)

    def test_switch_body(self) -> None:
        b1 = p.Body(1, 1)
        b2 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertEqual(c.body, b1)
        self.assertTrue(c in b1.shapes)
        self.assertTrue(c not in b2.shapes)
        c.body = b2
        self.assertEqual(c.body, b2)
        self.assertTrue(c not in b1.shapes)
        self.assertTrue(c in b2.shapes)

    def test_sensor(self) -> None:
        b1 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertFalse(c.sensor)
        c.sensor = True
        self.assertTrue(c.sensor)

    def test_elasticity(self) -> None:
        b1 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertEqual(c.elasticity, 0)
        c.elasticity = 1
        self.assertEqual(c.elasticity, 1)

    def test_friction(self) -> None:
        b1 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertEqual(c.friction, 0)
        c.friction = 1
        self.assertEqual(c.friction, 1)

    def test_surface_velocity(self) -> None:
        b1 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertEqual(c.surface_velocity, (0, 0))
        c.surface_velocity = (1, 2)
        self.assertEqual(c.surface_velocity, (1, 2))

    def test_collision_type(self) -> None:
        b1 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertEqual(c.collision_type, 0)
        c.collision_type = 1
        self.assertEqual(c.collision_type, 1)

    def test_filter(self) -> None:
        b1 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertEqual(c.filter, p.ShapeFilter(0, 0xFFFFFFFF, 0xFFFFFFFF))
        c.filter = p.ShapeFilter(1, 0xFFFFFFF2, 0xFFFFFFF3)
        self.assertEqual(c.filter, p.ShapeFilter(1, 0xFFFFFFF2, 0xFFFFFFF3))

    def test_space(self) -> None:
        b1 = p.Body(1, 1)
        c = p.Circle(b1, 1)
        self.assertEqual(c.space, None)
        s = p.Space()
        s.add(b1, c)
        self.assertEqual(c.space, s)

    def test_shapes_collide(self) -> None:
        b1 = p.Body(1, 1)
        s1 = p.Circle(b1, 10)

        b2 = p.Body(1, 1)
        b2.position = 30, 30
        s2 = p.Circle(b2, 10)

        c = s1.shapes_collide(s2)
        self.assertEqual(c.normal, (1, 0))
        self.assertEqual(len(c.points), 1)
        point = c.points[0]
        self.assertEqual(point.point_a, (10, 0))
        self.assertEqual(point.point_b, (-10, 0))
        self.assertEqual(point.distance, -20)

    def test_pickle(self) -> None:
        b = p.Body(1, 2)
        c = p.Circle(b, 3, (4, 5))
        c.sensor = True
        c.collision_type = 6
        c.filter = p.ShapeFilter()
        c.elasticity = 7
        c.friction = 8
        c.surface_velocity = (9, 10)

        s = pickle.dumps(c)
        c2 = pickle.loads(s)

        self.assertEqual(c.sensor, c2.sensor)
        self.assertEqual(c.collision_type, c2.collision_type)
        self.assertEqual(c.filter, c2.filter)
        self.assertEqual(c.elasticity, c2.elasticity)
        self.assertEqual(c.friction, c2.friction)
        self.assertEqual(c.surface_velocity, c2.surface_velocity)
        self.assertEqual(c.density, c2.density)
        self.assertEqual(c.mass, c2.mass)
        assert c.body is not None
        self.assertEqual(c.body.mass, c2.body.mass)
        self.assertIsNotNone
        c = p.Circle(None, 1)
        c.density = 3

        s = pickle.dumps(c)
        c2 = pickle.loads(s)

        self.assertEqual(c.mass, c2.mass)
        self.assertEqual(c.density, c2.density)

        c2 = c.copy()


class UnitTestCircle(unittest.TestCase):
    def test_circle_bb(self) -> None:
        b = p.Body(10, 10)
        c = p.Circle(b, 5)

        c.cache_bb()

        self.assertEqual(c.bb, p.BB(-5.0, -5.0, 5.0, 5.0))

    def test_circle_no_body(self) -> None:
        c = p.Circle(None, 5)

        bb = c.update(p.Transform(1, 2, 3, 4, 5, 6))
        self.assertEqual(c.bb, bb)
        self.assertEqual(c.bb, p.BB(0, 1, 10, 11))

    def test_offset(self) -> None:
        c = p.Circle(None, 5, (1, 2))

        self.assertEqual(c.offset, (1, 2))

    def test_offset_unsafe(self) -> None:
        c = p.Circle(None, 5, (1, 2))

        c.unsafe_set_offset((3, 4))

        self.assertEqual(c.offset, (3, 4))

    def test_radius(self) -> None:
        c = p.Circle(None, 5)

        self.assertEqual(c.radius, 5)

    def test_radius_unsafe(self) -> None:
        c = p.Circle(None, 5)

        c.unsafe_set_radius(3)

        self.assertEqual(c.radius, 3)

    def test_pickle(self) -> None:
        c = p.Circle(None, 3, (4, 5))

        s = pickle.dumps(c)
        c2 = pickle.loads(s)

        self.assertEqual(c.radius, c2.radius)
        self.assertEqual(c.offset, c2.offset)


class UnitTestSegment(unittest.TestCase):
    def test_copy_neighbors(self) -> None:
        for change_endpoints in (False, True):
            space = p.Space()
            segment = p.Segment(space.static_body, (-10, 0), (0, 0), 0)
            segment.set_neighbors((-20, 0), (10, 0))
            if change_endpoints:
                segment.unsafe_set_endpoints((-9, 0), (1, 0))
            space.add(segment)
            circle = p.Circle(p.Body(1, 1), 0.5)
            circle.body.position = segment.b + (0.25, 0.3)
            self.assertEqual(len(space.shape_query(circle)), 0)
            for restore in (
                lambda value: value.copy(),
                lambda value: pickle.loads(pickle.dumps(value, 2)),
                lambda value: pickle.loads(pickle.dumps(value, 5)),
            ):
                with self.subTest(change_endpoints=change_endpoints, restore=restore):
                    restored = restore(space)
                    self.assertEqual(len(restored.shape_query(circle)), 0)
                    copied_segment = restore(segment)
                    rebuilt = p.Space()
                    assert copied_segment.body is not None
                    rebuilt.add(copied_segment.body, copied_segment)
                    self.assertEqual(len(rebuilt.shape_query(circle)), 0)

    def test_legacy_segmentState(self) -> None:
        segment = p.Segment(None, (-10, 0), (0, 0), 0)
        state = segment.__getstate__()
        state["special"] = []
        restored = p.Segment.__new__(p.Segment)
        restored.__setstate__(state)
        self.assertEqual(restored.a, segment.a)
        self.assertEqual(restored.b, segment.b)

    def test_bb(self) -> None:
        b = p.Body(10, 10)
        c = p.Segment(b, (2, 2), (2, 3), 2)

        c.cache_bb()

        self.assertEqual(c.bb, p.BB(0, 0, 4.0, 5.0))

    def test_properties(self) -> None:
        c = p.Segment(None, (2, 2), (2, 3), 4)

        self.assertEqual(c.a, (2, 2))
        self.assertEqual(c.b, (2, 3))
        self.assertEqual(c.normal, (1, 0))
        self.assertEqual(c.radius, 4)

    def test_properties_unsafe(self) -> None:
        c = p.Segment(None, (2, 2), (2, 3), 4)

        c.unsafe_set_endpoints((3, 4), (5, 6))
        self.assertEqual(c.a, (3, 4))
        self.assertEqual(c.b, (5, 6))

        c.unsafe_set_radius(5)
        self.assertEqual(c.radius, 5)

    def test_set_neighbors(self) -> None:
        c = p.Segment(None, (2, 2), (2, 3), 1)
        c.set_neighbors((2, 2), (2, 3))

    def test_segment_segment_collision(self) -> None:
        s = p.Space()
        b1 = p.Body(10, 10)
        c1 = p.Segment(b1, (-1, -1), (1, 1), 1)
        b2 = p.Body(10, 10)
        c2 = p.Segment(b2, (1, -1), (-1, 1), 1)

        s.add(b1, b2, c1, c2)

        self.num_of_begins = 0

        def begin(arb: p.Arbiter, space: p.Space, data: Any) -> None:
            self.num_of_begins += 1

        s.on_collision(begin=begin)
        s.step(0.1)

        self.assertEqual(1, self.num_of_begins)

    def test_pickle(self) -> None:
        c = p.Segment(None, (1, 2), (3, 4), 5)

        s = pickle.dumps(c)
        c2 = pickle.loads(s)

        self.assertEqual(c.a, c2.a)
        self.assertEqual(c.b, c2.b)
        self.assertEqual(c.radius, c2.radius)


class UnitTestPoly(unittest.TestCase):
    def test_init(self) -> None:
        c = p.Poly(None, [(0, 0), (10, 10), (20, 0), (-10, 10)], None, 0)

        b = p.Body(1, 2)
        c = p.Poly(b, [(0, 0), (10, 10), (20, 0), (-10, 10)], p.Transform.identity(), 6)

    def test_vertices(self) -> None:
        vs = [(-10, 10), (0, 0), (20, 0), (10, 10)]
        c = p.Poly(None, vs, None, 0)

        self.assertEqual(c.get_vertices(), vs)

        c = p.Poly(None, vs, p.Transform(1, 2, 3, 4, 5, 6), 0)

        vs2 = [(5.0, 6.0), (25.0, 26.0), (45.0, 66.0), (25.0, 46.0)]
        self.assertEqual(c.get_vertices(), vs2)

    def test_vertices_unsafe(self) -> None:
        vs = [(-10, 10), (0, 0), (20, 0), (10, 10)]
        c = p.Poly(None, vs, None, 0)

        vs2 = [(-3, 3), (0, 0), (3, 0)]
        c.unsafe_set_vertices(vs2)
        self.assertEqual(c.get_vertices(), vs2)

        vs3 = [(-4, 4), (0, 0), (4, 0)]
        c.unsafe_set_vertices(vs3, p.Transform.identity())
        self.assertEqual(c.get_vertices(), vs3)

    def test_bb(self) -> None:
        c = p.Poly(None, [(2, 2), (4, 3), (3, 5)])
        bb = c.update(p.Transform.identity())
        self.assertEqual(bb, c.bb)
        self.assertEqual(c.bb, p.BB(2, 2, 4, 5))

        b = p.Body(1, 2)
        c = p.Poly(b, [(2, 2), (4, 3), (3, 5)])
        c.cache_bb()
        self.assertEqual(c.bb, p.BB(2, 2, 4, 5))

        s = p.Space()
        b = p.Body(1, 2)
        c = p.Poly(b, [(2, 2), (4, 3), (3, 5)])
        s.add(b, c)
        self.assertEqual(c.bb, p.BB(2, 2, 4, 5))

    def test_radius(self) -> None:
        c = p.Poly(None, [(2, 2), (4, 3), (3, 5)], radius=10)
        self.assertEqual(c.radius, 10)

    def test_radius_unsafe(self) -> None:
        c = p.Poly(None, [(2, 2), (4, 3), (3, 5)], radius=10)

        c.unsafe_set_radius(20)

        self.assertEqual(c.radius, 20)

    def test_create_box(self) -> None:
        c = p.Poly.create_box(None, (4, 2), 3)
        self.assertEqual(c.get_vertices(), [(2, -1), (2, 1), (-2, 1), (-2, -1)])

        c = p.Poly.create_box_bb(None, p.BB(1, 2, 3, 4), 3)
        self.assertEqual(c.get_vertices(), [(3, 2), (3, 4), (1, 4), (1, 2)])

    def test_pickle(self) -> None:
        c = p.Poly(None, [(1, 2), (3, 4), (5, 6)], radius=5)

        s = pickle.dumps(c)
        c2 = pickle.loads(s)

        self.assertEqual(c.get_vertices(), c2.get_vertices())
        self.assertEqual(c.radius, c2.radius)
