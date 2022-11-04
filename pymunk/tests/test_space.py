from __future__ import with_statement

import copy
import io
import pickle
import sys
import unittest
import warnings
from typing import Any, Callable, Sequence, cast

import pymunk as p
from pymunk import *
from pymunk.constraints import *
from pymunk.vec2d import Vec2d


class UnitTestSpace(unittest.TestCase):
    def _setUp(self) -> None:
        self.s = p.Space()

        self.b1, self.b2 = p.Body(1, 3), p.Body(10, 100)
        self.s.add(self.b1, self.b2)
        self.b1.position = 10, 0
        self.b2.position = 20, 0

        self.s1, self.s2 = p.Circle(self.b1, 5), p.Circle(self.b2, 10)
        self.s.add(self.s1, self.s2)
        pass

    def _tearDown(self) -> None:
        del self.s
        del self.b1, self.b2
        del self.s1, self.s2
        pass

    def testProperties(self) -> None:
        s = p.Space()

        self.assertEqual(s.iterations, 10)
        s.iterations = 15
        self.assertEqual(s.iterations, 15)

        self.assertEqual(s.gravity, (0, 0))
        s.gravity = Vec2d(10, 2)
        self.assertEqual(s.gravity, (10, 2))
        self.assertEqual(s.gravity.x, 10)

        self.assertEqual(s.damping, 1)
        s.damping = 3
        self.assertEqual(s.damping, 3)

        self.assertEqual(s.idle_speed_threshold, 0)
        s.idle_speed_threshold = 4
        self.assertEqual(s.idle_speed_threshold, 4)

        self.assertEqual(str(s.sleep_time_threshold), "inf")
        s.sleep_time_threshold = 5
        self.assertEqual(s.sleep_time_threshold, 5)

        self.assertAlmostEqual(s.collision_slop, 0.1)
        s.collision_slop = 6
        self.assertEqual(s.collision_slop, 6)

        self.assertAlmostEqual(s.collision_bias, 0.0017970074436)
        s.collision_bias = 0.2
        self.assertEqual(s.collision_bias, 0.2)

        self.assertEqual(s.collision_persistence, 3)
        s.collision_persistence = 9
        self.assertEqual(s.collision_persistence, 9)

        self.assertEqual(s.current_time_step, 0)
        s.step(0.1)
        self.assertEqual(s.current_time_step, 0.1)

        self.assertTrue(s.static_body != None)
        self.assertEqual(s.static_body.body_type, p.Body.STATIC)

        self.assertEqual(s.threads, 1)
        s.threads = 2
        self.assertEqual(s.threads, 1)

    def testThreaded(self) -> None:
        s = p.Space(threaded=True)
        s.step(1)
        s.threads = 2
        import platform

        if platform.system() == "Windows":
            self.assertEqual(s.threads, 1)
        else:
            self.assertEqual(s.threads, 2)
        s.step(1)

    def testSpatialHash(self) -> None:
        s = p.Space()
        s.use_spatial_hash(10, 100)
        s.step(1)
        s.add(p.Body(1, 2))
        s.step(1)

    def testAddRemove(self) -> None:
        s = p.Space()

        self.assertEqual(s.bodies, [])
        self.assertEqual(s.shapes, [])

        b = p.Body(1, 2)
        s.add(b)
        self.assertEqual(s.bodies, [b])
        self.assertEqual(s.shapes, [])

        c1 = p.Circle(b, 10)
        s.add(c1)
        self.assertEqual(s.bodies, [b])
        self.assertEqual(s.shapes, [c1])

        c2 = p.Circle(b, 15)
        s.add(c2)
        self.assertEqual(len(s.shapes), 2)
        self.assertTrue(c1 in s.shapes)
        self.assertTrue(c2 in s.shapes)

        s.remove(c1)
        self.assertEqual(s.shapes, [c2])

        s.remove(c2, b)
        self.assertEqual(s.bodies, [])
        self.assertEqual(s.shapes, [])

        # note that shape is before the body, which is something to test
        s.add(c2, b)
        self.assertEqual(s.bodies, [b])
        self.assertEqual(s.shapes, [c2])

    def testAddRemoveInStep(self) -> None:
        s = p.Space()

        b1 = p.Body(1, 2)
        c1 = p.Circle(b1, 2)

        b2 = p.Body(1, 2)
        c2 = p.Circle(b2, 2)

        s.add(b1, b2, c1, c2)

        b = p.Body(1, 2)
        c = p.Circle(b, 2)

        def pre_solve_add(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            space.add(b, c)
            space.add(c, b)
            self.assertTrue(b not in s.bodies)
            self.assertTrue(c not in s.shapes)
            return True

        def pre_solve_remove(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            space.remove(b, c)
            space.remove(c, b)
            self.assertTrue(b in s.bodies)
            self.assertTrue(c in s.shapes)
            return True

        s.add_collision_handler(0, 0).pre_solve = pre_solve_add

        s.step(0.1)
        return
        self.assertTrue(b in s.bodies)
        self.assertTrue(c in s.shapes)

        s.add_collision_handler(0, 0).pre_solve = pre_solve_remove

        s.step(0.1)

        self.assertTrue(b not in s.bodies)
        self.assertTrue(c not in s.shapes)

    def testRemoveInStep(self) -> None:
        self._setUp()
        s = self.s

        def pre_solve(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            space.remove(*arb.shapes)
            return True

        s.add_collision_handler(0, 0).pre_solve = pre_solve

        s.step(0.1)

        self.assertTrue(self.s1 not in s.shapes)
        self.assertTrue(self.s2 not in s.shapes)
        self._tearDown()

    def testAddShapeAsserts(self) -> None:
        s1 = p.Space()
        s2 = p.Space()
        c1 = p.Circle(s1.static_body, 10)
        s1.add(c1)

        self.assertRaises(AssertionError, s1.add, c1)
        self.assertRaises(AssertionError, s2.add, c1)

        c2 = p.Circle(None, 10)

        self.assertRaises(AssertionError, s1.add, c2)

        b = p.Body(1, 2)
        c3 = p.Circle(b, 10)

        self.assertRaises(AssertionError, s1.add, c3)

    def testAddBodyAsserts(self) -> None:
        s1 = p.Space()
        s2 = p.Space()
        c1 = p.Circle(s1.static_body, 10)

        s1.add(c1)

        self.assertRaises(AssertionError, s1.add, c1)
        self.assertRaises(AssertionError, s2.add, c1)

    def testAddConstraintAsserts(self) -> None:
        s1 = p.Space()
        b1 = p.Body(1, 2)
        b2 = p.Body(1, 2)
        c1 = p.PinJoint(b1, b2, (20, 0), (-20, 0))

        s1.add(c1)

        self.assertRaises(AssertionError, s1.add, c1)

    def testPointQueryNearestWithShapeFilter(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        s1 = p.Circle(b1, 10)
        s.add(b1, s1)

        tests = [
            {"c1": 0b00, "m1": 0b00, "c2": 0b00, "m2": 0b00, "hit": 0},
            {"c1": 0b01, "m1": 0b01, "c2": 0b01, "m2": 0b01, "hit": 1},
            {"c1": 0b10, "m1": 0b01, "c2": 0b01, "m2": 0b10, "hit": 1},
            {"c1": 0b01, "m1": 0b01, "c2": 0b11, "m2": 0b11, "hit": 1},
            {"c1": 0b11, "m1": 0b00, "c2": 0b11, "m2": 0b00, "hit": 0},
            {"c1": 0b00, "m1": 0b11, "c2": 0b00, "m2": 0b11, "hit": 0},
            {"c1": 0b01, "m1": 0b10, "c2": 0b10, "m2": 0b00, "hit": 0},
            {"c1": 0b01, "m1": 0b10, "c2": 0b10, "m2": 0b10, "hit": 0},
            {"c1": 0b01, "m1": 0b10, "c2": 0b10, "m2": 0b01, "hit": 1},
            {"c1": 0b01, "m1": 0b11, "c2": 0b00, "m2": 0b10, "hit": 0},
        ]

        for test in tests:
            f1 = p.ShapeFilter(categories=test["c1"], mask=test["m1"])
            f2 = p.ShapeFilter(categories=test["c2"], mask=test["m2"])
            s1.filter = f1
            hit = s.point_query_nearest((0, 0), 0, f2)
            self.assertEqual(
                hit != None,
                test["hit"],
                "Got {}!=None, expected {} for test: {}".format(hit, test["hit"], test),
            )

    def testPointQuery(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        b1.position = 19, 0
        s1 = p.Circle(b1, 10)
        s.add(b1, s1)

        b2 = p.Body(1, 1)
        b2.position = 0, 0
        s2 = p.Circle(b2, 10)
        s.add(b2, s2)
        s1.filter = p.ShapeFilter(categories=0b10, mask=0b01)
        hits = s.point_query((23, 0), 0, p.ShapeFilter(categories=0b01, mask=0b10))

        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].shape, s1)
        self.assertEqual(hits[0].point, (29, 0))
        self.assertEqual(hits[0].distance, -6)
        self.assertEqual(hits[0].gradient, (1, 0))

        hits = s.point_query((30, 0), 0, p.ShapeFilter())
        self.assertEqual(len(hits), 0)

        hits = s.point_query((30, 0), 30, p.ShapeFilter())
        self.assertEqual(len(hits), 2)
        self.assertEqual(hits[0].shape, s2)
        self.assertEqual(hits[0].point, (10, 0))
        self.assertEqual(hits[0].distance, 20)
        self.assertEqual(hits[0].gradient, (1, 0))

        self.assertEqual(hits[1].shape, s1)
        self.assertEqual(hits[1].point, (29, 0))
        self.assertEqual(hits[1].distance, 1)
        self.assertEqual(hits[1].gradient, (1, 0))

    def testPointQuerySensor(self) -> None:
        s = p.Space()
        c = p.Circle(s.static_body, 10)
        c.sensor = True
        s.add(c)
        hits = s.point_query((0, 0), 100, p.ShapeFilter())
        self.assertEqual(len(hits), 1)

    def testPointQueryNearest(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        b1.position = 19, 0
        s1 = p.Circle(b1, 10)
        s.add(b1, s1)

        hit = s.point_query_nearest((23, 0), 0, p.ShapeFilter())
        assert hit is not None
        self.assertEqual(hit.shape, s1)
        self.assertEqual(hit.point, (29, 0))
        self.assertEqual(hit.distance, -6)
        self.assertEqual(hit.gradient, (1, 0))

        hit = s.point_query_nearest((30, 0), 0, p.ShapeFilter())
        self.assertEqual(hit, None)

        hit = s.point_query_nearest((30, 0), 10, p.ShapeFilter())
        assert hit is not None
        self.assertEqual(hit.shape, s1)
        self.assertEqual(hit.point, (29, 0))
        self.assertEqual(hit.distance, 1)
        self.assertEqual(hit.gradient, (1, 0))

    def testPointQueryNearestSensor(self) -> None:
        s = p.Space()
        c = p.Circle(s.static_body, 10)
        c.sensor = True
        s.add(c)
        hit = s.point_query_nearest((0, 0), 100, p.ShapeFilter())
        self.assertEqual(hit, None)

    def testBBQuery(self) -> None:
        s = p.Space()

        b1 = p.Body(1, 1)
        b1.position = 19, 0
        s1 = p.Circle(b1, 10)
        s.add(b1, s1)

        b2 = p.Body(1, 1)
        b2.position = 0, 0
        s2 = p.Circle(b2, 10)
        s.add(b2, s2)

        bb = p.BB(-7, -7, 7, 7)
        hits = s.bb_query(bb, p.ShapeFilter())
        self.assertEqual(len(hits), 1)
        self.assertTrue(s2 in hits)
        self.assertTrue(s1 not in hits)

    def testBBQuerySensor(self) -> None:
        s = p.Space()
        c = p.Circle(s.static_body, 10)
        c.sensor = True
        s.add(c)
        hits = s.bb_query(p.BB(0, 0, 10, 10), p.ShapeFilter())
        self.assertEqual(len(hits), 1)

    def testShapeQuery(self) -> None:
        self._setUp()
        b = p.Body(body_type=p.Body.KINEMATIC)
        s = p.Circle(b, 2)
        b.position = 20, 1

        hits = self.s.shape_query(s)

        self.assertEqual(len(hits), 1)
        self.assertEqual(self.s2, hits[0].shape)
        self._tearDown()

    def testShapeQuerySensor(self) -> None:
        s = p.Space()
        c = p.Circle(s.static_body, 10)
        c.sensor = True
        s.add(c)
        hits = s.shape_query(p.Circle(None, 200))
        self.assertEqual(len(hits), 1)

    def testStaticPointQueries(self) -> None:
        self._setUp()
        b = p.Body(body_type=p.Body.KINEMATIC)
        c = p.Circle(b, 10)
        b.position = -50, -50

        self.s.add(b, c)

        hit = self.s.point_query_nearest((-50, -55), 0, p.ShapeFilter())
        assert hit is not None
        self.assertEqual(hit.shape, c)

        hits = self.s.point_query((-50, -55), 0, p.ShapeFilter())
        self.assertEqual(hits[0].shape, c)
        self._tearDown()

    def testReindexShape(self) -> None:
        s = p.Space()

        b = p.Body(body_type=p.Body.KINEMATIC)
        c = p.Circle(b, 10)

        s.add(b, c)

        b.position = -50, -50
        hit = s.point_query_nearest((-50, -55), 0, p.ShapeFilter())
        self.assertEqual(hit, None)
        s.reindex_shape(c)
        hit = s.point_query_nearest((-50, -55), 0, p.ShapeFilter())
        assert hit is not None
        self.assertEqual(hit.shape, c)

    def testReindexShapesForBody(self) -> None:
        s = p.Space()
        b = p.Body(body_type=p.Body.STATIC)
        c = p.Circle(b, 10)

        s.add(b, c)

        b.position = -50, -50
        hit = s.point_query_nearest((-50, -55), 0, p.ShapeFilter())
        self.assertEqual(hit, None)
        s.reindex_shapes_for_body(b)

        hit = s.point_query_nearest((-50, -55), 0, p.ShapeFilter())
        assert hit is not None
        self.assertEqual(hit.shape, c)

    def testReindexStatic(self) -> None:
        s = p.Space()
        b = p.Body(body_type=p.Body.STATIC)
        c = p.Circle(b, 10)

        s.add(b, c)

        b.position = -50, -50
        hit = s.point_query_nearest((-50, -55), 0, p.ShapeFilter())
        self.assertEqual(hit, None)
        s.reindex_static()
        hit = s.point_query_nearest((-50, -55), 0, p.ShapeFilter())
        assert hit is not None
        self.assertEqual(hit.shape, c)

    def testReindexStaticCollision(self) -> None:
        s = p.Space()
        b1 = p.Body(10, 1000)
        c1 = p.Circle(b1, 10)
        b1.position = Vec2d(20, 20)

        b2 = p.Body(body_type=p.Body.STATIC)
        s2 = p.Segment(b2, (-10, 0), (10, 0), 1)

        s.add(b1, c1)
        s.add(b2, s2)

        s2.unsafe_set_endpoints((-10, 0), (100, 0))
        s.gravity = 0, -100

        for _ in range(10):
            s.step(0.1)

        self.assertTrue(b1.position.y < 0)

        b1.position = Vec2d(20, 20)
        b1.velocity = 0, 0
        s.reindex_static()

        for _ in range(10):
            s.step(0.1)

        self.assertTrue(b1.position.y > 10)

    def testSegmentQuery(self) -> None:
        s = p.Space()

        b1 = p.Body(1, 1)
        b1.position = 19, 0
        s1 = p.Circle(b1, 10)
        s.add(b1, s1)

        b2 = p.Body(1, 1)
        b2.position = 0, 0
        s2 = p.Circle(b2, 10)
        s.add(b2, s2)

        hits = s.segment_query((-13, 0), (131, 0), 0, p.ShapeFilter())

        self.assertEqual(len(hits), 2)
        self.assertEqual(hits[0].shape, s2)
        self.assertEqual(hits[0].point, (-10, 0))
        self.assertEqual(hits[0].normal, (-1, 0))
        self.assertAlmostEqual(hits[0].alpha, 0.0208333333333)

        self.assertEqual(hits[1].shape, s1)
        self.assertEqual(hits[1].point, (9, 0))
        self.assertEqual(hits[1].normal, (-1, 0))
        self.assertAlmostEqual(hits[1].alpha, 0.1527777777777)

        hits = s.segment_query((-13, 50), (131, 50), 0, p.ShapeFilter())
        self.assertEqual(len(hits), 0)

    def testSegmentQuerySensor(self) -> None:
        s = p.Space()
        c = p.Circle(s.static_body, 10)
        c.sensor = True
        s.add(c)
        hits = s.segment_query((-20, 0), (20, 0), 1, p.ShapeFilter())
        self.assertEqual(len(hits), 1)

    def testSegmentQueryFirst(self) -> None:
        s = p.Space()

        b1 = p.Body(1, 1)
        b1.position = 19, 0
        s1 = p.Circle(b1, 10)
        s.add(b1, s1)

        b2 = p.Body(1, 1)
        b2.position = 0, 0
        s2 = p.Circle(b2, 10)
        s.add(b2, s2)

        hit = s.segment_query_first((-13, 0), (131, 0), 0, p.ShapeFilter())

        assert hit is not None
        self.assertEqual(hit.shape, s2)
        self.assertEqual(hit.point, (-10, 0))
        self.assertEqual(hit.normal, (-1, 0))
        self.assertAlmostEqual(hit.alpha, 0.0208333333333)

        hit = s.segment_query_first((-13, 50), (131, 50), 0, p.ShapeFilter())
        self.assertEqual(hit, None)

    def testSegmentQueryFirstSensor(self) -> None:
        s = p.Space()
        c = p.Circle(s.static_body, 10)
        c.sensor = True
        s.add(c)
        hit = s.segment_query_first((-20, 0), (20, 0), 1, p.ShapeFilter())
        self.assertIsNone(hit)

    def testStaticSegmentQueries(self) -> None:
        self._setUp()
        b = p.Body(body_type=p.Body.KINEMATIC)
        c = p.Circle(b, 10)
        b.position = -50, -50

        self.s.add(b, c)

        hit = self.s.segment_query_first((-70, -50), (-30, -50), 0, p.ShapeFilter())
        assert hit is not None
        self.assertEqual(hit.shape, c)
        hits = self.s.segment_query((-70, -50), (-30, -50), 0, p.ShapeFilter())
        self.assertEqual(hits[0].shape, c)
        self._tearDown()

    def testCollisionHandlerBegin(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        b2 = p.Body(1, 1)
        c2 = p.Circle(b2, 10)
        s.add(b1, c1, b2, c2)

        self.hits = 0

        def begin(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            self.hits += h.data["test"]
            return True

        h = s.add_collision_handler(0, 0)
        h.data["test"] = 1
        h.begin = begin

        for x in range(10):
            s.step(0.1)

        self.assertEqual(self.hits, 1)

    def testCollisionHandlerBeginNoReturn(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        b2 = p.Body(1, 1)
        c2 = p.Circle(b2, 10)
        s.add(b1, c1, b2, c2)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            def begin(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
                return  # type: ignore

            s.add_collision_handler(0, 0).begin = begin
            s.step(0.1)

            assert w is not None
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

    def testCollisionHandlerPreSolve(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        c1.collision_type = 1
        b2 = p.Body(1, 1)
        c2 = p.Circle(b2, 10)
        s.add(b1, c1, b2, c2)

        d = {}

        def pre_solve(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            d["shapes"] = arb.shapes
            d["space"] = space  # type: ignore
            d["test"] = data["test"]
            return True

        h = s.add_collision_handler(0, 1)
        h.data["test"] = 1
        h.pre_solve = pre_solve
        s.step(0.1)
        self.assertEqual(c1, d["shapes"][1])
        self.assertEqual(c2, d["shapes"][0])
        self.assertEqual(s, d["space"])
        self.assertEqual(1, d["test"])

    def testCollisionHandlerPreSolveNoReturn(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        b2 = p.Body(1, 1)
        c2 = p.Circle(b2, 10)
        s.add(b1, c1, b2, c2)

        def pre_solve(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            return  # type: ignore

        s.add_collision_handler(0, 0).pre_solve = pre_solve

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            s.step(0.1)
            assert w is not None
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

    def testCollisionHandlerPostSolve(self) -> None:
        self._setUp()
        self.hit = 0

        def post_solve(arb: p.Arbiter, space: p.Space, data: Any) -> None:
            self.hit += 1

        self.s.add_collision_handler(0, 0).post_solve = post_solve
        self.s.step(0.1)
        self.assertEqual(self.hit, 1)
        self._tearDown()

    def testCollisionHandlerSeparate(self) -> None:
        s = p.Space()

        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        b1.position = 9, 11

        b2 = p.Body(body_type=p.Body.STATIC)
        c2 = p.Circle(b2, 10)
        b2.position = 0, 0

        s.add(b1, c1, b2, c2)
        s.gravity = 0, -100

        self.separated = False

        def separate(arb: p.Arbiter, space: p.Space, data: Any) -> None:
            self.separated = data["test"]

        h = s.add_collision_handler(0, 0)
        h.data["test"] = True
        h.separate = separate

        for x in range(10):
            s.step(0.1)

        self.assertTrue(self.separated)

    def testCollisionHandlerRemoveSeparateAdd(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 10)
        c1 = p.Circle(b1, 10)
        c2 = p.Circle(s.static_body, 5)

        s.add(b1, c1, c2)

        def separate(*_: Any) -> None:
            s.add(p.Circle(s.static_body, 2))
            s.remove(c1)

        s.add_default_collision_handler().separate = separate

        s.step(1)
        s.remove(c1)

    def testCollisionHandlerKeyOrder(self) -> None:
        s = p.Space()
        h1 = s.add_collision_handler(1, 2)
        h2 = s.add_collision_handler(2, 1)

        self.assertEqual(h1, h2)

    def testWildcardCollisionHandler(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        b2 = p.Body(1, 1)
        c2 = p.Circle(b2, 10)
        s.add(b1, c1, b2, c2)

        d = {}

        def pre_solve(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            d["shapes"] = arb.shapes
            d["space"] = space  # type: ignore
            return True

        s.add_wildcard_collision_handler(1).pre_solve = pre_solve
        s.step(0.1)

        self.assertEqual({}, d)

        c1.collision_type = 1
        s.step(0.1)

        self.assertEqual(c1, d["shapes"][0])
        self.assertEqual(c2, d["shapes"][1])
        self.assertEqual(s, d["space"])

    def testDefaultCollisionHandler(self) -> None:
        s = p.Space()
        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        c1.collision_type = 1
        b2 = p.Body(1, 1)
        c2 = p.Circle(b2, 10)
        c2.collision_type = 2
        s.add(b1, c1, b2, c2)

        d = {}

        def pre_solve(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            d["shapes"] = arb.shapes
            d["space"] = space  # type: ignore
            return True

        s.add_default_collision_handler().pre_solve = pre_solve
        s.step(0.1)

        self.assertEqual(c1, d["shapes"][1])
        self.assertEqual(c2, d["shapes"][0])
        self.assertEqual(s, d["space"])

    def testPostStepCallback(self) -> None:
        s = p.Space()
        b1, b2 = p.Body(1, 3), p.Body(10, 100)
        s.add(b1, b2)
        b1.position = 10, 0
        b2.position = 20, 0
        s1, s2 = p.Circle(b1, 5), p.Circle(b2, 10)
        s.add(s1, s2)

        self.calls = 0

        def callback(
            space: p.Space,
            key: Any,
            shapes: Sequence[Shape],
            test_self: "UnitTestSpace",
        ) -> None:
            for shape in shapes:
                s.remove(shape)
            test_self.calls += 1

        def pre_solve(arb: p.Arbiter, space: p.Space, data: Any) -> bool:
            # note that we dont pass on the whole arbiters object, instead
            # we take only the shapes.
            space.add_post_step_callback(callback, 0, arb.shapes, test_self=self)
            return True

        ch = s.add_collision_handler(0, 0).pre_solve = pre_solve

        s.step(0.1)
        self.assertEqual([], s.shapes)
        self.assertEqual(self.calls, 1)

        s.step(0.1)

        self.assertEqual(self.calls, 1)

    def testDebugDraw(self) -> None:
        s = p.Space()

        b1 = p.Body(1, 3)
        s1 = p.Circle(b1, 5)
        s.add(b1, s1)
        s.step(1)
        o = p.SpaceDebugDrawOptions()

        new_out = io.StringIO()
        sys.stdout = new_out
        try:
            s.debug_draw(o)
        finally:
            sys.stdout = sys.__stdout__

        msg = (
            "draw_circle (Vec2d(0.0, 0.0), 0.0, 5.0, "
            "SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), "
            "SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))\n"
        )
        self.assertEqual(msg, new_out.getvalue())

    @unittest.skip(
        "Different behavior on windows sometimes. Expect it to be fixed in next major python version"
    )
    def testDebugDrawZeroLengthSpring(self) -> None:
        if sys.version_info < (3, 0):
            return
        s = p.Space()

        b1 = p.Body(1, 3)
        c = DampedSpring(b1, s.static_body, (0, 0), (0, 0), 0, 10, 1)
        s.add(b1, c)

        s.step(1)
        o = p.SpaceDebugDrawOptions()

        new_out = io.StringIO()
        sys.stdout = new_out
        try:
            s.debug_draw(o)
        finally:
            sys.stdout = sys.__stdout__

        expected = (
            "draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0))\n"
            "draw_dot (5.0, Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0)) \n"
            "draw_segment (Vec2d(0.0, 0.0), Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0))\n"
            "draw_segment (Vec2d(0.0, 0.0), Vec2d(0.0, 0.0), SpaceDebugColor(r=142.0, g=68.0, b=173.0, a=255.0))\n"
        )

        actual = new_out.getvalue()
        try:
            self.assertEqual(expected, actual)
        except:
            print("\nExpected", expected)
            print("\nActual", actual)
            raise

    def testPicklePymunkVersionCheck(self) -> None:
        pickle_string = b"\x80\x04\x95\xc5\x01\x00\x00\x00\x00\x00\x00\x8c\x0cpymunk.space\x94\x8c\x05Space\x94\x93\x94)\x81\x94}\x94(\x8c\x04init\x94]\x94\x8c\x08threaded\x94\x89\x86\x94a\x8c\x07general\x94]\x94(\x8c\niterations\x94K\n\x86\x94\x8c\x07gravity\x94\x8c\x0cpymunk.vec2d\x94\x8c\x05Vec2d\x94\x93\x94G\x00\x00\x00\x00\x00\x00\x00\x00G\x00\x00\x00\x00\x00\x00\x00\x00\x86\x94R\x94\x86\x94\x8c\x07damping\x94G?\xf0\x00\x00\x00\x00\x00\x00\x86\x94\x8c\x14idle_speed_threshold\x94G\x00\x00\x00\x00\x00\x00\x00\x00\x86\x94\x8c\x14sleep_time_threshold\x94G\x7f\xf0\x00\x00\x00\x00\x00\x00\x86\x94\x8c\x0ecollision_slop\x94G?\xb9\x99\x99\xa0\x00\x00\x00\x86\x94\x8c\x0ecollision_bias\x94G?]q2\x0c\xdfCc\x86\x94\x8c\x15collision_persistence\x94K\x03\x86\x94\x8c\x07threads\x94K\x01\x86\x94e\x8c\x06custom\x94]\x94h\x07\x89\x86\x94a\x8c\x07special\x94]\x94(\x8c\x0epymunk_version\x94\x8c\x050.0.1\x94\x86\x94\x8c\x06bodies\x94]\x94\x86\x94\x8c\x06shapes\x94]\x94\x86\x94\x8c\x0bconstraints\x94]\x94\x86\x94\x8c\t_handlers\x94]\x94\x86\x94eub."

        with self.assertRaisesRegex(
            AssertionError,
            r"Pymunk version [0-9.]+ of pickled object does not match current Pymunk version [0-9.]+",
        ):
            pickle.loads(pickle_string)

    def testCopyMethods(self) -> None:
        self._testCopyMethod(lambda x: cast(Space, pickle.loads(pickle.dumps(x))))
        self._testCopyMethod(lambda x: copy.deepcopy(x))
        self._testCopyMethod(lambda x: x.copy())

    def _testCopyMethod(self, copy_func: Callable[[Space], Space]) -> None:
        s = p.Space(threaded=True)
        s.iterations = 2
        s.gravity = 3, 4
        s.damping = 5
        s.idle_speed_threshold = 6
        s.sleep_time_threshold = 7
        s.collision_slop = 8
        s.collision_bias = 9
        s.collision_persistence = 10
        s.threads = 2

        b1 = p.Body(1, 2)
        b2 = p.Body(3, 4)
        b3 = p.Body(5, 6)
        c1 = p.Circle(b1, 7)
        c2 = p.Circle(b1, 8)
        c3 = p.Circle(b2, 9)
        c4 = p.Circle(s.static_body, 10)
        s.add(b1, b2, b3, c1, c2, c3, c4)
        s.static_body.custom = "x"

        j1 = PinJoint(b1, b2)
        j2 = PinJoint(s.static_body, b2)
        s.add(j1, j2)

        h = s.add_default_collision_handler()
        h.begin = f1

        h = s.add_wildcard_collision_handler(1)
        h.pre_solve = f1

        h = s.add_collision_handler(1, 2)
        h.post_solve = f1

        h = s.add_collision_handler(3, 4)
        h.separate = f1

        s2 = copy_func(s)

        # Assert properties
        self.assertEqual(s.threaded, s2.threaded)
        self.assertEqual(s.iterations, s2.iterations)
        self.assertEqual(s.gravity, s2.gravity)
        self.assertEqual(s.damping, s2.damping)
        self.assertEqual(s.idle_speed_threshold, s2.idle_speed_threshold)
        self.assertEqual(s.sleep_time_threshold, s2.sleep_time_threshold)
        self.assertEqual(s.collision_slop, s2.collision_slop)
        self.assertEqual(s.collision_bias, s2.collision_bias)
        self.assertEqual(s.collision_persistence, s2.collision_persistence)
        self.assertEqual(s.threads, s2.threads)

        # Assert shapes, bodies and constriants
        self.assertEqual([c.radius for c in s2.shapes], [7, 8, 9, 10])
        self.assertEqual([b.mass for b in s2.bodies], [1, 3, 5])
        self.assertEqual(s.static_body.custom, s2.static_body.custom)
        ja = [j.a for j in s2.constraints]
        self.assertIn(s2.static_body, ja)

        # Assert collision handlers
        h2 = s2.add_default_collision_handler()
        self.assertIsNotNone(h2.begin)
        self.assertIsNone(h2.pre_solve)
        self.assertIsNone(h2.post_solve)
        self.assertIsNone(h2.separate)

        h2 = s2.add_wildcard_collision_handler(1)
        self.assertIsNone(h2.begin)
        self.assertIsNotNone(h2.pre_solve)
        self.assertIsNone(h2.post_solve)
        self.assertIsNone(h2.separate)

        h2 = s2.add_collision_handler(1, 2)
        self.assertIsNone(h2.begin)
        self.assertIsNone(h2.pre_solve)
        self.assertIsNotNone(h2.post_solve)
        self.assertIsNone(h2.separate)

        h2 = s2.add_collision_handler(3, 4)
        self.assertIsNone(h2.begin)
        self.assertIsNone(h2.pre_solve)
        self.assertIsNone(h2.post_solve)
        self.assertIsNotNone(h2.separate)


def f1(*args: Any, **kwargs: Any) -> None:
    pass
