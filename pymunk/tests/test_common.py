import unittest
from typing import Any

import pymunk as p
from pymunk.vec2d import Vec2d

####################################################################


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
    def testManyBoxCrash(self) -> None:
        space = p.Space()
        size = 10
        for _ in [1, 2]:
            for _ in range(16):
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

        def remove_first(arbiter: p.Arbiter, space: p.Space, data: Any) -> None:
            first_shape = arbiter.shapes[0]
            if c1 in space.shapes:
                space.remove(c1)
            # space.add_post_step_callback(space.remove, first_shape, first_shape.body)
            space.remove(c1)

        space.add_collision_handler(2, 0).separate = remove_first

        space.step(1.0 / 60)
        b2.position = 22, 0
        space.step(1.0 / 60)


####################################################################
if __name__ == "__main__":
    print(f"testing pymunk version {p.version}")
    unittest.main()
