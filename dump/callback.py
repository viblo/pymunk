from ctypes import *

#ctypes.cdll.LoadLibrary("libex.dylib")
chipmunk_lib = windll.LoadLibrary("callback.dll")

#function_pointer = CFUNCTYPE
function_pointer = WINFUNCTYPE


class cpBody(Structure):
    pass
class cpArbiter(Structure):
    pass
    
cpArbiter._fields_ = [('x1', c_double),('x2', c_double),('x3', c_double),('x4', c_double),('x5', c_double),('x6', c_double)]
cpBody._fields_ = [('m1', c_double),('m2', c_double),('m3', c_double),('m4', c_double),('m5', c_double),('m6', c_double),]

cpBodyAlloc = chipmunk_lib.cpBodyAlloc
cpBodyAlloc.restype = POINTER(cpBody)
cpBodyAlloc.argtypes = []

cpBodyArbiterIteratorFunc = function_pointer(None, POINTER(cpBody), POINTER(cpArbiter), c_void_p)

cpBodyEachArbiter = chipmunk_lib.cpBodyEachArbiter
cpBodyEachArbiter.restype = None
cpBodyEachArbiter.argtypes = [POINTER(cpBody), cpBodyArbiterIteratorFunc, c_void_p]

class Body(object):
    def __init__(self):
        self._body = cpBodyAlloc()
        self._bodycontents = self._body.contents
    def get_arbiters(self):
        arbs = []
        def impl(body, _arbiter, _):
            #_arbs.append(_arbiter)
            arbs.append(Arbiter(_arbiter))
            return 0
        f = cpBodyArbiterIteratorFunc(impl)
        cpBodyEachArbiter(self._body, f, None)
        return arbs
        
class Arbiter(object):
    def __init__(self, _arbiter):
        self._arbiter = _arbiter
        self._arbitercontents = self._arbiter.contents
    
    
def test():
    b = Body()
    for x in range(100):
        arbs = b.get_arbiters()
        print arbs[0]._arbitercontents.x3
    
    
test()
