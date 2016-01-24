__docformat__ = "reStructuredText"

from ctypes import *
from .vec2d import Vec2d
from ._base import *

class ContactPoint(Structure):
    """Contains information about a contact point. 
    
    pointA and pointB are the contact position on the surface of each shape.
    
    distance is the penetration distance of the two shapes. Overlapping 
    means it will be negative. /// This value is calculated as 
    dot(point2 - point1), normal) and is ignored when you set the 
    Arbiter.contact_point_set.
    """
     
    __slots__ = ['pointA', 'pointB', 'distance']

    def __repr__(self):
        return 'ContactPoint(%s, %s, %s)' % (self.pointA, self.pointB, self.distance)
    
ContactPoint._fields_ = [
    ('pointA', Vec2d),
    ('pointB', Vec2d),
    ('distance', cpFloat)
]

class ContactPointSet(Structure):
    """Contact point sets make getting contact information simpler.
    
    count is the number of contact points in the set.
    
    normal is the normal of the collision
    
    points is the array of contact points. Can be at most 2 points.
    """
    
    __slots__ = ["count", "normal", "points"]
    
    def __repr__(self):
        points = []
        i = 0
        for i in range(self.count):
            points.append(self.points[i])
        points = ",".join([p.__repr__() for p in points])
        return 'ContactPointSet(%s, %s, [%s])' % (self.count, self.normal, points)

ContactPointSet._fields_ = [
    ('count', c_int),
    ('normal', Vec2d),
    ('points', ContactPoint * 2)
]
