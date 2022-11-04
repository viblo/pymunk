import unittest
from io import StringIO
from unittest.mock import patch

import pymunk


class UnitTestSpaceDebugDrawOptions(unittest.TestCase):
    def testTransform(self) -> None:
        options = pymunk.SpaceDebugDrawOptions()
        transform = pymunk.Transform.translation(2, 3).scaled(2)
        options.transform = transform
        self.assertEqual(options.transform, transform)

        space = pymunk.Space()
        body = pymunk.Body(1, 10)
        body.position = 4, 5
        space.add(
            body,
            pymunk.Circle(body, 2, offset=(-4, -5)),
            pymunk.Segment(body, (0, 0), (3, 4), 3),
            pymunk.Poly(body, [(5, 0), (5, 5), (7, 3)], None, 4),
        )

        with patch("sys.stdout", new=StringIO()) as out:
            space.debug_draw(options)
            actual = out.getvalue()

        self.assertEqual(
            actual,
            "draw_circle (Vec2d(2.0, 3.0), 0.0, 4.0, "
            "SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), "
            "SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))\n"
            "draw_fat_segment (Vec2d(10.0, 13.0), Vec2d(16.0, 21.0), 6.0, "
            "SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), "
            "SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))\n"
            "draw_polygon "
            "([Vec2d(20.0, 13.0), Vec2d(24.0, 19.0), Vec2d(20.0, 23.0)], 8.0, "
            "SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0), "
            "SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0))\n",
        )
