"""Basic benchmark of pymunk Vec2d class.

Results with 100000 iterations, all on windows (lower is better)
python 2.6: 5.63 sec
pypy-1.9: 11.12 sec
pypy-c-jit-53293-478bc4f20cb7-win32: 11.12 sec
"""

import timeit

import operator
import math
import ctypes 

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

def run():
    for x in range(100000):
        s = 0
        for x in range(10):
            v1 = Vec2d(1,3)
            v2 = Vec2d(1,3)
            v3 = v1+v2.cpvrotate(v1)
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