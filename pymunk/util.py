# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2024 Victor Blomqvist
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

"""This submodule contains utility functions, mainly to help with polygon
creation.

.. note:: this submodule is deprectade by the autogeometry submodule. Expect it 
to be removed in the next Pymunk release. 

"""
__docformat__ = "reStructuredText"

from math import sqrt

from .vec2d import Vec2d

X, Y = 0, 1

from functools import partial


def is_clockwise(points):
    """
    Check if the points given forms a clockwise polygon

    :return: True if the points forms a clockwise polygon
    """
    a = 0
    i, j = 0, 0
    for i in range(len(points)):
        j = i + 1
        if j == len(points):
            j = 0
        a += points[i][X] * points[j][Y] - points[i][Y] * points[j][X]
    return a <= 0  # or is it the other way around?


def is_left(p0, p1, p2):
    """Test if p2 is left, on or right of the (infinite) line (p0,p1).

    :return: > 0 for p2 left of the line through p0 and p1
        = 0 for p2 on the line
        < 0 for p2 right of the line
    """
    # cast the answer to an int so it can be used directly from sort()
    # cast is not a good idea.. use something else
    # return int((p1.x - p0.x)*(p2.y-p0.y) - (p2.x-p0.x)*(p1.y-p0.y))
    sorting = (p1[X] - p0[X]) * (p2[Y] - p0[Y]) - (p2[X] - p0[X]) * (p1[Y] - p0[Y])
    if sorting > 0:
        return 1
    elif sorting < 0:
        return -1
    else:
        return 0


def is_convex(points):
    """Test if a polygon (list of (x,y)) is convex or not

    :return: True if the polygon is convex, False otherwise
    """

    assert len(points) > 2, "need at least 3 points to form a polygon"

    p0 = points[0]
    p1 = points[1]
    p2 = points[2]
    xc, yc = 0, 0
    is_same_winding = is_left(p0, p1, p2)
    for p2 in points[2:] + [p0] + [p1]:
        if is_same_winding != is_left(p0, p1, p2):
            return False
        a = p1[X] - p0[X], p1[Y] - p0[Y]  # p1-p0
        b = p2[X] - p1[X], p2[Y] - p1[Y]  # p2-p1
        if sign(a[X]) != sign(b[X]):
            xc += 1
        if sign(a[Y]) != sign(b[Y]):
            yc += 1
        p0, p1 = p1, p2

    return xc <= 2 and yc <= 2


def sign(x):
    """Sign function.

    :return -1 if x < 0, else return 1
    """
    if x < 0:
        return -1
    else:
        return 1


def reduce_poly(points, tolerance=0.5):
    """Remove close points to simplify a polyline
    tolerance is the min distance between two points squared.

    :return: The reduced polygon as a list of (x,y)
    """

    assert len(points) > 0, "reduce_poly can not simplify an empty points list"

    curr_p = points[0]
    reduced_ps = [points[0]]

    for p in points[1:]:
        distance = (curr_p[X] - p[X]) ** 2 + (curr_p[Y] - p[Y]) ** 2
        if distance > tolerance:
            curr_p = p
            reduced_ps.append(p)

    return reduced_ps


def convex_hull(points):
    """Create a convex hull from a list of points.
    This function uses the Graham Scan Algorithm.

    :return: Convex hull as a list of (x,y)
    """

    assert len(points) > 2, "need at least 3 points to form a convex hull"

    ### Find lowest rightmost point
    p0 = points[0]
    for p in points[1:]:
        if p[Y] < p0[Y]:
            p0 = p
        elif p[Y] == p0[Y] and p[X] > p0[X]:
            p0 = p
    points.remove(p0)

    ### Sort the points angularly about p0 as center
    f = partial(is_left, p0)
    points.sort(key=_cmp_to_key(f))
    points.reverse()
    points.insert(0, p0)

    ### Find the hull points
    hull = [p0, points[1]]

    for p in points[2:]:
        pt1 = hull[-1]
        pt2 = hull[-2]
        l = is_left(pt2, pt1, p)
        if l > 0:
            hull.append(p)
        else:
            while l <= 0 and len(hull) > 2:
                hull.pop()
                pt1 = hull[-1]
                pt2 = hull[-2]
                l = is_left(pt2, pt1, p)
            hull.append(p)
    return hull


def calc_center(points):
    """Calculate the center of a polygon

    :return: The center (x,y)
    """

    # ref: http://en.wikipedia.org/wiki/Polygon

    assert len(points) > 0, "need at least 1 points to calculate the center"

    area = calc_area(points)

    p1 = points[0]
    cx = cy = 0
    for p2 in points[1:] + [points[0]]:
        tmp = p1[X] * p2[Y] - p2[X] * p1[Y]
        cx += (p1[X] + p2[X]) * tmp
        cy += (p1[Y] + p2[Y]) * tmp
        p1 = p2
    c = 1 / (6.0 * area) * cx, 1 / (6.0 * area) * cy
    return c


def poly_vectors_around_center(pointlist, points_as_Vec2d=True):
    """Rearranges vectors around the center
    If points_as_Vec2d, then return points are also Vec2d, else pos

    :return: pointlist ([Vec2d/pos, ...])
    """

    poly_points_center = []
    cx, cy = calc_center(pointlist)

    if points_as_Vec2d:
        for p in pointlist:
            x = p[X] - cx
            y = p[Y] - cy
            poly_points_center.append(Vec2d(x, y))

    else:
        for p in pointlist:
            x = p[X] - cx
            y = cy - p[Y]
            poly_points_center.append((x, y))

    return poly_points_center


def calc_area(points):
    """Calculate the area of a polygon

    :return: Area of polygon
    """

    # ref: http://en.wikipedia.org/wiki/Polygon

    if len(points) < 3:
        return 0

    p1 = points[0]
    a = 0
    for p2 in points[1:] + [points[0]]:
        a += p1[X] * p2[Y] - p2[X] * p1[Y]
        p1 = p2
    a = 0.5 * a

    return a


def calc_perimeter(points):
    """Calculate the perimeter of a polygon

    :return: Perimeter of polygon
    """

    if len(points) < 2:
        return 0

    p1 = points[0]
    c = 0
    for p2 in points[1:] + [points[0]]:
        c += sqrt((p2[X] - p1[X]) ** 2 + (p2[Y] - p1[Y]) ** 2)
        p1 = p2
    return c


### "hidden" functions


def _cmp_to_key(mycmp):
    "Convert a cmp= function into a key= function, useful for python 3"

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


def _is_corner(a, b, c):
    # returns if point b is an outer corner
    return not (is_clockwise([a, b, c]))


def _point_in_triangle(p, a, b, c):
    # measure area of whole triangle
    whole = abs(calc_area([a, b, c]))
    # measure areas of inner triangles formed by p
    parta = abs(calc_area([a, b, p]))
    partb = abs(calc_area([b, c, p]))
    partc = abs(calc_area([c, a, p]))
    # allow for potential rounding error in area calcs
    # (not that i've encountered one yet, but just in case...)
    thresh = 0.0000001
    # return if the sum of the inner areas = the whole area
    return (parta + partb + partc) < (whole + thresh)


def _get_ear(poly):
    count = len(poly)
    # not even a poly
    if count < 3:
        return [], []
    # only a triangle anyway
    if count == 3:
        return poly, []

    # start checking points
    for i in range(count):
        ia = (i - 1) % count
        ib = i
        ic = (i + 1) % count
        a = poly[ia]
        b = poly[ib]
        c = poly[ic]
        # is point b an outer corner?
        if _is_corner(a, b, c):
            # are there any other points inside triangle abc?
            valid = True
            for j in range(count):
                if not (j in (ia, ib, ic)):
                    p = poly[j]
                    if _point_in_triangle(p, a, b, c):
                        valid = False
            # if no such point found, abc must be an "ear"
            if valid:
                remaining = []
                for j in range(count):
                    if j != ib:
                        remaining.append(poly[j])
                # return the ear, and what's left of the polygon after the ear is clipped
                return [a, b, c], remaining

    # no ear was found, so something is wrong with the given poly (not anticlockwise? self-intersects?)
    return [], []


def _attempt_reduction(hulla, hullb):
    inter = [vec for vec in hulla if vec in hullb]
    if len(inter) == 2:
        starta = hulla.index(inter[1])
        tempa = hulla[starta:] + hulla[:starta]
        tempa = tempa[1:]
        startb = hullb.index(inter[0])
        tempb = hullb[startb:] + hullb[:startb]
        tempb = tempb[1:]
        reduced = tempa + tempb
        if is_convex(reduced):
            return reduced
    # reduction failed, return None
    return None


def _reduce_hulls(hulls):
    count = len(hulls)
    # 1 or less hulls passed
    if count < 2:
        return hulls, False

    # check all hulls in the list against each other
    for ia in range(count - 1):
        for ib in range(ia + 1, count):
            # see if hulls can be reduced to one
            reduction = _attempt_reduction(hulls[ia], hulls[ib])
            if reduction != None:
                # they can so return a new list of hulls and a True
                newhulls = [reduction]
                for j in range(count):
                    if not (j in (ia, ib)):
                        newhulls.append(hulls[j])
                return newhulls, True

    # nothing was reduced, send the original hull list back with a False
    return hulls, False


### major functions


def triangulate(poly):
    """Triangulates poly and returns a list of triangles

    :Parameters:
        poly
            list of points that form an anticlockwise polygon
            (self-intersecting polygons won't work, results are undefined)
    """
    triangles = []
    remaining = poly[:]
    # while the poly still needs clipping
    while len(remaining) > 2:
        # rotate the list:
        # this stops the starting point from getting stale which sometimes
        # a "fan" of polys, which often leads to poor convexisation
        remaining = remaining[1:] + remaining[:1]
        # clip the ear, store it
        ear, remaining = _get_ear(remaining)
        if ear != []:
            triangles.append(ear)
    # return stored triangles
    return triangles


def convexise(triangles):
    """Reduces a list of triangles (such as returned by triangulate()) to a
    non-optimum list of convex polygons

    :Parameters:
        triangles
            list of anticlockwise triangles (a list of three points) to reduce
    """
    # fun fact: convexise probably isn't a real word
    hulls = triangles[:]
    reduced = True
    # keep trying to reduce until it won't reduce any more
    while reduced:
        hulls, reduced = _reduce_hulls(hulls)
    # return reduced hull list
    return hulls


__all__ = [
    "is_clockwise",
    "reduce_poly",
    "convex_hull",
    "calc_area",
    "calc_center",
    "poly_vectors_around_center",
    "is_convex",
    "calc_perimeter",
    "triangulate",
    "convexise",
]
