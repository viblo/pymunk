
from ctypes import * 
from .vec2d import Vec2d
cpVect = Vec2d
STRING = c_char_p

from .libload import load_library, platform_specific_functions
_lib_debug = True #Set to True to print the Chipmunk path.
chipmunk_lib = load_library("chipmunk", print_path=_lib_debug)
function_pointer = platform_specific_functions()['function_pointer']



# cpffloor = floor # alias
# def cpAssertWarn(condition,message): return if(!(condition)) cpMessage(message, #condition, __FILE__, __LINE__, 0) # macro
# cpfsqrt = sqrt # alias
# cpfpow = pow # alias
# def CP_DefineBodyGetter(type,member,name): return static inline type cpBodyGet ##name(const cpBody *body){return body->member;} # macro
def CP_HASH_PAIR(A,B): return ((cpHashValue)(A)*CP_HASH_COEF ^ (cpHashValue)(B)*CP_HASH_COEF) # macro
cpArbiterStateCached = 4
# cpfceil = ceil # alias
# cpmalloc = malloc # alias
# def CP_DefineBodyProperty(type,member,name): return CP_DefineBodyGetter(type, member, name) CP_DefineBodySetter(type, member, name) # macro
cpArbiterStateFirstColl = 1
cpArbiterStateNormal = 0
# cpfmod = fmod # alias
# cpfexp = exp # alias
# def CP_DeclareShapeGetter(struct,type,name): return type struct ##Get ##name(cpShape *shape) # macro
CP_POLY_SHAPE = 2
CP_CIRCLE_SHAPE = 0
# cprealloc = realloc # alias
# def CP_DefineConstraintProperty(struct,type,member,name): return CP_DefineConstraintGetter(struct, type, member, name) CP_DefineConstraintSetter(struct, type, member, name) # macro
# def CP_ARBITER_GET_BODIES(arb,a,b): return cpBody *a, *b; cpArbiterGetBodies(arb, &a, &b); # macro
# def CP_DefineConstraintGetter(struct,type,member,name): return static inline type struct ##Get ##name(const cpConstraint *constraint){ cpConstraintCheckCast(constraint, struct); return ((struct *)constraint)->member; } # macro
def MAKE_REF(name): return __typeof__(name) *_ ##name = name # macro
# cpfacos = acos # alias
# def cpAssert(condition,message): return if(!(condition)) cpMessage(message, #condition, __FILE__, __LINE__, 1) # macro
CP_SEGMENT_SHAPE = 1
cpArbiterStateSleep = 3
# cpfree = free # alias
# def cpConstraintCheckCast(constraint,struct): return cpAssert(constraint->klass == struct ##GetClass(), "Constraint is not a "#struct); # macro
# cpfsin = sin # alias
# def CP_ARBITER_GET_SHAPES(arb,a,b): return cpShape *a, *b; cpArbiterGetShapes(arb, &a, &b); # macro
# cpfcos = cos # alias
# def CP_DefineBodySetter(type,member,name): return static inline void cpBodySet ##name(cpBody *body, const type value){ cpBodyActivate(body); body->member = value; } # macro
# def CP_DefineConstraintSetter(struct,type,member,name): return static inline void struct ##Set ##name(cpConstraint *constraint, type value){ cpConstraintCheckCast(constraint, struct); cpConstraintActivateBodies(constraint); ((struct *)constraint)->member = value; } # macro
cpArbiterStateIgnore = 2
# cpfatan2 = atan2 # alias
CP_NUM_SHAPES = 3
# cpcalloc = calloc # alias
cpMessage = chipmunk_lib.cpMessage
cpMessage.restype = None
cpMessage.argtypes = [STRING, STRING, STRING, c_int, c_int]
cpVersionString = (STRING).in_dll(chipmunk_lib, 'cpVersionString')
cpInitChipmunk = chipmunk_lib.cpInitChipmunk
cpInitChipmunk.restype = None
cpInitChipmunk.argtypes = []
cpFloat = c_double
#cpVect class def removed
cpMomentForCircle = chipmunk_lib.cpMomentForCircle
cpMomentForCircle.restype = cpFloat
cpMomentForCircle.argtypes = [cpFloat, cpFloat, cpFloat, cpVect]
cpMomentForSegment = chipmunk_lib.cpMomentForSegment
cpMomentForSegment.restype = cpFloat
cpMomentForSegment.argtypes = [cpFloat, cpVect, cpVect]
cpMomentForPoly = chipmunk_lib.cpMomentForPoly
cpMomentForPoly.restype = cpFloat
cpMomentForPoly.argtypes = [cpFloat, c_int, POINTER(cpVect), cpVect]
cpMomentForBox = chipmunk_lib.cpMomentForBox
cpMomentForBox.restype = cpFloat
cpMomentForBox.argtypes = [cpFloat, cpFloat, cpFloat]
_cpv = (function_pointer(cpVect, cpFloat, cpFloat)).in_dll(chipmunk_lib, '_cpv')
cpBool = c_int
_cpveql = (function_pointer(cpBool, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpveql')
_cpvadd = (function_pointer(cpVect, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvadd')
_cpvneg = (function_pointer(cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvneg')
_cpvsub = (function_pointer(cpVect, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvsub')
_cpvmult = (function_pointer(cpVect, cpVect, cpFloat)).in_dll(chipmunk_lib, '_cpvmult')
_cpvdot = (function_pointer(cpFloat, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvdot')
_cpvcross = (function_pointer(cpFloat, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvcross')
_cpvperp = (function_pointer(cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvperp')
_cpvrperp = (function_pointer(cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvrperp')
_cpvproject = (function_pointer(cpVect, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvproject')
_cpvrotate = (function_pointer(cpVect, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvrotate')
_cpvunrotate = (function_pointer(cpVect, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvunrotate')
_cpvlengthsq = (function_pointer(cpFloat, cpVect)).in_dll(chipmunk_lib, '_cpvlengthsq')
_cpvlerp = (function_pointer(cpVect, cpVect, cpVect, cpFloat)).in_dll(chipmunk_lib, '_cpvlerp')
_cpvnormalize = (function_pointer(cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvnormalize')
_cpvnormalize_safe = (function_pointer(cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvnormalize_safe')
_cpvclamp = (function_pointer(cpVect, cpVect, cpFloat)).in_dll(chipmunk_lib, '_cpvclamp')
_cpvlerpconst = (function_pointer(cpVect, cpVect, cpVect, cpFloat)).in_dll(chipmunk_lib, '_cpvlerpconst')
_cpvdist = (function_pointer(cpFloat, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvdist')
_cpvdistsq = (function_pointer(cpFloat, cpVect, cpVect)).in_dll(chipmunk_lib, '_cpvdistsq')
_cpvnear = (function_pointer(cpBool, cpVect, cpVect, cpFloat)).in_dll(chipmunk_lib, '_cpvnear')
class cpBB(Structure):
    pass
_cpBBNew = (function_pointer(cpBB, cpFloat, cpFloat, cpFloat, cpFloat)).in_dll(chipmunk_lib, '_cpBBNew')
class cpBody(Structure):
    pass
_cpBodyWorld2Local = (function_pointer(cpVect, POINTER(cpBody), cpVect)).in_dll(chipmunk_lib, '_cpBodyWorld2Local')
_cpBodyLocal2World = (function_pointer(cpVect, POINTER(cpBody), cpVect)).in_dll(chipmunk_lib, '_cpBodyLocal2World')
_cpBodyApplyImpulse = (function_pointer(None, POINTER(cpBody), cpVect, cpVect)).in_dll(chipmunk_lib, '_cpBodyApplyImpulse')
_cpBodyIsSleeping = (function_pointer(cpBool, POINTER(cpBody))).in_dll(chipmunk_lib, '_cpBodyIsSleeping')
_cpBodyIsRogue = (function_pointer(cpBool, POINTER(cpBody))).in_dll(chipmunk_lib, '_cpBodyIsRogue')
_cpBodyKineticEnergy = (function_pointer(cpFloat, POINTER(cpBody))).in_dll(chipmunk_lib, '_cpBodyKineticEnergy')
class cpArbiter(Structure):
    pass
_cpArbiterIsFirstContact = (function_pointer(cpBool, POINTER(cpArbiter))).in_dll(chipmunk_lib, '_cpArbiterIsFirstContact')
class cpShape(Structure):
    pass
_cpArbiterGetShapes = (function_pointer(None, POINTER(cpArbiter), POINTER(POINTER(cpShape)), POINTER(POINTER(cpShape)))).in_dll(chipmunk_lib, '_cpArbiterGetShapes')
_cpArbiterGetNormal = (function_pointer(cpVect, POINTER(cpArbiter), c_int)).in_dll(chipmunk_lib, '_cpArbiterGetNormal')
_cpArbiterGetPoint = (function_pointer(cpVect, POINTER(cpArbiter), c_int)).in_dll(chipmunk_lib, '_cpArbiterGetPoint')
class cpConstraint(Structure):
    pass
_cpConstraintGetImpulse = (function_pointer(cpFloat, POINTER(cpConstraint))).in_dll(chipmunk_lib, '_cpConstraintGetImpulse')
class cpSegmentQueryInfo(Structure):
    pass
_cpSegmentQueryHitPoint = (function_pointer(cpVect, cpVect, cpVect, cpSegmentQueryInfo)).in_dll(chipmunk_lib, '_cpSegmentQueryHitPoint')
_cpSegmentQueryHitDist = (function_pointer(cpFloat, cpVect, cpVect, cpSegmentQueryInfo)).in_dll(chipmunk_lib, '_cpSegmentQueryHitDist')
#cpVect._pack_ = 4
#cpVect _fields_ def removed
cpHashValue = c_uint
cpDataPointer = c_void_p
cpCollisionType = c_uint
cpGroup = c_uint
cpLayers = c_uint
cpTimestamp = c_uint
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
cpConstraintPreStepFunction = function_pointer(None, POINTER(cpConstraint), cpFloat, cpFloat)
cpConstraintApplyImpulseFunction = function_pointer(None, POINTER(cpConstraint))
cpConstraintGetImpulseFunction = function_pointer(cpFloat, POINTER(cpConstraint))
class cpConstraintClass(Structure):
    pass
cpConstraintClass._fields_ = [
    ('preStep', cpConstraintPreStepFunction),
    ('applyImpulse', cpConstraintApplyImpulseFunction),
    ('getImpulse', cpConstraintGetImpulseFunction),
]
#cpConstraint._pack_ = 4
cpConstraint._fields_ = [
    ('klass', POINTER(cpConstraintClass)),
    ('a', POINTER(cpBody)),
    ('b', POINTER(cpBody)),
    ('maxForce', cpFloat),
    ('biasCoef', cpFloat),
    ('maxBias', cpFloat),
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
cpDampedSpringForceFunc = function_pointer(cpFloat, POINTER(cpConstraint), cpFloat)
cpDampedSpringGetClass = chipmunk_lib.cpDampedSpringGetClass
cpDampedSpringGetClass.restype = POINTER(cpConstraintClass)
cpDampedSpringGetClass.argtypes = []
class cpDampedSpring(Structure):
    pass
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
    ('jMax', cpFloat),
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
    ('k1', cpVect),
    ('k2', cpVect),
    ('jAcc', cpVect),
    ('jMaxLen', cpFloat),
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
    ('jnMax', cpFloat),
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
#cpPivotJoint._pack_ = 4
cpPivotJoint._fields_ = [
    ('constraint', cpConstraint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('r1', cpVect),
    ('r2', cpVect),
    ('k1', cpVect),
    ('k2', cpVect),
    ('jAcc', cpVect),
    ('jMaxLen', cpFloat),
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
    ('jMax', cpFloat),
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
    ('jMax', cpFloat),
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
    ('jMax', cpFloat),
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
    ('jnMax', cpFloat),
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
class cpContact(Structure):
    pass
#cpContact._pack_ = 4
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
    ('hash', cpHashValue),
]
cpContactInit = chipmunk_lib.cpContactInit
cpContactInit.restype = POINTER(cpContact)
cpContactInit.argtypes = [POINTER(cpContact), cpVect, cpVect, cpFloat, cpHashValue]

# values for enumeration 'cpArbiterState'
cpArbiterState = c_int # enum
class cpCollisionHandler(Structure):
    pass
#cpArbiter._pack_ = 4
cpArbiter._fields_ = [
    ('numContacts', c_int),
    ('contacts', POINTER(cpContact)),
    ('private_a', POINTER(cpShape)),
    ('private_b', POINTER(cpShape)),
    ('e', cpFloat),
    ('u', cpFloat),
    ('surface_vr', cpVect),
    ('stamp', cpTimestamp),
    ('handler', POINTER(cpCollisionHandler)),
    ('swappedColl', cpBool),
    ('state', cpArbiterState),
]
cpArbiterInit = chipmunk_lib.cpArbiterInit
cpArbiterInit.restype = POINTER(cpArbiter)
cpArbiterInit.argtypes = [POINTER(cpArbiter), POINTER(cpShape), POINTER(cpShape)]
cpArbiterUpdate = chipmunk_lib.cpArbiterUpdate
cpArbiterUpdate.restype = None
cpArbiterUpdate.argtypes = [POINTER(cpArbiter), POINTER(cpContact), c_int, POINTER(cpCollisionHandler), POINTER(cpShape), POINTER(cpShape)]
cpArbiterPreStep = chipmunk_lib.cpArbiterPreStep
cpArbiterPreStep.restype = None
cpArbiterPreStep.argtypes = [POINTER(cpArbiter), cpFloat]
cpArbiterApplyCachedImpulse = chipmunk_lib.cpArbiterApplyCachedImpulse
cpArbiterApplyCachedImpulse.restype = None
cpArbiterApplyCachedImpulse.argtypes = [POINTER(cpArbiter)]
cpArbiterApplyImpulse = chipmunk_lib.cpArbiterApplyImpulse
cpArbiterApplyImpulse.restype = None
cpArbiterApplyImpulse.argtypes = [POINTER(cpArbiter), cpFloat]
cpArbiterTotalImpulse = chipmunk_lib.cpArbiterTotalImpulse
cpArbiterTotalImpulse.restype = cpVect
cpArbiterTotalImpulse.argtypes = [POINTER(cpArbiter)]
cpArbiterTotalImpulseWithFriction = chipmunk_lib.cpArbiterTotalImpulseWithFriction
cpArbiterTotalImpulseWithFriction.restype = cpVect
cpArbiterTotalImpulseWithFriction.argtypes = [POINTER(cpArbiter)]
cpArbiterIgnore = chipmunk_lib.cpArbiterIgnore
cpArbiterIgnore.restype = None
cpArbiterIgnore.argtypes = [POINTER(cpArbiter)]
cpArbiterGetNormal = chipmunk_lib.cpArbiterGetNormal
cpArbiterGetNormal.restype = cpVect
cpArbiterGetNormal.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterGetPoint = chipmunk_lib.cpArbiterGetPoint
cpArbiterGetPoint.restype = cpVect
cpArbiterGetPoint.argtypes = [POINTER(cpArbiter), c_int]
class cpArray(Structure):
    pass
cpArray._fields_ = [
    ('num', c_int),
    ('max', c_int),
    ('arr', POINTER(c_void_p)),
]
cpArrayIter = function_pointer(None, c_void_p, c_void_p)
cpArrayNew = chipmunk_lib.cpArrayNew
cpArrayNew.restype = POINTER(cpArray)
cpArrayNew.argtypes = [c_int]
cpArrayFree = chipmunk_lib.cpArrayFree
cpArrayFree.restype = None
cpArrayFree.argtypes = [POINTER(cpArray)]
cpArrayPush = chipmunk_lib.cpArrayPush
cpArrayPush.restype = None
cpArrayPush.argtypes = [POINTER(cpArray), c_void_p]
cpArrayPop = chipmunk_lib.cpArrayPop
cpArrayPop.restype = c_void_p
cpArrayPop.argtypes = [POINTER(cpArray)]
cpArrayDeleteObj = chipmunk_lib.cpArrayDeleteObj
cpArrayDeleteObj.restype = None
cpArrayDeleteObj.argtypes = [POINTER(cpArray), c_void_p]
cpArrayContains = chipmunk_lib.cpArrayContains
cpArrayContains.restype = cpBool
cpArrayContains.argtypes = [POINTER(cpArray), c_void_p]
#cpBB._pack_ = 4
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
cpBodyVelocityFunc = function_pointer(None, POINTER(cpBody), cpVect, cpFloat, cpFloat)
cpBodyPositionFunc = function_pointer(None, POINTER(cpBody), cpFloat)
class cpComponentNode(Structure):
    pass
#cpComponentNode._pack_ = 4
cpComponentNode._fields_ = [
    ('parent', POINTER(cpBody)),
    ('next', POINTER(cpBody)),
    ('rank', c_int),
    ('idleTime', cpFloat),
]
class cpSpace(Structure):
    pass
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
    ('v_bias', cpVect),
    ('w_bias', cpFloat),
    ('space', POINTER(cpSpace)),
    ('shapesList', POINTER(cpShape)),
    ('node', cpComponentNode),
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
cpBodyActivate = chipmunk_lib.cpBodyActivate
cpBodyActivate.restype = None
cpBodyActivate.argtypes = [POINTER(cpBody)]
cpBodySleep = chipmunk_lib.cpBodySleep
cpBodySleep.restype = None
cpBodySleep.argtypes = [POINTER(cpBody)]
cpBodySetMass = chipmunk_lib.cpBodySetMass
cpBodySetMass.restype = None
cpBodySetMass.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetMoment = chipmunk_lib.cpBodySetMoment
cpBodySetMoment.restype = None
cpBodySetMoment.argtypes = [POINTER(cpBody), cpFloat]
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
cpCollideShapes = chipmunk_lib.cpCollideShapes
cpCollideShapes.restype = c_int
cpCollideShapes.argtypes = [POINTER(cpShape), POINTER(cpShape), POINTER(cpContact)]
class cpHashSetBin(Structure):
    pass
cpHashSetBin._fields_ = [
    ('elt', c_void_p),
    ('hash', cpHashValue),
    ('next', POINTER(cpHashSetBin)),
]
cpHashSetEqlFunc = function_pointer(cpBool, c_void_p, c_void_p)
cpHashSetTransFunc = function_pointer(c_void_p, c_void_p, c_void_p)
class cpHashSet(Structure):
    pass
cpHashSet._fields_ = [
    ('entries', c_int),
    ('size', c_int),
    ('eql', cpHashSetEqlFunc),
    ('trans', cpHashSetTransFunc),
    ('default_value', c_void_p),
    ('table', POINTER(POINTER(cpHashSetBin))),
    ('pooledBins', POINTER(cpHashSetBin)),
    ('allocatedBuffers', POINTER(cpArray)),
]
cpHashSetFree = chipmunk_lib.cpHashSetFree
cpHashSetFree.restype = None
cpHashSetFree.argtypes = [POINTER(cpHashSet)]
cpHashSetNew = chipmunk_lib.cpHashSetNew
cpHashSetNew.restype = POINTER(cpHashSet)
cpHashSetNew.argtypes = [c_int, cpHashSetEqlFunc, cpHashSetTransFunc]
cpHashSetInsert = chipmunk_lib.cpHashSetInsert
cpHashSetInsert.restype = c_void_p
cpHashSetInsert.argtypes = [POINTER(cpHashSet), cpHashValue, c_void_p, c_void_p]
cpHashSetRemove = chipmunk_lib.cpHashSetRemove
cpHashSetRemove.restype = c_void_p
cpHashSetRemove.argtypes = [POINTER(cpHashSet), cpHashValue, c_void_p]
cpHashSetFind = chipmunk_lib.cpHashSetFind
cpHashSetFind.restype = c_void_p
cpHashSetFind.argtypes = [POINTER(cpHashSet), cpHashValue, c_void_p]
cpHashSetIterFunc = function_pointer(None, c_void_p, c_void_p)
cpHashSetEach = chipmunk_lib.cpHashSetEach
cpHashSetEach.restype = None
cpHashSetEach.argtypes = [POINTER(cpHashSet), cpHashSetIterFunc, c_void_p]
cpHashSetFilterFunc = function_pointer(cpBool, c_void_p, c_void_p)
cpHashSetFilter = chipmunk_lib.cpHashSetFilter
cpHashSetFilter.restype = None
cpHashSetFilter.argtypes = [POINTER(cpHashSet), cpHashSetFilterFunc, c_void_p]
class cpPolyShapeAxis(Structure):
    pass
#cpPolyShapeAxis._pack_ = 4
cpPolyShapeAxis._fields_ = [
    ('n', cpVect),
    ('d', cpFloat),
]
class cpPolyShape(Structure):
    pass
class cpShapeClass(Structure):
    pass
#cpShape._pack_ = 4
cpShape._fields_ = [
    ('klass', POINTER(cpShapeClass)),
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
    ('next', POINTER(cpShape)),
    ('hashid', cpHashValue),
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
cpBoxShapeInit = chipmunk_lib.cpBoxShapeInit
cpBoxShapeInit.restype = POINTER(cpPolyShape)
cpBoxShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpFloat, cpFloat]
cpBoxShapeNew = chipmunk_lib.cpBoxShapeNew
cpBoxShapeNew.restype = POINTER(cpShape)
cpBoxShapeNew.argtypes = [POINTER(cpBody), cpFloat, cpFloat]
cpPolyValidate = chipmunk_lib.cpPolyValidate
cpPolyValidate.restype = cpBool
cpPolyValidate.argtypes = [POINTER(cpVect), c_int]
cpPolyShapeGetNumVerts = chipmunk_lib.cpPolyShapeGetNumVerts
cpPolyShapeGetNumVerts.restype = c_int
cpPolyShapeGetNumVerts.argtypes = [POINTER(cpShape)]
cpPolyShapeGetVert = chipmunk_lib.cpPolyShapeGetVert
cpPolyShapeGetVert.restype = cpVect
cpPolyShapeGetVert.argtypes = [POINTER(cpShape), c_int]
#cpSegmentQueryInfo._pack_ = 4
cpSegmentQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('t', cpFloat),
    ('n', cpVect),
]

# values for enumeration 'cpShapeType'
cpShapeType = c_int # enum
cpShapeClass._fields_ = [
    ('type', cpShapeType),
    ('cacheData', function_pointer(cpBB, POINTER(cpShape), cpVect, cpVect)),
    ('destroy', function_pointer(None, POINTER(cpShape))),
    ('pointQuery', function_pointer(cpBool, POINTER(cpShape), cpVect)),
    ('segmentQuery', function_pointer(None, POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo))),
]
cpShapeInit = chipmunk_lib.cpShapeInit
cpShapeInit.restype = POINTER(cpShape)
cpShapeInit.argtypes = [POINTER(cpShape), POINTER(cpShapeClass), POINTER(cpBody)]
cpShapeDestroy = chipmunk_lib.cpShapeDestroy
cpShapeDestroy.restype = None
cpShapeDestroy.argtypes = [POINTER(cpShape)]
cpShapeFree = chipmunk_lib.cpShapeFree
cpShapeFree.restype = None
cpShapeFree.argtypes = [POINTER(cpShape)]
cpShapeCacheBB = chipmunk_lib.cpShapeCacheBB
cpShapeCacheBB.restype = cpBB
cpShapeCacheBB.argtypes = [POINTER(cpShape)]
cpShapePointQuery = chipmunk_lib.cpShapePointQuery
cpShapePointQuery.restype = cpBool
cpShapePointQuery.argtypes = [POINTER(cpShape), cpVect]
class cpCircleShape(Structure):
    pass
#cpCircleShape._pack_ = 4
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
cpResetShapeIdCounter = chipmunk_lib.cpResetShapeIdCounter
cpResetShapeIdCounter.restype = None
cpResetShapeIdCounter.argtypes = []
cpShapeSegmentQuery = chipmunk_lib.cpShapeSegmentQuery
cpShapeSegmentQuery.restype = cpBool
cpShapeSegmentQuery.argtypes = [POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo)]
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
class cpContactBufferHeader(Structure):
    pass
cpContactBufferHeader._fields_ = [
    ('stamp', cpTimestamp),
    ('next', POINTER(cpContactBufferHeader)),
    ('numContacts', c_uint),
]
class cpSpaceHash(Structure):
    pass
#cpSpace._pack_ = 4
cpSpace._fields_ = [
    ('iterations', c_int),
    ('elasticIterations', c_int),
    ('gravity', cpVect),
    ('damping', cpFloat),
    ('idleSpeedThreshold', cpFloat),
    ('sleepTimeThreshold', cpFloat),
    ('locked', cpBool),
    ('stamp', cpTimestamp),
    ('staticShapes', POINTER(cpSpaceHash)),
    ('activeShapes', POINTER(cpSpaceHash)),
    ('bodies', POINTER(cpArray)),
    ('sleepingComponents', POINTER(cpArray)),
    ('arbiters', POINTER(cpArray)),
    ('pooledArbiters', POINTER(cpArray)),
    ('contactBuffersHead', POINTER(cpContactBufferHeader)),
    ('_contactBuffersTail', POINTER(cpContactBufferHeader)),
    ('allocatedBuffers', POINTER(cpArray)),
    ('contactSet', POINTER(cpHashSet)),
    ('constraints', POINTER(cpArray)),
    ('collFuncSet', POINTER(cpHashSet)),
    ('defaultHandler', cpCollisionHandler),
    ('postStepCallbacks', POINTER(cpHashSet)),
    ('staticBody', cpBody),
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
cpPostStepFunc = function_pointer(None, POINTER(cpSpace), c_void_p, c_void_p)
cpSpaceAddPostStepCallback = chipmunk_lib.cpSpaceAddPostStepCallback
cpSpaceAddPostStepCallback.restype = None
cpSpaceAddPostStepCallback.argtypes = [POINTER(cpSpace), cpPostStepFunc, c_void_p, c_void_p]
cpSpacePointQueryFunc = function_pointer(None, POINTER(cpShape), c_void_p)
cpSpacePointQuery = chipmunk_lib.cpSpacePointQuery
cpSpacePointQuery.restype = None
cpSpacePointQuery.argtypes = [POINTER(cpSpace), cpVect, cpLayers, cpGroup, cpSpacePointQueryFunc, c_void_p]
cpSpacePointQueryFirst = chipmunk_lib.cpSpacePointQueryFirst
cpSpacePointQueryFirst.restype = POINTER(cpShape)
cpSpacePointQueryFirst.argtypes = [POINTER(cpSpace), cpVect, cpLayers, cpGroup]
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
cpSpaceBodyIterator = function_pointer(None, POINTER(cpBody), c_void_p)
cpSpaceEachBody = chipmunk_lib.cpSpaceEachBody
cpSpaceEachBody.restype = None
cpSpaceEachBody.argtypes = [POINTER(cpSpace), cpSpaceBodyIterator, c_void_p]
cpSpaceStep = chipmunk_lib.cpSpaceStep
cpSpaceStep.restype = None
cpSpaceStep.argtypes = [POINTER(cpSpace), cpFloat]
class cpHandle(Structure):
    pass
cpHandle._fields_ = [
    ('obj', c_void_p),
    ('retain', c_int),
    ('stamp', cpTimestamp),
]
class cpSpaceHashBin(Structure):
    pass
cpSpaceHashBin._fields_ = [
    ('handle', POINTER(cpHandle)),
    ('next', POINTER(cpSpaceHashBin)),
]
cpSpaceHashBBFunc = function_pointer(cpBB, c_void_p)
#cpSpaceHash._pack_ = 4
cpSpaceHash._fields_ = [
    ('numcells', c_int),
    ('celldim', cpFloat),
    ('bbfunc', cpSpaceHashBBFunc),
    ('handleSet', POINTER(cpHashSet)),
    ('pooledHandles', POINTER(cpArray)),
    ('table', POINTER(POINTER(cpSpaceHashBin))),
    ('pooledBins', POINTER(cpSpaceHashBin)),
    ('allocatedBuffers', POINTER(cpArray)),
    ('stamp', cpTimestamp),
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
cpSpaceHashResize = chipmunk_lib.cpSpaceHashResize
cpSpaceHashResize.restype = None
cpSpaceHashResize.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int]
cpSpaceHashIterator = function_pointer(None, c_void_p, c_void_p)
cpSpaceHashQueryFunc = function_pointer(None, c_void_p, c_void_p, c_void_p)
cpSpaceHashSegmentQueryFunc = function_pointer(cpFloat, c_void_p, c_void_p, c_void_p)
cpSpaceHashSegmentQuery = chipmunk_lib.cpSpaceHashSegmentQuery
cpSpaceHashSegmentQuery.restype = None
cpSpaceHashSegmentQuery.argtypes = [POINTER(cpSpaceHash), c_void_p, cpVect, cpVect, cpFloat, cpSpaceHashSegmentQueryFunc, c_void_p]
cpvlength = chipmunk_lib.cpvlength
cpvlength.restype = cpFloat
cpvlength.argtypes = [cpVect]
cpvslerp = chipmunk_lib.cpvslerp
cpvslerp.restype = cpVect
cpvslerp.argtypes = [cpVect, cpVect, cpFloat]
cpvslerpconst = chipmunk_lib.cpvslerpconst
cpvslerpconst.restype = cpVect
cpvslerpconst.argtypes = [cpVect, cpVect, cpFloat]
cpvforangle = chipmunk_lib.cpvforangle
cpvforangle.restype = cpVect
cpvforangle.argtypes = [cpFloat]
cpvtoangle = chipmunk_lib.cpvtoangle
cpvtoangle.restype = cpFloat
cpvtoangle.argtypes = [cpVect]
cpvstr = chipmunk_lib.cpvstr
cpvstr.restype = STRING
cpvstr.argtypes = [cpVect]
CP_MAX_CONTACTS_PER_ARBITER = 6 # Variable c_int '6'
CP_BUFFER_BYTES = 32768 # Variable c_int '32768'
cpTrue = 1 # Variable c_int '1'
CP_NO_GROUP = 0 # Variable c_uint '0u'
CP_HASH_COEF = 3344921057 # Variable c_ulong '-950046239ul'
CP_ALL_LAYERS = 4294967295L # Variable c_uint '-1u'
CP_USE_DOUBLES = 1 # Variable c_int '1'
cpFalse = 0 # Variable c_int '0'
__all__ = ['cpBodyResetForces', 'CP_BUFFER_BYTES', '_cpvnear',
           'cpSpaceBBQueryFunc', 'cpCollisionHandler', 'cpvslerp',
           'cpvlength', 'cpHashSetFind', 'cpRatchetJointInit',
           'cpDampedSpring', 'cpBodySetAngle', 'cpArbiterInit',
           'cpDampedRotarySpringAlloc', 'cpRotaryLimitJoint',
           'cpHashSetEach', 'cpMessage', 'cpContactInit',
           '_cpBodyIsRogue', 'cpArrayFree', 'cpSpaceHashIterator',
           'cpDampedSpringNew', 'cpHashSetRemove',
           'cpGrooveJointAlloc', 'cpvforangle', '_cpvunrotate',
           '_cpvrotate', 'cpSpacePointQueryFunc', 'cpHashSetIterFunc',
           'cpConstraintGetImpulseFunction',
           '_cpConstraintGetImpulse', 'cpSpaceHashSegmentQueryFunc',
           'cpArrayDeleteObj', 'cpPolyShapeAlloc',
           'cpDampedSpringInit', '_cpSegmentQueryHitDist',
           'cpSegmentQueryInfo', 'cpMomentForBox', 'cpSpace',
           'cpDampedRotarySpringNew', 'cpSpaceSegmentQueryFirst',
           'cpCircleShapeGetOffset', 'cpGearJointInit',
           'cpGrooveJointInit', 'cpArbiterGetPoint', 'cpBodyActivate',
           'cpSpacePointQuery', 'cpBody', '_cpveql', 'cpBodySetMass',
           'cpvstr', 'cpMomentForPoly', 'cpShapeType',
           'cpCircleShapeSetOffset', 'cpBodyDestroy', 'cpDataPointer',
           'cpArbiterStateNormal', 'cpArrayPush', 'CP_USE_DOUBLES',
           'CP_SEGMENT_SHAPE', 'cpArbiterState', 'cpHashSetNew',
           'cpVect', 'cpDampedRotarySpringGetClass',
           'cpDampedSpringForceFunc', 'cpSpaceHashInit',
           'cpSpaceRemoveStaticShape', 'cpSegmentShapeNew',
           'cpPolyShapeInit', 'CP_HASH_COEF', 'cpHashSetInsert',
           'cpPolyShapeNew', 'cpArbiterApplyCachedImpulse',
           'cpArbiterIgnore', 'cpSlideJoint', 'CP_POLY_SHAPE',
           'cpBodyUpdateVelocity', 'cpSpaceAlloc',
           'cpCircleShapeAlloc', '_cpArbiterGetShapes',
           'cpBodyUpdatePosition', 'cpCollisionPreSolveFunc',
           'cpSpaceDestroy', 'CP_NUM_SHAPES', 'cpContact',
           'cpSegmentShape', 'cpShapePointQuery', 'cpSlideJointAlloc',
           'cpSpaceNew', 'cpArbiterGetNormal', 'cpConstraint',
           'cpArbiter', 'cpArbiterStateSleep', 'cpGrooveJoint',
           'cpArbiterStateIgnore', 'cpSpaceAddCollisionHandler',
           'cpSpaceFree', 'cpCircleShapeNew', 'cpSpaceInit',
           'cpArrayIter', 'cpSpaceHashBin', 'cpBool',
           'cpCollisionBeginFunc', '_cpArbiterGetPoint',
           'cpArbiterUpdate', 'cpBBClampVect', 'cpFalse',
           'cpPivotJointNew', 'cpTrue', 'cpPivotJointNew2',
           'cpCircleShapeSetRadius', 'cpBodyFree',
           'cpRatchetJointGetClass', 'cpGearJointAlloc',
           'cpSpaceRemoveBody', 'cpBoxShapeNew',
           'CP_MAX_CONTACTS_PER_ARBITER', 'cpSpaceHashBBFunc',
           'cpSegmentShapeSetRadius', '_cpvnormalize_safe',
           'cpPivotJointInit', 'cpShapeSegmentQuery', 'cpHashSetBin',
           'cpHashSetTransFunc', 'cpSpaceBodyIterator',
           'cpVersionString', 'cpArrayContains', '_cpvnormalize',
           'cpBoxShapeInit', 'cpSegmentShapeAlloc', 'cpComponentNode',
           '_cpArbiterIsFirstContact', 'cpShapeFree', '_cpvperp',
           'cpPolyShape', 'cpSpaceAddBody', 'cpCollideShapes',
           'cpShape', 'cpPolyShapeGetNumVerts',
           'cpSimpleMotorGetClass', 'cpSpaceRemoveShape', '_cpvdot',
           'cpContactBufferHeader', '_cpvrperp', 'CP_CIRCLE_SHAPE',
           'cpSpaceHash', 'cpBodySleep', 'cpSpaceSegmentQuery',
           'cpSpaceHashAlloc', 'cpPinJoint', '_cpArbiterGetNormal',
           'cpDampedRotarySpringTorqueFunc', 'cpBBWrapVect',
           'cpSegmentShapeGetA', '_cpvcross', 'cpSegmentShapeGetB',
           '_cpBodyIsSleeping', 'cpGrooveJointGetClass',
           'cpCircleShapeInit', 'cpCollisionSeparateFunc',
           'cpPolyShapeGetVert', '_cpvmult', 'CP_HASH_PAIR', '_cpv',
           'cpBB', 'cpSpaceAddStaticShape', 'cpPinJointInit',
           'cpGearJoint', 'cpSpaceHashResize', 'cpSlideJointInit',
           'cpBodyVelocityFunc', 'cpSpaceAddShape', 'cpPinJointAlloc',
           'cpArrayNew', 'cpHashValue', 'cpCollisionPostSolveFunc',
           'cpConstraintDestroy', 'MAKE_REF', 'cpArrayPop', 'cpArray',
           '_cpvlerpconst', 'cpSlideJointNew',
           'cpArbiterTotalImpulseWithFriction', 'cpDampedSpringAlloc',
           'cpArbiterStateFirstColl', 'cpRotaryLimitJointAlloc',
           'cpSegmentShapeInit', 'cpSimpleMotorAlloc',
           'cpShapeCacheBB', 'cpShapeInit', 'cpCollisionType',
           'cpGroup', 'cpMomentForCircle', 'cpSegmentShapeGetRadius',
           'cpHandle', 'cpTimestamp', 'cpGearJointSetRatio',
           'cpSpaceStep', 'cpSpaceHashSegmentQuery',
           'cpRotaryLimitJointInit', 'cpSpaceRemoveConstraint',
           'cpvtoangle', 'cpSpaceSetDefaultCollisionHandler',
           '_cpvclamp', 'cpSpaceAddPostStepCallback',
           'cpRotaryLimitJointNew', 'cpPivotJointGetClass',
           'cpArbiterApplyImpulse', 'cpLayers', 'cpHashSetFree',
           'cpConstraintFree', '_cpvproject', 'cpBodyInit',
           'cpGearJointGetClass', 'cpBodyNew', 'cpBodySetMoment',
           'cpHashSet', 'cpBodyPositionFunc',
           'cpGrooveJointSetGrooveA', 'cpGrooveJointSetGrooveB',
           '_cpBodyLocal2World', 'cpConstraintClass', 'cpFloat',
           '_cpvlerp', 'cpPinJointNew', '_cpvlengthsq',
           'cpPostStepFunc', '_cpSegmentQueryHitPoint',
           'cpConstraintApplyImpulseFunction', 'cpInitChipmunk',
           'cpRatchetJointAlloc', 'cpCircleShapeGetRadius',
           'cpSpaceAddConstraint', '_cpBodyKineticEnergy',
           'cpSpaceHashNew', '_cpBodyWorld2Local', 'cpBodyApplyForce',
           'cpSpacePointQueryFirst', 'CP_NO_GROUP',
           'cpMomentForSegment', 'cpSimpleMotorNew',
           'cpRotaryLimitJointGetClass',
           'cpSpaceRemoveCollisionHandler', 'cpSpaceEachBody',
           'cpPivotJointAlloc', 'cpRatchetJointNew', 'cpGearJointNew',
           'cpArbiterTotalImpulse', 'cpvslerpconst', 'CP_ALL_LAYERS',
           'cpSpaceBBQuery', 'cpResetShapeIdCounter', 'cpPivotJoint',
           'cpDampedRotarySpringInit', 'cpArbiterPreStep',
           'cpSlideJointGetClass', 'cpDampedRotarySpring', '_cpvneg',
           'cpSimpleMotor', 'cpHashSetFilterFunc', '_cpvsub',
           'cpSegmentShapeSetEndpoints', '_cpBodyApplyImpulse',
           'cpPolyShapeSetVerts', 'cpRatchetJoint',
           'cpSpaceHashQueryFunc', 'cpConstraintPreStepFunction',
           'cpPinJointGetClass', 'cpDampedSpringGetClass',
           'cpHashSetEqlFunc', 'cpPolyShapeAxis',
           'cpArbiterStateCached', '_cpvdistsq',
           'cpSegmentShapeGetNormal', 'cpShapeDestroy',
           'cpSimpleMotorInit', '_cpvadd', '_cpvdist', 'cpShapeClass',
           'cpBodyAlloc', 'cpGrooveJointNew', 'cpHashSetFilter',
           'cpCircleShape', 'cpSpaceSegmentQueryFunc',
           'cpPolyValidate', '_cpBBNew']
