
from ctypes import * 
from vec2d import Vec2d
cpVect = Vec2d

from libload import load_library
_lib_debug = True #Set to True to print the Chipmunk path.
chipmunk_lib = load_library("libchipmunk", print_path=_lib_debug)

STRING = c_char_p


# def CP_HASH_PAIR(A,B): return ((unsigned int)(A)*CP_HASH_COEF ^ (unsigned int)(B)*CP_HASH_COEF) # macro
CP_CIRCLE_SHAPE = 0
CP_NUM_SHAPES = 3
CP_POLY_SHAPE = 2
CP_SEGMENT_SHAPE = 1
cpFloat = c_float
class MSVC_EVIL_FLOAT_HACK(Union):
    pass
MSVC_EVIL_FLOAT_HACK._fields_ = [
    ('Bytes', c_ubyte * 4),
    ('Value', c_float),
]
cpInitChipmunk = chipmunk_lib.cpInitChipmunk
cpInitChipmunk.restype = None
cpInitChipmunk.argtypes = []
#cpVect class def removed
cpMomentForCircle = chipmunk_lib.cpMomentForCircle
cpMomentForCircle.restype = cpFloat
cpMomentForCircle.argtypes = [cpFloat, cpFloat, cpFloat, cpVect]
cpMomentForPoly = chipmunk_lib.cpMomentForPoly
cpMomentForPoly.restype = cpFloat
cpMomentForPoly.argtypes = [cpFloat, c_int, POINTER(cpVect), cpVect]
class cpContact(Structure):
    pass
#cpVect _fields_ def removed
cpContact._fields_ = [
    ('p', cpVect),
    ('n', cpVect),
    ('dist', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('nMass', cpFloat),
    ('tMass', cpFloat),
    ('bounce', cpFloat),
    ('jnAcc', cpFloat),
    ('jtAcc', cpFloat),
    ('jBias', cpFloat),
    ('bias', cpFloat),
    ('hash', c_uint),
]
cpContactInit = chipmunk_lib.cpContactInit
cpContactInit.restype = POINTER(cpContact)
cpContactInit.argtypes = [POINTER(cpContact), cpVect, cpVect, cpFloat, c_uint]
cpContactsSumImpulses = chipmunk_lib.cpContactsSumImpulses
cpContactsSumImpulses.restype = cpVect
cpContactsSumImpulses.argtypes = [POINTER(cpContact), c_int]
cpContactsSumImpulsesWithFriction = chipmunk_lib.cpContactsSumImpulsesWithFriction
cpContactsSumImpulsesWithFriction.restype = cpVect
cpContactsSumImpulsesWithFriction.argtypes = [POINTER(cpContact), c_int]
class cpArbiter(Structure):
    pass
class cpShape(Structure):
    pass
cpArbiter._fields_ = [
    ('numContacts', c_int),
    ('contacts', POINTER(cpContact)),
    ('a', POINTER(cpShape)),
    ('b', POINTER(cpShape)),
    ('u', cpFloat),
    ('e', cpFloat),
    ('target_v', cpVect),
    ('stamp', c_int),
]
cpArbiterAlloc = chipmunk_lib.cpArbiterAlloc
cpArbiterAlloc.restype = POINTER(cpArbiter)
cpArbiterAlloc.argtypes = []
cpArbiterInit = chipmunk_lib.cpArbiterInit
cpArbiterInit.restype = POINTER(cpArbiter)
cpArbiterInit.argtypes = [POINTER(cpArbiter), POINTER(cpShape), POINTER(cpShape), c_int]
cpArbiterNew = chipmunk_lib.cpArbiterNew
cpArbiterNew.restype = POINTER(cpArbiter)
cpArbiterNew.argtypes = [POINTER(cpShape), POINTER(cpShape), c_int]
cpArbiterDestroy = chipmunk_lib.cpArbiterDestroy
cpArbiterDestroy.restype = None
cpArbiterDestroy.argtypes = [POINTER(cpArbiter)]
cpArbiterFree = chipmunk_lib.cpArbiterFree
cpArbiterFree.restype = None
cpArbiterFree.argtypes = [POINTER(cpArbiter)]
cpArbiterInject = chipmunk_lib.cpArbiterInject
cpArbiterInject.restype = None
cpArbiterInject.argtypes = [POINTER(cpArbiter), POINTER(cpContact), c_int]
cpArbiterPreStep = chipmunk_lib.cpArbiterPreStep
cpArbiterPreStep.restype = None
cpArbiterPreStep.argtypes = [POINTER(cpArbiter), cpFloat]
cpArbiterApplyImpulse = chipmunk_lib.cpArbiterApplyImpulse
cpArbiterApplyImpulse.restype = None
cpArbiterApplyImpulse.argtypes = [POINTER(cpArbiter)]
class cpArray(Structure):
    pass
cpArray._fields_ = [
    ('num', c_int),
    ('max', c_int),
    ('arr', POINTER(c_void_p)),
]
cpArrayIter = CFUNCTYPE(None, c_void_p, c_void_p)
cpArrayAlloc = chipmunk_lib.cpArrayAlloc
cpArrayAlloc.restype = POINTER(cpArray)
cpArrayAlloc.argtypes = []
cpArrayInit = chipmunk_lib.cpArrayInit
cpArrayInit.restype = POINTER(cpArray)
cpArrayInit.argtypes = [POINTER(cpArray), c_int]
cpArrayNew = chipmunk_lib.cpArrayNew
cpArrayNew.restype = POINTER(cpArray)
cpArrayNew.argtypes = [c_int]
cpArrayDestroy = chipmunk_lib.cpArrayDestroy
cpArrayDestroy.restype = None
cpArrayDestroy.argtypes = [POINTER(cpArray)]
cpArrayFree = chipmunk_lib.cpArrayFree
cpArrayFree.restype = None
cpArrayFree.argtypes = [POINTER(cpArray)]
cpArrayPush = chipmunk_lib.cpArrayPush
cpArrayPush.restype = None
cpArrayPush.argtypes = [POINTER(cpArray), c_void_p]
cpArrayDeleteIndex = chipmunk_lib.cpArrayDeleteIndex
cpArrayDeleteIndex.restype = None
cpArrayDeleteIndex.argtypes = [POINTER(cpArray), c_int]
cpArrayDeleteObj = chipmunk_lib.cpArrayDeleteObj
cpArrayDeleteObj.restype = None
cpArrayDeleteObj.argtypes = [POINTER(cpArray), c_void_p]
cpArrayEach = chipmunk_lib.cpArrayEach
cpArrayEach.restype = None
cpArrayEach.argtypes = [POINTER(cpArray), cpArrayIter, c_void_p]
cpArrayContains = chipmunk_lib.cpArrayContains
cpArrayContains.restype = c_int
cpArrayContains.argtypes = [POINTER(cpArray), c_void_p]
class cpBB(Structure):
    pass
cpBB._fields_ = [
    ('l', cpFloat),
    ('b', cpFloat),
    ('r', cpFloat),
    ('t', cpFloat),
]
cpBBClampVect = chipmunk_lib.cpBBClampVect
cpBBClampVect.restype = cpVect
cpBBClampVect.argtypes = [cpBB, cpVect]
cpBBWrapVect = chipmunk_lib.cpBBWrapVect
cpBBWrapVect.restype = cpVect
cpBBWrapVect.argtypes = [cpBB, cpVect]
class cpBody(Structure):
    pass
cpBody._fields_ = [
    ('m', cpFloat),
    ('m_inv', cpFloat),
    ('i', cpFloat),
    ('i_inv', cpFloat),
    ('p', cpVect),
    ('v', cpVect),
    ('f', cpVect),
    ('v_bias', cpVect),
    ('a', cpFloat),
    ('w', cpFloat),
    ('t', cpFloat),
    ('w_bias', cpFloat),
    ('rot', cpVect),
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
cpBodyDestroy = chipmunk_lib.cpBodyDestroy
cpBodyDestroy.restype = None
cpBodyDestroy.argtypes = [POINTER(cpBody)]
cpBodyFree = chipmunk_lib.cpBodyFree
cpBodyFree.restype = None
cpBodyFree.argtypes = [POINTER(cpBody)]
cpBodySetMass = chipmunk_lib.cpBodySetMass
cpBodySetMass.restype = None
cpBodySetMass.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetMoment = chipmunk_lib.cpBodySetMoment
cpBodySetMoment.restype = None
cpBodySetMoment.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetAngle = chipmunk_lib.cpBodySetAngle
cpBodySetAngle.restype = None
cpBodySetAngle.argtypes = [POINTER(cpBody), cpFloat]
cpBodySlew = chipmunk_lib.cpBodySlew
cpBodySlew.restype = None
cpBodySlew.argtypes = [POINTER(cpBody), cpVect, cpFloat]
cpBodyUpdateVelocity = chipmunk_lib.cpBodyUpdateVelocity
cpBodyUpdateVelocity.restype = None
cpBodyUpdateVelocity.argtypes = [POINTER(cpBody), cpVect, cpFloat, cpFloat]
cpBodyUpdatePosition = chipmunk_lib.cpBodyUpdatePosition
cpBodyUpdatePosition.restype = None
cpBodyUpdatePosition.argtypes = [POINTER(cpBody), cpFloat]
cpBodyResetForces = chipmunk_lib.cpBodyResetForces
cpBodyResetForces.restype = None
cpBodyResetForces.argtypes = [POINTER(cpBody)]
cpBodyApplyForce = chipmunk_lib.cpBodyApplyForce
cpBodyApplyForce.restype = None
cpBodyApplyForce.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpDampedSpring = chipmunk_lib.cpDampedSpring
cpDampedSpring.restype = None
cpDampedSpring.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat, cpFloat]
cpCollideShapes = chipmunk_lib.cpCollideShapes
cpCollideShapes.restype = c_int
cpCollideShapes.argtypes = [POINTER(cpShape), POINTER(cpShape), POINTER(POINTER(cpContact))]
class cpHashSetBin(Structure):
    pass
cpHashSetBin._fields_ = [
    ('elt', c_void_p),
    ('hash', c_uint),
    ('next', POINTER(cpHashSetBin)),
]
cpHashSetEqlFunc = CFUNCTYPE(c_int, c_void_p, c_void_p)
cpHashSetTransFunc = CFUNCTYPE(c_void_p, c_void_p, c_void_p)
cpHashSetIterFunc = CFUNCTYPE(None, c_void_p, c_void_p)
cpHashSetRejectFunc = CFUNCTYPE(c_int, c_void_p, c_void_p)
class cpHashSet(Structure):
    pass
cpHashSet._fields_ = [
    ('entries', c_int),
    ('size', c_int),
    ('eql', cpHashSetEqlFunc),
    ('trans', cpHashSetTransFunc),
    ('default_value', c_void_p),
    ('table', POINTER(POINTER(cpHashSetBin))),
]
cpHashSetDestroy = chipmunk_lib.cpHashSetDestroy
cpHashSetDestroy.restype = None
cpHashSetDestroy.argtypes = [POINTER(cpHashSet)]
cpHashSetFree = chipmunk_lib.cpHashSetFree
cpHashSetFree.restype = None
cpHashSetFree.argtypes = [POINTER(cpHashSet)]
cpHashSetAlloc = chipmunk_lib.cpHashSetAlloc
cpHashSetAlloc.restype = POINTER(cpHashSet)
cpHashSetAlloc.argtypes = []
cpHashSetInit = chipmunk_lib.cpHashSetInit
cpHashSetInit.restype = POINTER(cpHashSet)
cpHashSetInit.argtypes = [POINTER(cpHashSet), c_int, cpHashSetEqlFunc, cpHashSetTransFunc]
cpHashSetNew = chipmunk_lib.cpHashSetNew
cpHashSetNew.restype = POINTER(cpHashSet)
cpHashSetNew.argtypes = [c_int, cpHashSetEqlFunc, cpHashSetTransFunc]
cpHashSetInsert = chipmunk_lib.cpHashSetInsert
cpHashSetInsert.restype = c_void_p
cpHashSetInsert.argtypes = [POINTER(cpHashSet), c_uint, c_void_p, c_void_p]
cpHashSetRemove = chipmunk_lib.cpHashSetRemove
cpHashSetRemove.restype = c_void_p
cpHashSetRemove.argtypes = [POINTER(cpHashSet), c_uint, c_void_p]
cpHashSetFind = chipmunk_lib.cpHashSetFind
cpHashSetFind.restype = c_void_p
cpHashSetFind.argtypes = [POINTER(cpHashSet), c_uint, c_void_p]
cpHashSetEach = chipmunk_lib.cpHashSetEach
cpHashSetEach.restype = None
cpHashSetEach.argtypes = [POINTER(cpHashSet), cpHashSetIterFunc, c_void_p]
cpHashSetReject = chipmunk_lib.cpHashSetReject
cpHashSetReject.restype = None
cpHashSetReject.argtypes = [POINTER(cpHashSet), cpHashSetRejectFunc, c_void_p]
class cpJoint(Structure):
    pass
cpJoint._fields_ = [
    ('a', POINTER(cpBody)),
    ('b', POINTER(cpBody)),
    ('preStep', CFUNCTYPE(None, POINTER(cpJoint), c_float)),
    ('applyImpulse', CFUNCTYPE(None, POINTER(cpJoint))),
]
cpJointDestroy = chipmunk_lib.cpJointDestroy
cpJointDestroy.restype = None
cpJointDestroy.argtypes = [POINTER(cpJoint)]
cpJointFree = chipmunk_lib.cpJointFree
cpJointFree.restype = None
cpJointFree.argtypes = [POINTER(cpJoint)]
class cpPinJoint(Structure):
    pass
cpPinJoint._fields_ = [
    ('joint', cpJoint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('dist', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('n', cpVect),
    ('nMass', cpFloat),
    ('jnAcc', cpFloat),
    ('jBias', cpFloat),
    ('bias', cpFloat),
]
cpPinJointAlloc = chipmunk_lib.cpPinJointAlloc
cpPinJointAlloc.restype = POINTER(cpPinJoint)
cpPinJointAlloc.argtypes = []
cpPinJointInit = chipmunk_lib.cpPinJointInit
cpPinJointInit.restype = POINTER(cpPinJoint)
cpPinJointInit.argtypes = [POINTER(cpPinJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPinJointNew = chipmunk_lib.cpPinJointNew
cpPinJointNew.restype = POINTER(cpJoint)
cpPinJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
class cpSlideJoint(Structure):
    pass
cpSlideJoint._fields_ = [
    ('joint', cpJoint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('min', cpFloat),
    ('max', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('n', cpVect),
    ('nMass', cpFloat),
    ('jnAcc', cpFloat),
    ('jBias', cpFloat),
    ('bias', cpFloat),
]
cpSlideJointAlloc = chipmunk_lib.cpSlideJointAlloc
cpSlideJointAlloc.restype = POINTER(cpSlideJoint)
cpSlideJointAlloc.argtypes = []
cpSlideJointInit = chipmunk_lib.cpSlideJointInit
cpSlideJointInit.restype = POINTER(cpSlideJoint)
cpSlideJointInit.argtypes = [POINTER(cpSlideJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpSlideJointNew = chipmunk_lib.cpSlideJointNew
cpSlideJointNew.restype = POINTER(cpJoint)
cpSlideJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
class cpPivotJoint(Structure):
    pass
cpPivotJoint._fields_ = [
    ('joint', cpJoint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('r1', cpVect),
    ('r2', cpVect),
    ('k1', cpVect),
    ('k2', cpVect),
    ('jAcc', cpVect),
    ('jBias', cpVect),
    ('bias', cpVect),
]
cpPivotJointAlloc = chipmunk_lib.cpPivotJointAlloc
cpPivotJointAlloc.restype = POINTER(cpPivotJoint)
cpPivotJointAlloc.argtypes = []
cpPivotJointInit = chipmunk_lib.cpPivotJointInit
cpPivotJointInit.restype = POINTER(cpPivotJoint)
cpPivotJointInit.argtypes = [POINTER(cpPivotJoint), POINTER(cpBody), POINTER(cpBody), cpVect]
cpPivotJointNew = chipmunk_lib.cpPivotJointNew
cpPivotJointNew.restype = POINTER(cpJoint)
cpPivotJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect]
class cpGrooveJoint(Structure):
    pass
cpGrooveJoint._fields_ = [
    ('joint', cpJoint),
    ('grv_n', cpVect),
    ('grv_a', cpVect),
    ('grv_b', cpVect),
    ('anchr2', cpVect),
    ('grv_tn', cpVect),
    ('clamp', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('k1', cpVect),
    ('k2', cpVect),
    ('jAcc', cpVect),
    ('jBias', cpVect),
    ('bias', cpVect),
]
cpGrooveJointAlloc = chipmunk_lib.cpGrooveJointAlloc
cpGrooveJointAlloc.restype = POINTER(cpGrooveJoint)
cpGrooveJointAlloc.argtypes = []
cpGrooveJointInit = chipmunk_lib.cpGrooveJointInit
cpGrooveJointInit.restype = POINTER(cpGrooveJoint)
cpGrooveJointInit.argtypes = [POINTER(cpGrooveJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
cpGrooveJointNew = chipmunk_lib.cpGrooveJointNew
cpGrooveJointNew.restype = POINTER(cpJoint)
cpGrooveJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
class cpPolyShapeAxis(Structure):
    pass
cpPolyShapeAxis._fields_ = [
    ('n', cpVect),
    ('d', cpFloat),
]
class cpPolyShape(Structure):
    pass

# values for enumeration 'cpShapeType'
cpShapeType = c_int # enum
cpShape._fields_ = [
    ('type', cpShapeType),
    ('cacheData', CFUNCTYPE(cpBB, POINTER(cpShape), cpVect, cpVect)),
    ('destroy', CFUNCTYPE(None, POINTER(cpShape))),
    ('id', c_uint),
    ('bb', cpBB),
    ('collision_type', c_uint),
    ('group', c_uint),
    ('layers', c_uint),
    ('data', c_void_p),
    ('body', POINTER(cpBody)),
    ('e', cpFloat),
    ('u', cpFloat),
    ('surface_v', cpVect),
]
cpPolyShape._fields_ = [
    ('shape', cpShape),
    ('numVerts', c_int),
    ('verts', POINTER(cpVect)),
    ('axes', POINTER(cpPolyShapeAxis)),
    ('tVerts', POINTER(cpVect)),
    ('tAxes', POINTER(cpPolyShapeAxis)),
]
cpPolyShapeAlloc = chipmunk_lib.cpPolyShapeAlloc
cpPolyShapeAlloc.restype = POINTER(cpPolyShape)
cpPolyShapeAlloc.argtypes = []
cpPolyShapeInit = chipmunk_lib.cpPolyShapeInit
cpPolyShapeInit.restype = POINTER(cpPolyShape)
cpPolyShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpPolyShapeNew = chipmunk_lib.cpPolyShapeNew
cpPolyShapeNew.restype = POINTER(cpShape)
cpPolyShapeNew.argtypes = [POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpResetShapeIdCounter = chipmunk_lib.cpResetShapeIdCounter
cpResetShapeIdCounter.restype = None
cpResetShapeIdCounter.argtypes = []
cpShapeInit = chipmunk_lib.cpShapeInit
cpShapeInit.restype = POINTER(cpShape)
cpShapeInit.argtypes = [POINTER(cpShape), cpShapeType, POINTER(cpBody)]
cpShapeDestroy = chipmunk_lib.cpShapeDestroy
cpShapeDestroy.restype = None
cpShapeDestroy.argtypes = [POINTER(cpShape)]
cpShapeFree = chipmunk_lib.cpShapeFree
cpShapeFree.restype = None
cpShapeFree.argtypes = [POINTER(cpShape)]
cpShapeCacheBB = chipmunk_lib.cpShapeCacheBB
cpShapeCacheBB.restype = cpBB
cpShapeCacheBB.argtypes = [POINTER(cpShape)]
class cpCircleShape(Structure):
    pass
cpCircleShape._fields_ = [
    ('shape', cpShape),
    ('c', cpVect),
    ('r', cpFloat),
    ('tc', cpVect),
]
cpCircleShapeAlloc = chipmunk_lib.cpCircleShapeAlloc
cpCircleShapeAlloc.restype = POINTER(cpCircleShape)
cpCircleShapeAlloc.argtypes = []
cpCircleShapeInit = chipmunk_lib.cpCircleShapeInit
cpCircleShapeInit.restype = POINTER(cpCircleShape)
cpCircleShapeInit.argtypes = [POINTER(cpCircleShape), POINTER(cpBody), cpFloat, cpVect]
cpCircleShapeNew = chipmunk_lib.cpCircleShapeNew
cpCircleShapeNew.restype = POINTER(cpShape)
cpCircleShapeNew.argtypes = [POINTER(cpBody), cpFloat, cpVect]
class cpSegmentShape(Structure):
    pass
cpSegmentShape._fields_ = [
    ('shape', cpShape),
    ('a', cpVect),
    ('b', cpVect),
    ('n', cpVect),
    ('r', cpFloat),
    ('ta', cpVect),
    ('tb', cpVect),
    ('tn', cpVect),
]
cpSegmentShapeAlloc = chipmunk_lib.cpSegmentShapeAlloc
cpSegmentShapeAlloc.restype = POINTER(cpSegmentShape)
cpSegmentShapeAlloc.argtypes = []
cpSegmentShapeInit = chipmunk_lib.cpSegmentShapeInit
cpSegmentShapeInit.restype = POINTER(cpSegmentShape)
cpSegmentShapeInit.argtypes = [POINTER(cpSegmentShape), POINTER(cpBody), cpVect, cpVect, cpFloat]
cpSegmentShapeNew = chipmunk_lib.cpSegmentShapeNew
cpSegmentShapeNew.restype = POINTER(cpShape)
cpSegmentShapeNew.argtypes = [POINTER(cpBody), cpVect, cpVect, cpFloat]
cpCollFunc = CFUNCTYPE(c_int, POINTER(cpShape), POINTER(cpShape), POINTER(cpContact), c_int, c_float, c_void_p)
class cpCollPairFunc(Structure):
    pass
cpCollPairFunc._fields_ = [
    ('a', c_uint),
    ('b', c_uint),
    ('func', cpCollFunc),
    ('data', c_void_p),
]
class cpSpace(Structure):
    pass
class cpSpaceHash(Structure):
    pass
cpSpace._fields_ = [
    ('iterations', c_int),
    ('gravity', cpVect),
    ('damping', cpFloat),
    ('stamp', c_int),
    ('staticShapes', POINTER(cpSpaceHash)),
    ('activeShapes', POINTER(cpSpaceHash)),
    ('bodies', POINTER(cpArray)),
    ('arbiters', POINTER(cpArray)),
    ('contactSet', POINTER(cpHashSet)),
    ('joints', POINTER(cpArray)),
    ('collFuncSet', POINTER(cpHashSet)),
    ('defaultPairFunc', cpCollPairFunc),
]
cpSpaceAlloc = chipmunk_lib.cpSpaceAlloc
cpSpaceAlloc.restype = POINTER(cpSpace)
cpSpaceAlloc.argtypes = []
cpSpaceInit = chipmunk_lib.cpSpaceInit
cpSpaceInit.restype = POINTER(cpSpace)
cpSpaceInit.argtypes = [POINTER(cpSpace)]
cpSpaceNew = chipmunk_lib.cpSpaceNew
cpSpaceNew.restype = POINTER(cpSpace)
cpSpaceNew.argtypes = []
cpSpaceDestroy = chipmunk_lib.cpSpaceDestroy
cpSpaceDestroy.restype = None
cpSpaceDestroy.argtypes = [POINTER(cpSpace)]
cpSpaceFree = chipmunk_lib.cpSpaceFree
cpSpaceFree.restype = None
cpSpaceFree.argtypes = [POINTER(cpSpace)]
cpSpaceFreeChildren = chipmunk_lib.cpSpaceFreeChildren
cpSpaceFreeChildren.restype = None
cpSpaceFreeChildren.argtypes = [POINTER(cpSpace)]
cpSpaceAddCollisionPairFunc = chipmunk_lib.cpSpaceAddCollisionPairFunc
cpSpaceAddCollisionPairFunc.restype = None
cpSpaceAddCollisionPairFunc.argtypes = [POINTER(cpSpace), c_uint, c_uint, cpCollFunc, c_void_p]
cpSpaceRemoveCollisionPairFunc = chipmunk_lib.cpSpaceRemoveCollisionPairFunc
cpSpaceRemoveCollisionPairFunc.restype = None
cpSpaceRemoveCollisionPairFunc.argtypes = [POINTER(cpSpace), c_uint, c_uint]
cpSpaceSetDefaultCollisionPairFunc = chipmunk_lib.cpSpaceSetDefaultCollisionPairFunc
cpSpaceSetDefaultCollisionPairFunc.restype = None
cpSpaceSetDefaultCollisionPairFunc.argtypes = [POINTER(cpSpace), cpCollFunc, c_void_p]
cpSpaceAddShape = chipmunk_lib.cpSpaceAddShape
cpSpaceAddShape.restype = None
cpSpaceAddShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddStaticShape = chipmunk_lib.cpSpaceAddStaticShape
cpSpaceAddStaticShape.restype = None
cpSpaceAddStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddBody = chipmunk_lib.cpSpaceAddBody
cpSpaceAddBody.restype = None
cpSpaceAddBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceAddJoint = chipmunk_lib.cpSpaceAddJoint
cpSpaceAddJoint.restype = None
cpSpaceAddJoint.argtypes = [POINTER(cpSpace), POINTER(cpJoint)]
cpSpaceRemoveShape = chipmunk_lib.cpSpaceRemoveShape
cpSpaceRemoveShape.restype = None
cpSpaceRemoveShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveStaticShape = chipmunk_lib.cpSpaceRemoveStaticShape
cpSpaceRemoveStaticShape.restype = None
cpSpaceRemoveStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveBody = chipmunk_lib.cpSpaceRemoveBody
cpSpaceRemoveBody.restype = None
cpSpaceRemoveBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceRemoveJoint = chipmunk_lib.cpSpaceRemoveJoint
cpSpaceRemoveJoint.restype = None
cpSpaceRemoveJoint.argtypes = [POINTER(cpSpace), POINTER(cpJoint)]
cpSpaceBodyIterator = CFUNCTYPE(None, POINTER(cpBody), c_void_p)
cpSpaceEachBody = chipmunk_lib.cpSpaceEachBody
cpSpaceEachBody.restype = None
cpSpaceEachBody.argtypes = [POINTER(cpSpace), cpSpaceBodyIterator, c_void_p]
cpSpaceResizeStaticHash = chipmunk_lib.cpSpaceResizeStaticHash
cpSpaceResizeStaticHash.restype = None
cpSpaceResizeStaticHash.argtypes = [POINTER(cpSpace), cpFloat, c_int]
cpSpaceResizeActiveHash = chipmunk_lib.cpSpaceResizeActiveHash
cpSpaceResizeActiveHash.restype = None
cpSpaceResizeActiveHash.argtypes = [POINTER(cpSpace), cpFloat, c_int]
cpSpaceRehashStatic = chipmunk_lib.cpSpaceRehashStatic
cpSpaceRehashStatic.restype = None
cpSpaceRehashStatic.argtypes = [POINTER(cpSpace)]
cpSpaceStep = chipmunk_lib.cpSpaceStep
cpSpaceStep.restype = None
cpSpaceStep.argtypes = [POINTER(cpSpace), cpFloat]
class cpHandle(Structure):
    pass
cpHandle._fields_ = [
    ('obj', c_void_p),
    ('retain', c_int),
    ('stamp', c_int),
]
class cpSpaceHashBin(Structure):
    pass
cpSpaceHashBin._fields_ = [
    ('handle', POINTER(cpHandle)),
    ('next', POINTER(cpSpaceHashBin)),
]
cpSpaceHashBBFunc = CFUNCTYPE(cpBB, c_void_p)
cpSpaceHash._fields_ = [
    ('numcells', c_int),
    ('celldim', cpFloat),
    ('bbfunc', cpSpaceHashBBFunc),
    ('handleSet', POINTER(cpHashSet)),
    ('table', POINTER(POINTER(cpSpaceHashBin))),
    ('bins', POINTER(cpSpaceHashBin)),
    ('stamp', c_int),
]
cpSpaceHashAlloc = chipmunk_lib.cpSpaceHashAlloc
cpSpaceHashAlloc.restype = POINTER(cpSpaceHash)
cpSpaceHashAlloc.argtypes = []
cpSpaceHashInit = chipmunk_lib.cpSpaceHashInit
cpSpaceHashInit.restype = POINTER(cpSpaceHash)
cpSpaceHashInit.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int, cpSpaceHashBBFunc]
cpSpaceHashNew = chipmunk_lib.cpSpaceHashNew
cpSpaceHashNew.restype = POINTER(cpSpaceHash)
cpSpaceHashNew.argtypes = [cpFloat, c_int, cpSpaceHashBBFunc]
cpSpaceHashDestroy = chipmunk_lib.cpSpaceHashDestroy
cpSpaceHashDestroy.restype = None
cpSpaceHashDestroy.argtypes = [POINTER(cpSpaceHash)]
cpSpaceHashFree = chipmunk_lib.cpSpaceHashFree
cpSpaceHashFree.restype = None
cpSpaceHashFree.argtypes = [POINTER(cpSpaceHash)]
cpSpaceHashResize = chipmunk_lib.cpSpaceHashResize
cpSpaceHashResize.restype = None
cpSpaceHashResize.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int]
cpSpaceHashInsert = chipmunk_lib.cpSpaceHashInsert
cpSpaceHashInsert.restype = None
cpSpaceHashInsert.argtypes = [POINTER(cpSpaceHash), c_void_p, c_uint, cpBB]
cpSpaceHashRemove = chipmunk_lib.cpSpaceHashRemove
cpSpaceHashRemove.restype = None
cpSpaceHashRemove.argtypes = [POINTER(cpSpaceHash), c_void_p, c_uint]
cpSpaceHashIterator = CFUNCTYPE(None, c_void_p, c_void_p)
cpSpaceHashEach = chipmunk_lib.cpSpaceHashEach
cpSpaceHashEach.restype = None
cpSpaceHashEach.argtypes = [POINTER(cpSpaceHash), cpSpaceHashIterator, c_void_p]
cpSpaceHashRehash = chipmunk_lib.cpSpaceHashRehash
cpSpaceHashRehash.restype = None
cpSpaceHashRehash.argtypes = [POINTER(cpSpaceHash)]
cpSpaceHashRehashObject = chipmunk_lib.cpSpaceHashRehashObject
cpSpaceHashRehashObject.restype = None
cpSpaceHashRehashObject.argtypes = [POINTER(cpSpaceHash), c_void_p, c_uint]
cpSpaceHashQueryFunc = CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)
cpSpaceHashQuery = chipmunk_lib.cpSpaceHashQuery
cpSpaceHashQuery.restype = None
cpSpaceHashQuery.argtypes = [POINTER(cpSpaceHash), c_void_p, cpBB, cpSpaceHashQueryFunc, c_void_p]
cpSpaceHashQueryRehash = chipmunk_lib.cpSpaceHashQueryRehash
cpSpaceHashQueryRehash.restype = None
cpSpaceHashQueryRehash.argtypes = [POINTER(cpSpaceHash), cpSpaceHashQueryFunc, c_void_p]
cpvlength = chipmunk_lib.cpvlength
cpvlength.restype = cpFloat
cpvlength.argtypes = [cpVect]
cpvlengthsq = chipmunk_lib.cpvlengthsq
cpvlengthsq.restype = cpFloat
cpvlengthsq.argtypes = [cpVect]
cpvnormalize = chipmunk_lib.cpvnormalize
cpvnormalize.restype = cpVect
cpvnormalize.argtypes = [cpVect]
cpvforangle = chipmunk_lib.cpvforangle
cpvforangle.restype = cpVect
cpvforangle.argtypes = [cpFloat]
cpvtoangle = chipmunk_lib.cpvtoangle
cpvtoangle.restype = cpFloat
cpvtoangle.argtypes = [cpVect]
cpvstr = chipmunk_lib.cpvstr
cpvstr.restype = STRING
cpvstr.argtypes = [cpVect]
CP_HASH_COEF = 3344921057L # Variable c_ulong
__all__ = ['cpSpaceRehashStatic', 'cpSpaceAddCollisionPairFunc',
           'cpSpaceResizeStaticHash', 'cpHashSetReject',
           'cpBodySetAngle', 'cpSpaceRemoveCollisionPairFunc',
           'cpHashSetEach', 'cpContactInit', 'cpArrayIter',
           'cpSpaceHashRehash', 'cpHashSetRemove',
           'cpGrooveJointAlloc', 'cpArray', 'cpSlideJointNew',
           'cpHashSetIterFunc', 'cpShapeType', 'cpArrayDeleteObj',
           'cpPolyShapeAlloc', 'cpArbiterFree', 'cpSpaceRemoveJoint',
           'cpSpace', 'cpArbiterPreStep', 'cpSpaceHashDestroy',
           'cpGrooveJointInit', 'cpBodyAlloc', 'cpSpaceHashAlloc',
           'cpBody', 'cpBodySetMass', 'cpvstr', 'cpMomentForPoly',
           'cpJointDestroy', 'cpSpaceHashNew', 'cpBodyDestroy',
           'cpArrayPush', 'cpSpaceHashFree', 'CP_SEGMENT_SHAPE',
           'cpHashSetNew', 'cpVect', 'cpSpaceHashRemove',
           'cpSpaceHashInit', 'cpBodySlew', 'cpSegmentShapeNew',
           'cpPolyShapeInit', 'CP_HASH_COEF', 'cpPolyShapeNew',
           'cpArrayContains', 'cpHashSetRejectFunc', 'cpSlideJoint',
           'CP_POLY_SHAPE', 'cpBodyUpdateVelocity', 'cpSpaceAlloc',
           'cpCircleShapeAlloc', 'cpPinJointAlloc',
           'cpHashSetDestroy', 'cpSpaceDestroy', 'CP_NUM_SHAPES',
           'cpContact', 'cpDampedSpring', 'cpSegmentShape',
           'cpSlideJointAlloc', 'cpArbiter', 'cpSpaceNew',
           'cpGrooveJoint', 'cpCircleShape', 'cpSpaceFree',
           'cpCircleShapeNew', 'cpSpaceInit', 'cpArrayFree',
           'cpSpaceHashBin', 'cpBBClampVect', 'cpPivotJointNew',
           'cpArrayEach', 'cpBodyFree', 'cpPivotJointInit',
           'cpSpaceRemoveBody', 'cpSpaceHashBBFunc', 'cpHashSetInit',
           'cpArbiterDestroy', 'cpSpaceBodyIterator',
           'cpSpaceAddBody', 'cpBodySetMoment', 'cpHashSetInsert',
           'cpContactsSumImpulsesWithFriction', 'cpShapeFree',
           'cpHashSetBin', 'cpShape', 'cpSpaceRemoveShape',
           'CP_CIRCLE_SHAPE', 'cpSpaceHash', 'cpArbiterNew',
           'cpPinJoint', 'cpvlengthsq', 'cpBBWrapVect', 'cpJointFree',
           'cpArrayInit', 'cpPinJointInit', 'cpSpaceHashResize',
           'cpArbiterInject', 'cpSpaceAddShape', 'cpvnormalize',
           'cpArrayNew', 'cpBodyUpdatePosition', 'cpSpaceHashEach',
           'cpSpaceEachBody', 'cpSpaceSetDefaultCollisionPairFunc',
           'cpHashSetFind', 'cpHashSetEqlFunc', 'cpPolyShapeAxis',
           'cpHashSetTransFunc', 'cpShapeCacheBB', 'cpShapeInit',
           'cpArrayAlloc', 'cpSpaceHashIterator', 'cpSpaceHashQuery',
           'cpMomentForCircle', 'cpvtoangle', 'cpSpaceAddJoint',
           'cpSpaceHashRehashObject', 'cpArbiterApplyImpulse',
           'cpHashSetFree', 'cpContactsSumImpulses',
           'cpCollideShapes', 'cpBodyInit', 'cpCollFunc', 'cpBodyNew',
           'cpSpaceStep', 'cpHashSet', 'cpArbiterAlloc', 'cpFloat',
           'cpPinJointNew', 'MSVC_EVIL_FLOAT_HACK', 'cpPolyShape',
           'cpvforangle', 'cpSpaceFreeChildren', 'cpCollPairFunc',
           'cpArrayDeleteIndex', 'cpBodyResetForces',
           'cpBodyApplyForce', 'cpSpaceHashQueryRehash',
           'cpArbiterInit', 'cpSpaceResizeActiveHash',
           'cpPivotJointAlloc', 'cpSpaceRemoveStaticShape', 'cpJoint',
           'cpResetShapeIdCounter', 'cpPivotJoint',
           'cpSegmentShapeInit', 'cpHashSetAlloc',
           'cpCircleShapeInit', 'cpBB', 'cpSlideJointInit',
           'cpArrayDestroy', 'cpSpaceHashQueryFunc',
           'cpSpaceAddStaticShape', 'cpSegmentShapeAlloc',
           'cpSpaceHashInsert', 'cpShapeDestroy', 'cpInitChipmunk',
           'cpGrooveJointNew', 'cpHandle', 'cpvlength']
