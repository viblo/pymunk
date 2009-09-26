__version__ = "$Id$"
__docformat__ = "reStructuredText"

import operator
import math
import ctypes 

float_type = ctypes.c_double

class Vec2d(ctypes.Structure):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']
    
    @classmethod
    def from_param(cls, arg):
        """Used by ctypes to automatically create Vec2ds"""
        return cls(arg)
        
    def __init__(self, x_or_pair=None, y = None):
        if x_or_pair != None:
            if y == None:
                self.x = x_or_pair[0]
                self.y = x_or_pair[1]
            else:
                self.x = x_or_pair
                self.y = y
 
    def __len__(self):
        return 2
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
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
        print(1)
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        print(2)
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        print(3)
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        print(4)
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        print(5)
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        print(6)
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        print(7)
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        print(8)
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        print(9)
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
    length = property(get_length, __setlength, doc = """Gets or sets the magnitude of the vector""")
       
    def rotate(self, angle_degrees):
        """Rotate the vector by angle_degrees degrees."""
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotated(self, angle_degrees):
        """Create and return a new vector by rotating this vector by 
        angle_degrees degrees.
        
        :return: Rotade vector
        """
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)
    
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, doc="""Gets or sets the angle of a vector""")
 
    def get_angle_between(self, other):
        """Get the angle between the vector and the other in degrees
        
        :return: The angle
        """
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))
            
    def normalized(self):
        """Get a normalized copy of the vector
        
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
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())
 
    # Extra functions, mainly for chipmunk
    def cpvrotate(self, other):
        return Vec2d(self.x*other.x - self.y*other.y, self.x*other.y + self.y*other.x)
    def cpvunrotate(self, other):
        return Vec2d(self.x*other.x + self.y*other.y, self.y*other.x - self.x*other.y)
    
    # Pickle, does not work atm.
    def __getstate__(self):
        return [self.x, self.y]
        
    def __setstate__(self, dict):
        self.x, self.y = dict
    def __newobj__(cls, *args):
        return cls.__new__(cls, *args)    
Vec2d._fields_ = [
            ('x', float_type),
            ('y', float_type),
        ]
########################################################################
## Unit Testing                                                       ##
########################################################################
if __name__ == "__main__":
 
    import unittest
    import pickle
 
    ####################################################################
    class UnitTestVec2d(unittest.TestCase):
    
        def setUp(self):
            pass
        
        def testCreationAndAccess(self):
            v = Vec2d(111, 222)
            self.assert_(v.x == 111 and v.y == 222)
            v.x = 333
            v[1] = 444
            self.assert_(v[0] == 333 and v[1] == 444)
 
        def testMath(self):
            v = Vec2d(111,222)
            self.assertEqual(v + 1, Vec2d(112, 223))
            self.assert_(v - 2 == [109, 220])
            self.assert_(v * 3 == (333, 666))
            self.assert_(v / 2.0 == Vec2d(55.5, 111))
            #self.assert_(v / 2 == (55, 111)) # Not supported since this is a c_float structure in the bottom
            self.assert_(v ** Vec2d(2, 3) == [12321, 10941048])
            self.assert_(v + [-11, 78] == Vec2d(100, 300))
            #self.assert_(v / [11,2] == [10,111]) # Not supported since this is a c_float structure in the bottom
 
        def testReverseMath(self):
            v = Vec2d(111, 222)
            self.assert_(1 + v == Vec2d(112, 223))
            self.assert_(2 - v == [-109, -220])
            self.assert_(3 * v == (333, 666))
            #self.assert_([222,999] / v == [2,4]) # Not supported since this is a c_float structure in the bottom
            self.assert_([111, 222] ** Vec2d(2, 3) == [12321, 10941048])
            self.assert_([-11, 78] + v == Vec2d(100, 300))
 
        def testUnary(self):
            v = Vec2d(111, 222)
            v = -v
            self.assert_(v == [-111, -222])
            v = abs(v)
            self.assert_(v == [111, 222])
 
        def testLength(self):
            v = Vec2d(3,4)
            self.assert_(v.length == 5)
            self.assert_(v.get_length_sqrd() == 25)
            self.assert_(v.normalize_return_length() == 5)
            self.assertAlmostEquals(v.length, 1)
            v.length = 5
            self.assert_(v == Vec2d(3, 4))
            v2 = Vec2d(10, -2)
            self.assert_(v.get_distance(v2) == (v - v2).get_length())
            
        def testAngles(self):            
            v = Vec2d(0, 3)
            self.assertEquals(v.angle, 90)
            v2 = Vec2d(v)
            v.rotate(-90)
            self.assertEqual(v.get_angle_between(v2), 90)
            v2.angle -= 90
            self.assertEqual(v.length, v2.length)
            self.assertEquals(v2.angle, 0)
            self.assertEqual(v2, [3, 0])
            self.assert_((v - v2).length < .00001)
            self.assertEqual(v.length, v2.length)
            v2.rotate(300)
            self.assertAlmostEquals(v.get_angle_between(v2), -60) # Allow a little more error than usual (floats..)
            v2.rotate(v2.get_angle_between(v))
            angle = v.get_angle_between(v2)
            self.assertAlmostEquals(v.get_angle_between(v2), 0)  
 
        def testHighLevel(self):
            basis0 = Vec2d(5.0, 0)
            basis1 = Vec2d(0, .5)
            v = Vec2d(10, 1)
            self.assert_(v.convert_to_basis(basis0, basis1) == [2, 2])
            self.assert_(v.projection(basis0) == (10, 0))
            self.assert_(basis0.dot(basis1) == 0)
            
        def testCross(self):
            lhs = Vec2d(1, .5)
            rhs = Vec2d(4, 6)
            self.assert_(lhs.cross(rhs) == 4)
            
        def testComparison(self):
            int_vec = Vec2d(3, -2)
            flt_vec = Vec2d(3.0, -2.0)
            zero_vec = Vec2d(0, 0)
            self.assert_(int_vec == flt_vec)
            self.assert_(int_vec != zero_vec)
            self.assert_((flt_vec == zero_vec) == False)
            self.assert_((flt_vec != int_vec) == False)
            self.assert_(int_vec == (3, -2))
            self.assert_(int_vec != [0, 0])
            self.assert_(int_vec != 5)
            self.assert_(int_vec != [3, -2, -5])
        
        def testInplace(self):
            inplace_vec = Vec2d(5, 13)
            inplace_ref = inplace_vec
            inplace_src = Vec2d(inplace_vec)    
            inplace_vec *= .5
            inplace_vec += .5
            inplace_vec /= (3, 6)
            inplace_vec += Vec2d(-1, -1)
            alternate = (inplace_src*.5 + .5)/Vec2d(3, 6) + [-1, -1]
            self.assertEquals(inplace_vec, inplace_ref)
            self.assertEquals(inplace_vec, alternate)
        
        def testPickle(self):
            return # pickling does not work atm
            testvec = Vec2d(5, .3)
            testvec_str = pickle.dumps(testvec)
            loaded_vec = pickle.loads(testvec_str)
            self.assertEquals(testvec, loaded_vec)
    
    ####################################################################
    unittest.main()
 
    ######################################################################## 
del float_type
__all__ = ["Vec2d"]
