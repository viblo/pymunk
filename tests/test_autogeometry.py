from pymunk.vec2d import Vec2d
import pymunk.auto_geometry as a

import unittest


class UnitTestAutoGeometry(unittest.TestCase):
    def test_is_closed(self):
        
        self.assertFalse(a.is_closed([(0,0), (1,1), (0,1)]))
        self.assertTrue(a.is_closed([(0,0), (1,1), (0,1), (0,0)]))