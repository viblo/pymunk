
from ctypes import * 
from .vec2d import Vec2d
cpVect = Vec2d
STRING = c_char_p

from .libload import load_library, platform_specific_functions
try:
    import pymunkoptions
    _lib_debug = pymunkoptions.options["debug"]
except:
    _lib_debug = True #Set to True to print the Chipmunk path.
chipmunk_lib = load_library("chipmunk", debug_lib=_lib_debug)
function_pointer = platform_specific_functions()['function_pointer']


STRING = c_char_p


free = None # symbol removed
free = None # symbol removed
free = None # symbol removed
cpfree = free # alias
cpArbiterStateFirstColl = 0
# cpfpow = pow # alias
# cpfmod = fmod # alias
# cpffloor = floor # alias
# cpfexp = exp # alias
# cpfcos = cos # alias
# cpfceil = ceil # alias
# cpfatan2 = atan2 # alias
# cpfacos = acos # alias
size_t = c_uint
calloc = None # symbol removed
calloc = None # symbol removed
calloc = None # symbol removed
cpcalloc = calloc # alias
# def cpAssertSoft(__condition__,...): return if(!(__condition__)) cpMessage(#__condition__, __FILE__, __LINE__, 1, 0, __VA_ARGS__) # macro
# def cpAssertHard(__condition__,...): return if(!(__condition__)) cpMessage(#__condition__, __FILE__, __LINE__, 1, 1, __VA_ARGS__) # macro
def cpBodyAssertSane(body): return cpBodySanityCheck(body) # macro
# def cpAssertWarn(__condition__,...): return if(!(__condition__)) cpMessage(#__condition__, __FILE__, __LINE__, 0, 0, __VA_ARGS__) # macro
# cpfsqrt = sqrt # alias
cpArbiterStateIgnore = 2
cpArbiterStateCached = 3
realloc = None # symbol removed
realloc = None # symbol removed
realloc = None # symbol removed
cprealloc = realloc # alias
cpArbiterStateNormal = 1
# def cpConstraintCheckCast(constraint,struct): return cpAssertHard(constraint->CP_PRIVATE(klass) == struct ##GetClass(), "Constraint is not a "#struct) # macro
# cpfsin = sin # alias
cpMessage = chipmunk_lib.cpMessage
cpMessage.restype = None
cpMessage.argtypes = [STRING, STRING, c_int, c_int, c_int, STRING]
class cpArray(Structure):
    pass
cpArray._fields_ = [
]
class cpHashSet(Structure):
    pass
cpHashSet._fields_ = [
]
class cpBody(Structure):
    pass
class cpShape(Structure):
    pass
class cpConstraint(Structure):
    pass
class cpCollisionHandler(Structure):
    pass
class cpArbiter(Structure):
    pass
class cpSpace(Structure):
    pass
cpVersionString = (STRING).in_dll(chipmunk_lib, 'cpVersionString')
cpInitChipmunk = chipmunk_lib.cpInitChipmunk
cpInitChipmunk.restype = None
cpInitChipmunk.argtypes = []
cpEnableSegmentToSegmentCollisions = chipmunk_lib.cpEnableSegmentToSegmentCollisions
cpEnableSegmentToSegmentCollisions.restype = None
cpEnableSegmentToSegmentCollisions.argtypes = []
cpFloat = c_double
#cpVect class def removed
cpMomentForCircle = chipmunk_lib.cpMomentForCircle
cpMomentForCircle.restype = cpFloat
cpMomentForCircle.argtypes = [cpFloat, cpFloat, cpFloat, cpVect]
cpAreaForCircle = chipmunk_lib.cpAreaForCircle
cpAreaForCircle.restype = cpFloat
cpAreaForCircle.argtypes = [cpFloat, cpFloat]
cpMomentForSegment = chipmunk_lib.cpMomentForSegment
cpMomentForSegment.restype = cpFloat
cpMomentForSegment.argtypes = [cpFloat, cpVect, cpVect]
cpAreaForSegment = chipmunk_lib.cpAreaForSegment
cpAreaForSegment.restype = cpFloat
cpAreaForSegment.argtypes = [cpVect, cpVect, cpFloat]
cpMomentForPoly = chipmunk_lib.cpMomentForPoly
cpMomentForPoly.restype = cpFloat
cpMomentForPoly.argtypes = [cpFloat, c_int, POINTER(cpVect), cpVect]
cpAreaForPoly = chipmunk_lib.cpAreaForPoly
cpAreaForPoly.restype = cpFloat
cpAreaForPoly.argtypes = [c_int, POINTER(cpVect)]
cpCentroidForPoly = chipmunk_lib.cpCentroidForPoly
cpCentroidForPoly.restype = cpVect
cpCentroidForPoly.argtypes = [c_int, POINTER(cpVect)]
cpRecenterPoly = chipmunk_lib.cpRecenterPoly
cpRecenterPoly.restype = None
cpRecenterPoly.argtypes = [c_int, POINTER(cpVect)]
cpMomentForBox = chipmunk_lib.cpMomentForBox
cpMomentForBox.restype = cpFloat
cpMomentForBox.argtypes = [cpFloat, cpFloat, cpFloat]
class cpBB(Structure):
    pass
cpMomentForBox2 = chipmunk_lib.cpMomentForBox2
cpMomentForBox2.restype = cpFloat
cpMomentForBox2.argtypes = [cpFloat, cpBB]
cpConvexHull = chipmunk_lib.cpConvexHull
cpConvexHull.restype = c_int
cpConvexHull.argtypes = [c_int, POINTER(cpVect), POINTER(cpVect), POINTER(c_int), cpFloat]

if sizeof(c_void_p) == 4: uintptr_t = c_uint 
else: uintptr_t = c_ulonglong

cpHashValue = uintptr_t
uint32_t = c_uint32
cpCollisionID = uint32_t
cpBool = c_int
cpDataPointer = c_void_p
cpCollisionType = uintptr_t
cpGroup = uintptr_t
cpLayers = c_uint
cpTimestamp = c_uint
#cpVect._pack_ = 4
#cpVect _fields_ def removed
class cpMat2x2(Structure):
    pass
#cpMat2x2._pack_ = 4
cpMat2x2._fields_ = [
    ('a', cpFloat),
    ('b', cpFloat),
    ('c', cpFloat),
    ('d', cpFloat),
]
cpCircleShapeSetRadius = chipmunk_lib.cpCircleShapeSetRadius
cpCircleShapeSetRadius.restype = None
cpCircleShapeSetRadius.argtypes = [POINTER(cpShape), cpFloat]
cpCircleShapeSetOffset = chipmunk_lib.cpCircleShapeSetOffset
cpCircleShapeSetOffset.restype = None
cpCircleShapeSetOffset.argtypes = [POINTER(cpShape), cpVect]
cpSegmentShapeSetEndpoints = chipmunk_lib.cpSegmentShapeSetEndpoints
cpSegmentShapeSetEndpoints.restype = None
cpSegmentShapeSetEndpoints.argtypes = [POINTER(cpShape), cpVect, cpVect]
cpSegmentShapeSetRadius = chipmunk_lib.cpSegmentShapeSetRadius
cpSegmentShapeSetRadius.restype = None
cpSegmentShapeSetRadius.argtypes = [POINTER(cpShape), cpFloat]
cpPolyShapeSetVerts = chipmunk_lib.cpPolyShapeSetVerts
cpPolyShapeSetVerts.restype = None
cpPolyShapeSetVerts.argtypes = [POINTER(cpShape), c_int, POINTER(cpVect), cpVect]
cpPolyShapeSetRadius = chipmunk_lib.cpPolyShapeSetRadius
cpPolyShapeSetRadius.restype = None
cpPolyShapeSetRadius.argtypes = [POINTER(cpShape), cpFloat]
class cpConstraintClass(Structure):
    pass
cpConstraintPreStepImpl = function_pointer(None, POINTER(cpConstraint), cpFloat)
cpConstraintApplyCachedImpulseImpl = function_pointer(None, POINTER(cpConstraint), cpFloat)
cpConstraintApplyImpulseImpl = function_pointer(None, POINTER(cpConstraint), cpFloat)
cpConstraintGetImpulseImpl = function_pointer(cpFloat, POINTER(cpConstraint))
cpConstraintClass._fields_ = [
    ('preStep', cpConstraintPreStepImpl),
    ('applyCachedImpulse', cpConstraintApplyCachedImpulseImpl),
    ('applyImpulse', cpConstraintApplyImpulseImpl),
    ('getImpulse', cpConstraintGetImpulseImpl),
]
cpConstraintPreSolveFunc = function_pointer(None, POINTER(cpConstraint), POINTER(cpSpace))
cpConstraintPostSolveFunc = function_pointer(None, POINTER(cpConstraint), POINTER(cpSpace))
#cpConstraint._pack_ = 4
cpConstraint._fields_ = [
    ('klass_private', POINTER(cpConstraintClass)),
    ('a', POINTER(cpBody)),
    ('b', POINTER(cpBody)),
    ('space_private', POINTER(cpSpace)),
    ('next_a_private', POINTER(cpConstraint)),
    ('next_b_private', POINTER(cpConstraint)),
    ('maxForce', cpFloat),
    ('errorBias', cpFloat),
    ('maxBias', cpFloat),
    ('preSolve', cpConstraintPreSolveFunc),
    ('postSolve', cpConstraintPostSolveFunc),
    ('data', cpDataPointer),
]
cpConstraintDestroy = chipmunk_lib.cpConstraintDestroy
cpConstraintDestroy.restype = None
cpConstraintDestroy.argtypes = [POINTER(cpConstraint)]
cpConstraintFree = chipmunk_lib.cpConstraintFree
cpConstraintFree.restype = None
cpConstraintFree.argtypes = [POINTER(cpConstraint)]
cpDampedRotarySpringTorqueFunc = function_pointer(cpFloat, POINTER(cpConstraint), cpFloat)
cpDampedRotarySpringGetClass = chipmunk_lib.cpDampedRotarySpringGetClass
cpDampedRotarySpringGetClass.restype = POINTER(cpConstraintClass)
cpDampedRotarySpringGetClass.argtypes = []
class cpDampedRotarySpring(Structure):
    pass
#cpDampedRotarySpring._pack_ = 4
cpDampedRotarySpring._fields_ = [
    ('constraint', cpConstraint),
    ('restAngle', cpFloat),
    ('stiffness', cpFloat),
    ('damping', cpFloat),
    ('springTorqueFunc', cpDampedRotarySpringTorqueFunc),
    ('target_wrn', cpFloat),
    ('w_coef', cpFloat),
    ('iSum', cpFloat),
    ('jAcc', cpFloat),
]
cpDampedRotarySpringAlloc = chipmunk_lib.cpDampedRotarySpringAlloc
cpDampedRotarySpringAlloc.restype = POINTER(cpDampedRotarySpring)
cpDampedRotarySpringAlloc.argtypes = []
cpDampedRotarySpringInit = chipmunk_lib.cpDampedRotarySpringInit
cpDampedRotarySpringInit.restype = POINTER(cpDampedRotarySpring)
cpDampedRotarySpringInit.argtypes = [POINTER(cpDampedRotarySpring), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat, cpFloat]
cpDampedRotarySpringNew = chipmunk_lib.cpDampedRotarySpringNew
cpDampedRotarySpringNew.restype = POINTER(cpConstraint)
cpDampedRotarySpringNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat, cpFloat]
class cpDampedSpring(Structure):
    pass
cpDampedSpringForceFunc = function_pointer(cpFloat, POINTER(cpConstraint), cpFloat)
cpDampedSpringGetClass = chipmunk_lib.cpDampedSpringGetClass
cpDampedSpringGetClass.restype = POINTER(cpConstraintClass)
cpDampedSpringGetClass.argtypes = []
#cpDampedSpring._pack_ = 4
cpDampedSpring._fields_ = [
    ('constraint', cpConstraint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('restLength', cpFloat),
    ('stiffness', cpFloat),
    ('damping', cpFloat),
    ('springForceFunc', cpDampedSpringForceFunc),
    ('target_vrn', cpFloat),
    ('v_coef', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('nMass', cpFloat),
    ('n', cpVect),
    ('jAcc', cpFloat),
]
cpDampedSpringAlloc = chipmunk_lib.cpDampedSpringAlloc
cpDampedSpringAlloc.restype = POINTER(cpDampedSpring)
cpDampedSpringAlloc.argtypes = []
cpDampedSpringInit = chipmunk_lib.cpDampedSpringInit
cpDampedSpringInit.restype = POINTER(cpDampedSpring)
cpDampedSpringInit.argtypes = [POINTER(cpDampedSpring), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat]
cpDampedSpringNew = chipmunk_lib.cpDampedSpringNew
cpDampedSpringNew.restype = POINTER(cpConstraint)
cpDampedSpringNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat]
cpGearJointGetClass = chipmunk_lib.cpGearJointGetClass
cpGearJointGetClass.restype = POINTER(cpConstraintClass)
cpGearJointGetClass.argtypes = []
class cpGearJoint(Structure):
    pass
#cpGearJoint._pack_ = 4
cpGearJoint._fields_ = [
    ('constraint', cpConstraint),
    ('phase', cpFloat),
    ('ratio', cpFloat),
    ('ratio_inv', cpFloat),
    ('iSum', cpFloat),
    ('bias', cpFloat),
    ('jAcc', cpFloat),
]
cpGearJointAlloc = chipmunk_lib.cpGearJointAlloc
cpGearJointAlloc.restype = POINTER(cpGearJoint)
cpGearJointAlloc.argtypes = []
cpGearJointInit = chipmunk_lib.cpGearJointInit
cpGearJointInit.restype = POINTER(cpGearJoint)
cpGearJointInit.argtypes = [POINTER(cpGearJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpGearJointNew = chipmunk_lib.cpGearJointNew
cpGearJointNew.restype = POINTER(cpConstraint)
cpGearJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpGearJointSetRatio = chipmunk_lib.cpGearJointSetRatio
cpGearJointSetRatio.restype = None
cpGearJointSetRatio.argtypes = [POINTER(cpConstraint), cpFloat]
cpGrooveJointGetClass = chipmunk_lib.cpGrooveJointGetClass
cpGrooveJointGetClass.restype = POINTER(cpConstraintClass)
cpGrooveJointGetClass.argtypes = []
class cpGrooveJoint(Structure):
    pass
#cpGrooveJoint._pack_ = 4
cpGrooveJoint._fields_ = [
    ('constraint', cpConstraint),
    ('grv_n', cpVect),
    ('grv_a', cpVect),
    ('grv_b', cpVect),
    ('anchr2', cpVect),
    ('grv_tn', cpVect),
    ('clamp', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('k', cpMat2x2),
    ('jAcc', cpVect),
    ('bias', cpVect),
]
cpGrooveJointAlloc = chipmunk_lib.cpGrooveJointAlloc
cpGrooveJointAlloc.restype = POINTER(cpGrooveJoint)
cpGrooveJointAlloc.argtypes = []
cpGrooveJointInit = chipmunk_lib.cpGrooveJointInit
cpGrooveJointInit.restype = POINTER(cpGrooveJoint)
cpGrooveJointInit.argtypes = [POINTER(cpGrooveJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
cpGrooveJointNew = chipmunk_lib.cpGrooveJointNew
cpGrooveJointNew.restype = POINTER(cpConstraint)
cpGrooveJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
cpGrooveJointSetGrooveA = chipmunk_lib.cpGrooveJointSetGrooveA
cpGrooveJointSetGrooveA.restype = None
cpGrooveJointSetGrooveA.argtypes = [POINTER(cpConstraint), cpVect]
cpGrooveJointSetGrooveB = chipmunk_lib.cpGrooveJointSetGrooveB
cpGrooveJointSetGrooveB.restype = None
cpGrooveJointSetGrooveB.argtypes = [POINTER(cpConstraint), cpVect]
cpPinJointGetClass = chipmunk_lib.cpPinJointGetClass
cpPinJointGetClass.restype = POINTER(cpConstraintClass)
cpPinJointGetClass.argtypes = []
class cpPinJoint(Structure):
    pass
#cpPinJoint._pack_ = 4
cpPinJoint._fields_ = [
    ('constraint', cpConstraint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('dist', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('n', cpVect),
    ('nMass', cpFloat),
    ('jnAcc', cpFloat),
    ('bias', cpFloat),
]
cpPinJointAlloc = chipmunk_lib.cpPinJointAlloc
cpPinJointAlloc.restype = POINTER(cpPinJoint)
cpPinJointAlloc.argtypes = []
cpPinJointInit = chipmunk_lib.cpPinJointInit
cpPinJointInit.restype = POINTER(cpPinJoint)
cpPinJointInit.argtypes = [POINTER(cpPinJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPinJointNew = chipmunk_lib.cpPinJointNew
cpPinJointNew.restype = POINTER(cpConstraint)
cpPinJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPivotJointGetClass = chipmunk_lib.cpPivotJointGetClass
cpPivotJointGetClass.restype = POINTER(cpConstraintClass)
cpPivotJointGetClass.argtypes = []
class cpPivotJoint(Structure):
    pass
cpPivotJoint._fields_ = [
    ('constraint', cpConstraint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('r1', cpVect),
    ('r2', cpVect),
    ('k', cpMat2x2),
    ('jAcc', cpVect),
    ('bias', cpVect),
]
cpPivotJointAlloc = chipmunk_lib.cpPivotJointAlloc
cpPivotJointAlloc.restype = POINTER(cpPivotJoint)
cpPivotJointAlloc.argtypes = []
cpPivotJointInit = chipmunk_lib.cpPivotJointInit
cpPivotJointInit.restype = POINTER(cpPivotJoint)
cpPivotJointInit.argtypes = [POINTER(cpPivotJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPivotJointNew = chipmunk_lib.cpPivotJointNew
cpPivotJointNew.restype = POINTER(cpConstraint)
cpPivotJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect]
cpPivotJointNew2 = chipmunk_lib.cpPivotJointNew2
cpPivotJointNew2.restype = POINTER(cpConstraint)
cpPivotJointNew2.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpRatchetJointGetClass = chipmunk_lib.cpRatchetJointGetClass
cpRatchetJointGetClass.restype = POINTER(cpConstraintClass)
cpRatchetJointGetClass.argtypes = []
class cpRatchetJoint(Structure):
    pass
#cpRatchetJoint._pack_ = 4
cpRatchetJoint._fields_ = [
    ('constraint', cpConstraint),
    ('angle', cpFloat),
    ('phase', cpFloat),
    ('ratchet', cpFloat),
    ('iSum', cpFloat),
    ('bias', cpFloat),
    ('jAcc', cpFloat),
]
cpRatchetJointAlloc = chipmunk_lib.cpRatchetJointAlloc
cpRatchetJointAlloc.restype = POINTER(cpRatchetJoint)
cpRatchetJointAlloc.argtypes = []
cpRatchetJointInit = chipmunk_lib.cpRatchetJointInit
cpRatchetJointInit.restype = POINTER(cpRatchetJoint)
cpRatchetJointInit.argtypes = [POINTER(cpRatchetJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRatchetJointNew = chipmunk_lib.cpRatchetJointNew
cpRatchetJointNew.restype = POINTER(cpConstraint)
cpRatchetJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRotaryLimitJointGetClass = chipmunk_lib.cpRotaryLimitJointGetClass
cpRotaryLimitJointGetClass.restype = POINTER(cpConstraintClass)
cpRotaryLimitJointGetClass.argtypes = []
class cpRotaryLimitJoint(Structure):
    pass
#cpRotaryLimitJoint._pack_ = 4
cpRotaryLimitJoint._fields_ = [
    ('constraint', cpConstraint),
    ('min', cpFloat),
    ('max', cpFloat),
    ('iSum', cpFloat),
    ('bias', cpFloat),
    ('jAcc', cpFloat),
]
cpRotaryLimitJointAlloc = chipmunk_lib.cpRotaryLimitJointAlloc
cpRotaryLimitJointAlloc.restype = POINTER(cpRotaryLimitJoint)
cpRotaryLimitJointAlloc.argtypes = []
cpRotaryLimitJointInit = chipmunk_lib.cpRotaryLimitJointInit
cpRotaryLimitJointInit.restype = POINTER(cpRotaryLimitJoint)
cpRotaryLimitJointInit.argtypes = [POINTER(cpRotaryLimitJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRotaryLimitJointNew = chipmunk_lib.cpRotaryLimitJointNew
cpRotaryLimitJointNew.restype = POINTER(cpConstraint)
cpRotaryLimitJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpSimpleMotorGetClass = chipmunk_lib.cpSimpleMotorGetClass
cpSimpleMotorGetClass.restype = POINTER(cpConstraintClass)
cpSimpleMotorGetClass.argtypes = []
class cpSimpleMotor(Structure):
    pass
#cpSimpleMotor._pack_ = 4
cpSimpleMotor._fields_ = [
    ('constraint', cpConstraint),
    ('rate', cpFloat),
    ('iSum', cpFloat),
    ('jAcc', cpFloat),
]
cpSimpleMotorAlloc = chipmunk_lib.cpSimpleMotorAlloc
cpSimpleMotorAlloc.restype = POINTER(cpSimpleMotor)
cpSimpleMotorAlloc.argtypes = []
cpSimpleMotorInit = chipmunk_lib.cpSimpleMotorInit
cpSimpleMotorInit.restype = POINTER(cpSimpleMotor)
cpSimpleMotorInit.argtypes = [POINTER(cpSimpleMotor), POINTER(cpBody), POINTER(cpBody), cpFloat]
cpSimpleMotorNew = chipmunk_lib.cpSimpleMotorNew
cpSimpleMotorNew.restype = POINTER(cpConstraint)
cpSimpleMotorNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat]
cpSlideJointGetClass = chipmunk_lib.cpSlideJointGetClass
cpSlideJointGetClass.restype = POINTER(cpConstraintClass)
cpSlideJointGetClass.argtypes = []
class cpSlideJoint(Structure):
    pass
#cpSlideJoint._pack_ = 4
cpSlideJoint._fields_ = [
    ('constraint', cpConstraint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('min', cpFloat),
    ('max', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('n', cpVect),
    ('nMass', cpFloat),
    ('jnAcc', cpFloat),
    ('bias', cpFloat),
]
cpSlideJointAlloc = chipmunk_lib.cpSlideJointAlloc
cpSlideJointAlloc.restype = POINTER(cpSlideJoint)
cpSlideJointAlloc.argtypes = []
cpSlideJointInit = chipmunk_lib.cpSlideJointInit
cpSlideJointInit.restype = POINTER(cpSlideJoint)
cpSlideJointInit.argtypes = [POINTER(cpSlideJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpSlideJointNew = chipmunk_lib.cpSlideJointNew
cpSlideJointNew.restype = POINTER(cpConstraint)
cpSlideJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpCollisionBeginFunc = function_pointer(cpBool, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
cpCollisionPreSolveFunc = function_pointer(cpBool, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
cpCollisionPostSolveFunc = function_pointer(None, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
cpCollisionSeparateFunc = function_pointer(None, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
cpCollisionHandler._fields_ = [
    ('a', cpCollisionType),
    ('b', cpCollisionType),
    ('begin', cpCollisionBeginFunc),
    ('preSolve', cpCollisionPreSolveFunc),
    ('postSolve', cpCollisionPostSolveFunc),
    ('separate', cpCollisionSeparateFunc),
    ('data', c_void_p),
]
class cpContact(Structure):
    pass
cpContact._fields_ = [
]

# values for enumeration 'cpArbiterState'
cpArbiterState = c_int # enum
class cpArbiterThread(Structure):
    pass
cpArbiterThread._fields_ = [
    ('next', POINTER(cpArbiter)),
    ('prev', POINTER(cpArbiter)),
]
#cpArbiter._pack_ = 4
cpArbiter._fields_ = [
    ('e', cpFloat),
    ('u', cpFloat),
    ('surface_vr', cpVect),
    ('data', cpDataPointer),
    ('a_private', POINTER(cpShape)),
    ('b_private', POINTER(cpShape)),
    ('body_a_private', POINTER(cpBody)),
    ('body_b_private', POINTER(cpBody)),
    ('thread_a_private', cpArbiterThread),
    ('thread_b_private', cpArbiterThread),
    ('numContacts_private', c_int),
    ('contacts_private', POINTER(cpContact)),
    ('stamp_private', cpTimestamp),
    ('handler_private', POINTER(cpCollisionHandler)),
    ('swappedColl_private', cpBool),
    ('state_private', cpArbiterState),
]
cpArbiterGetSurfaceVelocity = chipmunk_lib.cpArbiterGetSurfaceVelocity
cpArbiterGetSurfaceVelocity.restype = cpVect
cpArbiterGetSurfaceVelocity.argtypes = [POINTER(cpArbiter)]
cpArbiterSetSurfaceVelocity = chipmunk_lib.cpArbiterSetSurfaceVelocity
cpArbiterSetSurfaceVelocity.restype = None
cpArbiterSetSurfaceVelocity.argtypes = [POINTER(cpArbiter), cpVect]
cpArbiterTotalImpulse = chipmunk_lib.cpArbiterTotalImpulse
cpArbiterTotalImpulse.restype = cpVect
cpArbiterTotalImpulse.argtypes = [POINTER(cpArbiter)]
cpArbiterTotalImpulseWithFriction = chipmunk_lib.cpArbiterTotalImpulseWithFriction
cpArbiterTotalImpulseWithFriction.restype = cpVect
cpArbiterTotalImpulseWithFriction.argtypes = [POINTER(cpArbiter)]
cpArbiterTotalKE = chipmunk_lib.cpArbiterTotalKE
cpArbiterTotalKE.restype = cpFloat
cpArbiterTotalKE.argtypes = [POINTER(cpArbiter)]
cpArbiterIgnore = chipmunk_lib.cpArbiterIgnore
cpArbiterIgnore.restype = None
cpArbiterIgnore.argtypes = [POINTER(cpArbiter)]
class cpContactPointSet(Structure):
    pass
class N17cpContactPointSet4DOT_25E(Structure):
    pass
#N17cpContactPointSet4DOT_25E._pack_ = 4
N17cpContactPointSet4DOT_25E._fields_ = [
    ('point', cpVect),
    ('normal', cpVect),
    ('dist', cpFloat),
]
cpContactPointSet._fields_ = [
    ('count', c_int),
    ('points', N17cpContactPointSet4DOT_25E * 2),
]
cpArbiterGetContactPointSet = chipmunk_lib.cpArbiterGetContactPointSet
cpArbiterGetContactPointSet.restype = cpContactPointSet
cpArbiterGetContactPointSet.argtypes = [POINTER(cpArbiter)]
cpArbiterSetContactPointSet = chipmunk_lib.cpArbiterSetContactPointSet
cpArbiterSetContactPointSet.restype = None
cpArbiterSetContactPointSet.argtypes = [POINTER(cpArbiter), POINTER(cpContactPointSet)]
cpArbiterIsFirstContact = chipmunk_lib.cpArbiterIsFirstContact
cpArbiterIsFirstContact.restype = cpBool
cpArbiterIsFirstContact.argtypes = [POINTER(cpArbiter)]
cpArbiterGetCount = chipmunk_lib.cpArbiterGetCount
cpArbiterGetCount.restype = c_int
cpArbiterGetCount.argtypes = [POINTER(cpArbiter)]
cpArbiterGetNormal = chipmunk_lib.cpArbiterGetNormal
cpArbiterGetNormal.restype = cpVect
cpArbiterGetNormal.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterGetPoint = chipmunk_lib.cpArbiterGetPoint
cpArbiterGetPoint.restype = cpVect
cpArbiterGetPoint.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterGetDepth = chipmunk_lib.cpArbiterGetDepth
cpArbiterGetDepth.restype = cpFloat
cpArbiterGetDepth.argtypes = [POINTER(cpArbiter), c_int]
#cpBB._pack_ = 4
cpBB._fields_ = [
    ('l', cpFloat),
    ('b', cpFloat),
    ('r', cpFloat),
    ('t', cpFloat),
]
cpBBWrapVect = chipmunk_lib.cpBBWrapVect
cpBBWrapVect.restype = cpVect
cpBBWrapVect.argtypes = [cpBB, cpVect]
cpBodyVelocityFunc = function_pointer(None, POINTER(cpBody), cpVect, cpFloat, cpFloat)
cpBodyPositionFunc = function_pointer(None, POINTER(cpBody), cpFloat)
class cpComponentNode(Structure):
    pass
#cpComponentNode._pack_ = 4
cpComponentNode._fields_ = [
    ('root', POINTER(cpBody)),
    ('next', POINTER(cpBody)),
    ('idleTime', cpFloat),
]
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
    ('data', cpDataPointer),
    ('v_limit', cpFloat),
    ('w_limit', cpFloat),
    ('v_bias_private', cpVect),
    ('w_bias_private', cpFloat),
    ('space_private', POINTER(cpSpace)),
    ('shapeList_private', POINTER(cpShape)),
    ('arbiterList_private', POINTER(cpArbiter)),
    ('constraintList_private', POINTER(cpConstraint)),
    ('node_private', cpComponentNode),
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
cpBodyInitStatic = chipmunk_lib.cpBodyInitStatic
cpBodyInitStatic.restype = POINTER(cpBody)
cpBodyInitStatic.argtypes = [POINTER(cpBody)]
cpBodyNewStatic = chipmunk_lib.cpBodyNewStatic
cpBodyNewStatic.restype = POINTER(cpBody)
cpBodyNewStatic.argtypes = []
cpBodyDestroy = chipmunk_lib.cpBodyDestroy
cpBodyDestroy.restype = None
cpBodyDestroy.argtypes = [POINTER(cpBody)]
cpBodyFree = chipmunk_lib.cpBodyFree
cpBodyFree.restype = None
cpBodyFree.argtypes = [POINTER(cpBody)]
cpBodySanityCheck = chipmunk_lib.cpBodySanityCheck
cpBodySanityCheck.restype = None
cpBodySanityCheck.argtypes = [POINTER(cpBody)]
cpBodyActivate = chipmunk_lib.cpBodyActivate
cpBodyActivate.restype = None
cpBodyActivate.argtypes = [POINTER(cpBody)]
cpBodyActivateStatic = chipmunk_lib.cpBodyActivateStatic
cpBodyActivateStatic.restype = None
cpBodyActivateStatic.argtypes = [POINTER(cpBody), POINTER(cpShape)]
cpBodySleep = chipmunk_lib.cpBodySleep
cpBodySleep.restype = None
cpBodySleep.argtypes = [POINTER(cpBody)]
cpBodySleepWithGroup = chipmunk_lib.cpBodySleepWithGroup
cpBodySleepWithGroup.restype = None
cpBodySleepWithGroup.argtypes = [POINTER(cpBody), POINTER(cpBody)]
cpBodySetMass = chipmunk_lib.cpBodySetMass
cpBodySetMass.restype = None
cpBodySetMass.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetMoment = chipmunk_lib.cpBodySetMoment
cpBodySetMoment.restype = None
cpBodySetMoment.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetPos = chipmunk_lib.cpBodySetPos
cpBodySetPos.restype = None
cpBodySetPos.argtypes = [POINTER(cpBody), cpVect]
cpBodySetAngle = chipmunk_lib.cpBodySetAngle
cpBodySetAngle.restype = None
cpBodySetAngle.argtypes = [POINTER(cpBody), cpFloat]
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
cpBodyApplyImpulse = chipmunk_lib.cpBodyApplyImpulse
cpBodyApplyImpulse.restype = None
cpBodyApplyImpulse.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpBodyGetVelAtWorldPoint = chipmunk_lib.cpBodyGetVelAtWorldPoint
cpBodyGetVelAtWorldPoint.restype = cpVect
cpBodyGetVelAtWorldPoint.argtypes = [POINTER(cpBody), cpVect]
cpBodyGetVelAtLocalPoint = chipmunk_lib.cpBodyGetVelAtLocalPoint
cpBodyGetVelAtLocalPoint.restype = cpVect
cpBodyGetVelAtLocalPoint.argtypes = [POINTER(cpBody), cpVect]
cpBodyShapeIteratorFunc = function_pointer(None, POINTER(cpBody), POINTER(cpShape), c_void_p)
cpBodyEachShape = chipmunk_lib.cpBodyEachShape
cpBodyEachShape.restype = None
cpBodyEachShape.argtypes = [POINTER(cpBody), cpBodyShapeIteratorFunc, c_void_p]
cpBodyConstraintIteratorFunc = function_pointer(None, POINTER(cpBody), POINTER(cpConstraint), c_void_p)
cpBodyEachConstraint = chipmunk_lib.cpBodyEachConstraint
cpBodyEachConstraint.restype = None
cpBodyEachConstraint.argtypes = [POINTER(cpBody), cpBodyConstraintIteratorFunc, c_void_p]
cpBodyArbiterIteratorFunc = function_pointer(None, POINTER(cpBody), POINTER(cpArbiter), c_void_p)
cpBodyEachArbiter = chipmunk_lib.cpBodyEachArbiter
cpBodyEachArbiter.restype = None
cpBodyEachArbiter.argtypes = [POINTER(cpBody), cpBodyArbiterIteratorFunc, c_void_p]
class cpSplittingPlane(Structure):
    pass
#cpSplittingPlane._pack_ = 4
cpSplittingPlane._fields_ = [
    ('n', cpVect),
    ('d', cpFloat),
]
class cpPolyShape(Structure):
    pass
class cpShapeClass(Structure):
    pass
#cpShape._pack_ = 4
cpShape._fields_ = [
    ('klass_private', POINTER(cpShapeClass)),
    ('body', POINTER(cpBody)),
    ('bb', cpBB),
    ('sensor', cpBool),
    ('e', cpFloat),
    ('u', cpFloat),
    ('surface_v', cpVect),
    ('data', cpDataPointer),
    ('collision_type', cpCollisionType),
    ('group', cpGroup),
    ('layers', cpLayers),
    ('space_private', POINTER(cpSpace)),
    ('next_private', POINTER(cpShape)),
    ('prev_private', POINTER(cpShape)),
    ('hashid_private', cpHashValue),
]
#cpPolyShape._pack_ = 4
cpPolyShape._fields_ = [
    ('shape', cpShape),
    ('numVerts', c_int),
    ('verts', POINTER(cpVect)),
    ('tVerts', POINTER(cpVect)),
    ('planes', POINTER(cpSplittingPlane)),
    ('tPlanes', POINTER(cpSplittingPlane)),
    ('r', cpFloat),
]
cpPolyShapeAlloc = chipmunk_lib.cpPolyShapeAlloc
cpPolyShapeAlloc.restype = POINTER(cpPolyShape)
cpPolyShapeAlloc.argtypes = []
cpPolyShapeInit = chipmunk_lib.cpPolyShapeInit
cpPolyShapeInit.restype = POINTER(cpPolyShape)
cpPolyShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpPolyShapeInit2 = chipmunk_lib.cpPolyShapeInit2
cpPolyShapeInit2.restype = POINTER(cpPolyShape)
cpPolyShapeInit2.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), c_int, POINTER(cpVect), cpVect, cpFloat]
cpPolyShapeNew = chipmunk_lib.cpPolyShapeNew
cpPolyShapeNew.restype = POINTER(cpShape)
cpPolyShapeNew.argtypes = [POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpPolyShapeNew2 = chipmunk_lib.cpPolyShapeNew2
cpPolyShapeNew2.restype = POINTER(cpShape)
cpPolyShapeNew2.argtypes = [POINTER(cpBody), c_int, POINTER(cpVect), cpVect, cpFloat]
cpBoxShapeInit = chipmunk_lib.cpBoxShapeInit
cpBoxShapeInit.restype = POINTER(cpPolyShape)
cpBoxShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpFloat, cpFloat]
cpBoxShapeInit2 = chipmunk_lib.cpBoxShapeInit2
cpBoxShapeInit2.restype = POINTER(cpPolyShape)
cpBoxShapeInit2.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpBB]
cpBoxShapeInit3 = chipmunk_lib.cpBoxShapeInit3
cpBoxShapeInit3.restype = POINTER(cpPolyShape)
cpBoxShapeInit3.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpBB, cpFloat]
cpBoxShapeNew = chipmunk_lib.cpBoxShapeNew
cpBoxShapeNew.restype = POINTER(cpShape)
cpBoxShapeNew.argtypes = [POINTER(cpBody), cpFloat, cpFloat]
cpBoxShapeNew2 = chipmunk_lib.cpBoxShapeNew2
cpBoxShapeNew2.restype = POINTER(cpShape)
cpBoxShapeNew2.argtypes = [POINTER(cpBody), cpBB]
cpPolyValidate = chipmunk_lib.cpPolyValidate
cpPolyValidate.restype = cpBool
cpPolyValidate.argtypes = [POINTER(cpVect), c_int]
cpPolyShapeGetNumVerts = chipmunk_lib.cpPolyShapeGetNumVerts
cpPolyShapeGetNumVerts.restype = c_int
cpPolyShapeGetNumVerts.argtypes = [POINTER(cpShape)]
cpPolyShapeGetVert = chipmunk_lib.cpPolyShapeGetVert
cpPolyShapeGetVert.restype = cpVect
cpPolyShapeGetVert.argtypes = [POINTER(cpShape), c_int]
cpPolyShapeGetRadius = chipmunk_lib.cpPolyShapeGetRadius
cpPolyShapeGetRadius.restype = cpFloat
cpPolyShapeGetRadius.argtypes = [POINTER(cpShape)]
class cpNearestPointQueryInfo(Structure):
    pass
#cpNearestPointQueryInfo._pack_ = 4
cpNearestPointQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('p', cpVect),
    ('d', cpFloat),
    ('g', cpVect),
]
class cpSegmentQueryInfo(Structure):
    pass
#cpSegmentQueryInfo._pack_ = 4
cpSegmentQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('t', cpFloat),
    ('n', cpVect),
]

# values for enumeration 'cpShapeType'
CP_CIRCLE_SHAPE = 0
CP_SEGMENT_SHAPE = 1
CP_POLY_SHAPE = 2
CP_NUM_SHAPES = 3
cpShapeType = c_int # enum
cpShapeCacheDataImpl = function_pointer(cpBB, POINTER(cpShape), cpVect, cpVect)
cpShapeDestroyImpl = function_pointer(None, POINTER(cpShape))
cpShapeNearestPointQueryImpl = function_pointer(None, POINTER(cpShape), cpVect, POINTER(cpNearestPointQueryInfo))
cpShapeSegmentQueryImpl = function_pointer(None, POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo))
cpShapeClass._fields_ = [
    ('type', cpShapeType),
    ('cacheData', cpShapeCacheDataImpl),
    ('destroy', cpShapeDestroyImpl),
    ('nearestPointQuery', cpShapeNearestPointQueryImpl),
    ('segmentQuery', cpShapeSegmentQueryImpl),
]
cpShapeDestroy = chipmunk_lib.cpShapeDestroy
cpShapeDestroy.restype = None
cpShapeDestroy.argtypes = [POINTER(cpShape)]
cpShapeFree = chipmunk_lib.cpShapeFree
cpShapeFree.restype = None
cpShapeFree.argtypes = [POINTER(cpShape)]
cpShapeCacheBB = chipmunk_lib.cpShapeCacheBB
cpShapeCacheBB.restype = cpBB
cpShapeCacheBB.argtypes = [POINTER(cpShape)]
cpShapeUpdate = chipmunk_lib.cpShapeUpdate
cpShapeUpdate.restype = cpBB
cpShapeUpdate.argtypes = [POINTER(cpShape), cpVect, cpVect]
cpShapePointQuery = chipmunk_lib.cpShapePointQuery
cpShapePointQuery.restype = cpBool
cpShapePointQuery.argtypes = [POINTER(cpShape), cpVect]
cpShapeNearestPointQuery = chipmunk_lib.cpShapeNearestPointQuery
cpShapeNearestPointQuery.restype = cpFloat
cpShapeNearestPointQuery.argtypes = [POINTER(cpShape), cpVect, POINTER(cpNearestPointQueryInfo)]
cpShapeSegmentQuery = chipmunk_lib.cpShapeSegmentQuery
cpShapeSegmentQuery.restype = cpBool
cpShapeSegmentQuery.argtypes = [POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo)]
cpShapeSetBody = chipmunk_lib.cpShapeSetBody
cpShapeSetBody.restype = None
cpShapeSetBody.argtypes = [POINTER(cpShape), POINTER(cpBody)]
cpResetShapeIdCounter = chipmunk_lib.cpResetShapeIdCounter
cpResetShapeIdCounter.restype = None
cpResetShapeIdCounter.argtypes = []
class cpCircleShape(Structure):
    pass
#cpCircleShape._pack_ = 4
cpCircleShape._fields_ = [
    ('shape', cpShape),
    ('c', cpVect),
    ('tc', cpVect),
    ('r', cpFloat),
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
cpCircleShapeGetOffset = chipmunk_lib.cpCircleShapeGetOffset
cpCircleShapeGetOffset.restype = cpVect
cpCircleShapeGetOffset.argtypes = [POINTER(cpShape)]
cpCircleShapeGetRadius = chipmunk_lib.cpCircleShapeGetRadius
cpCircleShapeGetRadius.restype = cpFloat
cpCircleShapeGetRadius.argtypes = [POINTER(cpShape)]
class cpSegmentShape(Structure):
    pass
#cpSegmentShape._pack_ = 4
cpSegmentShape._fields_ = [
    ('shape', cpShape),
    ('a', cpVect),
    ('b', cpVect),
    ('n', cpVect),
    ('ta', cpVect),
    ('tb', cpVect),
    ('tn', cpVect),
    ('r', cpFloat),
    ('a_tangent', cpVect),
    ('b_tangent', cpVect),
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
cpSegmentShapeSetNeighbors = chipmunk_lib.cpSegmentShapeSetNeighbors
cpSegmentShapeSetNeighbors.restype = None
cpSegmentShapeSetNeighbors.argtypes = [POINTER(cpShape), cpVect, cpVect]
cpSegmentShapeGetA = chipmunk_lib.cpSegmentShapeGetA
cpSegmentShapeGetA.restype = cpVect
cpSegmentShapeGetA.argtypes = [POINTER(cpShape)]
cpSegmentShapeGetB = chipmunk_lib.cpSegmentShapeGetB
cpSegmentShapeGetB.restype = cpVect
cpSegmentShapeGetB.argtypes = [POINTER(cpShape)]
cpSegmentShapeGetNormal = chipmunk_lib.cpSegmentShapeGetNormal
cpSegmentShapeGetNormal.restype = cpVect
cpSegmentShapeGetNormal.argtypes = [POINTER(cpShape)]
cpSegmentShapeGetRadius = chipmunk_lib.cpSegmentShapeGetRadius
cpSegmentShapeGetRadius.restype = cpFloat
cpSegmentShapeGetRadius.argtypes = [POINTER(cpShape)]
class cpContactBufferHeader(Structure):
    pass
cpContactBufferHeader._fields_ = [
]
cpSpaceArbiterApplyImpulseFunc = function_pointer(None, POINTER(cpArbiter))
class cpSpatialIndex(Structure):
    pass
#cpSpace._pack_ = 4
cpSpace._fields_ = [
    ('iterations', c_int),
    ('gravity', cpVect),
    ('damping', cpFloat),
    ('idleSpeedThreshold', cpFloat),
    ('sleepTimeThreshold', cpFloat),
    ('collisionSlop', cpFloat),
    ('collisionBias', cpFloat),
    ('collisionPersistence', cpTimestamp),
    ('enableContactGraph', cpBool),
    ('data', cpDataPointer),
    ('staticBody', POINTER(cpBody)),
    ('stamp_private', cpTimestamp),
    ('curr_dt_private', cpFloat),
    ('bodies_private', POINTER(cpArray)),
    ('rousedBodies_private', POINTER(cpArray)),
    ('sleepingComponents_private', POINTER(cpArray)),
    ('staticShapes_private', POINTER(cpSpatialIndex)),
    ('activeShapes_private', POINTER(cpSpatialIndex)),
    ('arbiters_private', POINTER(cpArray)),
    ('contactBuffersHead_private', POINTER(cpContactBufferHeader)),
    ('cachedArbiters_private', POINTER(cpHashSet)),
    ('pooledArbiters_private', POINTER(cpArray)),
    ('constraints_private', POINTER(cpArray)),
    ('allocatedBuffers_private', POINTER(cpArray)),
    ('locked_private', c_int),
    ('collisionHandlers_private', POINTER(cpHashSet)),
    ('defaultHandler_private', cpCollisionHandler),
    ('skipPostStep_private', cpBool),
    ('postStepCallbacks_private', POINTER(cpArray)),
    ('_staticBody_private', cpBody),
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
cpSpaceSetDefaultCollisionHandler = chipmunk_lib.cpSpaceSetDefaultCollisionHandler
cpSpaceSetDefaultCollisionHandler.restype = None
cpSpaceSetDefaultCollisionHandler.argtypes = [POINTER(cpSpace), cpCollisionBeginFunc, cpCollisionPreSolveFunc, cpCollisionPostSolveFunc, cpCollisionSeparateFunc, c_void_p]
cpSpaceAddCollisionHandler = chipmunk_lib.cpSpaceAddCollisionHandler
cpSpaceAddCollisionHandler.restype = None
cpSpaceAddCollisionHandler.argtypes = [POINTER(cpSpace), cpCollisionType, cpCollisionType, cpCollisionBeginFunc, cpCollisionPreSolveFunc, cpCollisionPostSolveFunc, cpCollisionSeparateFunc, c_void_p]
cpSpaceRemoveCollisionHandler = chipmunk_lib.cpSpaceRemoveCollisionHandler
cpSpaceRemoveCollisionHandler.restype = None
cpSpaceRemoveCollisionHandler.argtypes = [POINTER(cpSpace), cpCollisionType, cpCollisionType]
cpSpaceAddShape = chipmunk_lib.cpSpaceAddShape
cpSpaceAddShape.restype = POINTER(cpShape)
cpSpaceAddShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddStaticShape = chipmunk_lib.cpSpaceAddStaticShape
cpSpaceAddStaticShape.restype = POINTER(cpShape)
cpSpaceAddStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddBody = chipmunk_lib.cpSpaceAddBody
cpSpaceAddBody.restype = POINTER(cpBody)
cpSpaceAddBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceAddConstraint = chipmunk_lib.cpSpaceAddConstraint
cpSpaceAddConstraint.restype = POINTER(cpConstraint)
cpSpaceAddConstraint.argtypes = [POINTER(cpSpace), POINTER(cpConstraint)]
cpSpaceRemoveShape = chipmunk_lib.cpSpaceRemoveShape
cpSpaceRemoveShape.restype = None
cpSpaceRemoveShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveStaticShape = chipmunk_lib.cpSpaceRemoveStaticShape
cpSpaceRemoveStaticShape.restype = None
cpSpaceRemoveStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveBody = chipmunk_lib.cpSpaceRemoveBody
cpSpaceRemoveBody.restype = None
cpSpaceRemoveBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceRemoveConstraint = chipmunk_lib.cpSpaceRemoveConstraint
cpSpaceRemoveConstraint.restype = None
cpSpaceRemoveConstraint.argtypes = [POINTER(cpSpace), POINTER(cpConstraint)]
cpSpaceContainsShape = chipmunk_lib.cpSpaceContainsShape
cpSpaceContainsShape.restype = cpBool
cpSpaceContainsShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceContainsBody = chipmunk_lib.cpSpaceContainsBody
cpSpaceContainsBody.restype = cpBool
cpSpaceContainsBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceContainsConstraint = chipmunk_lib.cpSpaceContainsConstraint
cpSpaceContainsConstraint.restype = cpBool
cpSpaceContainsConstraint.argtypes = [POINTER(cpSpace), POINTER(cpConstraint)]
cpSpaceConvertBodyToStatic = chipmunk_lib.cpSpaceConvertBodyToStatic
cpSpaceConvertBodyToStatic.restype = None
cpSpaceConvertBodyToStatic.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceConvertBodyToDynamic = chipmunk_lib.cpSpaceConvertBodyToDynamic
cpSpaceConvertBodyToDynamic.restype = None
cpSpaceConvertBodyToDynamic.argtypes = [POINTER(cpSpace), POINTER(cpBody), cpFloat, cpFloat]
cpPostStepFunc = function_pointer(None, POINTER(cpSpace), c_void_p, c_void_p)
cpSpaceAddPostStepCallback = chipmunk_lib.cpSpaceAddPostStepCallback
cpSpaceAddPostStepCallback.restype = cpBool
cpSpaceAddPostStepCallback.argtypes = [POINTER(cpSpace), cpPostStepFunc, c_void_p, c_void_p]
cpSpacePointQueryFunc = function_pointer(None, POINTER(cpShape), c_void_p)
cpSpacePointQuery = chipmunk_lib.cpSpacePointQuery
cpSpacePointQuery.restype = None
cpSpacePointQuery.argtypes = [POINTER(cpSpace), cpVect, cpLayers, cpGroup, cpSpacePointQueryFunc, c_void_p]
cpSpacePointQueryFirst = chipmunk_lib.cpSpacePointQueryFirst
cpSpacePointQueryFirst.restype = POINTER(cpShape)
cpSpacePointQueryFirst.argtypes = [POINTER(cpSpace), cpVect, cpLayers, cpGroup]
cpSpaceNearestPointQueryFunc = function_pointer(None, POINTER(cpShape), cpFloat, cpVect, c_void_p)
cpSpaceNearestPointQuery = chipmunk_lib.cpSpaceNearestPointQuery
cpSpaceNearestPointQuery.restype = None
cpSpaceNearestPointQuery.argtypes = [POINTER(cpSpace), cpVect, cpFloat, cpLayers, cpGroup, cpSpaceNearestPointQueryFunc, c_void_p]
cpSpaceNearestPointQueryNearest = chipmunk_lib.cpSpaceNearestPointQueryNearest
cpSpaceNearestPointQueryNearest.restype = POINTER(cpShape)
cpSpaceNearestPointQueryNearest.argtypes = [POINTER(cpSpace), cpVect, cpFloat, cpLayers, cpGroup, POINTER(cpNearestPointQueryInfo)]
cpSpaceSegmentQueryFunc = function_pointer(None, POINTER(cpShape), cpFloat, cpVect, c_void_p)
cpSpaceSegmentQuery = chipmunk_lib.cpSpaceSegmentQuery
cpSpaceSegmentQuery.restype = None
cpSpaceSegmentQuery.argtypes = [POINTER(cpSpace), cpVect, cpVect, cpLayers, cpGroup, cpSpaceSegmentQueryFunc, c_void_p]
cpSpaceSegmentQueryFirst = chipmunk_lib.cpSpaceSegmentQueryFirst
cpSpaceSegmentQueryFirst.restype = POINTER(cpShape)
cpSpaceSegmentQueryFirst.argtypes = [POINTER(cpSpace), cpVect, cpVect, cpLayers, cpGroup, POINTER(cpSegmentQueryInfo)]
cpSpaceBBQueryFunc = function_pointer(None, POINTER(cpShape), c_void_p)
cpSpaceBBQuery = chipmunk_lib.cpSpaceBBQuery
cpSpaceBBQuery.restype = None
cpSpaceBBQuery.argtypes = [POINTER(cpSpace), cpBB, cpLayers, cpGroup, cpSpaceBBQueryFunc, c_void_p]
cpSpaceShapeQueryFunc = function_pointer(None, POINTER(cpShape), POINTER(cpContactPointSet), c_void_p)
cpSpaceShapeQuery = chipmunk_lib.cpSpaceShapeQuery
cpSpaceShapeQuery.restype = cpBool
cpSpaceShapeQuery.argtypes = [POINTER(cpSpace), POINTER(cpShape), cpSpaceShapeQueryFunc, c_void_p]
cpSpaceActivateShapesTouchingShape = chipmunk_lib.cpSpaceActivateShapesTouchingShape
cpSpaceActivateShapesTouchingShape.restype = None
cpSpaceActivateShapesTouchingShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceBodyIteratorFunc = function_pointer(None, POINTER(cpBody), c_void_p)
cpSpaceEachBody = chipmunk_lib.cpSpaceEachBody
cpSpaceEachBody.restype = None
cpSpaceEachBody.argtypes = [POINTER(cpSpace), cpSpaceBodyIteratorFunc, c_void_p]
cpSpaceShapeIteratorFunc = function_pointer(None, POINTER(cpShape), c_void_p)
cpSpaceEachShape = chipmunk_lib.cpSpaceEachShape
cpSpaceEachShape.restype = None
cpSpaceEachShape.argtypes = [POINTER(cpSpace), cpSpaceShapeIteratorFunc, c_void_p]
cpSpaceConstraintIteratorFunc = function_pointer(None, POINTER(cpConstraint), c_void_p)
cpSpaceEachConstraint = chipmunk_lib.cpSpaceEachConstraint
cpSpaceEachConstraint.restype = None
cpSpaceEachConstraint.argtypes = [POINTER(cpSpace), cpSpaceConstraintIteratorFunc, c_void_p]
cpSpaceReindexStatic = chipmunk_lib.cpSpaceReindexStatic
cpSpaceReindexStatic.restype = None
cpSpaceReindexStatic.argtypes = [POINTER(cpSpace)]
cpSpaceReindexShape = chipmunk_lib.cpSpaceReindexShape
cpSpaceReindexShape.restype = None
cpSpaceReindexShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceReindexShapesForBody = chipmunk_lib.cpSpaceReindexShapesForBody
cpSpaceReindexShapesForBody.restype = None
cpSpaceReindexShapesForBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceUseSpatialHash = chipmunk_lib.cpSpaceUseSpatialHash
cpSpaceUseSpatialHash.restype = None
cpSpaceUseSpatialHash.argtypes = [POINTER(cpSpace), cpFloat, c_int]
cpSpaceStep = chipmunk_lib.cpSpaceStep
cpSpaceStep.restype = None
cpSpaceStep.argtypes = [POINTER(cpSpace), cpFloat]
cpSpatialIndexBBFunc = function_pointer(cpBB, c_void_p)
cpSpatialIndexIteratorFunc = function_pointer(None, c_void_p, c_void_p)
cpSpatialIndexQueryFunc = function_pointer(cpCollisionID, c_void_p, c_void_p, cpCollisionID, c_void_p)
cpSpatialIndexSegmentQueryFunc = function_pointer(cpFloat, c_void_p, c_void_p, c_void_p)
class cpSpatialIndexClass(Structure):
    pass
cpSpatialIndex._fields_ = [
    ('klass', POINTER(cpSpatialIndexClass)),
    ('bbfunc', cpSpatialIndexBBFunc),
    ('staticIndex', POINTER(cpSpatialIndex)),
    ('dynamicIndex', POINTER(cpSpatialIndex)),
]
class cpSpaceHash(Structure):
    pass
cpSpaceHash._fields_ = [
]
cpSpaceHashAlloc = chipmunk_lib.cpSpaceHashAlloc
cpSpaceHashAlloc.restype = POINTER(cpSpaceHash)
cpSpaceHashAlloc.argtypes = []
cpSpaceHashInit = chipmunk_lib.cpSpaceHashInit
cpSpaceHashInit.restype = POINTER(cpSpatialIndex)
cpSpaceHashInit.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int, cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSpaceHashNew = chipmunk_lib.cpSpaceHashNew
cpSpaceHashNew.restype = POINTER(cpSpatialIndex)
cpSpaceHashNew.argtypes = [cpFloat, c_int, cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSpaceHashResize = chipmunk_lib.cpSpaceHashResize
cpSpaceHashResize.restype = None
cpSpaceHashResize.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int]
class cpBBTree(Structure):
    pass
cpBBTree._fields_ = [
]
cpBBTreeAlloc = chipmunk_lib.cpBBTreeAlloc
cpBBTreeAlloc.restype = POINTER(cpBBTree)
cpBBTreeAlloc.argtypes = []
cpBBTreeInit = chipmunk_lib.cpBBTreeInit
cpBBTreeInit.restype = POINTER(cpSpatialIndex)
cpBBTreeInit.argtypes = [POINTER(cpBBTree), cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpBBTreeNew = chipmunk_lib.cpBBTreeNew
cpBBTreeNew.restype = POINTER(cpSpatialIndex)
cpBBTreeNew.argtypes = [cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpBBTreeOptimize = chipmunk_lib.cpBBTreeOptimize
cpBBTreeOptimize.restype = None
cpBBTreeOptimize.argtypes = [POINTER(cpSpatialIndex)]
cpBBTreeVelocityFunc = function_pointer(cpVect, c_void_p)
cpBBTreeSetVelocityFunc = chipmunk_lib.cpBBTreeSetVelocityFunc
cpBBTreeSetVelocityFunc.restype = None
cpBBTreeSetVelocityFunc.argtypes = [POINTER(cpSpatialIndex), cpBBTreeVelocityFunc]
class cpSweep1D(Structure):
    pass
cpSweep1D._fields_ = [
]
cpSweep1DAlloc = chipmunk_lib.cpSweep1DAlloc
cpSweep1DAlloc.restype = POINTER(cpSweep1D)
cpSweep1DAlloc.argtypes = []
cpSweep1DInit = chipmunk_lib.cpSweep1DInit
cpSweep1DInit.restype = POINTER(cpSpatialIndex)
cpSweep1DInit.argtypes = [POINTER(cpSweep1D), cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSweep1DNew = chipmunk_lib.cpSweep1DNew
cpSweep1DNew.restype = POINTER(cpSpatialIndex)
cpSweep1DNew.argtypes = [cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSpatialIndexDestroyImpl = function_pointer(None, POINTER(cpSpatialIndex))
cpSpatialIndexCountImpl = function_pointer(c_int, POINTER(cpSpatialIndex))
cpSpatialIndexEachImpl = function_pointer(None, POINTER(cpSpatialIndex), cpSpatialIndexIteratorFunc, c_void_p)
cpSpatialIndexContainsImpl = function_pointer(cpBool, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexInsertImpl = function_pointer(None, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexRemoveImpl = function_pointer(None, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexReindexImpl = function_pointer(None, POINTER(cpSpatialIndex))
cpSpatialIndexReindexObjectImpl = function_pointer(None, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexReindexQueryImpl = function_pointer(None, POINTER(cpSpatialIndex), cpSpatialIndexQueryFunc, c_void_p)
cpSpatialIndexQueryImpl = function_pointer(None, POINTER(cpSpatialIndex), c_void_p, cpBB, cpSpatialIndexQueryFunc, c_void_p)
cpSpatialIndexSegmentQueryImpl = function_pointer(None, POINTER(cpSpatialIndex), c_void_p, cpVect, cpVect, cpFloat, cpSpatialIndexSegmentQueryFunc, c_void_p)
cpSpatialIndexClass._fields_ = [
    ('destroy', cpSpatialIndexDestroyImpl),
    ('count', cpSpatialIndexCountImpl),
    ('each', cpSpatialIndexEachImpl),
    ('contains', cpSpatialIndexContainsImpl),
    ('insert', cpSpatialIndexInsertImpl),
    ('remove', cpSpatialIndexRemoveImpl),
    ('reindex', cpSpatialIndexReindexImpl),
    ('reindexObject', cpSpatialIndexReindexObjectImpl),
    ('reindexQuery', cpSpatialIndexReindexQueryImpl),
    ('query', cpSpatialIndexQueryImpl),
    ('segmentQuery', cpSpatialIndexSegmentQueryImpl),
]
cpSpatialIndexFree = chipmunk_lib.cpSpatialIndexFree
cpSpatialIndexFree.restype = None
cpSpatialIndexFree.argtypes = [POINTER(cpSpatialIndex)]
cpSpatialIndexCollideStatic = chipmunk_lib.cpSpatialIndexCollideStatic
cpSpatialIndexCollideStatic.restype = None
cpSpatialIndexCollideStatic.argtypes = [POINTER(cpSpatialIndex), POINTER(cpSpatialIndex), cpSpatialIndexQueryFunc, c_void_p]
cpvslerp = chipmunk_lib.cpvslerp
cpvslerp.restype = cpVect
cpvslerp.argtypes = [cpVect, cpVect, cpFloat]
cpvslerpconst = chipmunk_lib.cpvslerpconst
cpvslerpconst.restype = cpVect
cpvslerpconst.argtypes = [cpVect, cpVect, cpFloat]
cpvstr = chipmunk_lib.cpvstr
cpvstr.restype = STRING
cpvstr.argtypes = [cpVect]
cpFalse = 0 # Variable c_int '0'
cpTrue = 1 # Variable c_int '1'
__all__ = ['cpBodySleep', 'cpBodyResetForces', 'cpShapeUpdate',
           'cpSpacePointQuery', 'cpPolyShapeNew2',
           'cpSpaceActivateShapesTouchingShape',
           'cpArbiterIsFirstContact', 'cpBodyEachShape',
           'cpCollisionHandler', 'cpfree', 'cpResetShapeIdCounter',
           'cpvslerp', 'cpShapeCacheBB', 'cpBoxShapeInit2',
           'cpBoxShapeInit3', 'cpRatchetJointInit',
           'cpCircleShapeNew', 'size_t', 'cpDampedSpring',
           'cpBodySetAngle', 'cpSpatialIndexCountImpl',
           'cpSpaceShapeIteratorFunc', 'cpSpatialIndexDestroyImpl',
           'cpDampedRotarySpringAlloc', 'cpRotaryLimitJoint',
           'cpSpatialIndexSegmentQueryImpl', 'cpMessage',
           'cpContactPointSet', 'cpShapeSetBody', 'cpDampedSpringNew',
           'cpSpaceBBQueryFunc', 'cpSweep1DNew', 'cpGrooveJointAlloc',
           'cpBodyVelocityFunc', 'cpArray', 'cpSlideJointNew',
           'cpBodyEachConstraint', 'cpSpaceReindexShape',
           'cpEnableSegmentToSegmentCollisions',
           'cpConstraintGetImpulseImpl', 'cpDampedSpringInit',
           'cpSpaceContainsBody', 'cpSegmentQueryInfo',
           'cpMomentForBox', 'cpSpace', 'cpDampedRotarySpringNew',
           'cpSpaceSegmentQueryFirst', 'cpCircleShapeGetOffset',
           'cpBodyConstraintIteratorFunc', 'cpGearJointInit',
           'cpGrooveJointInit', 'N17cpContactPointSet4DOT_25E',
           'cpPolyShapeSetRadius', 'cpBody', 'cpBodySetMass',
           'cpBodySetPos', 'cpvstr', 'cpMomentForPoly',
           'cpArbiterSetContactPointSet', 'cpCircleShapeSetOffset',
           'cpBodyDestroy', 'cpDataPointer', 'cpArbiterStateNormal',
           'cpSweep1DAlloc', 'CP_SEGMENT_SHAPE', 'cpArbiterState',
           'cpVect', 'cpSpaceContainsShape',
           'cpDampedRotarySpringGetClass', 'cpDampedSpringForceFunc',
           'cpSpatialIndexQueryFunc', 'cpSplittingPlane',
           'cpSpaceHashInit', 'cpSpaceRemoveStaticShape',
           'cpArbiterGetDepth', 'cpPolyShapeInit',
           'cpSpatialIndexReindexImpl', 'cpPolyShapeNew',
           'cpSegmentShapeSetRadius', 'cpArbiterIgnore',
           'cpSpatialIndexClass', 'cpSlideJoint', 'CP_POLY_SHAPE',
           'cpcalloc', 'cpSpaceAlloc', 'cpCircleShapeAlloc',
           'cpPinJointAlloc', 'cpBodyUpdatePosition',
           'cpCollisionPreSolveFunc', 'cpBBTreeOptimize',
           'cpShapeSegmentQueryImpl', 'cpSpaceDestroy',
           'cpAreaForCircle', 'cpContact', 'cpBodyShapeIteratorFunc',
           'cpSegmentShape', 'cpSpaceReindexShapesForBody',
           'cpSlideJointAlloc', 'cpConstraintApplyImpulseImpl',
           'cpSegmentShapeSetNeighbors', 'cpSpaceUseSpatialHash',
           'cpArbiterGetNormal', 'cpConstraint', 'cpArbiter',
           'cpPivotJointNew2', 'cpGrooveJoint',
           'cpArbiterStateIgnore', 'cpSpaceAddCollisionHandler',
           'cpSpaceFree', 'cpCircleShapeInit', 'cpSpaceInit',
           'cpNearestPointQueryInfo', 'CP_NUM_SHAPES', 'cpBool',
           'cpCollisionBeginFunc', 'cpSpatialIndexInsertImpl',
           'cpRecenterPoly', 'cpFalse', 'cpArbiterGetContactPointSet',
           'cpPivotJointNew', 'cpSpaceConvertBodyToDynamic',
           'cpBBTreeAlloc', 'cpConstraintApplyCachedImpulseImpl',
           'cpArbiterGetCount', 'cpSegmentShapeNew',
           'cpCircleShapeSetRadius', 'cpBodyFree',
           'cpRatchetJointGetClass', 'free', 'cpGearJointAlloc',
           'cpSpaceRemoveBody', 'cpCentroidForPoly', 'cpBoxShapeNew',
           'cpBodySleepWithGroup', 'cpConstraintPreSolveFunc',
           'cpSpatialIndexEachImpl', 'cpCollisionType',
           'cpSpaceReindexStatic', 'cpPivotJointInit',
           'cpShapeSegmentQuery', 'cpSpaceConvertBodyToStatic',
           'cpSpatialIndexFree', 'cpVersionString',
           'cpSpaceArbiterApplyImpulseFunc',
           'cpSpaceNearestPointQueryFunc', 'cpBodySetMoment',
           'cpBoxShapeInit', 'cpSegmentShapeAlloc',
           'cpBBTreeSetVelocityFunc', 'cpShapeFree',
           'cpPolyShapeGetVert', 'cpSpaceAddBody', 'cpShapeType',
           'cpShape', 'cpPolyShapeGetNumVerts',
           'cpSimpleMotorGetClass', 'cpSpaceRemoveShape', 'cpBBTree',
           'cpContactBufferHeader', 'cpGrooveJointGetClass',
           'CP_CIRCLE_SHAPE', 'cpSpaceHash', 'realloc',
           'cpSpaceSegmentQuery', 'cpSpaceHashAlloc', 'cpPinJoint',
           'cpConstraintPreStepImpl', 'cpArbiterTotalKE',
           'cpSpacePointQueryFunc', 'cpDampedRotarySpringTorqueFunc',
           'cpBBWrapVect', 'cpSegmentShapeGetA',
           'cpShapeNearestPointQuery', 'cpSegmentShapeGetB',
           'cpSpaceNew', 'cpBodyInit', 'cpBodyAssertSane',
           'cpArbiterGetPoint', 'cpCollisionSeparateFunc',
           'cpMomentForBox2', 'cpBoxShapeNew2',
           'cpBodyArbiterIteratorFunc',
           'cpShapeNearestPointQueryImpl', 'cpBodyUpdateVelocity',
           'cpCircleShapeGetRadius', 'cpSpatialIndexQueryImpl',
           'cpBB', 'cpBodyInitStatic', 'cpPinJointInit',
           'cpGearJoint', 'cpSpaceHashResize', 'cpSlideJointInit',
           'cpPolyShapeAlloc', 'cpSpaceAddShape', 'cpAreaForSegment',
           'cpSpaceSetDefaultCollisionHandler', 'uintptr_t',
           'cpHashValue', 'cpCollisionPostSolveFunc',
           'cpConstraintDestroy', 'cpSimpleMotorNew',
           'cpSpaceEachBody', 'cpPolyShapeInit2',
           'cpSpatialIndexContainsImpl', 'cpMat2x2',
           'cpDampedSpringAlloc', 'cpArbiterStateFirstColl',
           'cpRotaryLimitJointAlloc', 'cpShapeDestroyImpl',
           'cpSimpleMotorAlloc', 'cpBodyEachArbiter',
           'cpSpaceShapeQueryFunc', 'cpSpaceBodyIteratorFunc',
           'cpSpaceNearestPointQuery', 'cpSpaceEachConstraint',
           'cpSpatialIndexSegmentQueryFunc', 'cpGroup',
           'cpMomentForCircle', 'cpSegmentShapeGetRadius',
           'cpSpatialIndexReindexObjectImpl', 'cpBBTreeInit',
           'cpTimestamp', 'cpTrue', 'cpGearJointSetRatio',
           'cpRotaryLimitJointInit', 'cpSpaceRemoveConstraint',
           'cpBodyActivateStatic', 'cpSweep1D', 'cpSweep1DInit',
           'cpSpatialIndex', 'cpSpaceAddPostStepCallback',
           'cpRotaryLimitJointNew', 'cpPivotJointGetClass',
           'cpBodyNewStatic', 'cpSpaceShapeQuery', 'cpLayers',
           'cpPolyShapeGetRadius', 'cpPivotJointAlloc',
           'cpConstraintFree', 'cpSpatialIndexBBFunc',
           'cpCollisionID', 'cpGearJointGetClass', 'cpBodyNew',
           'cpSpaceStep', 'cpHashSet', 'cpSpaceAddConstraint',
           'cpGrooveJointSetGrooveA', 'cpGrooveJointSetGrooveB',
           'cpSpaceConstraintIteratorFunc', 'cpConstraintClass',
           'cpFloat', 'cpShapePointQuery', 'cpPinJointNew',
           'cpBodySanityCheck', 'cpPostStepFunc',
           'cpSpatialIndexReindexQueryImpl',
           'cpConstraintPostSolveFunc', 'cpPolyShape',
           'cpShapeCacheDataImpl', 'cpBodyPositionFunc',
           'cpBodyGetVelAtLocalPoint', 'cpRatchetJointAlloc',
           'cpSpaceHashNew', 'cpSpaceSegmentQueryFunc',
           'cpArbiterThread', 'cpBodyApplyForce',
           'cpSpacePointQueryFirst', 'cpMomentForSegment',
           'cpArbiterTotalImpulseWithFriction',
           'cpRotaryLimitJointGetClass',
           'cpSpaceRemoveCollisionHandler', 'cpBBTreeNew',
           'cpSpaceEachShape', 'cpConvexHull', 'cpRatchetJointNew',
           'cpGearJointNew', 'cpArbiterTotalImpulse', 'cprealloc',
           'cpvslerpconst', 'cpSpatialIndexCollideStatic',
           'cpSpaceBBQuery', 'cpAreaForPoly',
           'cpArbiterSetSurfaceVelocity', 'cpPivotJoint',
           'cpDampedRotarySpringInit', 'cpSegmentShapeInit',
           'cpSlideJointGetClass', 'cpDampedRotarySpring',
           'cpSimpleMotor', 'calloc', 'cpComponentNode',
           'cpSegmentShapeSetEndpoints', 'cpPolyShapeSetVerts',
           'cpRatchetJoint', 'cpSpaceAddStaticShape',
           'cpSpaceNearestPointQueryNearest',
           'cpSpatialIndexIteratorFunc', 'cpDampedSpringGetClass',
           'cpSpatialIndexRemoveImpl', 'cpArbiterStateCached',
           'cpBodyGetVelAtWorldPoint', 'cpSegmentShapeGetNormal',
           'cpShapeDestroy', 'cpSimpleMotorInit',
           'cpBodyApplyImpulse', 'cpArbiterGetSurfaceVelocity',
           'cpInitChipmunk', 'cpShapeClass', 'cpBodyAlloc',
           'cpGrooveJointNew', 'uint32_t', 'cpCircleShape',
           'cpBodyActivate', 'cpBBTreeVelocityFunc', 'cpPolyValidate',
           'cpPinJointGetClass', 'cpSpaceContainsConstraint']
