
from ctypes import * 
from .vec2d import Vec2d
cpVect = Vec2d
STRING = c_char_p

from .libload import load_library, platform_specific_functions
_lib_debug = True #Set to True to print the Chipmunk path.
chipmunk_lib = load_library("chipmunk", print_path=_lib_debug)
function_pointer = platform_specific_functions()['function_pointer']



def __attribute_format_strfmon__(a,b): return __attribute__ ((__format__ (__strfmon__, a, b))) # macro
def CP_PRIVATE(symbol): return symbol ##_private # macro
# cpfsqrt = sqrt # alias
# def CP_DefineArbiterStructProperty(type,member,name): return CP_DefineArbiterStructGetter(type, member, name) CP_DefineArbiterStructSetter(type, member, name) # macro
# cprealloc = realloc # alias
def __REDIRECT_NTH_LDBL(name,proto,alias): return __REDIRECT_NTH (name, proto, alias) # macro
# def CP_DefineArbiterStructSetter(type,member,name): return static inline void cpArbiterSet ##name(cpArbiter *arb, type value){arb->member = value;} # macro
cpArbiterStateFirstColl = 0
cpArbiterStateCached = 3
# cpfpow = pow # alias
def __REDIRECT_LDBL(name,proto,alias): return __REDIRECT (name, proto, alias) # macro
# def __ASMNAME2(prefix,cname): return __STRING (prefix) cname # macro
def __va_arg_pack_len(): return __builtin_va_arg_pack_len () # macro
# def __nonnull(params): return __attribute__ ((__nonnull__ params)) # macro
# def __REDIRECT(name,proto,alias): return name proto __asm__ (__ASMNAME (#alias)) # macro
# cpfatan2 = atan2 # alias
# cpfree = free # alias
CP_POLY_SHAPE = 2
# def CP_DefineConstraintProperty(struct,type,member,name): return CP_DefineConstraintGetter(struct, type, member, name) CP_DefineConstraintSetter(struct, type, member, name) # macro
def __PMT(args): return args # macro
# def __LDBL_REDIR(name,proto): return name proto # macro
CP_CIRCLE_SHAPE = 0
# cpfcos = cos # alias
# def cpAssertHard(condition,...): return if(!(condition)) cpMessage(#condition, __FILE__, __LINE__, 1, 1, __VA_ARGS__) # macro
cpArbiterStateNormal = 1
# def CP_DefineConstraintStructGetter(type,member,name): return static inline type cpConstraint ##Get ##name(const cpConstraint *constraint){return constraint->member;} # macro
# def __errordecl(name,msg): return extern void name (void) __attribute__((__error__ (msg))) # macro
cpArbiterStateIgnore = 2
# def CP_DefineBodyStructGetter(type,member,name): return static inline type cpBodyGet ##name(const cpBody *body){return body->member;} # macro
def __P(args): return args # macro
# def cpAssertWarn(condition,...): return if(!(condition)) cpMessage(#condition, __FILE__, __LINE__, 0, 0, __VA_ARGS__) # macro
# def CP_DefineShapeStructSetter(type,member,name,activates): return static inline void cpShapeSet ##name(cpShape *shape, type value){ if(activates && shape->body) cpBodyActivate(shape->body); shape->member = value; } # macro
def __attribute_format_arg__(x): return __attribute__ ((__format_arg__ (x))) # macro
# def __warndecl(name,msg): return extern void name (void) __attribute__((__warning__ (msg))) # macro
# cpfsin = sin # alias
# def CP_DefineConstraintStructSetter(type,member,name): return static inline void cpConstraint ##Set ##name(cpConstraint *constraint, type value){ cpConstraintActivateBodies(constraint); constraint->member = value; } # macro
# cpfacos = acos # alias
# def cpAssertSoft(condition,...): return if(!(condition)) cpMessage(#condition, __FILE__, __LINE__, 1, 0, __VA_ARGS__) # macro
# __WCHAR_MAX = __WCHAR_MAX__ # alias
def __GLIBC_PREREQ(maj,min): return ((__GLIBC__ << 16) + __GLIBC_MINOR__ >= ((maj) << 16) + (min)) # macro
# cpfmod = fmod # alias
# def CP_DefineShapeStructProperty(type,member,name,activates): return CP_DefineShapeStructGetter(type, member, name) CP_DefineShapeStructSetter(type, member, name, activates) # macro
CP_NUM_SHAPES = 3
def __CONCAT(x,y): return x ## y # macro
def __STRING(x): return #x # macro
# def __LDBL_REDIR1_NTH(name,proto,alias): return name proto __THROW # macro
def __GNUC_PREREQ(maj,min): return ((__GNUC__ << 16) + __GNUC_MINOR__ >= ((maj) << 16) + (min)) # macro
def __warnattr(msg): return __attribute__((__warning__ (msg))) # macro
# def CP_DefineSpaceStructGetter(type,member,name): return static inline type cpSpaceGet ##name(const cpSpace *space){return space->member;} # macro
# def __LDBL_REDIR_NTH(name,proto): return name proto __THROW # macro
def __ASMNAME(cname): return __ASMNAME2 (__USER_LABEL_PREFIX__, cname) # macro
# cpcalloc = calloc # alias
# def CP_DefineSpaceStructProperty(type,member,name): return CP_DefineSpaceStructGetter(type, member, name) CP_DefineSpaceStructSetter(type, member, name) # macro
# def CP_DefineArbiterStructGetter(type,member,name): return static inline type cpArbiterGet ##name(const cpArbiter *arb){return arb->member;} # macro
# def CP_DefineBodyStructProperty(type,member,name): return CP_DefineBodyStructGetter(type, member, name) CP_DefineBodyStructSetter(type, member, name) # macro
# def cpConstraintCheckCast(constraint,struct): return cpAssertHard(constraint->CP_PRIVATE(klass) == struct ##GetClass(), "Constraint is not a "#struct) # macro
# def CP_DefineConstraintSetter(struct,type,member,name): return static inline void struct ##Set ##name(cpConstraint *constraint, type value){ cpConstraintCheckCast(constraint, struct); cpConstraintActivateBodies(constraint); ((struct *)constraint)->member = value; } # macro
# def CP_ARBITER_GET_SHAPES(arb,a,b): return cpShape *a, *b; cpArbiterGetShapes(arb, &a, &b); # macro
def __bos0(ptr): return __builtin_object_size (ptr, 0) # macro
CP_SEGMENT_SHAPE = 1
# def CP_DefineShapeStructGetter(type,member,name): return static inline type cpShapeGet ##name(const cpShape *shape){return shape->member;} # macro
# cpfexp = exp # alias
# def __LDBL_REDIR1(name,proto,alias): return name proto # macro
# cpffloor = floor # alias
def cpBodyAssertSane(body): return cpBodySanityCheck(body) # macro
# cpfceil = ceil # alias
# def CP_DefineConstraintStructProperty(type,member,name): return CP_DefineConstraintStructGetter(type, member, name) CP_DefineConstraintStructSetter(type, member, name) # macro
def __bos(ptr): return __builtin_object_size (ptr, __USE_FORTIFY_LEVEL > 1) # macro
# def CP_ARBITER_GET_BODIES(arb,a,b): return cpBody *a, *b; cpArbiterGetBodies(arb, &a, &b); # macro
# def __REDIRECT_NTH(name,proto,alias): return name proto __THROW __asm__ (__ASMNAME (#alias)) # macro
# def CP_DefineBodyStructSetter(type,member,name): return static inline void cpBodySet ##name(cpBody *body, const type value){ cpBodyActivate(body); cpBodyAssertSane(body); body->member = value; } # macro
# def CP_DeclareShapeGetter(struct,type,name): return type struct ##Get ##name(const cpShape *shape) # macro
# def CP_DefineSpaceStructSetter(type,member,name): return static inline void cpSpaceSet ##name(cpSpace *space, type value){space->member = value;} # macro
def __va_arg_pack(): return __builtin_va_arg_pack () # macro
# def CP_DefineConstraintGetter(struct,type,member,name): return static inline type struct ##Get ##name(const cpConstraint *constraint){ cpConstraintCheckCast(constraint, struct); return ((struct *)constraint)->member; } # macro
# def __NTH(fct): return fct throw () # macro
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
if sizeof(c_void_p) == 4: uintptr_t = c_uint 
else: uintptr_t = c_ulonglong
cpHashValue = uintptr_t
cpBool = c_int
cpDataPointer = c_void_p
cpCollisionType = uintptr_t
cpGroup = uintptr_t
cpLayers = c_uint
cpTimestamp = c_uint
#cpVect._pack_ = 4
#cpVect _fields_ def removed
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
class cpConstraintClass(Structure):
    pass
cpConstraintPreStepImpl = function_pointer(None, POINTER(cpConstraint), cpFloat)
cpConstraintApplyCachedImpulseImpl = function_pointer(None, POINTER(cpConstraint), cpFloat)
cpConstraintApplyImpulseImpl = function_pointer(None, POINTER(cpConstraint))
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
class N17cpContactPointSet3DOT_0E(Structure):
    pass
#N17cpContactPointSet3DOT_0E._pack_ = 4
N17cpContactPointSet3DOT_0E._fields_ = [
    ('point', cpVect),
    ('normal', cpVect),
    ('dist', cpFloat),
]
cpContactPointSet._fields_ = [
    ('count', c_int),
    ('points', N17cpContactPointSet3DOT_0E * 4),
]
cpArbiterGetContactPointSet = chipmunk_lib.cpArbiterGetContactPointSet
cpArbiterGetContactPointSet.restype = cpContactPointSet
cpArbiterGetContactPointSet.argtypes = [POINTER(cpArbiter)]
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
cpPolyShape._fields_ = [
    ('shape', cpShape),
    ('numVerts', c_int),
    ('verts', POINTER(cpVect)),
    ('tVerts', POINTER(cpVect)),
    ('axes', POINTER(cpPolyShapeAxis)),
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
cpBoxShapeInit2 = chipmunk_lib.cpBoxShapeInit2
cpBoxShapeInit2.restype = POINTER(cpPolyShape)
cpBoxShapeInit2.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpBB]
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
class cpSegmentQueryInfo(Structure):
    pass
#cpSegmentQueryInfo._pack_ = 4
cpSegmentQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('t', cpFloat),
    ('n', cpVect),
]

# values for enumeration 'cpShapeType'
cpShapeType = c_int # enum
cpShapeCacheDataImpl = function_pointer(cpBB, POINTER(cpShape), cpVect, cpVect)
cpShapeDestroyImpl = function_pointer(None, POINTER(cpShape))
cpShapePointQueryImpl = function_pointer(cpBool, POINTER(cpShape), cpVect)
cpShapeSegmentQueryImpl = function_pointer(None, POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo))
cpShapeClass._fields_ = [
    ('type', cpShapeType),
    ('cacheData', cpShapeCacheDataImpl),
    ('destroy', cpShapeDestroyImpl),
    ('pointQuery', cpShapePointQueryImpl),
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
cpShapeSetBody = chipmunk_lib.cpShapeSetBody
cpShapeSetBody.restype = None
cpShapeSetBody.argtypes = [POINTER(cpShape), POINTER(cpBody)]
cpResetShapeIdCounter = chipmunk_lib.cpResetShapeIdCounter
cpResetShapeIdCounter.restype = None
cpResetShapeIdCounter.argtypes = []
cpShapeSegmentQuery = chipmunk_lib.cpShapeSegmentQuery
cpShapeSegmentQuery.restype = cpBool
cpShapeSegmentQuery.argtypes = [POINTER(cpShape), cpVect, cpVect, POINTER(cpSegmentQueryInfo)]
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
    ('postStepCallbacks_private', POINTER(cpHashSet)),
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
cpSpatialIndexQueryFunc = function_pointer(None, c_void_p, c_void_p, c_void_p)
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
cpSpatialIndexPointQueryImpl = function_pointer(None, POINTER(cpSpatialIndex), cpVect, cpSpatialIndexQueryFunc, c_void_p)
cpSpatialIndexSegmentQueryImpl = function_pointer(None, POINTER(cpSpatialIndex), c_void_p, cpVect, cpVect, cpFloat, cpSpatialIndexSegmentQueryFunc, c_void_p)
cpSpatialIndexQueryImpl = function_pointer(None, POINTER(cpSpatialIndex), c_void_p, cpBB, cpSpatialIndexQueryFunc, c_void_p)
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
cpSpatialIndexFree = chipmunk_lib.cpSpatialIndexFree
cpSpatialIndexFree.restype = None
cpSpatialIndexFree.argtypes = [POINTER(cpSpatialIndex)]
cpSpatialIndexCollideStatic = chipmunk_lib.cpSpatialIndexCollideStatic
cpSpatialIndexCollideStatic.restype = None
cpSpatialIndexCollideStatic.argtypes = [POINTER(cpSpatialIndex), POINTER(cpSpatialIndex), cpSpatialIndexQueryFunc, c_void_p]
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
_POSIX_C_SOURCE = 200809 # Variable c_long '200809l'
CP_VERSION_MINOR = 0 # Variable c_int '0'
_ATFILE_SOURCE = 1 # Variable c_int '1'
CP_BUFFER_BYTES = 32768 # Variable c_int '32768'
CP_ALL_LAYERS = 4294967295 # Variable c_uint '-1u'
__GNU_LIBRARY__ = 6 # Variable c_int '6'
__USE_SVID = 1 # Variable c_int '1'
M_E = 2.7182818284590451 # Variable c_double '2.71828182845904509079559829842764884233474731445e+0'
__USE_UNIX98 = 1 # Variable c_int '1'
CP_USE_DOUBLES = 1 # Variable c_int '1'
__USE_ANSI = 1 # Variable c_int '1'
__USE_LARGEFILE64 = 1 # Variable c_int '1'
__WCHAR_MIN = -2147483648 # Variable c_int '-0x080000000'
__USE_MISC = 1 # Variable c_int '1'
__USE_POSIX199309 = 1 # Variable c_int '1'
CP_MAX_CONTACTS_PER_ARBITER = 4 # Variable c_int '4'
_BITS_WCHAR_H = 1 # Variable c_int '1'
__GLIBC_MINOR__ = 10 # Variable c_int '10'
__USE_POSIX2 = 1 # Variable c_int '1'
_XOPEN_SOURCE_EXTENDED = 1 # Variable c_int '1'
CP_NO_GROUP = 0 # Variable c_uint '0u'
CP_ALLOW_PRIVATE_ACCESS = 0 # Variable c_int '0'
__WORDSIZE = 32 # Variable c_int '32'
__USE_ISOC99 = 1 # Variable c_int '1'
__USE_FORTIFY_LEVEL = 0 # Variable c_int '0'
__USE_XOPEN = 1 # Variable c_int '1'
_SYS_CDEFS_H = 1 # Variable c_int '1'
_LARGEFILE64_SOURCE = 1 # Variable c_int '1'
_STDINT_H = 1 # Variable c_int '1'
_XOPEN_SOURCE = 700 # Variable c_int '700'
__GLIBC_HAVE_LONG_LONG = 1 # Variable c_int '1'
_SVID_SOURCE = 1 # Variable c_int '1'
__USE_XOPEN2K = 1 # Variable c_int '1'
cpTrue = 1 # Variable c_int '1'
__STDC_IEC_559__ = 1 # Variable c_int '1'
CP_VERSION_RELEASE = 2 # Variable c_int '2'
__USE_ISOC95 = 1 # Variable c_int '1'
__USE_XOPEN2K8 = 1 # Variable c_int '1'
__STDC_ISO_10646__ = 200009 # Variable c_long '200009l'
__USE_ATFILE = 1 # Variable c_int '1'
__GLIBC__ = 2 # Variable c_int '2'
__STDC_IEC_559_COMPLEX__ = 1 # Variable c_int '1'
CP_VERSION_MAJOR = 6 # Variable c_int '6'
__USE_XOPEN_EXTENDED = 1 # Variable c_int '1'
M_PI = 3.1415926535897931 # Variable c_double '3.14159265358979311599796346854418516159057617188e+0'
__USE_GNU = 1 # Variable c_int '1'
__USE_POSIX199506 = 1 # Variable c_int '1'
__USE_BSD = 1 # Variable c_int '1'
_POSIX_SOURCE = 1 # Variable c_int '1'
__USE_LARGEFILE = 1 # Variable c_int '1'
_ISOC99_SOURCE = 1 # Variable c_int '1'
_FEATURES_H = 1 # Variable c_int '1'
_BSD_SOURCE = 1 # Variable c_int '1'
__USE_POSIX = 1 # Variable c_int '1'
cpFalse = 0 # Variable c_int '0'
_LARGEFILE_SOURCE = 1 # Variable c_int '1'
int8_t = c_int8
int16_t = c_int16
int32_t = c_int32
int64_t = c_int64
uint8_t = c_uint8
uint16_t = c_uint16
uint32_t = c_uint32
uint64_t = c_uint64
int_least8_t = c_byte
int_least16_t = c_short
int_least32_t = c_int
int_least64_t = c_longlong
uint_least8_t = c_ubyte
uint_least16_t = c_ushort
uint_least32_t = c_uint
uint_least64_t = c_ulonglong
int_fast8_t = c_byte
int_fast16_t = c_int
int_fast32_t = c_int
int_fast64_t = c_longlong
uint_fast8_t = c_ubyte
uint_fast16_t = c_uint
uint_fast32_t = c_uint
uint_fast64_t = c_ulonglong
intptr_t = c_int
intmax_t = c_longlong
uintmax_t = c_ulonglong
__all__ = ['_ATFILE_SOURCE', 'cpBodyEachShape', 'int_fast32_t',
           'cpContactPointSet', 'uint8_t', 'cpSpacePointQueryFunc',
           'cpConstraintGetImpulseImpl', 'cpBodyActivate', 'cpBody',
           'cpBodySetMass', '__GLIBC_PREREQ', 'cpBoxShapeNew2',
           '__ASMNAME', 'M_PI', 'cpVect',
           'cpDampedRotarySpringGetClass', 'cpPivotJointNew2',
           'cpSpatialIndexQueryFunc', 'cpArbiterGetDepth',
           'cpInitChipmunk', 'cpPinJointAlloc',
           'cpBodyUpdatePosition', 'cpSpaceDestroy',
           'cpAreaForCircle', 'cpBodyShapeIteratorFunc',
           '__USE_POSIX199309', 'cpSlideJointAlloc',
           'cpConstraintApplyImpulseImpl', 'cpGrooveJoint', 'M_E',
           'cpSpaceContainsShape', 'cpPivotJointNew',
           'cpRatchetJointGetClass', 'cpConstraintPreSolveFunc',
           'cpCentroidForPoly', 'cpBoxShapeNew', 'cpBBTree',
           'cpCollisionType', 'cpBodyNewStatic',
           'cpSpatialIndexInsertImpl', 'cpBBClampVect', 'cpFalse',
           '__PMT', 'uint_fast8_t', '_LARGEFILE_SOURCE',
           'cpGrooveJointGetClass', 'cpConstraintFree',
           'cpSpatialIndexCountImpl', 'cpCollisionSeparateFunc',
           'cpBodyArbiterIteratorFunc', 'CP_VERSION_MAJOR',
           'CP_ALLOW_PRIVATE_ACCESS', 'cpBodyInitStatic',
           'cpSpatialIndexQueryImpl', 'cpSpaceHashResize',
           'uint_least32_t', 'int_least64_t',
           'cpSpatialIndexCollideStatic', 'cpCollisionPostSolveFunc',
           '__USE_FORTIFY_LEVEL', 'cpSpatialIndexContainsImpl',
           'cpSpaceConstraintIteratorFunc', 'cpDampedSpringAlloc',
           'cpRotaryLimitJointAlloc', 'cpShapeCacheBB',
           'cpSpaceBodyIteratorFunc',
           'cpSpatialIndexSegmentQueryFunc', '__USE_XOPEN_EXTENDED',
           'cpMomentForCircle', 'cpSpaceRemoveConstraint',
           'cpBodyActivateStatic', 'cpvtoangle', 'cpSpatialIndex',
           'cpShapeSegmentQueryImpl', 'cpLayers', 'CP_VERSION_MINOR',
           'cpBodyInit', 'cpAreaForSegment', 'cpSegmentShape',
           'cpGrooveJointSetGrooveB', 'uint_fast32_t',
           'cpSpaceShapeQuery', 'cpRatchetJointAlloc',
           'cpConstraintPostSolveFunc', 'cpBodyApplyForce',
           'cpPolyShape', '__WORDSIZE',
           'cpSpaceRemoveCollisionHandler', 'cpBBTreeNew',
           'cpBBTreeAlloc', 'cpSimpleMotorGetClass', 'cpvslerpconst',
           '_XOPEN_SOURCE', 'cpTrue', 'cpSegmentShapeInit',
           '__USE_ISOC95', 'cpSimpleMotor', '__GLIBC__',
           'cpSpaceAddConstraint', 'cpSlideJointInit',
           'cpBodyApplyImpulse', 'cpPinJointGetClass',
           'cpSpaceContainsConstraint', 'cpSpaceBBQueryFunc',
           'cpSpaceActivateShapesTouchingShape', '__USE_XOPEN',
           'cpMomentForSegment', 'cpSpaceShapeIteratorFunc',
           'cpSpaceReindexStatic', '__USE_POSIX2', 'uint_least16_t',
           'cpArray', 'cpSpatialIndexIteratorFunc',
           'cpPolyShapeAlloc', 'cpDampedSpringInit',
           'cpBBTreeVelocityFunc', 'cpSegmentQueryInfo',
           'cpMomentForBox', 'cpDampedRotarySpringNew',
           'cpCircleShapeSetOffset', 'cpPivotJointAlloc',
           'cpBodyEachConstraint', 'CP_SEGMENT_SHAPE',
           'cpShapeUpdate', '__USE_POSIX', 'cpPolyShapeNew',
           'cpSlideJoint', 'CP_POLY_SHAPE', 'cpBodyUpdateVelocity',
           'cpShapeDestroyImpl', '_POSIX_SOURCE', 'CP_NUM_SHAPES',
           'int_fast64_t', 'uint_fast16_t', '_BITS_WCHAR_H',
           '__GLIBC_MINOR__', 'cpSpaceNew', 'cpShapeClass',
           'cpSpaceInit', 'uint_least8_t', 'cpCircleShapeSetRadius',
           'cpBodyFree', 'cpPivotJointInit', 'CP_VERSION_RELEASE',
           'cpBBTreeSetVelocityFunc', '__P',
           'cpConstraintPreStepImpl', '__USE_GNU', 'cpBodySetMoment',
           '__attribute_format_arg__', 'cpShape', '_POSIX_C_SOURCE',
           'cpContactBufferHeader', 'cpSpaceHash', 'cpPinJoint',
           'cpArbiterTotalKE', '__USE_SVID', 'cpBBWrapVect',
           '__USE_ANSI', 'cpBodySleepWithGroup', 'cpMomentForBox2',
           'cpPolyShapeGetVert', 'cpGearJoint', '__USE_ISOC99',
           'cpSpaceAddShape', 'cpConstraintDestroy',
           'cpBodyConstraintIteratorFunc', 'cpPolyShapeAxis',
           '__STDC_ISO_10646__', 'cpBodyEachArbiter',
           'cpSegmentShapeGetRadius', 'cpGearJointSetRatio',
           'CP_PRIVATE', '__USE_LARGEFILE', 'cpSweep1D',
           'cpSweep1DInit', '_FEATURES_H', 'cpArbiterStateCached',
           'cpRotaryLimitJointNew', 'uint64_t', '__REDIRECT_NTH_LDBL',
           'cpGearJointGetClass', 'cpHashSet', 'cpPinJointNew',
           'cpSpaceEachConstraint', 'cpBoxShapeInit',
           'cpArbiterThread', 'cpArbiterTotalImpulseWithFriction',
           'cpRotaryLimitJointGetClass', 'cpSpaceEachShape',
           'cpGearJointNew', 'cpSpaceRemoveStaticShape',
           'cpArbiterState', 'cpBB', 'cpSegmentShapeGetNormal',
           'cpShapeDestroy', 'cpvforangle', 'cpGrooveJointNew',
           'cpSpaceSegmentQueryFunc', 'CP_BUFFER_BYTES',
           '__USE_ATFILE', 'cpvslerp', '__GNU_LIBRARY__',
           'cpRatchetJointInit', '__USE_LARGEFILE64',
           'cpDampedRotarySpringAlloc', 'cpRotaryLimitJoint',
           'cpSpatialIndexSegmentQueryImpl', 'cpDampedSpringNew',
           'intptr_t', 'int_fast8_t', 'cpSpaceSegmentQueryFirst',
           'cpCircleShapeGetOffset', 'cpGearJointInit',
           'cpGrooveJointInit', 'cpSpaceUseSpatialHash',
           'cpPostStepFunc', '__GLIBC_HAVE_LONG_LONG', 'cpBodySetPos',
           'cpvstr', 'cpMomentForPoly', 'cpBodyDestroy',
           'cpDataPointer', 'cpArbiterStateNormal', 'cpPivotJoint',
           'cpSpatialIndexEachImpl', 'cpSpaceHashInit',
           '__attribute_format_strfmon__', 'cpSpaceReindexShape',
           'cpPolyShapeInit', 'cpSpatialIndexReindexImpl',
           'cpShapeSegmentQuery', '__bos', 'cpSpaceAlloc',
           'cpCollisionPreSolveFunc', 'int16_t', 'CP_USE_DOUBLES',
           '__warnattr', 'cpSpatialIndexPointQueryImpl',
           'cpArbiterGetNormal', 'cpCircleShape', 'uint_fast64_t',
           'cpBool', 'cpCollisionBeginFunc', 'cpShapePointQueryImpl',
           'cpArbiterGetContactPointSet', '__USE_XOPEN2K',
           'cpSpaceRemoveBody', 'cpSegmentShapeSetRadius', 'uint16_t',
           'cpSweep1DNew', 'cpBodySleep', 'int32_t', 'cpSweep1DAlloc',
           'cpDampedRotarySpringTorqueFunc', 'cpSegmentShapeGetA',
           'cpSegmentShapeGetB', '__USE_MISC',
           'CP_MAX_CONTACTS_PER_ARBITER', 'cpShapeSetBody',
           'cpHashValue', '_STDINT_H', 'cpSimpleMotorNew',
           'cpArbiterStateFirstColl', 'cpSimpleMotorAlloc',
           'cpSpaceShapeQueryFunc', 'cpSpatialIndexDestroyImpl',
           'cpGroup', 'cpSpaceHashNew',
           'cpSpatialIndexReindexObjectImpl',
           'cpRotaryLimitJointInit', 'cpSpaceAddBody',
           'cpSpatialIndexBBFunc', '__USE_POSIX199506',
           'cpSlideJointNew', 'uintmax_t',
           'cpSpaceSetDefaultCollisionHandler', 'int_fast16_t',
           'cpArbiterGetPoint', 'cpSpaceAddCollisionHandler',
           'CP_NO_GROUP', 'cpRatchetJointNew', '_SYS_CDEFS_H',
           'cpShapeCacheDataImpl', 'CP_ALL_LAYERS', 'cpSpaceBBQuery',
           'cpSlideJointGetClass', 'cpDampedRotarySpring',
           'cpSegmentShapeSetEndpoints', '__REDIRECT_LDBL',
           'cpPolyShapeSetVerts', 'cpSpaceAddStaticShape',
           'cpSpatialIndexRemoveImpl', 'cpPolyShapeGetNumVerts',
           'cpSegmentShapeAlloc', 'cpSpaceStep', 'cpSimpleMotorInit',
           'cpSpaceRemoveShape', 'uint32_t', 'cpvlength',
           'cpPolyValidate', '_XOPEN_SOURCE_EXTENDED',
           'cpSpacePointQuery', 'cpCollisionHandler',
           'N17cpContactPointSet3DOT_0E', 'cpBoxShapeInit2',
           'cpBBTreeOptimize', 'cpDampedSpring', 'cpBodySetAngle',
           '__USE_XOPEN2K8', 'cpSpaceReindexShapesForBody',
           'cpGrooveJointAlloc', 'cpBodyVelocityFunc', 'cpShapeType',
           'cpSpaceContainsBody', 'cpSpace', '__STDC_IEC_559__',
           'cpBodyAlloc', 'cpSpaceHashAlloc',
           'cpDampedSpringForceFunc', '_ISOC99_SOURCE',
           'cpSegmentShapeNew', 'cpArbiterIgnore',
           'cpCircleShapeAlloc', 'intmax_t', 'cpContact',
           'cpConstraint', 'cpArbiter', 'cpArbiterStateIgnore',
           'int_least8_t', 'cpSpaceFree', 'cpCircleShapeNew',
           'cpRecenterPoly', 'int_least16_t',
           'cpConstraintApplyCachedImpulseImpl', '_SVID_SOURCE',
           'cpGearJointAlloc', 'cpGrooveJointSetGrooveA',
           'cpSpatialIndexFree', 'cpVersionString',
           'cpSpaceAddPostStepCallback', '__USE_BSD', '__CONCAT',
           'cpShapeFree', 'CP_CIRCLE_SHAPE', 'uint_least64_t',
           '__USE_UNIX98', 'cpBodyAssertSane',
           'cpCircleShapeGetRadius', 'cpPinJointInit', 'uintptr_t',
           'cpShapePointQuery', 'cpSpaceEachBody', 'int8_t',
           '__STDC_IEC_559_COMPLEX__', 'cpBBTreeInit', 'cpTimestamp',
           'cpSegmentShapeSetNeighbors', 'cpPivotJointGetClass',
           'cpMessage', 'cpBodyNew', 'cpConstraintClass', 'cpFloat',
           '__STRING', 'int64_t', 'cpBodySanityCheck',
           'cpSpatialIndexReindexQueryImpl', '__WCHAR_MIN',
           '__GNUC_PREREQ', 'cpBodyPositionFunc', 'cpBodyResetForces',
           'cpSpacePointQueryFirst', 'cpArbiterTotalImpulse',
           '_BSD_SOURCE', 'cpSpatialIndexClass',
           '_LARGEFILE64_SOURCE', '__va_arg_pack', 'cpAreaForPoly',
           'cpResetShapeIdCounter', 'cpDampedRotarySpringInit',
           '__va_arg_pack_len', 'cpSpaceSegmentQuery', '__bos0',
           'cpComponentNode', 'cpCircleShapeInit', 'cpRatchetJoint',
           'int_least32_t', 'cpDampedSpringGetClass']
