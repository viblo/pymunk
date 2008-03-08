"""Contains utility functions, mainly to help with polygon creation"""
__docformat__ = "reStructuredText"

from vec2d import vec2d
from functools import partial

def is_clockwise(points): 
    """
    Check if the points given forms a clockwise polygon
    
    :return: True if the points forms a clockwise polygon
    """
    a = 0
    i,j = 0,0
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
    # TODO: cast is not a good idea.. use something else
    #return int((p1.x - p0.x)*(p2.y-p0.y) - (p2.x-p0.x)*(p1.y-p0.y))
    sorting = (p1.x - p0.x)*(p2.y-p0.y) - (p2.x-p0.x)*(p1.y-p0.y)
    if sorting > 0: return 1
    elif sorting < 0: return -1 
    else: return 0
    
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
    tot_x, tot_y = 0,0
    for p in points:
        tot_x += p[0]
        tot_y += p[1]
    n = len(points)
    return (tot_x/n, tot_y/n)
    
def poly_vectors_around_center(vec2d_pointlist):
    """Change polygon vectors around the center
    
    :return: pointlist ([vec2d, vec2d, vec2d, ...])
    """
    
    poly_points_center = []
    center = cx, cy = calc_center(vec2d_pointlist)
    	
    for p in vec2d_pointlist:
        x = p.x - cx
        y = p.y - cy
        poly_points_center.append(vec2d((x, y)))
        
    return poly_points_center	
