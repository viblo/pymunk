from ctypes import *
import sys
sys.path.insert(0,'..')

import pymunk 

sendbody_lib = windll.LoadLibrary("sendbody.dll")

cpBody = pymunk._chipmunk.cpBody

mass_sum = sendbody_lib.mass_sum
mass_sum.restype = c_double
mass_sum.argtypes = [c_int, POINTER(POINTER(cpBody))]

b1 = pymunk.Body(1, 1)
b2 = pymunk.Body(10, 1)
bodies = [b1._body, b2._body, b1._body]
arr = (POINTER(cpBody) * len(bodies))(*bodies)

print mass_sum(len(arr), arr)  




 

