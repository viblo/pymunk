__docformat__ = "reStructuredText"

from collections import namedtuple

from .vec2d import Vec2d
from ._base import *

class ContactPoint(
    namedtuple('ContactPoint', ['point_a', 'point_b', 'distance'])):
    """Contains information about a contact point. 
    
    point_a and point_b are the contact position on the surface of each shape.
    
    distance is the penetration distance of the two shapes. Overlapping 
    means it will be negative. This value is calculated as 
    dot(point2 - point1), normal) and is ignored when you set the 
    Arbiter.contact_point_set.
    """
    
    __slots__ = ()

class ContactPointSet(
    namedtuple('ContactPointSet', ['normal', 'points'])):
    """Contact point sets make getting contact information simpler.
    
    normal is the normal of the collision
    
    points is the array of contact points. Can be at most 2 points.
    """
    
    __slots__ = ()
    
    def __repr__(self):
        points = []
        i = 0
        for i in range(self.count):
            points.append(self.points[i])
        points = ",".join([p.__repr__() for p in points])
        return 'ContactPointSet(%s, %s, [%s])' % (self.count, self.normal, points)
