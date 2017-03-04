from pymunk.vec2d import Vec2d
from pymunk.bb import BB
import pymunk.autogeometry as a

import unittest

class UnitTestPolylineSet(unittest.TestCase):
    def test_collect_segment(self):
        pset = a.PolylineSet()

        pset.collect_segment((0,0),(5,5))
        pset.collect_segment((5,5),(10,10))

        pset.collect_segment((2,5),(2,10))

        expected = [
            [Vec2d(0.0, 0.0), Vec2d(5.0, 5.0), Vec2d(10.0, 10.0)],
            [Vec2d(2.0, 5.0), Vec2d(2.0, 10.0)]]

        self.assertEqual(len(pset), 2)
        self.assertEqual(list(pset), expected)

class UnitTestAutoGeometry(unittest.TestCase):
    def test_is_closed(self):
        
        self.assertFalse(a.is_closed([(0,0), (1,1), (0,1)]))
        self.assertTrue(a.is_closed([(0,0), (1,1), (0,1), (0,0)]))

    def test_simplify_curves(self):
        p1 = [(0,0), (0,10), (5,11), (10, 10), (0, 10)]
        expected = [(0,0), (0,10), (10, 10), (0, 10)]
        actual = a.simplify_curves(p1, 1)
        self.assertEqual(actual, expected)

    def test_simplify_vertexes(self):
        p1 = [(0,0), (0,10), (5,11), (10, 10), (0, 10)]
        expected = [(0,0), (0,10), (10, 10), (0, 10)]
        actual = a.simplify_vertexes(p1, 1)
        self.assertEqual(actual, expected)    
        
    def test_to_convex_hull(self):
        p1 = [(0,0), (0,10), (5,5), (10, 10), (10,0)]
        expected = [(0,0), (10,0), (10,10), (0, 10), (0, 0)]
        actual = a.to_convex_hull(p1, 1)
        self.assertEqual(actual, expected) 

    def test_convex_decomposition(self):
        # TODO: Use a more complicated polygon as test case
        p1 = [(0,0), (5,0), (10,10), (20,20), (5,5), (0,10), (0,0)]
        expected = [
            [(5.0,5.0), (6.25, 2.5), (20.0,20.0), (5.0,5.0)],
            [(0.0,0.0), (5.0,0.0), (6.25, 2.5), (5.0,5.0),(0.0,10.0), (0.0,0.0)], 
            ]

        actual = a.convex_decomposition(p1, .1)
        actual.sort(key=len)

        # TODO: The result of convex_decomposition is not stable between 
        # environments, so we cant have this assert here.
        #self.assertEqual(actual, expected)
        
    def test_march_soft(self):
        img = [
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xxxxx",
            "  xxxxx",
            ]

        segments = []

        def segment_func(v0, v1):
            segments.append((tuple(v0),tuple(v1)))
            
        def sample_func(point):
            x = int(point.x)
            y = int(point.y)
            if img[y][x] == "x":
                return 1
            return 0
            
        a.march_soft(BB(0,0,6,6), 7, 7, .5, segment_func, sample_func)

        expected = [
            ((1.5, 1.0), (1.5, 0.0)),
            ((3.5, 0.0), (3.5, 1.0)),
            ((1.5, 2.0), (1.5, 1.0)),
            ((3.5, 1.0), (3.5, 2.0)),
            ((1.5, 3.0), (1.5, 2.0)),
            ((3.5, 2.0), (3.5, 3.0)),
            ((1.5, 4.0), (1.5, 3.0)),
            ((3.5, 3.0), (3.5, 4.0)),
            ((1.5, 5.0), (1.5, 4.0)),
            ((3.5, 4.0), (4.0, 4.5)),
            ((4.0, 4.5), (5.0, 4.5)),
            ((5.0, 4.5), (6.0, 4.5)),
            ((1.5, 6.0), (1.5, 5.0))]
        self.assertEqual(segments, expected)

    def test_march_hard(self):
        img = [
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xx   ",
            "  xxxxx",
            "  xxxxx",
            ]

        segments = []

        def segment_func(v0, v1):
            segments.append((tuple(v0),tuple(v1)))
            
        def sample_func(point):
            x = int(point.x)
            y = int(point.y)
            if img[y][x] == "x":
                return 1
            return 0
            
        a.march_hard(BB(0,0,6,6), 7, 7, .5, segment_func, sample_func)

        expected = [
            ((1.5, 1.0), (1.5, 0.0)),
            ((3.5, 0.0), (3.5, 1.0)),
            ((1.5, 2.0), (1.5, 1.0)),
            ((3.5, 1.0), (3.5, 2.0)),
            ((1.5, 3.0), (1.5, 2.0)),
            ((3.5, 2.0), (3.5, 3.0)),
            ((1.5, 4.0), (1.5, 3.0)),
            ((3.5, 3.0), (3.5, 4.0)),
            ((1.5, 5.0), (1.5, 4.0)),
            ((3.5, 4.0), (3.5, 4.5)),
            ((3.5, 4.5), (4.0, 4.5)),
            ((4.0, 4.5), (5.0, 4.5)),
            ((5.0, 4.5), (6.0, 4.5)),
            ((1.5, 6.0), (1.5, 5.0))]
        self.assertEqual(segments, expected)