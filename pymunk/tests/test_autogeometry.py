import unittest
from typing import Any
from unittest.mock import patch

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
    def _assert_result_released(
        self, operation: str, allocator: str, conversion_error: bool
    ) -> None:
        native = a.lib
        allocated: list[Any] = []
        freed: list[Any] = []
        is_set = operation == "convex_decomposition"
        free_name = "cpPolylineSetFree" if is_set else "cpPolylineFree"
        points: list[tuple[float, float]] = [
            (0, 0),
            (4, 0),
            (4, 4),
            (2, 2),
            (0, 4),
            (0, 0),
        ]
        original = points.copy()

        def allocate(*args: Any) -> Any:
            result = getattr(native, allocator)(*args)
            allocated.append(result)
            return result

        def free(ptr: Any, *args: Any) -> None:
            # Only native results belong to these free functions. In particular,
            # the input allocated by ffi.new must not be freed here.
            self.assertIn(ptr, allocated)
            self.assertNotIn(ptr, freed)
            if is_set:
                self.assertEqual(args, (True,))
            getattr(native, free_name)(ptr, *args)
            freed.append(ptr)

        try:
            with patch.object(a, "lib", wraps=native) as calls:
                getattr(calls, allocator).side_effect = allocate
                getattr(calls, free_name).side_effect = free
                if conversion_error:
                    # Fail after one point has already been copied.
                    count = 0

                    def convert(x: float, y: float) -> Vec2d:
                        nonlocal count
                        count += 1
                        if count == 2:
                            raise ValueError("conversion interrupted")
                        return Vec2d(x, y)

                    with patch.object(a, "Vec2d", side_effect=convert):
                        with self.assertRaisesRegex(
                            ValueError, "conversion interrupted"
                        ):
                            getattr(a, operation)(points, 0.1)
                else:
                    actual = getattr(a, operation)(points, 0.1)
                    self.assertEqual(points, original)
                    self.assertIsInstance(actual[0][0] if is_set else actual[0], Vec2d)
                self.assertEqual(len(allocated), 1)
                self.assertEqual(freed, allocated)
        finally:
            # Original implementations leak their results. Keep the regression
            # test itself leak-free even when its ownership assertion fails.
            for ptr in allocated:
                if ptr not in freed:
                    if is_set:
                        getattr(native, free_name)(ptr, True)
                    else:
                        getattr(native, free_name)(ptr)

    def test_result_allocations_are_released(self) -> None:
        operations = (
            ("simplify_curves", "cpPolylineSimplifyCurves"),
            ("simplify_vertexes", "cpPolylineSimplifyVertexes"),
            ("to_convex_hull", "cpPolylineToConvexHull"),
            ("convex_decomposition", "cpPolylineConvexDecomposition"),
        )
        for operation, allocator in operations:
            for conversion_error in (False, True):
                with self.subTest(
                    operation=operation, conversion_error=conversion_error
                ):
                    self._assert_result_released(operation, allocator, conversion_error)

    def test_is_closed(self) -> None:
        not_closed: list[tuple[float, float]] = [(0, 0), (1, 1), (0, 1)]
        closed: list[tuple[float, float]] = [(0, 0), (1, 1), (0, 1), (0, 0)]
        self.assertFalse(a.is_closed(not_closed))
        self.assertTrue(a.is_closed(closed))

    def test_simplify_curves(self) -> None:
        p1: list[tuple[float, float]] = [(0, 0), (0, 10), (5, 11), (10, 10), (0, 10)]
        expected = [(0, 0), (0, 10), (10, 10), (0, 10)]
        actual = a.simplify_curves(p1, 1)
        self.assertEqual(actual, expected)

    def test_simplify_vertexes(self) -> None:
        p1: list[tuple[float, float]] = [(0, 0), (0, 10), (5, 11), (10, 10), (0, 10)]
        expected = [(0, 0), (0, 10), (10, 10), (0, 10)]
        actual = a.simplify_vertexes(p1, 1)
        self.assertEqual(actual, expected)

    def test_to_convex_hull(self) -> None:
        p1: list[tuple[float, float]] = [(0, 0), (0, 10), (5, 5), (10, 10), (10, 0)]
        expected = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        actual = a.to_convex_hull(p1, 1)
        self.assertEqual(actual, expected)

    def test_convex_decomposition(self) -> None:
        # TODO: Use a more complicated polygon as test case
        p1: list[tuple[float, float]] = [
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

        open_poly: list[tuple[float, float]] = [(0, 0), (10, 0), (10, 10)]
        with self.assertRaises(Exception):
            a.convex_decomposition(open_poly, 0.1)

        wrong_winding: list[tuple[float, float]] = [(0, 0), (10, 10), (10, 0), (0, 0)]
        with self.assertRaises(Exception):
            a.convex_decomposition(wrong_winding, 0.1)

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

        def sample_func(point: tuple[float, float]) -> float:
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

        def sample_func(point: tuple[float, float]) -> float:
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
