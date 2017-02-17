# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2011 Victor Blomqvist
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

"""This module contain the Vec2d class that is used in all of pymunk when a 
vector is needed.

The Vec2d class is used almost everywhere in pymunk for 2d coordinates and 
vectors, for example to define gravity vector in a space. However, pymunk is 
smart enough to convert tuples or tuple like objects to Vec2ds so you usually 
do not need to explicitly do conversions if you happen to have a tuple::

    >>> import pymunk
    >>> space = pymunk.Space()
    >>> space.gravity
    Vec2d(0.0, 0.0)
    >>> space.gravity = 3,5
    >>> space.gravity
    Vec2d(3.0, 5.0)
    >>> space.gravity += 2,6
    >>> space.gravity
    Vec2d(5.0, 11.0)
    
More examples::

    >>> from pymunk.vec2d import Vec2d
    >>> Vec2d(7.3, 4.2)
    Vec2d(7.3, 4.2)
    >>> Vec2d((7.3, 4.2))
    Vec2d(7.3, 4.2)
    >>> Vec2d(7.3, 4.2) + Vec2d((1,2))
    Vec2d(8.3, 6.2)
    
"""
__docformat__ = "reStructuredText"

import operator
import math

__all__ = ["Vec2d"]

class Vec2d(object):
    """2d vector class, supports vector and scalar operators, and also 
    provides some high level functions.
    """
    __slots__ = ("x", "y")

    @staticmethod        
    def _fromcffi(p):
        """Used as a speedy way to create Vec2ds internally in pymunk."""
        v = Vec2d.__new__(Vec2d)
        v.x = p.x
        v.y = p.y
        return v 

    def __init__(self, x_or_pair=None, y = None):
        if x_or_pair != None:
            if y == None:
                if hasattr(x_or_pair, "x") and hasattr(x_or_pair, "y"):
                    self.x = x_or_pair.x
                    self.y = x_or_pair.y
                else:
                    self.x = x_or_pair[0]
                    self.y = x_or_pair[1]
            else:
                self.x = x_or_pair
                self.y = y
        else:
            self.x = 0
            self.y = 0

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        raise IndexError()

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __setitem__(self, i, value):
        if i == 0:
            self.x = value
        elif i == 1:
            self.y = value
        else:
            raise IndexError()
   
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
    
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
    
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True
 
    def __nonzero__(self):
        return self.x != 0.0 or self.y != 0.0
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))
 
    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__
    
    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__
    
    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.truediv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))
 
    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))
 
    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))
 
    def __invert__(self):
        return Vec2d(-self.x, -self.y)
 
    
   
 
    # vectory functions
    def get_length_sqrd(self): 
        """Get the squared length of the vector.
        It is more efficent to use this method instead of first call 
        get_length() or access .length and then do a sqrt().
        
        :return: The squared length
        """
        return self.x**2 + self.y**2
 
    def get_length(self):
        """Get the length of the vector.
        
        :return: The length
        """
        return math.sqrt(self.x**2 + self.y**2)    
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, 
        doc = """Gets or sets the magnitude of the vector""")
       
    def rotate(self, angle_radians):
        """Rotate the vector by angle_radians radians."""
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotated(self, angle_radians):
        """Create and return a new vector by rotating this vector by 
        angle_radians radians.
        
        :return: Rotated vector
        """
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)
    
    def rotate_degrees(self, angle_degrees):
        """Rotate the vector by angle_degrees degrees."""
        self.rotate(math.radians(angle_degrees))
    
    def rotated_degrees(self, angle_degrees):
        """Create and return a new vector by rotating this vector by 
        angle_degrees degrees.
        
        :return: Rotade vector
        """
        return self.rotated(math.radians(angle_degrees))
    
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.atan2(self.y, self.x)
    def __setangle(self, angle):
        self.x = self.length
        self.y = 0
        self.rotate(angle)
    angle = property(get_angle, __setangle, 
        doc="""Gets or sets the angle (in radians) of a vector""")
 
    def get_angle_degrees(self):
        return math.degrees(self.get_angle())
    def __set_angle_degrees(self, angle_degrees):
        self.__setangle(math.radians(angle_degrees))
    angle_degrees = property(get_angle_degrees, __set_angle_degrees, 
        doc="""Gets or sets the angle (in degrees) of a vector""")
    
    def get_angle_between(self, other):
        """Get the angle between the vector and the other in radians
        
        :return: The angle
        """
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.atan2(cross, dot)
        
    def get_angle_degrees_between(self, other):
        """Get the angle between the vector and the other in degrees
        
        :return: The angle (in degrees)
        """
        return math.degrees(self.get_angle_between(other))
        
    def normalized(self):
        """Get a normalized copy of the vector
        Note: This function will return 0 if the length of the vector is 0.
        
        :return: A normalized vector
        """
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)
 
    def normalize_return_length(self):
        """Normalize the vector and return its length before the normalization
        
        :return: The length before the normalization
        """
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length
 
    def perpendicular(self):
        return Vec2d(-self.y, self.x)
    
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)
        
    def dot(self, other):
        """The dot product between the vector and other vector
            v1.dot(v2) -> v1.x*v2.x + v1.y*v2.y
            
        :return: The dot product
        """
        return float(self.x*other[0] + self.y*other[1])
        
    def get_distance(self, other):
        """The distance between the vector and other vector
        
        :return: The distance
        """
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)
        
    def get_dist_sqrd(self, other):
        """The squared distance between the vector and other vector
        It is more efficent to use this method than to call get_distance()
        first and then do a sqrt() on the result.
        
        :return: The squared distance
        """
        return (self.x - other[0])**2 + (self.y - other[1])**2
        
    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)
    
    def cross(self, other):
        """The cross product between the vector and other vector
            v1.cross(v2) -> v1.x*v2.y - v2.y*v1.x
        
        :return: The cross product
        """
        return self.x*other[1] - self.y*other[0]
    
    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)
    
    def convert_to_basis(self, x_vector, y_vector):
        x = self.dot(x_vector)/x_vector.get_length_sqrd()
        y = self.dot(y_vector)/y_vector.get_length_sqrd()
        return Vec2d(x, y)
    
    def __get_int_xy(self):
        return int(self.x), int(self.y)
    int_tuple = property(__get_int_xy, 
        doc="""Return the x and y values of this vector as ints""")
    
    @staticmethod
    def zero():
        """A vector of zero length"""
        return Vec2d(0, 0)
        
    @staticmethod
    def unit():
        """A unit vector pointing up"""
        return Vec2d(0, 1)
        
    @staticmethod
    def ones():
        """A vector where both x and y is 1"""
        return Vec2d(1, 1)
 
    # Extra functions, mainly for chipmunk
    def cpvrotate(self, other):
        """Uses complex multiplication to rotate this vector by the other. """
        return Vec2d(self.x*other.x - self.y*other.y, self.x*other.y + self.y*other.x)
    def cpvunrotate(self, other):
        """The inverse of cpvrotate"""
        return Vec2d(self.x*other.x + self.y*other.y, self.y*other.x - self.x*other.y)
    
    # Pickle
    def __reduce__(self):
        callable = Vec2d
        args = (self.x, self.y)
        return (callable, args)
    


