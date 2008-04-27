"""Contains utility functions, mainly to help with polygon creation"""
__docformat__ = "reStructuredText"

from vec2d import Vec2d
from functools import partial

from math import fabs, sqrt

X, Y = 0, 1 

def is_clockwise(points): 
    """
    Check if the points given forms a clockwise polygon
    
    :return: True if the points forms a clockwise polygon
    """
    a = 0
    i, j = 0, 0
    for i in range(len(points)):
        j = i + 1
        if j == len(points): j = 0
        a += points[i].x*points[j].y - points[i].y*points[j].x
    return a <= 0 #or is it the other way around?
    
def is_left(p0, p1, p2):
    """Test if p2 is left, on or right of the (infinite) line (p0,p1).
    
    :return: > 0 for p2 left of the line through p0 and p1
        = 0 for p2 on the line
        < 0 for p2 right of the line
    """
    # cast the answer to an int so it can be used directly from sort()
    # cast is not a good idea.. use something else
    #return int((p1.x - p0.x)*(p2.y-p0.y) - (p2.x-p0.x)*(p1.y-p0.y))
    sorting = (p1[X] - p0[X])*(p2[Y]-p0[Y]) - (p2[X]-p0[X])*(p1[Y]-p0[Y])
    if sorting > 0: return 1
    elif sorting < 0: return -1 
    else: return 0

def is_convex(points):
    """Test if a polygon (list of (x,y)) is convex or not
    
    :return: True if the polygon is convex, False otherwise
    """
    assert len(points) > 2, "not enough points to form a polygon"
    p0 = points[0]
    p1 = points[1]
    p2 = points[2]
    xc, yc = 0, 0
    is_same_winding = is_left(p0, p1, p2)
    for p2 in points[2:] + [p0] + [p1]:
        if is_same_winding != is_left(p0, p1, p2): 
            return False
        a = p1[X] - p0[X], p1[Y] - p0[Y] # p1-p0
        b = p2[X] - p1[X], p2[Y] - p1[Y] # p2-p1
        if sign(a[X]) != sign(b[X]): xc +=1
        if sign(a[Y]) != sign(b[Y]): yc +=1
        p0, p1 = p1, p2
   
    return xc <= 2 and yc <= 2

def sign(x): 
    """Sign function. 
    
    :return -1 if x < 0, else return 1
    """
    if x < 0: return -1 
    else: return 1
                
def reduce_poly(points, tolerance=500):
    """Remove close points to simplify a polyline
    tolerance is the min distance between two points squared.
    
    :return: The reduced polygon as a list of (x,y)
    """
    curr_p = points[0]
    reduced_ps = [points[0]]
    
    for p in points[1:]:
        if curr_p.get_dist_sqrd(p) > tolerance:
            curr_p = p
            reduced_ps.append(p)
            
    return reduced_ps
        
def convex_hull(points):
    """Create a convex hull from a list of points.
    This function uses the Graham Scan Algorithm.
    
    :return: Convex hull as a list of (x,y)
    """
    ### Find lowest rightmost point
    p0 = points[0]
    for p in points[1:]:
        if p.y < p0.y:
            p0 = p
        elif p.y == p0.y and p.x > p0.x:
            p0 = p
    points.remove(p0)
    
    ### Sort the points angularly about p0 as center
    f = partial(is_left, p0)
    points.sort(cmp = f)
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
    tot_x, tot_y = 0, 0
    for p in points:
        tot_x += p[0]
        tot_y += p[1]
    n = len(points)
    return (tot_x/n, tot_y/n)
    
def poly_vectors_around_center(pointlist, points_as_Vec2d=True):
    """Rearranges vectors around the center
    If points_as_Vec2d, then return points are also Vec2d, else pos
    
    :return: pointlist ([Vec2d/pos, ...])
    """
    
    poly_points_center = []
    cx, cy = calc_center(pointlist)

    if points_as_Vec2d:
        for p in pointlist:
            x = p.x - cx
            y = p.y - cy
            poly_points_center.append(Vec2d((x, y)))

    else:
        for p in pointlist:
            x = p[0] - cx
            y = cy - p[1]
            poly_points_center.append((x, y))
    
    return poly_points_center

def get_poly_UA(pointlist, points_as_Vec2d=True):
    """Calculates the circumference and area of a given polygon

    :return: int(U), int(A)    
    """
    p1 = p2 = None
    U = 0
    A = 0
    for p in pointlist:
        if p1 == None:
            p1 = p
            
        else:
            p2 = p
            
            # Extract x and y
            if points_as_Vec2d:
                x1, y1 = p1.x, p1.y
                x2, y2 = p2.x, p2.y
            else:    
                x1, y1 = p1
                x2, y2 = p2

            # Get distance between the two Points
            dx = fabs(x2 - x1)
            dy = fabs(y2 - y1)
            
            # U += c = sqrt(a^2+b^2) | A += (a*b)/2
            U += sqrt((dx*dx) + (dy*dy))
            A += ((dx*dy)/2)

            # Current End Point becomes Next Start Point
            p1 = p2
    
    return int(U), int(A)
    
__all__ = ["is_clockwise", "is_left", "reduce_poly", "convex_hull",
        "calc_center", "poly_vectors_around_center", "get_poly_UA", "is_convex"]
