from ctypes import *

#ctypes.cdll.LoadLibrary("libex.dylib")
chipmunk_lib = cdll.LoadLibrary("ex.dll")

#function_pointer = CFUNCTYPE
function_pointer = WINFUNCTYPE

float_type = c_double
cpFloat = c_double

class Vec2d(Structure):
    __slots__ = ['x', 'y']
     
    @classmethod
    def from_param(cls, arg):
        """Used by ctypes to automatically create Vec2ds"""
        return cls(arg)
        
    # def __init__(self, x_or_pair=None, y = None):
        # if x_or_pair != None:
            # if y == None:
                # self.x = x_or_pair[0]
                # self.y = x_or_pair[1]
            # else:
                # self.x = x_or_pair
                # self.y = y
  
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
           
Vec2d._fields_ = [
            ('x', float_type),
            ('y', float_type),
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


class Body(object):
    def __init__(self, mass, moment):
        self._body = cpBodyNew(mass, moment)
        self._bodycontents = self._body.contents 
        
    def _set_mass(self, mass):
        cpBodySetMass(self._body, mass)
    def _get_mass(self):
        return self._bodycontents.m
    mass = property(_get_mass, _set_mass)

    def _set_moment(self, moment):
        cpBodySetMoment(self._body, moment)
    def _get_moment(self):
        return self._bodycontents.i
    moment = property(_get_moment, _set_moment)
   