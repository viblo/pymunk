# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2023 Victor Blomqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------

"""
Pymunk is a easy-to-use pythonic 2d physics library that can be used whenever
you need 2d rigid body physics from Python.

Homepage: http://www.pymunk.org

This is the main containing module of Pymunk. It contains among other things
the very central Space, Body and Shape classes.

"""

__docformat__ = "reStructuredText"


__all__ = [
    "version",
    "chipmunk_version",
    "Space",
    "Body",
    "Shape",
    "Circle",
    "Poly",
    "Segment",
    "moment_for_circle",
    "moment_for_poly",
    "moment_for_segment",
    "moment_for_box",
    "SegmentQueryInfo",
    "ContactPoint",
    "ContactPointSet",
    "Arbiter",
    "CollisionHandler",
    "BB",
    "ShapeFilter",
    "Transform",
    "PointQueryInfo",
    "ShapeQueryInfo",
    "SpaceDebugDrawOptions",
    "Vec2d",
]

from typing import Sequence, Tuple, cast

from . import _chipmunk_cffi

cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
# logging.basicConfig(level=0)

from . import _version
from .arbiter import Arbiter
from .bb import BB
from .body import Body
from .collision_handler import CollisionHandler
from .constraints import *
from .contact_point_set import ContactPoint, ContactPointSet
from .query_info import PointQueryInfo, SegmentQueryInfo, ShapeQueryInfo
from .shape_filter import ShapeFilter
from .shapes import Circle, Poly, Segment, Shape
from .space import Space
from .space_debug_draw_options import SpaceDebugDrawOptions
from .transform import Transform
from .vec2d import Vec2d

version: str = _version.version
"""The release version of this pymunk installation.
Valid only if pymunk was installed from a source or binary
distribution (i.e. not in a checked-out copy from git).
"""

chipmunk_version: str = _version.chipmunk_version
"""The Chipmunk version used with this Pymunk version.

This property does not show a valid value in the compiled documentation, only
when you actually import pymunk and do pymunk.chipmunk_version

The string is in the following format:
<cpVersionString>R<github commit of chipmunk>
where cpVersionString is a version string set by Chipmunk and the git commit
hash corresponds to the git hash of the chipmunk source from
github.com/viblo/Chipmunk2D included with Pymunk.
"""


def moment_for_circle(
    mass: float,
    inner_radius: float,
    outer_radius: float,
    offset: Tuple[float, float] = (0, 0),
) -> float:
    """Calculate the moment of inertia for a hollow circle

    (A solid circle has an inner radius of 0)
    """
    assert len(offset) == 2

    return cp.cpMomentForCircle(mass, inner_radius, outer_radius, offset)


def moment_for_segment(
    mass: float, a: Tuple[float, float], b: Tuple[float, float], radius: float
) -> float:
    """Calculate the moment of inertia for a line segment

    The endpoints a and b are relative to the body
    """
    assert len(a) == 2
    assert len(b) == 2

    return cp.cpMomentForSegment(mass, a, b, radius)


def moment_for_box(mass: float, size: Tuple[float, float]) -> float:
    """Calculate the moment of inertia for a solid box centered on the body.

    size should be a tuple of (width, height)
    """
    assert len(size) == 2
    return cp.cpMomentForBox(mass, size[0], size[1])


def moment_for_poly(
    mass: float,
    vertices: Sequence[Tuple[float, float]],
    offset: Tuple[float, float] = (0, 0),
    radius: float = 0,
) -> float:
    """Calculate the moment of inertia for a solid polygon shape.

    Assumes the polygon center of gravity is at its centroid. The offset is
    added to each vertex.
    """
    assert len(offset) == 2
    vs = list(vertices)
    return cp.cpMomentForPoly(mass, len(vs), vs, offset, radius)


def area_for_circle(inner_radius: float, outer_radius: float) -> float:
    """Area of a hollow circle."""
    return cast(float, cp.cpAreaForCircle(inner_radius, outer_radius))


def area_for_segment(
    a: Tuple[float, float], b: Tuple[float, float], radius: float
) -> float:
    """Area of a beveled segment.

    (Will always be zero if radius is zero)
    """
    assert len(a) == 2
    assert len(b) == 2

    return cp.cpAreaForSegment(a, b, radius)


def area_for_poly(vertices: Sequence[Tuple[float, float]], radius: float = 0) -> float:
    """Signed area of a polygon shape.

    Returns a negative number for polygons with a clockwise winding.
    """
    vs = list(vertices)
    return cp.cpAreaForPoly(len(vs), vs, radius)


# del cp, ct, u
