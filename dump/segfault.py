from ctypes import *
from pymunk._chipmunk import *
from pymunk._chipmunk_ffi import *

s = cpSpaceNew()
b1 = cpBodyNew(1, 2)
b2 = cpBodyNew(3, 4)
c1 = cpCircleShapeNew(b1, 10, (0, 0))
c2 = cpCircleShapeNew(b2, 10, (0, 0))
cpSpaceAddShape(s, c1)
cpSpaceAddShape(s, c2)

cpSpaceStep(s, 1)

arbs = []
def impl(b, _arbiter, _):
    arbs.append(_arbiter)
    return 0
f = cpBodyArbiterIteratorFunc(impl)
cpBodyEachArbiter(b1, f, None)

arb = arbs[0]
shapeA_p = POINTER(cpShape)()
shapeB_p = POINTER(cpShape)()
cpArbiterGetShapes(arb, shapeA_p, shapeB_p)
print 1
print 2, shapeA_p.contents.sensor
print 3, shapeB_p.contents.sensor


