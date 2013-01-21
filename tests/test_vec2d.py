import math
import pickle
import unittest

import pymunk as p
from pymunk.vec2d import Vec2d


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
        
    def testAnglesDegrees(self):            
        v = Vec2d(0, 3)
        self.assertEquals(v.angle_degrees, 90)
        v2 = Vec2d(v)
        v.rotate_degrees(-90)
        self.assertEqual(v.get_angle_degrees_between(v2), 90)
        v2.angle_degrees -= 90
        self.assertEqual(v.length, v2.length)
        self.assertEquals(v2.angle_degrees, 0)
        self.assertEqual(v2, [3, 0])
        self.assert_((v - v2).length < .00001)
        self.assertEqual(v.length, v2.length)
        v2.rotate_degrees(300)
        self.assertAlmostEquals(v.get_angle_degrees_between(v2), -60) # Allow a little more error than usual (floats..)
        v2.rotate_degrees(v2.get_angle_degrees_between(v))
        angle = v.get_angle_degrees_between(v2)
        self.assertAlmostEquals(v.get_angle_degrees_between(v2), 0)  

    def testAnglesRadians(self):            
        v = Vec2d(0, 3)
        self.assertEquals(v.angle, math.pi/2.)
        v2 = Vec2d(v)
        v.rotate(-math.pi/2.)
        self.assertEqual(v.get_angle_between(v2), math.pi/2.)
        v2.angle -= math.pi/2.
        self.assertEqual(v.length, v2.length)
        self.assertEquals(v2.angle, 0)
        self.assertEqual(v2, [3, 0])
        self.assert_((v - v2).length < .00001)
        self.assertEqual(v.length, v2.length)
        v2.rotate(math.pi/3.*5.)
        self.assertAlmostEquals(v.get_angle_between(v2), -math.pi/3.) # Allow a little more error than usual (floats..)
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
        testvec = Vec2d(5, .3)
        testvec_str = pickle.dumps(testvec)
        loaded_vec = pickle.loads(testvec_str)
        self.assertEquals(testvec, loaded_vec)

if __name__ == "__main__":
    print ("testing pymunk.vec2d version " + p.version)
    unittest.main()