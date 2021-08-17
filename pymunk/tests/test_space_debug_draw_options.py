import unittest
from io import StringIO
from unittest.mock import patch

import pymunk


class UnitTestSpaceDebugDrawOptions(unittest.TestCase):
    def f(self, transform, shape):
        options = pymunk.SpaceDebugDrawOptions()
        options.transform = transform
        s = pymunk.Space()
        shape.body = s.static_body
        s.add(shape)
        s.debug_draw(options)

    def testTransform(self):
        options = pymunk.SpaceDebugDrawOptions()
        options.transform = pymunk.Transform.rotation(1)
        self.assertEqual(options.transform, pymunk.Transform.rotation(1))

    def testTransformCircle(self) -> None:
        return
        options = pymunk.SpaceDebugDrawOptions()
        draw_args = [(2, 3), 1, 4, (5, 6, 7, 8), (9, 10, 11, 12), pymunk.ffi.NULL]
        with patch("sys.stdout", new=StringIO()) as out:
            options._options.drawCircle(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_circle (Vec2d(2.0, 3.0), 1.0, 4.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.scaling(2)
            options._options.drawCircle(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_circle (Vec2d(4.0, 6.0), 1.0, 8.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.translation(3, 5)
            options._options.drawCircle(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_circle (Vec2d(5.0, 8.0), 1.0, 4.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

    def testTransformSegment(self) -> None:
        return
        options = pymunk.SpaceDebugDrawOptions()
        draw_args = [(2, 3), (4, 5), (5, 6, 7, 8), pymunk.ffi.NULL]
        with patch("sys.stdout", new=StringIO()) as out:
            options._options.drawSegment(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_segment (Vec2d(2.0, 3.0), "
                "Vec2d(4.0, 5.0), "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.scaling(2)
            options._options.drawSegment(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_segment (Vec2d(4.0, 6.0), "
                "Vec2d(8.0, 10.0), "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.translation(3, 5)
            options._options.drawSegment(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_segment (Vec2d(5.0, 8.0), "
                "Vec2d(7.0, 10.0), "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0))\n",
            )

    def testTransformFatSegment(self) -> None:
        return
        options = pymunk.SpaceDebugDrawOptions()
        draw_args = [(2, 3), (4, 5), 1, (5, 6, 7, 8), (9, 10, 11, 12), pymunk.ffi.NULL]
        with patch("sys.stdout", new=StringIO()) as out:
            options._options.drawFatSegment(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_fat_segment (Vec2d(2.0, 3.0), Vec2d(4.0, 5.0), 1.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.scaling(2)
            options._options.drawFatSegment(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_fat_segment (Vec2d(4.0, 6.0), Vec2d(8.0, 10.0), 2.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.translation(3, 5)
            options._options.drawFatSegment(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_fat_segment (Vec2d(5.0, 8.0), Vec2d(7.0, 10.0), 1.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

    def testTransformPolygon(self) -> None:
        return
        options = pymunk.SpaceDebugDrawOptions()
        draw_args = [
            3,
            [(2, 3), (4, 5), (3, 6)],
            1,
            (5, 6, 7, 8),
            (9, 10, 11, 12),
            pymunk.ffi.NULL,
        ]
        with patch("sys.stdout", new=StringIO()) as out:
            options._options.drawPolygon(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_polygon ([Vec2d(2.0, 3.0), Vec2d(4.0, 5.0), Vec2d(3.0, 6.0)], "
                "1.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.scaling(2)
            options._options.drawPolygon(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_polygon ([Vec2d(4.0, 6.0), Vec2d(8.0, 10.0), Vec2d(6.0, 12.0)], "
                "2.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.translation(3, 5)
            options._options.drawPolygon(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_polygon ([Vec2d(5.0, 8.0), Vec2d(7.0, 10.0), Vec2d(6.0, 11.0)], "
                "1.0, "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0), "
                "SpaceDebugColor(r=9.0, g=10.0, b=11.0, a=12.0))\n",
            )

    def testTransformDot(self) -> None:
        return
        options = pymunk.SpaceDebugDrawOptions()
        draw_args = [1, (2, 3), (5, 6, 7, 8), pymunk.ffi.NULL]
        with patch("sys.stdout", new=StringIO()) as out:
            options._options.drawDot(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_dot (1.0, Vec2d(2.0, 3.0), "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.scaling(2)
            options._options.drawDot(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_dot (1.0, Vec2d(4.0, 6.0), "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0))\n",
            )

        with patch("sys.stdout", new=StringIO()) as out:
            options.transform = pymunk.Transform.translation(3, 5)
            options._options.drawDot(*draw_args)

            self.assertEqual(
                out.getvalue(),
                "draw_dot (1.0, Vec2d(5.0, 8.0), "
                "SpaceDebugColor(r=5.0, g=6.0, b=7.0, a=8.0))\n",
            )
