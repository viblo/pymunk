import unittest
from typing import List, Tuple

import pymunk.autogeometry as a
from pymunk.bb import BB
from pymunk.vec2d import Vec2d


class UnitTestPolylineSet(unittest.TestCase):
    def test_collect_segment(self) -> None:
        pset = a.PolylineSet()

        pset.collect_segment((0, 0), (5, 5))
        pset.collect_segment((5, 5), (10, 10))

        pset.collect_segment((2, 5), (2, 10))

        expected = [
            [Vec2d(0.0, 0.0), Vec2d(5.0, 5.0), Vec2d(10.0, 10.0)],
            [Vec2d(2.0, 5.0), Vec2d(2.0, 10.0)],
        ]

        self.assertEqual(len(pset), 2)
        self.assertEqual(list(pset), expected)


class UnitTestAutoGeometry(unittest.TestCase):
    def test_is_closed(self) -> None:
        not_closed: List[Tuple[float, float]] = [(0, 0), (1, 1), (0, 1)]
        closed: List[Tuple[float, float]] = [(0, 0), (1, 1), (0, 1), (0, 0)]
        self.assertFalse(a.is_closed(not_closed))
        self.assertTrue(a.is_closed(closed))

    def test_simplify_curves(self) -> None:
        p1: List[Tuple[float, float]] = [(0, 0), (0, 10), (5, 11), (10, 10), (0, 10)]
        expected = [(0, 0), (0, 10), (10, 10), (0, 10)]
        actual = a.simplify_curves(p1, 1)
        self.assertEqual(actual, expected)

    def test_simplify_vertexes(self) -> None:
        p1: List[Tuple[float, float]] = [(0, 0), (0, 10), (5, 11), (10, 10), (0, 10)]
        expected = [(0, 0), (0, 10), (10, 10), (0, 10)]
        actual = a.simplify_vertexes(p1, 1)
        self.assertEqual(actual, expected)

    def test_to_convex_hull(self) -> None:
        p1: List[Tuple[float, float]] = [(0, 0), (0, 10), (5, 5), (10, 10), (10, 0)]
        expected = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        actual = a.to_convex_hull(p1, 1)
        self.assertEqual(actual, expected)

    def test_convex_decomposition(self) -> None:
        # TODO: Use a more complicated polygon as test case
        p1: List[Tuple[float, float]] = [
            (0, 0),
            (5, 0),
            (10, 10),
            (20, 20),
            (5, 5),
            (0, 10),
            (0, 0),
        ]
        expected = [
            [(5.0, 5.0), (6.25, 2.5), (20.0, 20.0), (5.0, 5.0)],
            [(0.0, 0.0), (5.0, 0.0), (6.25, 2.5), (5.0, 5.0), (0.0, 10.0), (0.0, 0.0)],
        ]

        actual = a.convex_decomposition(p1, 0.1)
        actual.sort(key=len)

        # TODO: The result of convex_decomposition is not stable between
        # environments, so we cant have this assert here.
        # self.assertEqual(actual, expected)

    def test_march_soft(self) -> None:
        img = [
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xxxxx",
            "  xxxxx",
        ]

        def sample_func(point: Tuple[float, float]) -> float:
            x = int(point[0])
            y = int(point[1])
            if img[y][x] == "x":
                return 1
            return 0

        pl_set = a.march_soft(BB(0, 0, 6, 6), 7, 7, 0.5, sample_func)

        expected = [
            [
                (1.5, 6.0),
                (1.5, 5.0),
                (1.5, 4.0),
                (1.5, 3.0),
                (1.5, 2.0),
                (1.5, 1.0),
                (1.5, 0.0),
            ],
            [
                (3.5, 0.0),
                (3.5, 1.0),
                (3.5, 2.0),
                (3.5, 3.0),
                (3.5, 4.0),
                (4.0, 4.5),
                (5.0, 4.5),
                (6.0, 4.5),
            ],
        ]
        self.assertEqual(list(pl_set), expected)

    def test_march_hard(self) -> None:
        img = [
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xxxxx",
            "  xxxxx",
        ]

        def sample_func(point: Tuple[float, float]) -> float:
            x = int(point[0])
            y = int(point[1])
            if img[y][x] == "x":
                return 1
            return 0

        actual = list(a.march_hard(BB(0, 0, 6, 6), 7, 7, 0.5, sample_func))

        expected = [
            [
                (1.5, 6.0),
                (1.5, 5.0),
                (1.5, 4.0),
                (1.5, 3.0),
                (1.5, 2.0),
                (1.5, 1.0),
                (1.5, 0.0),
            ],
            [
                (3.5, 0.0),
                (3.5, 1.0),
                (3.5, 2.0),
                (3.5, 3.0),
                (3.5, 4.0),
                (3.5, 4.5),
                (4.0, 4.5),
                (5.0, 4.5),
                (6.0, 4.5),
            ],
        ]
        self.assertEqual(actual, expected)
