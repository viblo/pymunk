import gc
import unittest
import weakref
from typing import Any

import pymunk as p
from pymunk._weakkeysview import WeakKeysView
from pymunk.vec2d import Vec2d


class UnitTestGeneral(unittest.TestCase):
    def testGeneral(self) -> None:
        p.version
        p.chipmunk_version

    def testMomentHelpers(self) -> None:
        m = p.moment_for_circle(1, 2, 3, (1, 2))
        self.assertAlmostEqual(m, 11.5)

        m = p.moment_for_segment(1, (-10, 0), (10, 0), 1)
        self.assertAlmostEqual(m, 40.6666666666)

        m = p.moment_for_poly(1, [(0, 0), (10, 10), (10, 0)], (1, 2), 3)
        self.assertAlmostEqual(m, 98.3333333333)

        m = p.moment_for_box(1, (2, 3))
        self.assertAlmostEqual(m, 1.08333333333)

    def testAreaHelpers(self) -> None:
        a = p.area_for_circle(1, 2)
        self.assertAlmostEqual(a, 9.4247779607)

        a = p.area_for_segment((-10, 0), (10, 0), 3)
        self.assertAlmostEqual(a, 148.27433388)

        a = p.area_for_poly([(0, 0), (10, 10), (10, 0)], 3)
        self.assertAlmostEqual(a, 80.700740753)


class UnitTestBugs(unittest.TestCase):
    def testGC(self) -> None:

        import gc
        import logging

        _logger = logging.getLogger(__name__)

        def make() -> list[Any]:
            s = p.Space()
            b1 = p.Body(1, 2)
            c1 = p.Circle(b1, 2)
            c2 = p.Circle(b1, 2)
            b2 = p.Body(1, 2)
            c3 = p.Circle(b2, 2)
            s.add(b1, c1, c2, b2, c3)
            s.step(1)
            return [s, b1, c1, c2, b2, c3]

        import itertools

        for order in itertools.permutations(range(6)):
            objs = make()
            _logger.debug("Order: %s", order)
            for i in order:
                o = objs[i]
                if o is p.Space:
                    del o._space
                if o is p.Circle:
                    del o._shape
                if o is p.Body:
                    del o._body
            gc.collect()

    def testManyBoxCrash(self) -> None:
        space = p.Space()
        for x in [1, 2]:
            for y in range(16):
                size = 10
                box_points = [
                    Vec2d(*p)
                    for p in [
                        (-size, -size),
                        (-size, size),
                        (size, size),
                        (size, -size),
                    ]
                ]
                body = p.Body(10, 20)
                shape = p.Poly(body, box_points)
                space.add(body, shape)
            space.step(1 / 50.0)

    def testNoStaticShape(self) -> None:
        space = p.Space()

        b1 = p.Body(1, float("inf"))
        c1 = p.Circle(b1, 10)
        c1.name = "c1"
        c1.collision_type = 2

        b2 = p.Body(1, float("inf"))
        c2 = p.Circle(b2, 10)
        c2.name = "c2"

        b3 = p.Body(1, float("inf"))
        c3 = p.Circle(b3, 10)
        c3.name = "c3"

        b1.position = 0, 0
        b2.position = 9, 0
        b3.position = -9, 0

        space.add(b1, c1, b2, c2, b3, c3)
        # print("\nc1", c1)

        def remove_first(arbiter: p.Arbiter, space: p.Space, data: Any) -> None:
            # print("SEP 1", arbiter.shapes)
            # print("  space.shapes", space.shapes)
            # print("  space._remove_later", space._remove_later)
            first_shape = arbiter.shapes[0]
            if c1 in space.shapes:
                space.remove(c1)
            #     print("  space.shapes", space.shapes)
            #     print("  space._remove_later", space._remove_later)
            # print("SEP done")
            # space.add_post_step_callback(space.remove, first_shape, first_shape.body)
            # space.remove(c1)

        space.on_collision(2, 0, separate=remove_first)
        # print(1)
        space.step(1.0 / 60)
        # print(2)
        b2.position = 22, 0
        space.step(1.0 / 60)
        # print(3)

    def testX(self) -> None:
        space = p.Space()

        b1 = p.Body(1, 1)
        c1 = p.Circle(b1, 10)
        c1.collision_type = 2

        b2 = p.Body(1, 2)
        c2 = p.Circle(b2, 10)

        b3 = p.Body(1, 3)
        c3 = p.Circle(b3, 10)

        # b1.position = 0, 0
        # b2.position = 9, 0
        # b3.position = -9, 0

        space.add(b1, c1, b2, c2, b3, c3)
        # print("\nc1", c1)

        def separate(arbiter: p.Arbiter, space: p.Space, data: Any) -> None:
            # print("SEP 1", arbiter.shapes)
            # print("  space.shapes", space.shapes)
            # print("  space._remove_later", space._remove_later)
            if c1 in space.shapes:
                space.remove(c1)
            #     print("  space.shapes", space.shapes)
            #     print("  space._remove_later", space._remove_later)
            # print("SEP done")
            # space.add_post_step_callback(space.remove, first_shape, first_shape.body)
            # space.remove(c1)

        space.on_collision(2, 0, separate=separate)
        # print(1)
        space.step(1)
        # print(2)
        b2.position = 22, 0
        space.step(1)
        # print(3)

    def testWeakKeysView(self) -> None:
        x1, x2, x3 = p.Body(1), p.Body(2), p.Body(3)

        d: weakref.WeakKeyDictionary[p.Body, int] = weakref.WeakKeyDictionary()

        d[x1] = 1
        d[x2] = 2

        keys1 = WeakKeysView(d)
        keys2 = WeakKeysView(d)

        del x2
        d[x3] = 3

        iterations = 0
        for x in keys2:
            iterations += 1
            del x3
            gc.collect()

        self.assertEqual(iterations, 1)
        gc.collect()

        self.assertEqual(len(d), 1)
        self.assertEqual(list(keys1), [x1])
        self.assertEqual(list(keys2), [x1])
        self.assertEqual(list(d.keys()), [x1])
