import ctypes
from ctypes import *

#ctypes.cdll.LoadLibrary("libex.dylib")
chipmunk_lib = cdll.LoadLibrary("./ex.so")

function_pointer = CFUNCTYPE
#function_pointer = WINFUNCTYPE

float_type = c_double
cpFloat = c_double



#class Vec2d(): # this would be very fast in pypy
class Vec2d(ctypes.Structure):
    """2d vector class, supports vector and scalar operators,
       and also provides some high level functions
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
 
    def cpvrotate(self, other):
        """Uses complex multiplication to rotate this vector by the other. """
        return Vec2d(self.x*other.x - self.y*other.y, self.x*other.y + self.y*other.x)
    
Vec2d._fields_ = [
            ('x', ctypes.c_double),
            ('y', ctypes.c_double),
        ]

cpVect = Vec2d
STRING = c_char_p

class cpBody(Structure):
    pass
    
cpBodyVelocityFunc = function_pointer(None, POINTER(cpBody), cpVect, cpFloat, cpFloat)
cpBodyPositionFunc = function_pointer(None, POINTER(cpBody), cpFloat)
    
#cpBody._pack_ = 4
cpBody._fields_ = [
    ('velocity_func', cpBodyVelocityFunc),
    ('position_func', cpBodyPositionFunc),
    ('m', cpFloat),
    ('m_inv', cpFloat),
    ('i', cpFloat),
    ('i_inv', cpFloat),
    ('p', cpVect),
    ('v', cpVect),
    ('f', cpVect),
    ('a', cpFloat),
    ('w', cpFloat),
    ('t', cpFloat),
    ('rot', cpVect),
    #('data', cpDataPointer),
    ('v_limit', cpFloat),
    ('w_limit', cpFloat),
    ('v_bias_private', cpVect),
    ('w_bias_private', cpFloat),
    #('space_private', POINTER(cpSpace)),
    #('shapeList_private', POINTER(cpShape)),
    #('arbiterList_private', POINTER(cpArbiter)),
    #('constraintList_private', POINTER(cpConstraint)),
    #('node_private', cpComponentNode),
]
cpBodyAlloc = chipmunk_lib.cpBodyAlloc
cpBodyAlloc.restype = POINTER(cpBody)
cpBodyAlloc.argtypes = []
cpBodyInit = chipmunk_lib.cpBodyInit
cpBodyInit.restype = POINTER(cpBody)
cpBodyInit.argtypes = [POINTER(cpBody), cpFloat, cpFloat]
cpBodyNew = chipmunk_lib.cpBodyNew
cpBodyNew.restype = POINTER(cpBody)
cpBodyNew.argtypes = [cpFloat, cpFloat] 

l = chipmunk_lib
b = l.cpBodyNew(3,4)

print b.contents.m, b.contents.p.x
b.contents.p.x = 3.5
print b.contents.m, b.contents.p.x

import timeit

import operator
import math

def run():
    b = l.cpBodyNew(15,17)
    for x in range(20000):
        s = 0
        for x in range(10):
            b.p = Vec2d(1,3)
            v1 = b.contents.p
            
            v2 = Vec2d(1,3)
            b.p = v1+v2.cpvrotate(v1)
            v3 = b.contents.p
            s+=v3.x+v3.y

                
def main():
    t = timeit.Timer('run()', "from __main__ import run") 
    print("runtime: %.2fs" % t.timeit(number=1))

if __name__ == '__main__':
    doprof = 0
    if not doprof: 
        main()
    else:
        import cProfile, pstats
        
        prof = cProfile.run("run()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats('cumulative', 'time', 'calls')
        stats.print_stats(30)
