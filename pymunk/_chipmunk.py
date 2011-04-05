from ctypes import *

STRING = c_char_p
_libraries = {}
_libraries['../pymunk/libchipmunk.so'] = CDLL('../pymunk/libchipmunk.so')


def CP_PRIVATE(symbol): return symbol ##_private # macro
# cpfexp = exp # alias
# def CP_DefineBodyStructSetter(type,member,name): return static inline void cpBodySet ##name(cpBody *body, const type value){ cpBodyActivate(body); body->member = value; } # macro
# def CP_ARBITER_GET_SHAPES(arb,a,b): return cpShape *a, *b; cpArbiterGetShapes(arb, &a, &b); # macro
# cpfatan2 = atan2 # alias
# cpfcos = cos # alias
# def CP_DefineShapeStructSetter(type,member,name,activates): return static inline void cpShapeSet ##name(cpShape *shape, type value){ if(activates) cpBodyActivate(shape->body); shape->member = value; } # macro
CP_POLY_SHAPE = 2
# def cpAssertWarn(condition,message): return if(!(condition)) cpMessage(message, #condition, __FILE__, __LINE__, 0) # macro
# def cpConstraintCheckCast(constraint,struct): return cpAssert(constraint->CP_PRIVATE(klass) == struct ##GetClass(), "Constraint is not a "#struct) # macro
# cpfmod = fmod # alias
# def CP_ARBITER_GET_BODIES(arb,a,b): return cpBody *a, *b; cpArbiterGetBodies(arb, &a, &b); # macro
# def cpAssert(condition,message): return if(!(condition)) cpMessage(message, #condition, __FILE__, __LINE__, 1) # macro
# def CP_DefineConstraintSetter(struct,type,member,name): return static inline void struct ##Set ##name(cpConstraint *constraint, type value){ cpConstraintCheckCast(constraint, struct); cpConstraintActivateBodies(constraint); ((struct *)constraint)->member = value; } # macro
cpArbiterStateIgnore = 2
# cpfree = free # alias
# cpfsqrt = sqrt # alias
# cpfpow = pow # alias
CP_SEGMENT_SHAPE = 1
# cprealloc = realloc # alias
# def CP_DefineBodyStructGetter(type,member,name): return static inline type cpBodyGet ##name(const cpBody *body){return body->member;} # macro
# def CP_DefineShapeStructProperty(type,member,name,activates): return CP_DefineShapeStructGetter(type, member, name) CP_DefineShapeStructSetter(type, member, name, activates) # macro
# def CP_DeclareShapeGetter(struct,type,name): return type struct ##Get ##name(const cpShape *shape) # macro
CP_CIRCLE_SHAPE = 0
# cpfacos = acos # alias
# def CP_DefineConstraintStructProperty(type,member,name): return CP_DefineConstraintStructGetter(type, member, name) CP_DefineConstraintStructSetter(type, member, name) # macro
cpArbiterStateFirstColl = 1
# def CP_DefineConstraintGetter(struct,type,member,name): return static inline type struct ##Get ##name(const cpConstraint *constraint){ cpConstraintCheckCast(constraint, struct); return ((struct *)constraint)->member; } # macro
# cpcalloc = calloc # alias
def MAKE_REF(name): return __typeof__(name) *_ ##name = name # macro
# cpmalloc = malloc # alias
# def CP_DefineShapeStructGetter(type,member,name): return static inline type cpShapeGet ##name(const cpShape *shape){return shape->member;} # macro
# def CP_DefineConstraintStructSetter(type,member,name): return static inline void cpConstraint ##Set ##name(cpConstraint *constraint, type value){ cpConstraintActivateBodies(constraint); constraint->member = value; } # macro
# def CP_DefineBodyStructProperty(type,member,name): return CP_DefineBodyStructGetter(type, member, name) CP_DefineBodyStructSetter(type, member, name) # macro
# def CP_DefineConstraintStructGetter(type,member,name): return static inline type cpConstraint ##Get ##name(const cpConstraint *constraint){return constraint->member;} # macro
CP_NUM_SHAPES = 3
# cpfsin = sin # alias
# cpfceil = ceil # alias
# cpffloor = floor # alias
cpArbiterStateCached = 3
cpArbiterStateNormal = 0
# def CP_DefineConstraintProperty(struct,type,member,name): return CP_DefineConstraintGetter(struct, type, member, name) CP_DefineConstraintSetter(struct, type, member, name) # macro
cpMessage = _libraries['../pymunk/libchipmunk.so'].cpMessage
cpMessage.restype = None
cpMessage.argtypes = [STRING, STRING, STRING, c_int, c_int]
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
class cpArbiter(Structure):
    pass
class cpSpace(Structure):
    pass
cpVersionString = (STRING).in_dll(_libraries['../pymunk/libchipmunk.so'], 'cpVersionString')
cpInitChipmunk = _libraries['../pymunk/libchipmunk.so'].cpInitChipmunk
cpInitChipmunk.restype = None
cpInitChipmunk.argtypes = []
cpFloat = c_double
class cpVect(Structure):
    pass
cpMomentForCircle = _libraries['../pymunk/libchipmunk.so'].cpMomentForCircle
cpMomentForCircle.restype = cpFloat
cpMomentForCircle.argtypes = [cpFloat, cpFloat, cpFloat, cpVect]
cpAreaForCircle = _libraries['../pymunk/libchipmunk.so'].cpAreaForCircle
cpAreaForCircle.restype = cpFloat
cpAreaForCircle.argtypes = [cpFloat, cpFloat]
cpMomentForSegment = _libraries['../pymunk/libchipmunk.so'].cpMomentForSegment
cpMomentForSegment.restype = cpFloat
cpMomentForSegment.argtypes = [cpFloat, cpVect, cpVect]
cpAreaForSegment = _libraries['../pymunk/libchipmunk.so'].cpAreaForSegment
cpAreaForSegment.restype = cpFloat
cpAreaForSegment.argtypes = [cpVect, cpVect, cpFloat]
cpMomentForPoly = _libraries['../pymunk/libchipmunk.so'].cpMomentForPoly
cpMomentForPoly.restype = cpFloat
cpMomentForPoly.argtypes = [cpFloat, c_int, POINTER(cpVect), cpVect]
cpAreaForPoly = _libraries['../pymunk/libchipmunk.so'].cpAreaForPoly
cpAreaForPoly.restype = cpFloat
cpAreaForPoly.argtypes = [c_int, POINTER(cpVect)]
cpCentroidForPoly = _libraries['../pymunk/libchipmunk.so'].cpCentroidForPoly
cpCentroidForPoly.restype = cpVect
cpCentroidForPoly.argtypes = [c_int, POINTER(cpVect)]
cpRecenterPoly = _libraries['../pymunk/libchipmunk.so'].cpRecenterPoly
cpRecenterPoly.restype = None
cpRecenterPoly.argtypes = [c_int, POINTER(cpVect)]
cpMomentForBox = _libraries['../pymunk/libchipmunk.so'].cpMomentForBox
cpMomentForBox.restype = cpFloat
cpMomentForBox.argtypes = [cpFloat, cpFloat, cpFloat]
_cpv = (CFUNCTYPE(cpVect, cpFloat, cpFloat)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpv')
cpBool = c_int
_cpveql = (CFUNCTYPE(cpBool, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpveql')
_cpvadd = (CFUNCTYPE(cpVect, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvadd')
_cpvneg = (CFUNCTYPE(cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvneg')
_cpvsub = (CFUNCTYPE(cpVect, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvsub')
_cpvmult = (CFUNCTYPE(cpVect, cpVect, cpFloat)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvmult')
_cpvdot = (CFUNCTYPE(cpFloat, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvdot')
_cpvcross = (CFUNCTYPE(cpFloat, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvcross')
_cpvperp = (CFUNCTYPE(cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvperp')
_cpvrperp = (CFUNCTYPE(cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvrperp')
_cpvproject = (CFUNCTYPE(cpVect, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvproject')
_cpvrotate = (CFUNCTYPE(cpVect, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvrotate')
_cpvunrotate = (CFUNCTYPE(cpVect, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvunrotate')
_cpvlengthsq = (CFUNCTYPE(cpFloat, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvlengthsq')
_cpvlerp = (CFUNCTYPE(cpVect, cpVect, cpVect, cpFloat)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvlerp')
_cpvnormalize = (CFUNCTYPE(cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvnormalize')
_cpvnormalize_safe = (CFUNCTYPE(cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvnormalize_safe')
_cpvclamp = (CFUNCTYPE(cpVect, cpVect, cpFloat)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvclamp')
_cpvlerpconst = (CFUNCTYPE(cpVect, cpVect, cpVect, cpFloat)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvlerpconst')
_cpvdist = (CFUNCTYPE(cpFloat, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvdist')
_cpvdistsq = (CFUNCTYPE(cpFloat, cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvdistsq')
_cpvnear = (CFUNCTYPE(cpBool, cpVect, cpVect, cpFloat)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpvnear')
class cpBB(Structure):
    pass
_cpBBNew = (CFUNCTYPE(cpBB, cpFloat, cpFloat, cpFloat, cpFloat)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBBNew')
_cpBBIntersects = (CFUNCTYPE(cpBool, cpBB, cpBB)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBBIntersects')
_cpBBContainsBB = (CFUNCTYPE(cpBool, cpBB, cpBB)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBBContainsBB')
_cpBBContainsVect = (CFUNCTYPE(cpBool, cpBB, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBBContainsVect')
_cpBBMerge = (CFUNCTYPE(cpBB, cpBB, cpBB)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBBMerge')
_cpBBExpand = (CFUNCTYPE(cpBB, cpBB, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBBExpand')
_cpBodyWorld2Local = (CFUNCTYPE(cpVect, POINTER(cpBody), cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBodyWorld2Local')
_cpBodyLocal2World = (CFUNCTYPE(cpVect, POINTER(cpBody), cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBodyLocal2World')
_cpBodyApplyImpulse = (CFUNCTYPE(None, POINTER(cpBody), cpVect, cpVect)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBodyApplyImpulse')
_cpBodyIsSleeping = (CFUNCTYPE(cpBool, POINTER(cpBody))).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBodyIsSleeping')
_cpBodyIsRogue = (CFUNCTYPE(cpBool, POINTER(cpBody))).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBodyIsRogue')
_cpBodyKineticEnergy = (CFUNCTYPE(cpFloat, POINTER(cpBody))).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpBodyKineticEnergy')
_cpArbiterIsFirstContact = (CFUNCTYPE(cpBool, POINTER(cpArbiter))).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpArbiterIsFirstContact')
_cpArbiterGetShapes = (CFUNCTYPE(None, POINTER(cpArbiter), POINTER(POINTER(cpShape)), POINTER(POINTER(cpShape)))).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpArbiterGetShapes')
_cpArbiterGetNormal = (CFUNCTYPE(cpVect, POINTER(cpArbiter), c_int)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpArbiterGetNormal')
_cpArbiterGetPoint = (CFUNCTYPE(cpVect, POINTER(cpArbiter), c_int)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpArbiterGetPoint')
_cpConstraintGetImpulse = (CFUNCTYPE(cpFloat, POINTER(cpConstraint))).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpConstraintGetImpulse')
class cpSegmentQueryInfo(Structure):
    pass
_cpSegmentQueryHitPoint = (CFUNCTYPE(cpVect, cpVect, cpVect, cpSegmentQueryInfo)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpSegmentQueryHitPoint')
_cpSegmentQueryHitDist = (CFUNCTYPE(cpFloat, cpVect, cpVect, cpSegmentQueryInfo)).in_dll(_libraries['../pymunk/libchipmunk.so'], '_cpSegmentQueryHitDist')
cpHashValue = c_uint
cpDataPointer = c_void_p
cpCollisionType = c_uint
cpGroup = c_uint
cpLayers = c_uint
cpTimestamp = c_uint
cpVect._pack_ = 4
cpVect._fields_ = [
    ('x', cpFloat),
    ('y', cpFloat),
]
cpCircleShapeSetRadius = _libraries['../pymunk/libchipmunk.so'].cpCircleShapeSetRadius
cpCircleShapeSetRadius.restype = None
cpCircleShapeSetRadius.argtypes = [POINTER(cpShape), cpFloat]
cpCircleShapeSetOffset = _libraries['../pymunk/libchipmunk.so'].cpCircleShapeSetOffset
cpCircleShapeSetOffset.restype = None
cpCircleShapeSetOffset.argtypes = [POINTER(cpShape), cpVect]
cpSegmentShapeSetEndpoints = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeSetEndpoints
cpSegmentShapeSetEndpoints.restype = None
cpSegmentShapeSetEndpoints.argtypes = [POINTER(cpShape), cpVect, cpVect]
cpSegmentShapeSetRadius = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeSetRadius
cpSegmentShapeSetRadius.restype = None
cpSegmentShapeSetRadius.argtypes = [POINTER(cpShape), cpFloat]
cpPolyShapeSetVerts = _libraries['../pymunk/libchipmunk.so'].cpPolyShapeSetVerts
cpPolyShapeSetVerts.restype = None
cpPolyShapeSetVerts.argtypes = [POINTER(cpShape), c_int, POINTER(cpVect), cpVect]
class cpConstraintClass(Structure):
    pass
cpConstraintPreStepImpl = CFUNCTYPE(None, POINTER(cpConstraint), cpFloat)
cpConstraintApplyCachedImpulseImpl = CFUNCTYPE(None, POINTER(cpConstraint), cpFloat)
cpConstraintApplyImpulseImpl = CFUNCTYPE(None, POINTER(cpConstraint))
cpConstraintGetImpulseImpl = CFUNCTYPE(cpFloat, POINTER(cpConstraint))
cpConstraintClass._fields_ = [
    ('preStep', cpConstraintPreStepImpl),
    ('applyCachedImpulse', cpConstraintApplyCachedImpulseImpl),
    ('applyImpulse', cpConstraintApplyImpulseImpl),
    ('getImpulse', cpConstraintGetImpulseImpl),
]
cpConstraint._pack_ = 4
cpConstraint._fields_ = [
    ('klass_private', POINTER(cpConstraintClass)),
    ('a', POINTER(cpBody)),
    ('b', POINTER(cpBody)),
    ('next_a_private', POINTER(cpConstraint)),
    ('next_b_private', POINTER(cpConstraint)),
    ('maxForce', cpFloat),
    ('errorBias', cpFloat),
    ('maxBias', cpFloat),
    ('data', cpDataPointer),
]
cpConstraintDestroy = _libraries['../pymunk/libchipmunk.so'].cpConstraintDestroy
cpConstraintDestroy.restype = None
cpConstraintDestroy.argtypes = [POINTER(cpConstraint)]
cpConstraintFree = _libraries['../pymunk/libchipmunk.so'].cpConstraintFree
cpConstraintFree.restype = None
cpConstraintFree.argtypes = [POINTER(cpConstraint)]
cpDampedRotarySpringTorqueFunc = CFUNCTYPE(cpFloat, POINTER(cpConstraint), cpFloat)
cpDampedRotarySpringGetClass = _libraries['../pymunk/libchipmunk.so'].cpDampedRotarySpringGetClass
cpDampedRotarySpringGetClass.restype = POINTER(cpConstraintClass)
cpDampedRotarySpringGetClass.argtypes = []
class cpDampedRotarySpring(Structure):
    pass
cpDampedRotarySpring._pack_ = 4
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
cpDampedRotarySpringAlloc = _libraries['../pymunk/libchipmunk.so'].cpDampedRotarySpringAlloc
cpDampedRotarySpringAlloc.restype = POINTER(cpDampedRotarySpring)
cpDampedRotarySpringAlloc.argtypes = []
cpDampedRotarySpringInit = _libraries['../pymunk/libchipmunk.so'].cpDampedRotarySpringInit
cpDampedRotarySpringInit.restype = POINTER(cpDampedRotarySpring)
cpDampedRotarySpringInit.argtypes = [POINTER(cpDampedRotarySpring), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat, cpFloat]
cpDampedRotarySpringNew = _libraries['../pymunk/libchipmunk.so'].cpDampedRotarySpringNew
cpDampedRotarySpringNew.restype = POINTER(cpConstraint)
cpDampedRotarySpringNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat, cpFloat]
class cpDampedSpring(Structure):
    pass
cpDampedSpringForceFunc = CFUNCTYPE(cpFloat, POINTER(cpConstraint), cpFloat)
cpDampedSpringGetClass = _libraries['../pymunk/libchipmunk.so'].cpDampedSpringGetClass
cpDampedSpringGetClass.restype = POINTER(cpConstraintClass)
cpDampedSpringGetClass.argtypes = []
cpDampedSpring._pack_ = 4
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
cpDampedSpringAlloc = _libraries['../pymunk/libchipmunk.so'].cpDampedSpringAlloc
cpDampedSpringAlloc.restype = POINTER(cpDampedSpring)
cpDampedSpringAlloc.argtypes = []
cpDampedSpringInit = _libraries['../pymunk/libchipmunk.so'].cpDampedSpringInit
cpDampedSpringInit.restype = POINTER(cpDampedSpring)
cpDampedSpringInit.argtypes = [POINTER(cpDampedSpring), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat]
cpDampedSpringNew = _libraries['../pymunk/libchipmunk.so'].cpDampedSpringNew
cpDampedSpringNew.restype = POINTER(cpConstraint)
cpDampedSpringNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat]
cpGearJointGetClass = _libraries['../pymunk/libchipmunk.so'].cpGearJointGetClass
cpGearJointGetClass.restype = POINTER(cpConstraintClass)
cpGearJointGetClass.argtypes = []
class cpGearJoint(Structure):
    pass
cpGearJoint._pack_ = 4
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
cpGearJointAlloc = _libraries['../pymunk/libchipmunk.so'].cpGearJointAlloc
cpGearJointAlloc.restype = POINTER(cpGearJoint)
cpGearJointAlloc.argtypes = []
cpGearJointInit = _libraries['../pymunk/libchipmunk.so'].cpGearJointInit
cpGearJointInit.restype = POINTER(cpGearJoint)
cpGearJointInit.argtypes = [POINTER(cpGearJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpGearJointNew = _libraries['../pymunk/libchipmunk.so'].cpGearJointNew
cpGearJointNew.restype = POINTER(cpConstraint)
cpGearJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpGearJointSetRatio = _libraries['../pymunk/libchipmunk.so'].cpGearJointSetRatio
cpGearJointSetRatio.restype = None
cpGearJointSetRatio.argtypes = [POINTER(cpConstraint), cpFloat]
cpGrooveJointGetClass = _libraries['../pymunk/libchipmunk.so'].cpGrooveJointGetClass
cpGrooveJointGetClass.restype = POINTER(cpConstraintClass)
cpGrooveJointGetClass.argtypes = []
class cpGrooveJoint(Structure):
    pass
cpGrooveJoint._pack_ = 4
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
cpGrooveJointAlloc = _libraries['../pymunk/libchipmunk.so'].cpGrooveJointAlloc
cpGrooveJointAlloc.restype = POINTER(cpGrooveJoint)
cpGrooveJointAlloc.argtypes = []
cpGrooveJointInit = _libraries['../pymunk/libchipmunk.so'].cpGrooveJointInit
cpGrooveJointInit.restype = POINTER(cpGrooveJoint)
cpGrooveJointInit.argtypes = [POINTER(cpGrooveJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
cpGrooveJointNew = _libraries['../pymunk/libchipmunk.so'].cpGrooveJointNew
cpGrooveJointNew.restype = POINTER(cpConstraint)
cpGrooveJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
cpGrooveJointSetGrooveA = _libraries['../pymunk/libchipmunk.so'].cpGrooveJointSetGrooveA
cpGrooveJointSetGrooveA.restype = None
cpGrooveJointSetGrooveA.argtypes = [POINTER(cpConstraint), cpVect]
cpGrooveJointSetGrooveB = _libraries['../pymunk/libchipmunk.so'].cpGrooveJointSetGrooveB
cpGrooveJointSetGrooveB.restype = None
cpGrooveJointSetGrooveB.argtypes = [POINTER(cpConstraint), cpVect]
cpPinJointGetClass = _libraries['../pymunk/libchipmunk.so'].cpPinJointGetClass
cpPinJointGetClass.restype = POINTER(cpConstraintClass)
cpPinJointGetClass.argtypes = []
class cpPinJoint(Structure):
    pass
cpPinJoint._pack_ = 4
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
cpPinJointAlloc = _libraries['../pymunk/libchipmunk.so'].cpPinJointAlloc
cpPinJointAlloc.restype = POINTER(cpPinJoint)
cpPinJointAlloc.argtypes = []
cpPinJointInit = _libraries['../pymunk/libchipmunk.so'].cpPinJointInit
cpPinJointInit.restype = POINTER(cpPinJoint)
cpPinJointInit.argtypes = [POINTER(cpPinJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPinJointNew = _libraries['../pymunk/libchipmunk.so'].cpPinJointNew
cpPinJointNew.restype = POINTER(cpConstraint)
cpPinJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPivotJointGetClass = _libraries['../pymunk/libchipmunk.so'].cpPivotJointGetClass
cpPivotJointGetClass.restype = POINTER(cpConstraintClass)
cpPivotJointGetClass.argtypes = []
class cpPivotJoint(Structure):
    pass
cpPivotJoint._pack_ = 4
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
cpPivotJointAlloc = _libraries['../pymunk/libchipmunk.so'].cpPivotJointAlloc
cpPivotJointAlloc.restype = POINTER(cpPivotJoint)
cpPivotJointAlloc.argtypes = []
cpPivotJointInit = _libraries['../pymunk/libchipmunk.so'].cpPivotJointInit
cpPivotJointInit.restype = POINTER(cpPivotJoint)
cpPivotJointInit.argtypes = [POINTER(cpPivotJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPivotJointNew = _libraries['../pymunk/libchipmunk.so'].cpPivotJointNew
cpPivotJointNew.restype = POINTER(cpConstraint)
cpPivotJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect]
cpPivotJointNew2 = _libraries['../pymunk/libchipmunk.so'].cpPivotJointNew2
cpPivotJointNew2.restype = POINTER(cpConstraint)
cpPivotJointNew2.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpRatchetJointGetClass = _libraries['../pymunk/libchipmunk.so'].cpRatchetJointGetClass
cpRatchetJointGetClass.restype = POINTER(cpConstraintClass)
cpRatchetJointGetClass.argtypes = []
class cpRatchetJoint(Structure):
    pass
cpRatchetJoint._pack_ = 4
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
cpRatchetJointAlloc = _libraries['../pymunk/libchipmunk.so'].cpRatchetJointAlloc
cpRatchetJointAlloc.restype = POINTER(cpRatchetJoint)
cpRatchetJointAlloc.argtypes = []
cpRatchetJointInit = _libraries['../pymunk/libchipmunk.so'].cpRatchetJointInit
cpRatchetJointInit.restype = POINTER(cpRatchetJoint)
cpRatchetJointInit.argtypes = [POINTER(cpRatchetJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRatchetJointNew = _libraries['../pymunk/libchipmunk.so'].cpRatchetJointNew
cpRatchetJointNew.restype = POINTER(cpConstraint)
cpRatchetJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRotaryLimitJointGetClass = _libraries['../pymunk/libchipmunk.so'].cpRotaryLimitJointGetClass
cpRotaryLimitJointGetClass.restype = POINTER(cpConstraintClass)
cpRotaryLimitJointGetClass.argtypes = []
class cpRotaryLimitJoint(Structure):
    pass
cpRotaryLimitJoint._pack_ = 4
cpRotaryLimitJoint._fields_ = [
    ('constraint', cpConstraint),
    ('min', cpFloat),
    ('max', cpFloat),
    ('iSum', cpFloat),
    ('bias', cpFloat),
    ('jAcc', cpFloat),
    ('jMax', cpFloat),
]
cpRotaryLimitJointAlloc = _libraries['../pymunk/libchipmunk.so'].cpRotaryLimitJointAlloc
cpRotaryLimitJointAlloc.restype = POINTER(cpRotaryLimitJoint)
cpRotaryLimitJointAlloc.argtypes = []
cpRotaryLimitJointInit = _libraries['../pymunk/libchipmunk.so'].cpRotaryLimitJointInit
cpRotaryLimitJointInit.restype = POINTER(cpRotaryLimitJoint)
cpRotaryLimitJointInit.argtypes = [POINTER(cpRotaryLimitJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRotaryLimitJointNew = _libraries['../pymunk/libchipmunk.so'].cpRotaryLimitJointNew
cpRotaryLimitJointNew.restype = POINTER(cpConstraint)
cpRotaryLimitJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpSimpleMotorGetClass = _libraries['../pymunk/libchipmunk.so'].cpSimpleMotorGetClass
cpSimpleMotorGetClass.restype = POINTER(cpConstraintClass)
cpSimpleMotorGetClass.argtypes = []
class cpSimpleMotor(Structure):
    pass
cpSimpleMotor._pack_ = 4
cpSimpleMotor._fields_ = [
    ('constraint', cpConstraint),
    ('rate', cpFloat),
    ('iSum', cpFloat),
    ('jAcc', cpFloat),
    ('jMax', cpFloat),
]
cpSimpleMotorAlloc = _libraries['../pymunk/libchipmunk.so'].cpSimpleMotorAlloc
cpSimpleMotorAlloc.restype = POINTER(cpSimpleMotor)
cpSimpleMotorAlloc.argtypes = []
cpSimpleMotorInit = _libraries['../pymunk/libchipmunk.so'].cpSimpleMotorInit
cpSimpleMotorInit.restype = POINTER(cpSimpleMotor)
cpSimpleMotorInit.argtypes = [POINTER(cpSimpleMotor), POINTER(cpBody), POINTER(cpBody), cpFloat]
cpSimpleMotorNew = _libraries['../pymunk/libchipmunk.so'].cpSimpleMotorNew
cpSimpleMotorNew.restype = POINTER(cpConstraint)
cpSimpleMotorNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat]
cpSlideJointGetClass = _libraries['../pymunk/libchipmunk.so'].cpSlideJointGetClass
cpSlideJointGetClass.restype = POINTER(cpConstraintClass)
cpSlideJointGetClass.argtypes = []
class cpSlideJoint(Structure):
    pass
cpSlideJoint._pack_ = 4
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
cpSlideJointAlloc = _libraries['../pymunk/libchipmunk.so'].cpSlideJointAlloc
cpSlideJointAlloc.restype = POINTER(cpSlideJoint)
cpSlideJointAlloc.argtypes = []
cpSlideJointInit = _libraries['../pymunk/libchipmunk.so'].cpSlideJointInit
cpSlideJointInit.restype = POINTER(cpSlideJoint)
cpSlideJointInit.argtypes = [POINTER(cpSlideJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpSlideJointNew = _libraries['../pymunk/libchipmunk.so'].cpSlideJointNew
cpSlideJointNew.restype = POINTER(cpConstraint)
cpSlideJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpCollisionBeginFunc = CFUNCTYPE(cpBool, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
cpCollisionPreSolveFunc = CFUNCTYPE(cpBool, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
cpCollisionPostSolveFunc = CFUNCTYPE(None, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
cpCollisionSeparateFunc = CFUNCTYPE(None, POINTER(cpArbiter), POINTER(cpSpace), c_void_p)
class cpCollisionHandler(Structure):
    pass
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
cpArbiter._pack_ = 4
cpArbiter._fields_ = [
    ('e', cpFloat),
    ('u', cpFloat),
    ('surface_vr', cpVect),
    ('a_private', POINTER(cpShape)),
    ('b_private', POINTER(cpShape)),
    ('body_a_private', POINTER(cpBody)),
    ('body_b_private', POINTER(cpBody)),
    ('next_a_private', POINTER(cpArbiter)),
    ('next_b_private', POINTER(cpArbiter)),
    ('numContacts_private', c_int),
    ('contacts_private', POINTER(cpContact)),
    ('stamp_private', cpTimestamp),
    ('handler_private', POINTER(cpCollisionHandler)),
    ('swappedColl_private', cpBool),
    ('state_private', cpArbiterState),
]
cpArbiterTotalImpulse = _libraries['../pymunk/libchipmunk.so'].cpArbiterTotalImpulse
cpArbiterTotalImpulse.restype = cpVect
cpArbiterTotalImpulse.argtypes = [POINTER(cpArbiter)]
cpArbiterTotalImpulseWithFriction = _libraries['../pymunk/libchipmunk.so'].cpArbiterTotalImpulseWithFriction
cpArbiterTotalImpulseWithFriction.restype = cpVect
cpArbiterTotalImpulseWithFriction.argtypes = [POINTER(cpArbiter)]
cpArbiterIgnore = _libraries['../pymunk/libchipmunk.so'].cpArbiterIgnore
cpArbiterIgnore.restype = None
cpArbiterIgnore.argtypes = [POINTER(cpArbiter)]
class cpContactPointSet(Structure):
    pass
class N17cpContactPointSet3DOT_0E(Structure):
    pass
N17cpContactPointSet3DOT_0E._pack_ = 4
N17cpContactPointSet3DOT_0E._fields_ = [
    ('point', cpVect),
    ('normal', cpVect),
    ('dist', cpFloat),
]
cpContactPointSet._fields_ = [
    ('count', c_int),
    ('points', N17cpContactPointSet3DOT_0E * 4),
]
cpArbiterGetContactPointSet = _libraries['../pymunk/libchipmunk.so'].cpArbiterGetContactPointSet
cpArbiterGetContactPointSet.restype = cpContactPointSet
cpArbiterGetContactPointSet.argtypes = [POINTER(cpArbiter)]
cpArbiterGetNormal = _libraries['../pymunk/libchipmunk.so'].cpArbiterGetNormal
cpArbiterGetNormal.restype = cpVect
cpArbiterGetNormal.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterGetPoint = _libraries['../pymunk/libchipmunk.so'].cpArbiterGetPoint
cpArbiterGetPoint.restype = cpVect
cpArbiterGetPoint.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterGetDepth = _libraries['../pymunk/libchipmunk.so'].cpArbiterGetDepth
cpArbiterGetDepth.restype = cpFloat
cpArbiterGetDepth.argtypes = [POINTER(cpArbiter), c_int]
cpBB._pack_ = 4
cpBB._fields_ = [
    ('l', cpFloat),
    ('b', cpFloat),
    ('r', cpFloat),
    ('t', cpFloat),
]
cpBBClampVect = _libraries['../pymunk/libchipmunk.so'].cpBBClampVect
cpBBClampVect.restype = cpVect
cpBBClampVect.argtypes = [cpBB, cpVect]
cpBBWrapVect = _libraries['../pymunk/libchipmunk.so'].cpBBWrapVect
cpBBWrapVect.restype = cpVect
cpBBWrapVect.argtypes = [cpBB, cpVect]
cpBodyVelocityFunc = CFUNCTYPE(None, POINTER(cpBody), cpVect, cpFloat, cpFloat)
cpBodyPositionFunc = CFUNCTYPE(None, POINTER(cpBody), cpFloat)
class cpComponentNode(Structure):
    pass
cpComponentNode._pack_ = 4
cpComponentNode._fields_ = [
    ('root', POINTER(cpBody)),
    ('next', POINTER(cpBody)),
    ('idleTime', cpFloat),
]
cpBody._pack_ = 4
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
cpBodyAlloc = _libraries['../pymunk/libchipmunk.so'].cpBodyAlloc
cpBodyAlloc.restype = POINTER(cpBody)
cpBodyAlloc.argtypes = []
cpBodyInit = _libraries['../pymunk/libchipmunk.so'].cpBodyInit
cpBodyInit.restype = POINTER(cpBody)
cpBodyInit.argtypes = [POINTER(cpBody), cpFloat, cpFloat]
cpBodyNew = _libraries['../pymunk/libchipmunk.so'].cpBodyNew
cpBodyNew.restype = POINTER(cpBody)
cpBodyNew.argtypes = [cpFloat, cpFloat]
cpBodyInitStatic = _libraries['../pymunk/libchipmunk.so'].cpBodyInitStatic
cpBodyInitStatic.restype = POINTER(cpBody)
cpBodyInitStatic.argtypes = [POINTER(cpBody)]
cpBodyNewStatic = _libraries['../pymunk/libchipmunk.so'].cpBodyNewStatic
cpBodyNewStatic.restype = POINTER(cpBody)
cpBodyNewStatic.argtypes = []
cpBodyDestroy = _libraries['../pymunk/libchipmunk.so'].cpBodyDestroy
cpBodyDestroy.restype = None
cpBodyDestroy.argtypes = [POINTER(cpBody)]
cpBodyFree = _libraries['../pymunk/libchipmunk.so'].cpBodyFree
cpBodyFree.restype = None
cpBodyFree.argtypes = [POINTER(cpBody)]
cpBodyActivate = _libraries['../pymunk/libchipmunk.so'].cpBodyActivate
cpBodyActivate.restype = None
cpBodyActivate.argtypes = [POINTER(cpBody)]
cpBodySleep = _libraries['../pymunk/libchipmunk.so'].cpBodySleep
cpBodySleep.restype = None
cpBodySleep.argtypes = [POINTER(cpBody)]
cpBodySleepWithGroup = _libraries['../pymunk/libchipmunk.so'].cpBodySleepWithGroup
cpBodySleepWithGroup.restype = None
cpBodySleepWithGroup.argtypes = [POINTER(cpBody), POINTER(cpBody)]
cpBodySetMass = _libraries['../pymunk/libchipmunk.so'].cpBodySetMass
cpBodySetMass.restype = None
cpBodySetMass.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetMoment = _libraries['../pymunk/libchipmunk.so'].cpBodySetMoment
cpBodySetMoment.restype = None
cpBodySetMoment.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetAngle = _libraries['../pymunk/libchipmunk.so'].cpBodySetAngle
cpBodySetAngle.restype = None
cpBodySetAngle.argtypes = [POINTER(cpBody), cpFloat]
cpBodyUpdateVelocity = _libraries['../pymunk/libchipmunk.so'].cpBodyUpdateVelocity
cpBodyUpdateVelocity.restype = None
cpBodyUpdateVelocity.argtypes = [POINTER(cpBody), cpVect, cpFloat, cpFloat]
cpBodyUpdatePosition = _libraries['../pymunk/libchipmunk.so'].cpBodyUpdatePosition
cpBodyUpdatePosition.restype = None
cpBodyUpdatePosition.argtypes = [POINTER(cpBody), cpFloat]
cpBodyResetForces = _libraries['../pymunk/libchipmunk.so'].cpBodyResetForces
cpBodyResetForces.restype = None
cpBodyResetForces.argtypes = [POINTER(cpBody)]
cpBodyApplyForce = _libraries['../pymunk/libchipmunk.so'].cpBodyApplyForce
cpBodyApplyForce.restype = None
cpBodyApplyForce.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpBodyShapeIteratorFunc = CFUNCTYPE(None, POINTER(cpBody), POINTER(cpShape), c_void_p)
cpBodyEachShape = _libraries['../pymunk/libchipmunk.so'].cpBodyEachShape
cpBodyEachShape.restype = None
cpBodyEachShape.argtypes = [POINTER(cpBody), cpBodyShapeIteratorFunc, c_void_p]
cpBodyConstraintIteratorFunc = CFUNCTYPE(None, POINTER(cpBody), POINTER(cpConstraint), c_void_p)
cpBodyEachConstraint = _libraries['../pymunk/libchipmunk.so'].cpBodyEachConstraint
cpBodyEachConstraint.restype = None
cpBodyEachConstraint.argtypes = [POINTER(cpBody), cpBodyConstraintIteratorFunc, c_void_p]
cpBodyArbiterIteratorFunc = CFUNCTYPE(None, POINTER(cpBody), POINTER(cpArbiter), c_void_p)
cpBodyEachArbiter = _libraries['../pymunk/libchipmunk.so'].cpBodyEachArbiter
cpBodyEachArbiter.restype = None
cpBodyEachArbiter.argtypes = [POINTER(cpBody), cpBodyArbiterIteratorFunc, c_void_p]
class cpPolyShapeAxis(Structure):
    pass
cpPolyShapeAxis._pack_ = 4
cpPolyShapeAxis._fields_ = [
    ('n', cpVect),
    ('d', cpFloat),
]
class cpPolyShape(Structure):
    pass
class cpShapeClass(Structure):
    pass
cpShape._pack_ = 4
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
    ('next_private', POINTER(cpShape)),
    ('hashid_private', cpHashValue),
]
cpPolyShape._fields_ = [
    ('shape', cpShape),
    ('numVerts', c_int),
    ('verts', POINTER(cpVect)),
    ('tVerts', POINTER(cpVect)),
    ('axes', POINTER(cpPolyShapeAxis)),
    ('tAxes', POINTER(cpPolyShapeAxis)),
]
cpPolyShapeAlloc = _libraries['../pymunk/libchipmunk.so'].cpPolyShapeAlloc
cpPolyShapeAlloc.restype = POINTER(cpPolyShape)
cpPolyShapeAlloc.argtypes = []
cpPolyShapeInit = _libraries['../pymunk/libchipmunk.so'].cpPolyShapeInit
cpPolyShapeInit.restype = POINTER(cpPolyShape)
cpPolyShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpPolyShapeNew = _libraries['../pymunk/libchipmunk.so'].cpPolyShapeNew
cpPolyShapeNew.restype = POINTER(cpShape)
cpPolyShapeNew.argtypes = [POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpBoxShapeInit = _libraries['../pymunk/libchipmunk.so'].cpBoxShapeInit
cpBoxShapeInit.restype = POINTER(cpPolyShape)
cpBoxShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpFloat, cpFloat]
cpBoxShapeNew = _libraries['../pymunk/libchipmunk.so'].cpBoxShapeNew
cpBoxShapeNew.restype = POINTER(cpShape)
cpBoxShapeNew.argtypes = [POINTER(cpBody), cpFloat, cpFloat]
cpPolyValidate = _libraries['../pymunk/libchipmunk.so'].cpPolyValidate
cpPolyValidate.restype = cpBool
cpPolyValidate.argtypes = [POINTER(cpVect), c_int]
cpPolyShapeGetNumVerts = _libraries['../pymunk/libchipmunk.so'].cpPolyShapeGetNumVerts
cpPolyShapeGetNumVerts.restype = c_int
cpPolyShapeGetNumVerts.argtypes = [POINTER(cpShape)]
cpPolyShapeGetVert = _libraries['../pymunk/libchipmunk.so'].cpPolyShapeGetVert
cpPolyShapeGetVert.restype = cpVect
cpPolyShapeGetVert.argtypes = [POINTER(cpShape), c_int]
cpSegmentQueryInfo._pack_ = 4
cpSegmentQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('t', cpFloat),
    ('n', cpVect),
]

# values for enumeration 'cpShapeType'
cpShapeType = c_int # enum
cpShapeCacheDataImpl = CFUNCTYPE(cpBB, POINTER(cpShape), cpVect, cpVect)
cpShapeDestroyImpl = CFUNCTYPE(None, POINTER(cpShape))
cpShapePointQueryImpl = CFUNCTYPE(cpBool, POINTER(cpShape), cpVect)
cpShapeSegmentQueryImpl = CFUNCTYPE(None, POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo))
cpShapeClass._fields_ = [
    ('type', cpShapeType),
    ('cacheData', cpShapeCacheDataImpl),
    ('destroy', cpShapeDestroyImpl),
    ('pointQuery', cpShapePointQueryImpl),
    ('segmentQuery', cpShapeSegmentQueryImpl),
]
cpShapeDestroy = _libraries['../pymunk/libchipmunk.so'].cpShapeDestroy
cpShapeDestroy.restype = None
cpShapeDestroy.argtypes = [POINTER(cpShape)]
cpShapeFree = _libraries['../pymunk/libchipmunk.so'].cpShapeFree
cpShapeFree.restype = None
cpShapeFree.argtypes = [POINTER(cpShape)]
cpShapeCacheBB = _libraries['../pymunk/libchipmunk.so'].cpShapeCacheBB
cpShapeCacheBB.restype = cpBB
cpShapeCacheBB.argtypes = [POINTER(cpShape)]
cpShapeUpdate = _libraries['../pymunk/libchipmunk.so'].cpShapeUpdate
cpShapeUpdate.restype = cpBB
cpShapeUpdate.argtypes = [POINTER(cpShape), cpVect, cpVect]
cpShapePointQuery = _libraries['../pymunk/libchipmunk.so'].cpShapePointQuery
cpShapePointQuery.restype = cpBool
cpShapePointQuery.argtypes = [POINTER(cpShape), cpVect]
cpResetShapeIdCounter = _libraries['../pymunk/libchipmunk.so'].cpResetShapeIdCounter
cpResetShapeIdCounter.restype = None
cpResetShapeIdCounter.argtypes = []
cpShapeSegmentQuery = _libraries['../pymunk/libchipmunk.so'].cpShapeSegmentQuery
cpShapeSegmentQuery.restype = cpBool
cpShapeSegmentQuery.argtypes = [POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo)]
class cpCircleShape(Structure):
    pass
cpCircleShape._pack_ = 4
cpCircleShape._fields_ = [
    ('shape', cpShape),
    ('c', cpVect),
    ('tc', cpVect),
    ('r', cpFloat),
]
cpCircleShapeAlloc = _libraries['../pymunk/libchipmunk.so'].cpCircleShapeAlloc
cpCircleShapeAlloc.restype = POINTER(cpCircleShape)
cpCircleShapeAlloc.argtypes = []
cpCircleShapeInit = _libraries['../pymunk/libchipmunk.so'].cpCircleShapeInit
cpCircleShapeInit.restype = POINTER(cpCircleShape)
cpCircleShapeInit.argtypes = [POINTER(cpCircleShape), POINTER(cpBody), cpFloat, cpVect]
cpCircleShapeNew = _libraries['../pymunk/libchipmunk.so'].cpCircleShapeNew
cpCircleShapeNew.restype = POINTER(cpShape)
cpCircleShapeNew.argtypes = [POINTER(cpBody), cpFloat, cpVect]
cpCircleShapeGetOffset = _libraries['../pymunk/libchipmunk.so'].cpCircleShapeGetOffset
cpCircleShapeGetOffset.restype = cpVect
cpCircleShapeGetOffset.argtypes = [POINTER(cpShape)]
cpCircleShapeGetRadius = _libraries['../pymunk/libchipmunk.so'].cpCircleShapeGetRadius
cpCircleShapeGetRadius.restype = cpFloat
cpCircleShapeGetRadius.argtypes = [POINTER(cpShape)]
class cpSegmentShape(Structure):
    pass
cpSegmentShape._pack_ = 4
cpSegmentShape._fields_ = [
    ('shape', cpShape),
    ('a', cpVect),
    ('b', cpVect),
    ('n', cpVect),
    ('ta', cpVect),
    ('tb', cpVect),
    ('tn', cpVect),
    ('r', cpFloat),
]
cpSegmentShapeAlloc = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeAlloc
cpSegmentShapeAlloc.restype = POINTER(cpSegmentShape)
cpSegmentShapeAlloc.argtypes = []
cpSegmentShapeInit = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeInit
cpSegmentShapeInit.restype = POINTER(cpSegmentShape)
cpSegmentShapeInit.argtypes = [POINTER(cpSegmentShape), POINTER(cpBody), cpVect, cpVect, cpFloat]
cpSegmentShapeNew = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeNew
cpSegmentShapeNew.restype = POINTER(cpShape)
cpSegmentShapeNew.argtypes = [POINTER(cpBody), cpVect, cpVect, cpFloat]
cpSegmentShapeGetA = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeGetA
cpSegmentShapeGetA.restype = cpVect
cpSegmentShapeGetA.argtypes = [POINTER(cpShape)]
cpSegmentShapeGetB = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeGetB
cpSegmentShapeGetB.restype = cpVect
cpSegmentShapeGetB.argtypes = [POINTER(cpShape)]
cpSegmentShapeGetNormal = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeGetNormal
cpSegmentShapeGetNormal.restype = cpVect
cpSegmentShapeGetNormal.argtypes = [POINTER(cpShape)]
cpSegmentShapeGetRadius = _libraries['../pymunk/libchipmunk.so'].cpSegmentShapeGetRadius
cpSegmentShapeGetRadius.restype = cpFloat
cpSegmentShapeGetRadius.argtypes = [POINTER(cpShape)]
class cpContactBufferHeader(Structure):
    pass
cpContactBufferHeader._fields_ = [
]
class cpSpatialIndex(Structure):
    pass
cpSpace._pack_ = 4
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
    ('prev_dt_private', cpFloat),
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
    ('postStepCallbacks_private', POINTER(cpHashSet)),
    ('_staticBody_private', cpBody),
]
cpSpaceAlloc = _libraries['../pymunk/libchipmunk.so'].cpSpaceAlloc
cpSpaceAlloc.restype = POINTER(cpSpace)
cpSpaceAlloc.argtypes = []
cpSpaceInit = _libraries['../pymunk/libchipmunk.so'].cpSpaceInit
cpSpaceInit.restype = POINTER(cpSpace)
cpSpaceInit.argtypes = [POINTER(cpSpace)]
cpSpaceNew = _libraries['../pymunk/libchipmunk.so'].cpSpaceNew
cpSpaceNew.restype = POINTER(cpSpace)
cpSpaceNew.argtypes = []
cpSpaceDestroy = _libraries['../pymunk/libchipmunk.so'].cpSpaceDestroy
cpSpaceDestroy.restype = None
cpSpaceDestroy.argtypes = [POINTER(cpSpace)]
cpSpaceFree = _libraries['../pymunk/libchipmunk.so'].cpSpaceFree
cpSpaceFree.restype = None
cpSpaceFree.argtypes = [POINTER(cpSpace)]
cpSpaceSetDefaultCollisionHandler = _libraries['../pymunk/libchipmunk.so'].cpSpaceSetDefaultCollisionHandler
cpSpaceSetDefaultCollisionHandler.restype = None
cpSpaceSetDefaultCollisionHandler.argtypes = [POINTER(cpSpace), cpCollisionBeginFunc, cpCollisionPreSolveFunc, cpCollisionPostSolveFunc, cpCollisionSeparateFunc, c_void_p]
cpSpaceAddCollisionHandler = _libraries['../pymunk/libchipmunk.so'].cpSpaceAddCollisionHandler
cpSpaceAddCollisionHandler.restype = None
cpSpaceAddCollisionHandler.argtypes = [POINTER(cpSpace), cpCollisionType, cpCollisionType, cpCollisionBeginFunc, cpCollisionPreSolveFunc, cpCollisionPostSolveFunc, cpCollisionSeparateFunc, c_void_p]
cpSpaceRemoveCollisionHandler = _libraries['../pymunk/libchipmunk.so'].cpSpaceRemoveCollisionHandler
cpSpaceRemoveCollisionHandler.restype = None
cpSpaceRemoveCollisionHandler.argtypes = [POINTER(cpSpace), cpCollisionType, cpCollisionType]
cpSpaceAddShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceAddShape
cpSpaceAddShape.restype = POINTER(cpShape)
cpSpaceAddShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddStaticShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceAddStaticShape
cpSpaceAddStaticShape.restype = POINTER(cpShape)
cpSpaceAddStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddBody = _libraries['../pymunk/libchipmunk.so'].cpSpaceAddBody
cpSpaceAddBody.restype = POINTER(cpBody)
cpSpaceAddBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceAddConstraint = _libraries['../pymunk/libchipmunk.so'].cpSpaceAddConstraint
cpSpaceAddConstraint.restype = POINTER(cpConstraint)
cpSpaceAddConstraint.argtypes = [POINTER(cpSpace), POINTER(cpConstraint)]
cpSpaceRemoveShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceRemoveShape
cpSpaceRemoveShape.restype = None
cpSpaceRemoveShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveStaticShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceRemoveStaticShape
cpSpaceRemoveStaticShape.restype = None
cpSpaceRemoveStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveBody = _libraries['../pymunk/libchipmunk.so'].cpSpaceRemoveBody
cpSpaceRemoveBody.restype = None
cpSpaceRemoveBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceRemoveConstraint = _libraries['../pymunk/libchipmunk.so'].cpSpaceRemoveConstraint
cpSpaceRemoveConstraint.restype = None
cpSpaceRemoveConstraint.argtypes = [POINTER(cpSpace), POINTER(cpConstraint)]
cpSpaceContainsShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceContainsShape
cpSpaceContainsShape.restype = cpBool
cpSpaceContainsShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceContainsBody = _libraries['../pymunk/libchipmunk.so'].cpSpaceContainsBody
cpSpaceContainsBody.restype = cpBool
cpSpaceContainsBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceContainsConstraint = _libraries['../pymunk/libchipmunk.so'].cpSpaceContainsConstraint
cpSpaceContainsConstraint.restype = cpBool
cpSpaceContainsConstraint.argtypes = [POINTER(cpSpace), POINTER(cpConstraint)]
cpPostStepFunc = CFUNCTYPE(None, POINTER(cpSpace), c_void_p, c_void_p)
cpSpaceAddPostStepCallback = _libraries['../pymunk/libchipmunk.so'].cpSpaceAddPostStepCallback
cpSpaceAddPostStepCallback.restype = None
cpSpaceAddPostStepCallback.argtypes = [POINTER(cpSpace), cpPostStepFunc, c_void_p, c_void_p]
cpSpacePointQueryFunc = CFUNCTYPE(None, POINTER(cpShape), c_void_p)
cpSpacePointQuery = _libraries['../pymunk/libchipmunk.so'].cpSpacePointQuery
cpSpacePointQuery.restype = None
cpSpacePointQuery.argtypes = [POINTER(cpSpace), cpVect, cpLayers, cpGroup, cpSpacePointQueryFunc, c_void_p]
cpSpacePointQueryFirst = _libraries['../pymunk/libchipmunk.so'].cpSpacePointQueryFirst
cpSpacePointQueryFirst.restype = POINTER(cpShape)
cpSpacePointQueryFirst.argtypes = [POINTER(cpSpace), cpVect, cpLayers, cpGroup]
cpSpaceSegmentQueryFunc = CFUNCTYPE(None, POINTER(cpShape), cpFloat, cpVect, c_void_p)
cpSpaceSegmentQuery = _libraries['../pymunk/libchipmunk.so'].cpSpaceSegmentQuery
cpSpaceSegmentQuery.restype = None
cpSpaceSegmentQuery.argtypes = [POINTER(cpSpace), cpVect, cpVect, cpLayers, cpGroup, cpSpaceSegmentQueryFunc, c_void_p]
cpSpaceSegmentQueryFirst = _libraries['../pymunk/libchipmunk.so'].cpSpaceSegmentQueryFirst
cpSpaceSegmentQueryFirst.restype = POINTER(cpShape)
cpSpaceSegmentQueryFirst.argtypes = [POINTER(cpSpace), cpVect, cpVect, cpLayers, cpGroup, POINTER(cpSegmentQueryInfo)]
cpSpaceBBQueryFunc = CFUNCTYPE(None, POINTER(cpShape), c_void_p)
cpSpaceBBQuery = _libraries['../pymunk/libchipmunk.so'].cpSpaceBBQuery
cpSpaceBBQuery.restype = None
cpSpaceBBQuery.argtypes = [POINTER(cpSpace), cpBB, cpLayers, cpGroup, cpSpaceBBQueryFunc, c_void_p]
cpSpaceShapeQueryFunc = CFUNCTYPE(None, POINTER(cpShape), POINTER(cpContactPointSet), c_void_p)
cpSpaceShapeQuery = _libraries['../pymunk/libchipmunk.so'].cpSpaceShapeQuery
cpSpaceShapeQuery.restype = cpBool
cpSpaceShapeQuery.argtypes = [POINTER(cpSpace), POINTER(cpShape), cpSpaceShapeQueryFunc, c_void_p]
cpSpaceActivateShapesTouchingShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceActivateShapesTouchingShape
cpSpaceActivateShapesTouchingShape.restype = None
cpSpaceActivateShapesTouchingShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceBodyIteratorFunc = CFUNCTYPE(None, POINTER(cpBody), c_void_p)
cpSpaceEachBody = _libraries['../pymunk/libchipmunk.so'].cpSpaceEachBody
cpSpaceEachBody.restype = None
cpSpaceEachBody.argtypes = [POINTER(cpSpace), cpSpaceBodyIteratorFunc, c_void_p]
cpSpaceShapeIteratorFunc = CFUNCTYPE(None, POINTER(cpShape), c_void_p)
cpSpaceEachShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceEachShape
cpSpaceEachShape.restype = None
cpSpaceEachShape.argtypes = [POINTER(cpSpace), cpSpaceShapeIteratorFunc, c_void_p]
cpSpaceReindexStatic = _libraries['../pymunk/libchipmunk.so'].cpSpaceReindexStatic
cpSpaceReindexStatic.restype = None
cpSpaceReindexStatic.argtypes = [POINTER(cpSpace)]
cpSpaceReindexShape = _libraries['../pymunk/libchipmunk.so'].cpSpaceReindexShape
cpSpaceReindexShape.restype = None
cpSpaceReindexShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceUseSpatialHash = _libraries['../pymunk/libchipmunk.so'].cpSpaceUseSpatialHash
cpSpaceUseSpatialHash.restype = None
cpSpaceUseSpatialHash.argtypes = [POINTER(cpSpace), cpFloat, c_int]
cpSpaceStep = _libraries['../pymunk/libchipmunk.so'].cpSpaceStep
cpSpaceStep.restype = None
cpSpaceStep.argtypes = [POINTER(cpSpace), cpFloat]
cpSpatialIndexBBFunc = CFUNCTYPE(cpBB, c_void_p)
cpSpatialIndexIteratorFunc = CFUNCTYPE(None, c_void_p, c_void_p)
cpSpatialIndexQueryFunc = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
cpSpatialIndexSegmentQueryFunc = CFUNCTYPE(cpFloat, c_void_p, c_void_p, c_void_p)
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
cpSpaceHashAlloc = _libraries['../pymunk/libchipmunk.so'].cpSpaceHashAlloc
cpSpaceHashAlloc.restype = POINTER(cpSpaceHash)
cpSpaceHashAlloc.argtypes = []
cpSpaceHashInit = _libraries['../pymunk/libchipmunk.so'].cpSpaceHashInit
cpSpaceHashInit.restype = POINTER(cpSpatialIndex)
cpSpaceHashInit.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int, cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSpaceHashNew = _libraries['../pymunk/libchipmunk.so'].cpSpaceHashNew
cpSpaceHashNew.restype = POINTER(cpSpatialIndex)
cpSpaceHashNew.argtypes = [cpFloat, c_int, cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSpaceHashResize = _libraries['../pymunk/libchipmunk.so'].cpSpaceHashResize
cpSpaceHashResize.restype = None
cpSpaceHashResize.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int]
class cpBBTree(Structure):
    pass
cpBBTree._fields_ = [
]
cpBBTreeAlloc = _libraries['../pymunk/libchipmunk.so'].cpBBTreeAlloc
cpBBTreeAlloc.restype = POINTER(cpBBTree)
cpBBTreeAlloc.argtypes = []
cpBBTreeInit = _libraries['../pymunk/libchipmunk.so'].cpBBTreeInit
cpBBTreeInit.restype = POINTER(cpSpatialIndex)
cpBBTreeInit.argtypes = [POINTER(cpBBTree), cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpBBTreeNew = _libraries['../pymunk/libchipmunk.so'].cpBBTreeNew
cpBBTreeNew.restype = POINTER(cpSpatialIndex)
cpBBTreeNew.argtypes = [cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpBBTreeOptimize = _libraries['../pymunk/libchipmunk.so'].cpBBTreeOptimize
cpBBTreeOptimize.restype = None
cpBBTreeOptimize.argtypes = [POINTER(cpSpatialIndex)]
cpBBTreeVelocityFunc = CFUNCTYPE(cpVect, c_void_p)
cpBBTreeSetVelocityFunc = _libraries['../pymunk/libchipmunk.so'].cpBBTreeSetVelocityFunc
cpBBTreeSetVelocityFunc.restype = None
cpBBTreeSetVelocityFunc.argtypes = [POINTER(cpSpatialIndex), cpBBTreeVelocityFunc]
class cpSweep1D(Structure):
    pass
cpSweep1D._fields_ = [
]
cpSweep1DAlloc = _libraries['../pymunk/libchipmunk.so'].cpSweep1DAlloc
cpSweep1DAlloc.restype = POINTER(cpSweep1D)
cpSweep1DAlloc.argtypes = []
cpSweep1DInit = _libraries['../pymunk/libchipmunk.so'].cpSweep1DInit
cpSweep1DInit.restype = POINTER(cpSpatialIndex)
cpSweep1DInit.argtypes = [POINTER(cpSweep1D), cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSweep1DNew = _libraries['../pymunk/libchipmunk.so'].cpSweep1DNew
cpSweep1DNew.restype = POINTER(cpSpatialIndex)
cpSweep1DNew.argtypes = [cpSpatialIndexBBFunc, POINTER(cpSpatialIndex)]
cpSpatialIndexDestroyImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex))
cpSpatialIndexCountImpl = CFUNCTYPE(c_int, POINTER(cpSpatialIndex))
cpSpatialIndexEachImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), cpSpatialIndexIteratorFunc, c_void_p)
cpSpatialIndexContainsImpl = CFUNCTYPE(cpBool, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexInsertImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexRemoveImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexReindexImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex))
cpSpatialIndexReindexObjectImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), c_void_p, cpHashValue)
cpSpatialIndexReindexQueryImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), cpSpatialIndexQueryFunc, c_void_p)
cpSpatialIndexPointQueryImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), cpVect, cpSpatialIndexQueryFunc, c_void_p)
cpSpatialIndexSegmentQueryImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), c_void_p, cpVect, cpVect, cpFloat, cpSpatialIndexSegmentQueryFunc, c_void_p)
cpSpatialIndexQueryImpl = CFUNCTYPE(None, POINTER(cpSpatialIndex), c_void_p, cpBB, cpSpatialIndexQueryFunc, c_void_p)
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
    ('pointQuery', cpSpatialIndexPointQueryImpl),
    ('segmentQuery', cpSpatialIndexSegmentQueryImpl),
    ('query', cpSpatialIndexQueryImpl),
]
cpSpatialIndexFree = _libraries['../pymunk/libchipmunk.so'].cpSpatialIndexFree
cpSpatialIndexFree.restype = None
cpSpatialIndexFree.argtypes = [POINTER(cpSpatialIndex)]
cpSpatialIndexCollideStatic = _libraries['../pymunk/libchipmunk.so'].cpSpatialIndexCollideStatic
cpSpatialIndexCollideStatic.restype = None
cpSpatialIndexCollideStatic.argtypes = [POINTER(cpSpatialIndex), POINTER(cpSpatialIndex), cpSpatialIndexQueryFunc, c_void_p]
cpvlength = _libraries['../pymunk/libchipmunk.so'].cpvlength
cpvlength.restype = cpFloat
cpvlength.argtypes = [cpVect]
cpvslerp = _libraries['../pymunk/libchipmunk.so'].cpvslerp
cpvslerp.restype = cpVect
cpvslerp.argtypes = [cpVect, cpVect, cpFloat]
cpvslerpconst = _libraries['../pymunk/libchipmunk.so'].cpvslerpconst
cpvslerpconst.restype = cpVect
cpvslerpconst.argtypes = [cpVect, cpVect, cpFloat]
cpvforangle = _libraries['../pymunk/libchipmunk.so'].cpvforangle
cpvforangle.restype = cpVect
cpvforangle.argtypes = [cpFloat]
cpvtoangle = _libraries['../pymunk/libchipmunk.so'].cpvtoangle
cpvtoangle.restype = cpFloat
cpvtoangle.argtypes = [cpVect]
cpvstr = _libraries['../pymunk/libchipmunk.so'].cpvstr
cpvstr.restype = STRING
cpvstr.argtypes = [cpVect]
CP_ALL_LAYERS = 4294967295L # Variable c_uint '-1u'
CP_BUFFER_BYTES = 32768 # Variable c_int '32768'
cpTrue = 1 # Variable c_int '1'
M_E = 2.7182818284590451 # Variable c_double '2.71828182845904509079559829842764884233474731445e+0'
CP_ALLOW_PRIVATE_ACCESS = 0 # Variable c_int '0'
CP_MAX_CONTACTS_PER_ARBITER = 4 # Variable c_int '4'
CP_NO_GROUP = 0L # Variable c_uint '0u'
CP_USE_DOUBLES = 1 # Variable c_int '1'
cpFalse = 0 # Variable c_int '0'
M_PI = 3.1415926535897931 # Variable c_double '3.14159265358979311599796346854418516159057617188e+0'
__all__ = ['cpBodyResetForces', 'cpShapeUpdate', '_cpBodyIsRogue',
           'cpSegmentShapeNew', 'cpSpaceActivateShapesTouchingShape',
           'cpBodyApplyForce', 'cpBodyEachShape',
           'cpRatchetJointAlloc', 'cpvslerp',
           'N17cpContactPointSet3DOT_0E', 'cpShapeCacheBB',
           'cpSpatialIndexEachImpl', 'cpRatchetJointInit',
           'cpCircleShapeNew', 'cpBBTreeOptimize', 'cpDampedSpring',
           'cpBodySetAngle', 'cpSpatialIndexCountImpl',
           'cpSpaceShapeIteratorFunc', 'cpSpatialIndexDestroyImpl',
           'cpDampedRotarySpringAlloc', 'cpRotaryLimitJoint',
           'cpSpatialIndexSegmentQueryImpl',
           'cpSpatialIndexInsertImpl', 'cpMessage',
           'cpContactPointSet', '_cpvnear', 'cpBBTreeVelocityFunc',
           'cpDampedSpringNew', 'cpSpaceBBQueryFunc',
           'cpSweep1DAlloc', 'cpPolyShapeGetVert',
           'cpGrooveJointAlloc', '_cpvunrotate', 'cpArray',
           'cpSpacePointQueryFunc', 'cpBodyEachConstraint',
           '_cpConstraintGetImpulse', 'cpConstraintGetImpulseImpl',
           'cpDampedSpringInit', '_cpSegmentQueryHitDist',
           'cpSpaceContainsBody', 'cpSegmentQueryInfo',
           'cpMomentForBox', 'cpSpace', 'cpDampedRotarySpringNew',
           'cpSpaceSegmentQueryFirst', 'cpCircleShapeGetOffset',
           'cpBodyConstraintIteratorFunc', 'cpGearJointInit',
           'cpGrooveJointInit', 'cpArbiterGetPoint', 'cpBodyActivate',
           'cpSpacePointQuery', 'cpBody', '_cpveql', 'cpBodySetMass',
           'cpvstr', 'cpMomentForPoly', 'cpCircleShapeSetOffset',
           'cpBodyDestroy', 'cpDataPointer', 'cpArbiterStateNormal',
           '_cpBBIntersects', 'CP_USE_DOUBLES', 'CP_SEGMENT_SHAPE',
           'cpArbiterState', 'cpVect', 'cpSpaceContainsShape',
           'cpDampedRotarySpringGetClass', 'cpDampedSpringForceFunc',
           'cpSpatialIndexIteratorFunc', 'cpSpaceHashInit',
           'cpSpaceRemoveStaticShape', 'cpPinJointAlloc',
           'cpPolyShapeInit', 'cpSpatialIndexReindexImpl',
           'cpPolyShapeNew', 'cpArbiterIgnore', 'cpCollisionHandler',
           'cpSlideJoint', 'CP_POLY_SHAPE', 'cpSpaceReindexStatic',
           'cpBodyUpdateVelocity', 'cpSpaceAlloc',
           'cpCircleShapeAlloc', '_cpArbiterGetShapes',
           'cpBodyUpdatePosition', 'cpCollisionPreSolveFunc',
           'cpShapeSegmentQueryImpl', 'cpSpaceDestroy',
           'CP_NUM_SHAPES', 'cpContact', 'cpBodyShapeIteratorFunc',
           'cpSegmentShape', 'cpShapePointQuery',
           'cpSpaceRemoveConstraint', 'cpSlideJointAlloc',
           'cpConstraintApplyImpulseImpl', 'cpSpaceNew',
           'cpSpatialIndexPointQueryImpl', 'cpSpaceUseSpatialHash',
           'cpArbiterGetNormal', 'cpConstraint', 'cpArbiter',
           'cpPivotJointNew2', 'cpGrooveJoint',
           'cpArbiterStateIgnore', 'cpSpaceAddCollisionHandler',
           'cpSpaceFree', 'cpSpatialIndexQueryFunc',
           'cpCircleShapeInit', 'M_E', 'cpSpaceInit', 'cpSweep1DNew',
           'cpBool', 'cpCollisionBeginFunc', '_cpArbiterGetPoint',
           'cpRecenterPoly', 'cpArbiterGetContactPointSet',
           'cpPivotJointNew', 'cpBBTreeAlloc',
           'cpConstraintApplyCachedImpulseImpl', 'cpSweep1DInit',
           'cpArbiterGetDepth', 'cpCircleShapeSetRadius',
           'cpBodyFree', 'cpRatchetJointGetClass', 'cpGearJointAlloc',
           'cpSpaceRemoveBody', 'cpCentroidForPoly', 'cpBoxShapeNew',
           'cpBBTreeSetVelocityFunc', 'cpBBTree',
           'cpPivotJointGetClass', 'cpSegmentShapeSetRadius',
           '_cpvnormalize_safe', 'cpPivotJointInit',
           'cpShapeSegmentQuery', 'cpSpaceReindexShape',
           'cpSpatialIndexFree', 'cpVersionString', 'cpSpaceAddBody',
           '_cpvnormalize', 'cpBoxShapeInit', 'CP_BUFFER_BYTES',
           'cpSegmentShapeAlloc', 'cpComponentNode',
           '_cpArbiterIsFirstContact', 'cpBBClampVect', '_cpvperp',
           'cpFalse', 'cpShapeType', 'cpShape',
           'cpPolyShapeGetNumVerts', 'cpSimpleMotorGetClass',
           'cpSpaceRemoveShape', '_cpvdot', 'cpContactBufferHeader',
           '_cpvrperp', 'CP_CIRCLE_SHAPE', 'cpSpaceHash',
           'cpBodySleep', 'cpSpaceSegmentQuery', 'cpSpaceHashAlloc',
           'cpPinJoint', '_cpArbiterGetNormal',
           'cpDampedRotarySpringTorqueFunc', 'cpBBWrapVect',
           'cpSegmentShapeGetA', '_cpvcross', 'cpSegmentShapeGetB',
           '_cpBodyIsSleeping', 'cpGrooveJointGetClass',
           'cpBodySleepWithGroup', 'cpCollisionSeparateFunc',
           'cpBodyArbiterIteratorFunc', '_cpvmult', 'cpvforangle',
           '_cpv', 'cpSpatialIndexQueryImpl', 'cpvtoangle', 'cpBB',
           'cpBodyInitStatic', 'cpPinJointInit', 'cpGearJoint',
           'cpSpaceHashResize', 'cpSlideJointInit',
           'cpPolyShapeAlloc', 'cpBodyVelocityFunc',
           'cpSpaceAddShape', 'cpAreaForSegment',
           'cpSpaceSetDefaultCollisionHandler', 'cpHashValue',
           'cpCollisionPostSolveFunc', 'cpConstraintDestroy',
           'cpSpatialIndexRemoveImpl', 'MAKE_REF', '_cpBBExpand',
           '_cpvrotate', '_cpvlerpconst',
           'cpSpatialIndexContainsImpl', 'cpSlideJointNew',
           'cpArbiterTotalImpulseWithFriction', 'cpDampedSpringAlloc',
           'cpArbiterStateFirstColl', 'cpRotaryLimitJointAlloc',
           'cpShapeDestroyImpl', 'cpSimpleMotorAlloc',
           'cpBodyEachArbiter', 'cpSpaceShapeQueryFunc',
           'cpSpaceBodyIteratorFunc', 'cpCollisionType',
           'CP_MAX_CONTACTS_PER_ARBITER', '_cpBBContainsVect',
           'cpSpatialIndexSegmentQueryFunc', 'cpGroup',
           'cpMomentForCircle', 'cpSegmentShapeGetRadius',
           'cpSpatialIndexReindexObjectImpl', 'cpBBTreeInit',
           'cpTimestamp', 'cpSpaceEachShape', 'cpGearJointSetRatio',
           'cpSpaceStep', 'cpRotaryLimitJointInit',
           'cpShapePointQueryImpl', 'cpSweep1D', 'cpSpatialIndex',
           '_cpvclamp', 'cpSpaceAddPostStepCallback',
           'cpRotaryLimitJointNew', 'cpAreaForCircle',
           'cpBodyNewStatic', 'cpSpaceShapeQuery', 'cpLayers',
           'cpSpatialIndexCollideStatic', 'cpConstraintFree',
           'cpSpatialIndexBBFunc', '_cpvproject', 'cpBodyInit',
           'cpGearJointGetClass', 'cpBodyNew', 'cpBodySetMoment',
           'cpHashSet', 'cpBodyPositionFunc',
           'cpGrooveJointSetGrooveA', 'cpGrooveJointSetGrooveB',
           '_cpBodyLocal2World', 'cpConstraintClass', 'cpFloat',
           '_cpvlerp', 'cpPinJointNew', '_cpvlengthsq',
           'cpPostStepFunc', 'cpSpatialIndexReindexQueryImpl',
           '_cpSegmentQueryHitPoint', 'cpPolyShape', 'M_PI',
           'cpShapeCacheDataImpl', 'cpInitChipmunk', '_cpBBMerge',
           'cpCircleShapeGetRadius', 'cpSpaceAddConstraint',
           '_cpBodyKineticEnergy', 'cpSpaceHashNew',
           '_cpBBContainsBB', '_cpBodyWorld2Local',
           'cpConstraintPreStepImpl', 'cpSpacePointQueryFirst',
           'CP_NO_GROUP', 'cpMomentForSegment', 'cpSimpleMotorNew',
           'cpRotaryLimitJointGetClass',
           'cpSpaceRemoveCollisionHandler', 'cpBBTreeNew',
           'cpSpaceEachBody', 'cpPivotJointAlloc',
           'cpRatchetJointNew', 'cpGearJointNew',
           'cpArbiterTotalImpulse', 'cpShapeFree',
           'cpSpatialIndexClass', 'cpvslerpconst', 'CP_ALL_LAYERS',
           'cpvlength', 'cpSpaceBBQuery', 'cpAreaForPoly',
           'cpResetShapeIdCounter', 'cpPivotJoint',
           'cpDampedRotarySpringInit', 'cpSegmentShapeInit',
           'cpSlideJointGetClass', 'CP_ALLOW_PRIVATE_ACCESS',
           'cpDampedRotarySpring', '_cpvneg', 'cpSimpleMotor',
           '_cpvsub', 'cpSegmentShapeSetEndpoints',
           '_cpBodyApplyImpulse', 'cpPolyShapeSetVerts',
           'cpRatchetJoint', 'cpSpaceAddStaticShape',
           'cpPinJointGetClass', 'cpDampedSpringGetClass',
           'CP_PRIVATE', 'cpPolyShapeAxis', 'cpArbiterStateCached',
           '_cpvdistsq', 'cpSegmentShapeGetNormal', 'cpShapeDestroy',
           'cpSimpleMotorInit', '_cpvadd', '_cpvdist', 'cpShapeClass',
           'cpBodyAlloc', 'cpGrooveJointNew', 'cpCircleShape',
           'cpTrue', 'cpSpaceSegmentQueryFunc', 'cpPolyValidate',
           '_cpBBNew', 'cpSpaceContainsConstraint']
