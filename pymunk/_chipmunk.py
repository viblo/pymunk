
from ctypes import * 
from .vec2d import Vec2d
from ._chipmunk_manual import ShapeFilter, uintptr_t, cpGroup, cpBitmask, Transform, cpFloat
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


# cpfsqrt = sqrt # alias
size_t = c_uint
calloc = None # symbol removed
calloc = None # symbol removed
calloc = None # symbol removed
cpcalloc = calloc # alias
free = None # symbol removed
free = None # symbol removed
free = None # symbol removed
cpfree = free # alias
# def cpAssertSoft(__condition__,...): return if(!(__condition__)){cpMessage(#__condition__, __FILE__, __LINE__, 1, 0, __VA_ARGS__), abort();} # macro
# cpfcos = cos # alias
# cpfexp = exp # alias
# def cpAssertWarn(__condition__,...): return if(!(__condition__)) cpMessage(#__condition__, __FILE__, __LINE__, 0, 0, __VA_ARGS__) # macro
# def cpAssertHard(__condition__,...): return if(!(__condition__)){cpMessage(#__condition__, __FILE__, __LINE__, 1, 1, __VA_ARGS__); abort();} # macro
# cpfacos = acos # alias
# cpfceil = ceil # alias
# cpfatan2 = atan2 # alias
realloc = None # symbol removed
realloc = None # symbol removed
realloc = None # symbol removed
cprealloc = realloc # alias
# cpfsin = sin # alias
# cpffloor = floor # alias
# cpfpow = pow # alias
# cpfmod = fmod # alias
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
cpBody._fields_ = [
]
class cpShape(Structure):
    pass
cpShape._fields_ = [
]
class cpCircleShape(Structure):
    pass
cpCircleShape._fields_ = [
]
class cpSegmentShape(Structure):
    pass
cpSegmentShape._fields_ = [
]
class cpPolyShape(Structure):
    pass
cpPolyShape._fields_ = [
]
class cpConstraint(Structure):
    pass
cpConstraint._fields_ = [
]
class cpPinJoint(Structure):
    pass
cpPinJoint._fields_ = [
]
class cpSlideJoint(Structure):
    pass
cpSlideJoint._fields_ = [
]
class cpPivotJoint(Structure):
    pass
cpPivotJoint._fields_ = [
]
class cpGrooveJoint(Structure):
    pass
cpGrooveJoint._fields_ = [
]
class cpDampedSpring(Structure):
    pass
cpDampedSpring._fields_ = [
]
class cpDampedRotarySpring(Structure):
    pass
cpDampedRotarySpring._fields_ = [
]
class cpRotaryLimitJoint(Structure):
    pass
cpRotaryLimitJoint._fields_ = [
]
class cpRatchetJoint(Structure):
    pass
cpRatchetJoint._fields_ = [
]
class cpGearJoint(Structure):
    pass
cpGearJoint._fields_ = [
]
class cpSimpleMotorJoint(Structure):
    pass
cpSimpleMotorJoint._fields_ = [
]
class cpCollisionHandler(Structure):
    pass
class cpContactPointSet(Structure):
    pass
class cpArbiter(Structure):
    pass
cpArbiter._fields_ = [
]
class cpSpace(Structure):
    pass
cpSpace._fields_ = [
]
cpVersionString = (STRING).in_dll(chipmunk_lib, 'cpVersionString')
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
cpMomentForSegment.argtypes = [cpFloat, cpVect, cpVect, cpFloat]
cpAreaForSegment = chipmunk_lib.cpAreaForSegment
cpAreaForSegment.restype = cpFloat
cpAreaForSegment.argtypes = [cpVect, cpVect, cpFloat]
cpMomentForPoly = chipmunk_lib.cpMomentForPoly
cpMomentForPoly.restype = cpFloat
cpMomentForPoly.argtypes = [cpFloat, c_int, POINTER(cpVect), cpVect, cpFloat]
cpAreaForPoly = chipmunk_lib.cpAreaForPoly
cpAreaForPoly.restype = cpFloat
cpAreaForPoly.argtypes = [c_int, POINTER(cpVect), cpFloat]
cpCentroidForPoly = chipmunk_lib.cpCentroidForPoly
cpCentroidForPoly.restype = cpVect
cpCentroidForPoly.argtypes = [c_int, POINTER(cpVect)]
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
cpBool = c_ubyte
cpDataPointer = c_void_p
cpCollisionType = uintptr_t
cpGroup = uintptr_t
cpBitmask = c_uint
cpTimestamp = c_uint
#cpVect._pack_ = 4
#cpVect _fields_ def removed
cpTransform = Transform

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
cpPolyShapeSetVerts.argtypes = [POINTER(cpShape), c_int, POINTER(cpVect), cpTransform]
cpPolyShapeSetVertsRaw = chipmunk_lib.cpPolyShapeSetVertsRaw
cpPolyShapeSetVertsRaw.restype = None
cpPolyShapeSetVertsRaw.argtypes = [POINTER(cpShape), c_int, POINTER(cpVect)]
cpPolyShapeSetRadius = chipmunk_lib.cpPolyShapeSetRadius
cpPolyShapeSetRadius.restype = None
cpPolyShapeSetRadius.argtypes = [POINTER(cpShape), cpFloat]
cpArbiterGetRestitution = chipmunk_lib.cpArbiterGetRestitution
cpArbiterGetRestitution.restype = cpFloat
cpArbiterGetRestitution.argtypes = [POINTER(cpArbiter)]
cpArbiterSetRestitution = chipmunk_lib.cpArbiterSetRestitution
cpArbiterSetRestitution.restype = None
cpArbiterSetRestitution.argtypes = [POINTER(cpArbiter), cpFloat]
cpArbiterGetFriction = chipmunk_lib.cpArbiterGetFriction
cpArbiterGetFriction.restype = cpFloat
cpArbiterGetFriction.argtypes = [POINTER(cpArbiter)]
cpArbiterSetFriction = chipmunk_lib.cpArbiterSetFriction
cpArbiterSetFriction.restype = None
cpArbiterSetFriction.argtypes = [POINTER(cpArbiter), cpFloat]
cpArbiterGetSurfaceVelocity = chipmunk_lib.cpArbiterGetSurfaceVelocity
cpArbiterGetSurfaceVelocity.restype = cpVect
cpArbiterGetSurfaceVelocity.argtypes = [POINTER(cpArbiter)]
cpArbiterSetSurfaceVelocity = chipmunk_lib.cpArbiterSetSurfaceVelocity
cpArbiterSetSurfaceVelocity.restype = None
cpArbiterSetSurfaceVelocity.argtypes = [POINTER(cpArbiter), cpVect]
cpArbiterGetUserData = chipmunk_lib.cpArbiterGetUserData
cpArbiterGetUserData.restype = cpDataPointer
cpArbiterGetUserData.argtypes = [POINTER(cpArbiter)]
cpArbiterSetUserData = chipmunk_lib.cpArbiterSetUserData
cpArbiterSetUserData.restype = None
cpArbiterSetUserData.argtypes = [POINTER(cpArbiter), cpDataPointer]
cpArbiterTotalImpulse = chipmunk_lib.cpArbiterTotalImpulse
cpArbiterTotalImpulse.restype = cpVect
cpArbiterTotalImpulse.argtypes = [POINTER(cpArbiter)]
cpArbiterTotalKE = chipmunk_lib.cpArbiterTotalKE
cpArbiterTotalKE.restype = cpFloat
cpArbiterTotalKE.argtypes = [POINTER(cpArbiter)]
cpArbiterIgnore = chipmunk_lib.cpArbiterIgnore
cpArbiterIgnore.restype = cpBool
cpArbiterIgnore.argtypes = [POINTER(cpArbiter)]
cpArbiterGetShapes = chipmunk_lib.cpArbiterGetShapes
cpArbiterGetShapes.restype = None
cpArbiterGetShapes.argtypes = [POINTER(cpArbiter), POINTER(POINTER(cpShape)), POINTER(POINTER(cpShape))]
cpArbiterGetBodies = chipmunk_lib.cpArbiterGetBodies
cpArbiterGetBodies.restype = None
cpArbiterGetBodies.argtypes = [POINTER(cpArbiter), POINTER(POINTER(cpBody)), POINTER(POINTER(cpBody))]
class N17cpContactPointSet4DOT_25E(Structure):
    pass
#N17cpContactPointSet4DOT_25E._pack_ = 4
N17cpContactPointSet4DOT_25E._fields_ = [
    ('pointA', cpVect),
    ('pointB', cpVect),
    ('distance', cpFloat),
]
cpContactPointSet._fields_ = [
    ('count', c_int),
    ('normal', cpVect),
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
cpArbiterIsRemoval = chipmunk_lib.cpArbiterIsRemoval
cpArbiterIsRemoval.restype = cpBool
cpArbiterIsRemoval.argtypes = [POINTER(cpArbiter)]
cpArbiterGetCount = chipmunk_lib.cpArbiterGetCount
cpArbiterGetCount.restype = c_int
cpArbiterGetCount.argtypes = [POINTER(cpArbiter)]
cpArbiterGetNormal = chipmunk_lib.cpArbiterGetNormal
cpArbiterGetNormal.restype = cpVect
cpArbiterGetNormal.argtypes = [POINTER(cpArbiter)]
cpArbiterGetPointA = chipmunk_lib.cpArbiterGetPointA
cpArbiterGetPointA.restype = cpVect
cpArbiterGetPointA.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterGetPointB = chipmunk_lib.cpArbiterGetPointB
cpArbiterGetPointB.restype = cpVect
cpArbiterGetPointB.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterGetDepth = chipmunk_lib.cpArbiterGetDepth
cpArbiterGetDepth.restype = cpFloat
cpArbiterGetDepth.argtypes = [POINTER(cpArbiter), c_int]
cpArbiterCallWildcardBeginA = chipmunk_lib.cpArbiterCallWildcardBeginA
cpArbiterCallWildcardBeginA.restype = cpBool
cpArbiterCallWildcardBeginA.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
cpArbiterCallWildcardBeginB = chipmunk_lib.cpArbiterCallWildcardBeginB
cpArbiterCallWildcardBeginB.restype = cpBool
cpArbiterCallWildcardBeginB.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
cpArbiterCallWildcardPreSolveA = chipmunk_lib.cpArbiterCallWildcardPreSolveA
cpArbiterCallWildcardPreSolveA.restype = cpBool
cpArbiterCallWildcardPreSolveA.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
cpArbiterCallWildcardPreSolveB = chipmunk_lib.cpArbiterCallWildcardPreSolveB
cpArbiterCallWildcardPreSolveB.restype = cpBool
cpArbiterCallWildcardPreSolveB.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
cpArbiterCallWildcardPostSolveA = chipmunk_lib.cpArbiterCallWildcardPostSolveA
cpArbiterCallWildcardPostSolveA.restype = None
cpArbiterCallWildcardPostSolveA.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
cpArbiterCallWildcardPostSolveB = chipmunk_lib.cpArbiterCallWildcardPostSolveB
cpArbiterCallWildcardPostSolveB.restype = None
cpArbiterCallWildcardPostSolveB.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
cpArbiterCallWildcardSeparateA = chipmunk_lib.cpArbiterCallWildcardSeparateA
cpArbiterCallWildcardSeparateA.restype = None
cpArbiterCallWildcardSeparateA.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
cpArbiterCallWildcardSeparateB = chipmunk_lib.cpArbiterCallWildcardSeparateB
cpArbiterCallWildcardSeparateB.restype = None
cpArbiterCallWildcardSeparateB.argtypes = [POINTER(cpArbiter), POINTER(cpSpace)]
#cpBB._pack_ = 4
cpBB._fields_ = [
    ('l', cpFloat),
    ('b', cpFloat),
    ('r', cpFloat),
    ('t', cpFloat),
]

# values for enumeration 'cpBodyType'
CP_BODY_TYPE_DYNAMIC = 0
CP_BODY_TYPE_KINEMATIC = 1
CP_BODY_TYPE_STATIC = 2
cpBodyType = c_int # enum
cpBodyVelocityFunc = function_pointer(None, POINTER(cpBody), cpVect, cpFloat, cpFloat)
cpBodyPositionFunc = function_pointer(None, POINTER(cpBody), cpFloat)
cpBodyAlloc = chipmunk_lib.cpBodyAlloc
cpBodyAlloc.restype = POINTER(cpBody)
cpBodyAlloc.argtypes = []
cpBodyInit = chipmunk_lib.cpBodyInit
cpBodyInit.restype = POINTER(cpBody)
cpBodyInit.argtypes = [POINTER(cpBody), cpFloat, cpFloat]
cpBodyNew = chipmunk_lib.cpBodyNew
cpBodyNew.restype = POINTER(cpBody)
cpBodyNew.argtypes = [cpFloat, cpFloat]
cpBodyNewKinematic = chipmunk_lib.cpBodyNewKinematic
cpBodyNewKinematic.restype = POINTER(cpBody)
cpBodyNewKinematic.argtypes = []
cpBodyNewStatic = chipmunk_lib.cpBodyNewStatic
cpBodyNewStatic.restype = POINTER(cpBody)
cpBodyNewStatic.argtypes = []
cpBodyDestroy = chipmunk_lib.cpBodyDestroy
cpBodyDestroy.restype = None
cpBodyDestroy.argtypes = [POINTER(cpBody)]
cpBodyFree = chipmunk_lib.cpBodyFree
cpBodyFree.restype = None
cpBodyFree.argtypes = [POINTER(cpBody)]
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
cpBodyIsSleeping = chipmunk_lib.cpBodyIsSleeping
cpBodyIsSleeping.restype = cpBool
cpBodyIsSleeping.argtypes = [POINTER(cpBody)]
cpBodyGetType = chipmunk_lib.cpBodyGetType
cpBodyGetType.restype = cpBodyType
cpBodyGetType.argtypes = [POINTER(cpBody)]
cpBodySetType = chipmunk_lib.cpBodySetType
cpBodySetType.restype = None
cpBodySetType.argtypes = [POINTER(cpBody), cpBodyType]
cpBodyGetSpace = chipmunk_lib.cpBodyGetSpace
cpBodyGetSpace.restype = POINTER(cpSpace)
cpBodyGetSpace.argtypes = [POINTER(cpBody)]
cpBodyGetMass = chipmunk_lib.cpBodyGetMass
cpBodyGetMass.restype = cpFloat
cpBodyGetMass.argtypes = [POINTER(cpBody)]
cpBodySetMass = chipmunk_lib.cpBodySetMass
cpBodySetMass.restype = None
cpBodySetMass.argtypes = [POINTER(cpBody), cpFloat]
cpBodyGetMoment = chipmunk_lib.cpBodyGetMoment
cpBodyGetMoment.restype = cpFloat
cpBodyGetMoment.argtypes = [POINTER(cpBody)]
cpBodySetMoment = chipmunk_lib.cpBodySetMoment
cpBodySetMoment.restype = None
cpBodySetMoment.argtypes = [POINTER(cpBody), cpFloat]
cpBodyGetPosition = chipmunk_lib.cpBodyGetPosition
cpBodyGetPosition.restype = cpVect
cpBodyGetPosition.argtypes = [POINTER(cpBody)]
cpBodySetPosition = chipmunk_lib.cpBodySetPosition
cpBodySetPosition.restype = None
cpBodySetPosition.argtypes = [POINTER(cpBody), cpVect]
cpBodyGetCenterOfGravity = chipmunk_lib.cpBodyGetCenterOfGravity
cpBodyGetCenterOfGravity.restype = cpVect
cpBodyGetCenterOfGravity.argtypes = [POINTER(cpBody)]
cpBodySetCenterOfGravity = chipmunk_lib.cpBodySetCenterOfGravity
cpBodySetCenterOfGravity.restype = None
cpBodySetCenterOfGravity.argtypes = [POINTER(cpBody), cpVect]
cpBodyGetVelocity = chipmunk_lib.cpBodyGetVelocity
cpBodyGetVelocity.restype = cpVect
cpBodyGetVelocity.argtypes = [POINTER(cpBody)]
cpBodySetVelocity = chipmunk_lib.cpBodySetVelocity
cpBodySetVelocity.restype = None
cpBodySetVelocity.argtypes = [POINTER(cpBody), cpVect]
cpBodyGetForce = chipmunk_lib.cpBodyGetForce
cpBodyGetForce.restype = cpVect
cpBodyGetForce.argtypes = [POINTER(cpBody)]
cpBodySetForce = chipmunk_lib.cpBodySetForce
cpBodySetForce.restype = None
cpBodySetForce.argtypes = [POINTER(cpBody), cpVect]
cpBodyGetAngle = chipmunk_lib.cpBodyGetAngle
cpBodyGetAngle.restype = cpFloat
cpBodyGetAngle.argtypes = [POINTER(cpBody)]
cpBodySetAngle = chipmunk_lib.cpBodySetAngle
cpBodySetAngle.restype = None
cpBodySetAngle.argtypes = [POINTER(cpBody), cpFloat]
cpBodyGetAngularVelocity = chipmunk_lib.cpBodyGetAngularVelocity
cpBodyGetAngularVelocity.restype = cpFloat
cpBodyGetAngularVelocity.argtypes = [POINTER(cpBody)]
cpBodySetAngularVelocity = chipmunk_lib.cpBodySetAngularVelocity
cpBodySetAngularVelocity.restype = None
cpBodySetAngularVelocity.argtypes = [POINTER(cpBody), cpFloat]
cpBodyGetTorque = chipmunk_lib.cpBodyGetTorque
cpBodyGetTorque.restype = cpFloat
cpBodyGetTorque.argtypes = [POINTER(cpBody)]
cpBodySetTorque = chipmunk_lib.cpBodySetTorque
cpBodySetTorque.restype = None
cpBodySetTorque.argtypes = [POINTER(cpBody), cpFloat]
cpBodyGetRotation = chipmunk_lib.cpBodyGetRotation
cpBodyGetRotation.restype = cpVect
cpBodyGetRotation.argtypes = [POINTER(cpBody)]
cpBodyGetUserData = chipmunk_lib.cpBodyGetUserData
cpBodyGetUserData.restype = cpDataPointer
cpBodyGetUserData.argtypes = [POINTER(cpBody)]
cpBodySetUserData = chipmunk_lib.cpBodySetUserData
cpBodySetUserData.restype = None
cpBodySetUserData.argtypes = [POINTER(cpBody), cpDataPointer]
cpBodySetVelocityUpdateFunc = chipmunk_lib.cpBodySetVelocityUpdateFunc
cpBodySetVelocityUpdateFunc.restype = None
cpBodySetVelocityUpdateFunc.argtypes = [POINTER(cpBody), cpBodyVelocityFunc]
cpBodySetPositionUpdateFunc = chipmunk_lib.cpBodySetPositionUpdateFunc
cpBodySetPositionUpdateFunc.restype = None
cpBodySetPositionUpdateFunc.argtypes = [POINTER(cpBody), cpBodyPositionFunc]
cpBodyUpdateVelocity = chipmunk_lib.cpBodyUpdateVelocity
cpBodyUpdateVelocity.restype = None
cpBodyUpdateVelocity.argtypes = [POINTER(cpBody), cpVect, cpFloat, cpFloat]
cpBodyUpdatePosition = chipmunk_lib.cpBodyUpdatePosition
cpBodyUpdatePosition.restype = None
cpBodyUpdatePosition.argtypes = [POINTER(cpBody), cpFloat]
cpBodyLocalToWorld = chipmunk_lib.cpBodyLocalToWorld
cpBodyLocalToWorld.restype = cpVect
cpBodyLocalToWorld.argtypes = [POINTER(cpBody), cpVect]
cpBodyWorldToLocal = chipmunk_lib.cpBodyWorldToLocal
cpBodyWorldToLocal.restype = cpVect
cpBodyWorldToLocal.argtypes = [POINTER(cpBody), cpVect]
cpBodyApplyForceAtWorldPoint = chipmunk_lib.cpBodyApplyForceAtWorldPoint
cpBodyApplyForceAtWorldPoint.restype = None
cpBodyApplyForceAtWorldPoint.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpBodyApplyForceAtLocalPoint = chipmunk_lib.cpBodyApplyForceAtLocalPoint
cpBodyApplyForceAtLocalPoint.restype = None
cpBodyApplyForceAtLocalPoint.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpBodyApplyImpulseAtWorldPoint = chipmunk_lib.cpBodyApplyImpulseAtWorldPoint
cpBodyApplyImpulseAtWorldPoint.restype = None
cpBodyApplyImpulseAtWorldPoint.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpBodyApplyImpulseAtLocalPoint = chipmunk_lib.cpBodyApplyImpulseAtLocalPoint
cpBodyApplyImpulseAtLocalPoint.restype = None
cpBodyApplyImpulseAtLocalPoint.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpBodyGetVelocityAtWorldPoint = chipmunk_lib.cpBodyGetVelocityAtWorldPoint
cpBodyGetVelocityAtWorldPoint.restype = cpVect
cpBodyGetVelocityAtWorldPoint.argtypes = [POINTER(cpBody), cpVect]
cpBodyGetVelocityAtLocalPoint = chipmunk_lib.cpBodyGetVelocityAtLocalPoint
cpBodyGetVelocityAtLocalPoint.restype = cpVect
cpBodyGetVelocityAtLocalPoint.argtypes = [POINTER(cpBody), cpVect]
cpBodyKineticEnergy = chipmunk_lib.cpBodyKineticEnergy
cpBodyKineticEnergy.restype = cpFloat
cpBodyKineticEnergy.argtypes = [POINTER(cpBody)]
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
cpConstraintPreSolveFunc = function_pointer(None, POINTER(cpConstraint), POINTER(cpSpace))
cpConstraintPostSolveFunc = function_pointer(None, POINTER(cpConstraint), POINTER(cpSpace))
cpConstraintDestroy = chipmunk_lib.cpConstraintDestroy
cpConstraintDestroy.restype = None
cpConstraintDestroy.argtypes = [POINTER(cpConstraint)]
cpConstraintFree = chipmunk_lib.cpConstraintFree
cpConstraintFree.restype = None
cpConstraintFree.argtypes = [POINTER(cpConstraint)]
cpConstraintGetSpace = chipmunk_lib.cpConstraintGetSpace
cpConstraintGetSpace.restype = POINTER(cpSpace)
cpConstraintGetSpace.argtypes = [POINTER(cpConstraint)]
cpConstraintGetBodyA = chipmunk_lib.cpConstraintGetBodyA
cpConstraintGetBodyA.restype = POINTER(cpBody)
cpConstraintGetBodyA.argtypes = [POINTER(cpConstraint)]
cpConstraintGetBodyB = chipmunk_lib.cpConstraintGetBodyB
cpConstraintGetBodyB.restype = POINTER(cpBody)
cpConstraintGetBodyB.argtypes = [POINTER(cpConstraint)]
cpConstraintGetMaxForce = chipmunk_lib.cpConstraintGetMaxForce
cpConstraintGetMaxForce.restype = cpFloat
cpConstraintGetMaxForce.argtypes = [POINTER(cpConstraint)]
cpConstraintSetMaxForce = chipmunk_lib.cpConstraintSetMaxForce
cpConstraintSetMaxForce.restype = None
cpConstraintSetMaxForce.argtypes = [POINTER(cpConstraint), cpFloat]
cpConstraintGetErrorBias = chipmunk_lib.cpConstraintGetErrorBias
cpConstraintGetErrorBias.restype = cpFloat
cpConstraintGetErrorBias.argtypes = [POINTER(cpConstraint)]
cpConstraintSetErrorBias = chipmunk_lib.cpConstraintSetErrorBias
cpConstraintSetErrorBias.restype = None
cpConstraintSetErrorBias.argtypes = [POINTER(cpConstraint), cpFloat]
cpConstraintGetMaxBias = chipmunk_lib.cpConstraintGetMaxBias
cpConstraintGetMaxBias.restype = cpFloat
cpConstraintGetMaxBias.argtypes = [POINTER(cpConstraint)]
cpConstraintSetMaxBias = chipmunk_lib.cpConstraintSetMaxBias
cpConstraintSetMaxBias.restype = None
cpConstraintSetMaxBias.argtypes = [POINTER(cpConstraint), cpFloat]
cpConstraintGetCollideBodies = chipmunk_lib.cpConstraintGetCollideBodies
cpConstraintGetCollideBodies.restype = cpBool
cpConstraintGetCollideBodies.argtypes = [POINTER(cpConstraint)]
cpConstraintSetCollideBodies = chipmunk_lib.cpConstraintSetCollideBodies
cpConstraintSetCollideBodies.restype = None
cpConstraintSetCollideBodies.argtypes = [POINTER(cpConstraint), cpBool]
cpConstraintGetPreSolveFunc = chipmunk_lib.cpConstraintGetPreSolveFunc
cpConstraintGetPreSolveFunc.restype = cpConstraintPreSolveFunc
cpConstraintGetPreSolveFunc.argtypes = [POINTER(cpConstraint)]
cpConstraintSetPreSolveFunc = chipmunk_lib.cpConstraintSetPreSolveFunc
cpConstraintSetPreSolveFunc.restype = None
cpConstraintSetPreSolveFunc.argtypes = [POINTER(cpConstraint), cpConstraintPreSolveFunc]
cpConstraintGetPostSolveFunc = chipmunk_lib.cpConstraintGetPostSolveFunc
cpConstraintGetPostSolveFunc.restype = cpConstraintPostSolveFunc
cpConstraintGetPostSolveFunc.argtypes = [POINTER(cpConstraint)]
cpConstraintSetPostSolveFunc = chipmunk_lib.cpConstraintSetPostSolveFunc
cpConstraintSetPostSolveFunc.restype = None
cpConstraintSetPostSolveFunc.argtypes = [POINTER(cpConstraint), cpConstraintPostSolveFunc]
cpConstraintGetUserData = chipmunk_lib.cpConstraintGetUserData
cpConstraintGetUserData.restype = cpDataPointer
cpConstraintGetUserData.argtypes = [POINTER(cpConstraint)]
cpConstraintSetUserData = chipmunk_lib.cpConstraintSetUserData
cpConstraintSetUserData.restype = None
cpConstraintSetUserData.argtypes = [POINTER(cpConstraint), cpDataPointer]
cpConstraintGetImpulse = chipmunk_lib.cpConstraintGetImpulse
cpConstraintGetImpulse.restype = cpFloat
cpConstraintGetImpulse.argtypes = [POINTER(cpConstraint)]
cpConstraintIsDampedRotarySpring = chipmunk_lib.cpConstraintIsDampedRotarySpring
cpConstraintIsDampedRotarySpring.restype = cpBool
cpConstraintIsDampedRotarySpring.argtypes = [POINTER(cpConstraint)]
cpDampedRotarySpringTorqueFunc = function_pointer(cpFloat, POINTER(cpConstraint), cpFloat)
cpDampedRotarySpringAlloc = chipmunk_lib.cpDampedRotarySpringAlloc
cpDampedRotarySpringAlloc.restype = POINTER(cpDampedRotarySpring)
cpDampedRotarySpringAlloc.argtypes = []
cpDampedRotarySpringInit = chipmunk_lib.cpDampedRotarySpringInit
cpDampedRotarySpringInit.restype = POINTER(cpDampedRotarySpring)
cpDampedRotarySpringInit.argtypes = [POINTER(cpDampedRotarySpring), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat, cpFloat]
cpDampedRotarySpringNew = chipmunk_lib.cpDampedRotarySpringNew
cpDampedRotarySpringNew.restype = POINTER(cpConstraint)
cpDampedRotarySpringNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat, cpFloat]
cpDampedRotarySpringGetRestAngle = chipmunk_lib.cpDampedRotarySpringGetRestAngle
cpDampedRotarySpringGetRestAngle.restype = cpFloat
cpDampedRotarySpringGetRestAngle.argtypes = [POINTER(cpConstraint)]
cpDampedRotarySpringSetRestAngle = chipmunk_lib.cpDampedRotarySpringSetRestAngle
cpDampedRotarySpringSetRestAngle.restype = None
cpDampedRotarySpringSetRestAngle.argtypes = [POINTER(cpConstraint), cpFloat]
cpDampedRotarySpringGetStiffness = chipmunk_lib.cpDampedRotarySpringGetStiffness
cpDampedRotarySpringGetStiffness.restype = cpFloat
cpDampedRotarySpringGetStiffness.argtypes = [POINTER(cpConstraint)]
cpDampedRotarySpringSetStiffness = chipmunk_lib.cpDampedRotarySpringSetStiffness
cpDampedRotarySpringSetStiffness.restype = None
cpDampedRotarySpringSetStiffness.argtypes = [POINTER(cpConstraint), cpFloat]
cpDampedRotarySpringGetDamping = chipmunk_lib.cpDampedRotarySpringGetDamping
cpDampedRotarySpringGetDamping.restype = cpFloat
cpDampedRotarySpringGetDamping.argtypes = [POINTER(cpConstraint)]
cpDampedRotarySpringSetDamping = chipmunk_lib.cpDampedRotarySpringSetDamping
cpDampedRotarySpringSetDamping.restype = None
cpDampedRotarySpringSetDamping.argtypes = [POINTER(cpConstraint), cpFloat]
cpDampedRotarySpringGetSpringTorqueFunc = chipmunk_lib.cpDampedRotarySpringGetSpringTorqueFunc
cpDampedRotarySpringGetSpringTorqueFunc.restype = cpDampedRotarySpringTorqueFunc
cpDampedRotarySpringGetSpringTorqueFunc.argtypes = [POINTER(cpConstraint)]
cpDampedRotarySpringSetSpringTorqueFunc = chipmunk_lib.cpDampedRotarySpringSetSpringTorqueFunc
cpDampedRotarySpringSetSpringTorqueFunc.restype = None
cpDampedRotarySpringSetSpringTorqueFunc.argtypes = [POINTER(cpConstraint), cpDampedRotarySpringTorqueFunc]
cpConstraintIsDampedSpring = chipmunk_lib.cpConstraintIsDampedSpring
cpConstraintIsDampedSpring.restype = cpBool
cpConstraintIsDampedSpring.argtypes = [POINTER(cpConstraint)]
cpDampedSpringForceFunc = function_pointer(cpFloat, POINTER(cpConstraint), cpFloat)
cpDampedSpringAlloc = chipmunk_lib.cpDampedSpringAlloc
cpDampedSpringAlloc.restype = POINTER(cpDampedSpring)
cpDampedSpringAlloc.argtypes = []
cpDampedSpringInit = chipmunk_lib.cpDampedSpringInit
cpDampedSpringInit.restype = POINTER(cpDampedSpring)
cpDampedSpringInit.argtypes = [POINTER(cpDampedSpring), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat]
cpDampedSpringNew = chipmunk_lib.cpDampedSpringNew
cpDampedSpringNew.restype = POINTER(cpConstraint)
cpDampedSpringNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat]
cpDampedSpringGetAnchorA = chipmunk_lib.cpDampedSpringGetAnchorA
cpDampedSpringGetAnchorA.restype = cpVect
cpDampedSpringGetAnchorA.argtypes = [POINTER(cpConstraint)]
cpDampedSpringSetAnchorA = chipmunk_lib.cpDampedSpringSetAnchorA
cpDampedSpringSetAnchorA.restype = None
cpDampedSpringSetAnchorA.argtypes = [POINTER(cpConstraint), cpVect]
cpDampedSpringGetAnchorB = chipmunk_lib.cpDampedSpringGetAnchorB
cpDampedSpringGetAnchorB.restype = cpVect
cpDampedSpringGetAnchorB.argtypes = [POINTER(cpConstraint)]
cpDampedSpringSetAnchorB = chipmunk_lib.cpDampedSpringSetAnchorB
cpDampedSpringSetAnchorB.restype = None
cpDampedSpringSetAnchorB.argtypes = [POINTER(cpConstraint), cpVect]
cpDampedSpringGetRestLength = chipmunk_lib.cpDampedSpringGetRestLength
cpDampedSpringGetRestLength.restype = cpFloat
cpDampedSpringGetRestLength.argtypes = [POINTER(cpConstraint)]
cpDampedSpringSetRestLength = chipmunk_lib.cpDampedSpringSetRestLength
cpDampedSpringSetRestLength.restype = None
cpDampedSpringSetRestLength.argtypes = [POINTER(cpConstraint), cpFloat]
cpDampedSpringGetStiffness = chipmunk_lib.cpDampedSpringGetStiffness
cpDampedSpringGetStiffness.restype = cpFloat
cpDampedSpringGetStiffness.argtypes = [POINTER(cpConstraint)]
cpDampedSpringSetStiffness = chipmunk_lib.cpDampedSpringSetStiffness
cpDampedSpringSetStiffness.restype = None
cpDampedSpringSetStiffness.argtypes = [POINTER(cpConstraint), cpFloat]
cpDampedSpringGetDamping = chipmunk_lib.cpDampedSpringGetDamping
cpDampedSpringGetDamping.restype = cpFloat
cpDampedSpringGetDamping.argtypes = [POINTER(cpConstraint)]
cpDampedSpringSetDamping = chipmunk_lib.cpDampedSpringSetDamping
cpDampedSpringSetDamping.restype = None
cpDampedSpringSetDamping.argtypes = [POINTER(cpConstraint), cpFloat]
cpDampedSpringGetSpringForceFunc = chipmunk_lib.cpDampedSpringGetSpringForceFunc
cpDampedSpringGetSpringForceFunc.restype = cpDampedSpringForceFunc
cpDampedSpringGetSpringForceFunc.argtypes = [POINTER(cpConstraint)]
cpDampedSpringSetSpringForceFunc = chipmunk_lib.cpDampedSpringSetSpringForceFunc
cpDampedSpringSetSpringForceFunc.restype = None
cpDampedSpringSetSpringForceFunc.argtypes = [POINTER(cpConstraint), cpDampedSpringForceFunc]
cpConstraintIsGearJoint = chipmunk_lib.cpConstraintIsGearJoint
cpConstraintIsGearJoint.restype = cpBool
cpConstraintIsGearJoint.argtypes = [POINTER(cpConstraint)]
cpGearJointAlloc = chipmunk_lib.cpGearJointAlloc
cpGearJointAlloc.restype = POINTER(cpGearJoint)
cpGearJointAlloc.argtypes = []
cpGearJointInit = chipmunk_lib.cpGearJointInit
cpGearJointInit.restype = POINTER(cpGearJoint)
cpGearJointInit.argtypes = [POINTER(cpGearJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpGearJointNew = chipmunk_lib.cpGearJointNew
cpGearJointNew.restype = POINTER(cpConstraint)
cpGearJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpGearJointGetPhase = chipmunk_lib.cpGearJointGetPhase
cpGearJointGetPhase.restype = cpFloat
cpGearJointGetPhase.argtypes = [POINTER(cpConstraint)]
cpGearJointSetPhase = chipmunk_lib.cpGearJointSetPhase
cpGearJointSetPhase.restype = None
cpGearJointSetPhase.argtypes = [POINTER(cpConstraint), cpFloat]
cpGearJointGetRatio = chipmunk_lib.cpGearJointGetRatio
cpGearJointGetRatio.restype = cpFloat
cpGearJointGetRatio.argtypes = [POINTER(cpConstraint)]
cpGearJointSetRatio = chipmunk_lib.cpGearJointSetRatio
cpGearJointSetRatio.restype = None
cpGearJointSetRatio.argtypes = [POINTER(cpConstraint), cpFloat]
cpConstraintIsGrooveJoint = chipmunk_lib.cpConstraintIsGrooveJoint
cpConstraintIsGrooveJoint.restype = cpBool
cpConstraintIsGrooveJoint.argtypes = [POINTER(cpConstraint)]
cpGrooveJointAlloc = chipmunk_lib.cpGrooveJointAlloc
cpGrooveJointAlloc.restype = POINTER(cpGrooveJoint)
cpGrooveJointAlloc.argtypes = []
cpGrooveJointInit = chipmunk_lib.cpGrooveJointInit
cpGrooveJointInit.restype = POINTER(cpGrooveJoint)
cpGrooveJointInit.argtypes = [POINTER(cpGrooveJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
cpGrooveJointNew = chipmunk_lib.cpGrooveJointNew
cpGrooveJointNew.restype = POINTER(cpConstraint)
cpGrooveJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpVect]
cpGrooveJointGetGrooveA = chipmunk_lib.cpGrooveJointGetGrooveA
cpGrooveJointGetGrooveA.restype = cpVect
cpGrooveJointGetGrooveA.argtypes = [POINTER(cpConstraint)]
cpGrooveJointSetGrooveA = chipmunk_lib.cpGrooveJointSetGrooveA
cpGrooveJointSetGrooveA.restype = None
cpGrooveJointSetGrooveA.argtypes = [POINTER(cpConstraint), cpVect]
cpGrooveJointGetGrooveB = chipmunk_lib.cpGrooveJointGetGrooveB
cpGrooveJointGetGrooveB.restype = cpVect
cpGrooveJointGetGrooveB.argtypes = [POINTER(cpConstraint)]
cpGrooveJointSetGrooveB = chipmunk_lib.cpGrooveJointSetGrooveB
cpGrooveJointSetGrooveB.restype = None
cpGrooveJointSetGrooveB.argtypes = [POINTER(cpConstraint), cpVect]
cpGrooveJointGetAnchorB = chipmunk_lib.cpGrooveJointGetAnchorB
cpGrooveJointGetAnchorB.restype = cpVect
cpGrooveJointGetAnchorB.argtypes = [POINTER(cpConstraint)]
cpGrooveJointSetAnchorB = chipmunk_lib.cpGrooveJointSetAnchorB
cpGrooveJointSetAnchorB.restype = None
cpGrooveJointSetAnchorB.argtypes = [POINTER(cpConstraint), cpVect]
cpConstraintIsPinJoint = chipmunk_lib.cpConstraintIsPinJoint
cpConstraintIsPinJoint.restype = cpBool
cpConstraintIsPinJoint.argtypes = [POINTER(cpConstraint)]
cpPinJointAlloc = chipmunk_lib.cpPinJointAlloc
cpPinJointAlloc.restype = POINTER(cpPinJoint)
cpPinJointAlloc.argtypes = []
cpPinJointInit = chipmunk_lib.cpPinJointInit
cpPinJointInit.restype = POINTER(cpPinJoint)
cpPinJointInit.argtypes = [POINTER(cpPinJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPinJointNew = chipmunk_lib.cpPinJointNew
cpPinJointNew.restype = POINTER(cpConstraint)
cpPinJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPinJointGetAnchorA = chipmunk_lib.cpPinJointGetAnchorA
cpPinJointGetAnchorA.restype = cpVect
cpPinJointGetAnchorA.argtypes = [POINTER(cpConstraint)]
cpPinJointSetAnchorA = chipmunk_lib.cpPinJointSetAnchorA
cpPinJointSetAnchorA.restype = None
cpPinJointSetAnchorA.argtypes = [POINTER(cpConstraint), cpVect]
cpPinJointGetAnchorB = chipmunk_lib.cpPinJointGetAnchorB
cpPinJointGetAnchorB.restype = cpVect
cpPinJointGetAnchorB.argtypes = [POINTER(cpConstraint)]
cpPinJointSetAnchorB = chipmunk_lib.cpPinJointSetAnchorB
cpPinJointSetAnchorB.restype = None
cpPinJointSetAnchorB.argtypes = [POINTER(cpConstraint), cpVect]
cpPinJointGetDist = chipmunk_lib.cpPinJointGetDist
cpPinJointGetDist.restype = cpFloat
cpPinJointGetDist.argtypes = [POINTER(cpConstraint)]
cpPinJointSetDist = chipmunk_lib.cpPinJointSetDist
cpPinJointSetDist.restype = None
cpPinJointSetDist.argtypes = [POINTER(cpConstraint), cpFloat]
cpConstraintIsPivotJoint = chipmunk_lib.cpConstraintIsPivotJoint
cpConstraintIsPivotJoint.restype = cpBool
cpConstraintIsPivotJoint.argtypes = [POINTER(cpConstraint)]
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
cpPivotJointGetAnchorA = chipmunk_lib.cpPivotJointGetAnchorA
cpPivotJointGetAnchorA.restype = cpVect
cpPivotJointGetAnchorA.argtypes = [POINTER(cpConstraint)]
cpPivotJointSetAnchorA = chipmunk_lib.cpPivotJointSetAnchorA
cpPivotJointSetAnchorA.restype = None
cpPivotJointSetAnchorA.argtypes = [POINTER(cpConstraint), cpVect]
cpPivotJointGetAnchorB = chipmunk_lib.cpPivotJointGetAnchorB
cpPivotJointGetAnchorB.restype = cpVect
cpPivotJointGetAnchorB.argtypes = [POINTER(cpConstraint)]
cpPivotJointSetAnchorB = chipmunk_lib.cpPivotJointSetAnchorB
cpPivotJointSetAnchorB.restype = None
cpPivotJointSetAnchorB.argtypes = [POINTER(cpConstraint), cpVect]
cpPolyShapeAlloc = chipmunk_lib.cpPolyShapeAlloc
cpPolyShapeAlloc.restype = POINTER(cpPolyShape)
cpPolyShapeAlloc.argtypes = []
cpPolyShapeInit = chipmunk_lib.cpPolyShapeInit
cpPolyShapeInit.restype = POINTER(cpPolyShape)
cpPolyShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), c_int, POINTER(cpVect), cpTransform, cpFloat]
cpPolyShapeInitRaw = chipmunk_lib.cpPolyShapeInitRaw
cpPolyShapeInitRaw.restype = POINTER(cpPolyShape)
cpPolyShapeInitRaw.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), c_int, POINTER(cpVect), cpFloat]
cpPolyShapeNew = chipmunk_lib.cpPolyShapeNew
cpPolyShapeNew.restype = POINTER(cpShape)
cpPolyShapeNew.argtypes = [POINTER(cpBody), c_int, POINTER(cpVect), cpTransform, cpFloat]
cpBoxShapeInit = chipmunk_lib.cpBoxShapeInit
cpBoxShapeInit.restype = POINTER(cpPolyShape)
cpBoxShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpFloat, cpFloat, cpFloat]
cpBoxShapeInit2 = chipmunk_lib.cpBoxShapeInit2
cpBoxShapeInit2.restype = POINTER(cpPolyShape)
cpBoxShapeInit2.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), cpBB, cpFloat]
cpBoxShapeNew = chipmunk_lib.cpBoxShapeNew
cpBoxShapeNew.restype = POINTER(cpShape)
cpBoxShapeNew.argtypes = [POINTER(cpBody), cpFloat, cpFloat, cpFloat]
cpBoxShapeNew2 = chipmunk_lib.cpBoxShapeNew2
cpBoxShapeNew2.restype = POINTER(cpShape)
cpBoxShapeNew2.argtypes = [POINTER(cpBody), cpBB, cpFloat]
cpPolyShapeGetCount = chipmunk_lib.cpPolyShapeGetCount
cpPolyShapeGetCount.restype = c_int
cpPolyShapeGetCount.argtypes = [POINTER(cpShape)]
cpPolyShapeGetVert = chipmunk_lib.cpPolyShapeGetVert
cpPolyShapeGetVert.restype = cpVect
cpPolyShapeGetVert.argtypes = [POINTER(cpShape), c_int]
cpPolyShapeGetRadius = chipmunk_lib.cpPolyShapeGetRadius
cpPolyShapeGetRadius.restype = cpFloat
cpPolyShapeGetRadius.argtypes = [POINTER(cpShape)]
cpConstraintIsRatchetJoint = chipmunk_lib.cpConstraintIsRatchetJoint
cpConstraintIsRatchetJoint.restype = cpBool
cpConstraintIsRatchetJoint.argtypes = [POINTER(cpConstraint)]
cpRatchetJointAlloc = chipmunk_lib.cpRatchetJointAlloc
cpRatchetJointAlloc.restype = POINTER(cpRatchetJoint)
cpRatchetJointAlloc.argtypes = []
cpRatchetJointInit = chipmunk_lib.cpRatchetJointInit
cpRatchetJointInit.restype = POINTER(cpRatchetJoint)
cpRatchetJointInit.argtypes = [POINTER(cpRatchetJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRatchetJointNew = chipmunk_lib.cpRatchetJointNew
cpRatchetJointNew.restype = POINTER(cpConstraint)
cpRatchetJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRatchetJointGetAngle = chipmunk_lib.cpRatchetJointGetAngle
cpRatchetJointGetAngle.restype = cpFloat
cpRatchetJointGetAngle.argtypes = [POINTER(cpConstraint)]
cpRatchetJointSetAngle = chipmunk_lib.cpRatchetJointSetAngle
cpRatchetJointSetAngle.restype = None
cpRatchetJointSetAngle.argtypes = [POINTER(cpConstraint), cpFloat]
cpRatchetJointGetPhase = chipmunk_lib.cpRatchetJointGetPhase
cpRatchetJointGetPhase.restype = cpFloat
cpRatchetJointGetPhase.argtypes = [POINTER(cpConstraint)]
cpRatchetJointSetPhase = chipmunk_lib.cpRatchetJointSetPhase
cpRatchetJointSetPhase.restype = None
cpRatchetJointSetPhase.argtypes = [POINTER(cpConstraint), cpFloat]
cpRatchetJointGetRatchet = chipmunk_lib.cpRatchetJointGetRatchet
cpRatchetJointGetRatchet.restype = cpFloat
cpRatchetJointGetRatchet.argtypes = [POINTER(cpConstraint)]
cpRatchetJointSetRatchet = chipmunk_lib.cpRatchetJointSetRatchet
cpRatchetJointSetRatchet.restype = None
cpRatchetJointSetRatchet.argtypes = [POINTER(cpConstraint), cpFloat]
cpConstraintIsRotaryLimitJoint = chipmunk_lib.cpConstraintIsRotaryLimitJoint
cpConstraintIsRotaryLimitJoint.restype = cpBool
cpConstraintIsRotaryLimitJoint.argtypes = [POINTER(cpConstraint)]
cpRotaryLimitJointAlloc = chipmunk_lib.cpRotaryLimitJointAlloc
cpRotaryLimitJointAlloc.restype = POINTER(cpRotaryLimitJoint)
cpRotaryLimitJointAlloc.argtypes = []
cpRotaryLimitJointInit = chipmunk_lib.cpRotaryLimitJointInit
cpRotaryLimitJointInit.restype = POINTER(cpRotaryLimitJoint)
cpRotaryLimitJointInit.argtypes = [POINTER(cpRotaryLimitJoint), POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRotaryLimitJointNew = chipmunk_lib.cpRotaryLimitJointNew
cpRotaryLimitJointNew.restype = POINTER(cpConstraint)
cpRotaryLimitJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat, cpFloat]
cpRotaryLimitJointGetMin = chipmunk_lib.cpRotaryLimitJointGetMin
cpRotaryLimitJointGetMin.restype = cpFloat
cpRotaryLimitJointGetMin.argtypes = [POINTER(cpConstraint)]
cpRotaryLimitJointSetMin = chipmunk_lib.cpRotaryLimitJointSetMin
cpRotaryLimitJointSetMin.restype = None
cpRotaryLimitJointSetMin.argtypes = [POINTER(cpConstraint), cpFloat]
cpRotaryLimitJointGetMax = chipmunk_lib.cpRotaryLimitJointGetMax
cpRotaryLimitJointGetMax.restype = cpFloat
cpRotaryLimitJointGetMax.argtypes = [POINTER(cpConstraint)]
cpRotaryLimitJointSetMax = chipmunk_lib.cpRotaryLimitJointSetMax
cpRotaryLimitJointSetMax.restype = None
cpRotaryLimitJointSetMax.argtypes = [POINTER(cpConstraint), cpFloat]

class cpPointQueryInfo(Structure):
    pass
#cpPointQueryInfo._pack_ = 4
cpPointQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('point', cpVect),
    ('distance', cpFloat),
    ('gradient', cpVect),
]

class cpSegmentQueryInfo(Structure):
    pass
#cpSegmentQueryInfo._pack_ = 4
cpSegmentQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('point', cpVect),
    ('normal', cpVect),
    ('alpha', cpFloat),
]


import collections
class ShapeFilter1(collections.namedtuple('ShapeFilter', ['group','categories','mask'])):
    @classmethod
    def from_param(cls, arg):
        print cls, arg
        print 1
        print "XXXXXXXXXXXXXXX"
        return cls(1,2,3)

cpShapeFilter = ShapeFilter        
"""
class cpShapeFilter(Structure):
    pass
cpShapeFilter._fields_ = [
    ('group', cpGroup),
    ('categories', cpBitmask),
    ('mask', cpBitmask),
]
"""
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
cpShapeUpdate.argtypes = [POINTER(cpShape), cpTransform]
cpShapePointQuery = chipmunk_lib.cpShapePointQuery
cpShapePointQuery.restype = cpFloat
cpShapePointQuery.argtypes = [POINTER(cpShape), cpVect, POINTER(cpPointQueryInfo)]
cpShapeSegmentQuery = chipmunk_lib.cpShapeSegmentQuery
cpShapeSegmentQuery.restype = cpBool
cpShapeSegmentQuery.argtypes = [POINTER(cpShape), cpVect, cpVect, cpFloat, POINTER(cpSegmentQueryInfo)]
cpShapesCollide = chipmunk_lib.cpShapesCollide
cpShapesCollide.restype = cpContactPointSet
cpShapesCollide.argtypes = [POINTER(cpShape), POINTER(cpShape)]
cpShapeGetSpace = chipmunk_lib.cpShapeGetSpace
cpShapeGetSpace.restype = POINTER(cpSpace)
cpShapeGetSpace.argtypes = [POINTER(cpShape)]
cpShapeGetBody = chipmunk_lib.cpShapeGetBody
cpShapeGetBody.restype = POINTER(cpBody)
cpShapeGetBody.argtypes = [POINTER(cpShape)]
cpShapeSetBody = chipmunk_lib.cpShapeSetBody
cpShapeSetBody.restype = None
cpShapeSetBody.argtypes = [POINTER(cpShape), POINTER(cpBody)]
cpShapeGetMass = chipmunk_lib.cpShapeGetMass
cpShapeGetMass.restype = cpFloat
cpShapeGetMass.argtypes = [POINTER(cpShape)]
cpShapeSetMass = chipmunk_lib.cpShapeSetMass
cpShapeSetMass.restype = None
cpShapeSetMass.argtypes = [POINTER(cpShape), cpFloat]
cpShapeGetDensity = chipmunk_lib.cpShapeGetDensity
cpShapeGetDensity.restype = cpFloat
cpShapeGetDensity.argtypes = [POINTER(cpShape)]
cpShapeSetDensity = chipmunk_lib.cpShapeSetDensity
cpShapeSetDensity.restype = None
cpShapeSetDensity.argtypes = [POINTER(cpShape), cpFloat]
cpShapeGetMoment = chipmunk_lib.cpShapeGetMoment
cpShapeGetMoment.restype = cpFloat
cpShapeGetMoment.argtypes = [POINTER(cpShape)]
cpShapeGetArea = chipmunk_lib.cpShapeGetArea
cpShapeGetArea.restype = cpFloat
cpShapeGetArea.argtypes = [POINTER(cpShape)]
cpShapeGetCenterOfGravity = chipmunk_lib.cpShapeGetCenterOfGravity
cpShapeGetCenterOfGravity.restype = cpVect
cpShapeGetCenterOfGravity.argtypes = [POINTER(cpShape)]
cpShapeGetBB = chipmunk_lib.cpShapeGetBB
cpShapeGetBB.restype = cpBB
cpShapeGetBB.argtypes = [POINTER(cpShape)]
cpShapeGetSensor = chipmunk_lib.cpShapeGetSensor
cpShapeGetSensor.restype = cpBool
cpShapeGetSensor.argtypes = [POINTER(cpShape)]
cpShapeSetSensor = chipmunk_lib.cpShapeSetSensor
cpShapeSetSensor.restype = None
cpShapeSetSensor.argtypes = [POINTER(cpShape), cpBool]
cpShapeGetElasticity = chipmunk_lib.cpShapeGetElasticity
cpShapeGetElasticity.restype = cpFloat
cpShapeGetElasticity.argtypes = [POINTER(cpShape)]
cpShapeSetElasticity = chipmunk_lib.cpShapeSetElasticity
cpShapeSetElasticity.restype = None
cpShapeSetElasticity.argtypes = [POINTER(cpShape), cpFloat]
cpShapeGetFriction = chipmunk_lib.cpShapeGetFriction
cpShapeGetFriction.restype = cpFloat
cpShapeGetFriction.argtypes = [POINTER(cpShape)]
cpShapeSetFriction = chipmunk_lib.cpShapeSetFriction
cpShapeSetFriction.restype = None
cpShapeSetFriction.argtypes = [POINTER(cpShape), cpFloat]
cpShapeGetSurfaceVelocity = chipmunk_lib.cpShapeGetSurfaceVelocity
cpShapeGetSurfaceVelocity.restype = cpVect
cpShapeGetSurfaceVelocity.argtypes = [POINTER(cpShape)]
cpShapeSetSurfaceVelocity = chipmunk_lib.cpShapeSetSurfaceVelocity
cpShapeSetSurfaceVelocity.restype = None
cpShapeSetSurfaceVelocity.argtypes = [POINTER(cpShape), cpVect]
cpShapeGetUserData = chipmunk_lib.cpShapeGetUserData
cpShapeGetUserData.restype = cpDataPointer
cpShapeGetUserData.argtypes = [POINTER(cpShape)]
cpShapeSetUserData = chipmunk_lib.cpShapeSetUserData
cpShapeSetUserData.restype = None
cpShapeSetUserData.argtypes = [POINTER(cpShape), cpDataPointer]
cpShapeGetCollisionType = chipmunk_lib.cpShapeGetCollisionType
cpShapeGetCollisionType.restype = cpCollisionType
cpShapeGetCollisionType.argtypes = [POINTER(cpShape)]
cpShapeSetCollisionType = chipmunk_lib.cpShapeSetCollisionType
cpShapeSetCollisionType.restype = None
cpShapeSetCollisionType.argtypes = [POINTER(cpShape), cpCollisionType]
cpShapeGetFilter = chipmunk_lib.cpShapeGetFilter
cpShapeGetFilter.restype = cpShapeFilter
cpShapeGetFilter.argtypes = [POINTER(cpShape)]
cpShapeSetFilter = chipmunk_lib.cpShapeSetFilter
cpShapeSetFilter.restype = None
cpShapeSetFilter.argtypes = [POINTER(cpShape), cpShapeFilter]
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
class cpSimpleMotor(Structure):
    pass
cpSimpleMotor._fields_ = [
]
cpConstraintIsSimpleMotor = chipmunk_lib.cpConstraintIsSimpleMotor
cpConstraintIsSimpleMotor.restype = cpBool
cpConstraintIsSimpleMotor.argtypes = [POINTER(cpConstraint)]
cpSimpleMotorAlloc = chipmunk_lib.cpSimpleMotorAlloc
cpSimpleMotorAlloc.restype = POINTER(cpSimpleMotor)
cpSimpleMotorAlloc.argtypes = []
cpSimpleMotorInit = chipmunk_lib.cpSimpleMotorInit
cpSimpleMotorInit.restype = POINTER(cpSimpleMotor)
cpSimpleMotorInit.argtypes = [POINTER(cpSimpleMotor), POINTER(cpBody), POINTER(cpBody), cpFloat]
cpSimpleMotorNew = chipmunk_lib.cpSimpleMotorNew
cpSimpleMotorNew.restype = POINTER(cpConstraint)
cpSimpleMotorNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpFloat]
cpSimpleMotorGetRate = chipmunk_lib.cpSimpleMotorGetRate
cpSimpleMotorGetRate.restype = cpFloat
cpSimpleMotorGetRate.argtypes = [POINTER(cpConstraint)]
cpSimpleMotorSetRate = chipmunk_lib.cpSimpleMotorSetRate
cpSimpleMotorSetRate.restype = None
cpSimpleMotorSetRate.argtypes = [POINTER(cpConstraint), cpFloat]
cpConstraintIsSlideJoint = chipmunk_lib.cpConstraintIsSlideJoint
cpConstraintIsSlideJoint.restype = cpBool
cpConstraintIsSlideJoint.argtypes = [POINTER(cpConstraint)]
cpSlideJointAlloc = chipmunk_lib.cpSlideJointAlloc
cpSlideJointAlloc.restype = POINTER(cpSlideJoint)
cpSlideJointAlloc.argtypes = []
cpSlideJointInit = chipmunk_lib.cpSlideJointInit
cpSlideJointInit.restype = POINTER(cpSlideJoint)
cpSlideJointInit.argtypes = [POINTER(cpSlideJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpSlideJointNew = chipmunk_lib.cpSlideJointNew
cpSlideJointNew.restype = POINTER(cpConstraint)
cpSlideJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpSlideJointGetAnchorA = chipmunk_lib.cpSlideJointGetAnchorA
cpSlideJointGetAnchorA.restype = cpVect
cpSlideJointGetAnchorA.argtypes = [POINTER(cpConstraint)]
cpSlideJointSetAnchorA = chipmunk_lib.cpSlideJointSetAnchorA
cpSlideJointSetAnchorA.restype = None
cpSlideJointSetAnchorA.argtypes = [POINTER(cpConstraint), cpVect]
cpSlideJointGetAnchorB = chipmunk_lib.cpSlideJointGetAnchorB
cpSlideJointGetAnchorB.restype = cpVect
cpSlideJointGetAnchorB.argtypes = [POINTER(cpConstraint)]
cpSlideJointSetAnchorB = chipmunk_lib.cpSlideJointSetAnchorB
cpSlideJointSetAnchorB.restype = None
cpSlideJointSetAnchorB.argtypes = [POINTER(cpConstraint), cpVect]
cpSlideJointGetMin = chipmunk_lib.cpSlideJointGetMin
cpSlideJointGetMin.restype = cpFloat
cpSlideJointGetMin.argtypes = [POINTER(cpConstraint)]
cpSlideJointSetMin = chipmunk_lib.cpSlideJointSetMin
cpSlideJointSetMin.restype = None
cpSlideJointSetMin.argtypes = [POINTER(cpConstraint), cpFloat]
cpSlideJointGetMax = chipmunk_lib.cpSlideJointGetMax
cpSlideJointGetMax.restype = cpFloat
cpSlideJointGetMax.argtypes = [POINTER(cpConstraint)]
cpSlideJointSetMax = chipmunk_lib.cpSlideJointSetMax
cpSlideJointSetMax.restype = None
cpSlideJointSetMax.argtypes = [POINTER(cpConstraint), cpFloat]
cpCollisionBeginFunc = function_pointer(cpBool, POINTER(cpArbiter), POINTER(cpSpace), cpDataPointer)
cpCollisionPreSolveFunc = function_pointer(cpBool, POINTER(cpArbiter), POINTER(cpSpace), cpDataPointer)
cpCollisionPostSolveFunc = function_pointer(None, POINTER(cpArbiter), POINTER(cpSpace), cpDataPointer)
cpCollisionSeparateFunc = function_pointer(None, POINTER(cpArbiter), POINTER(cpSpace), cpDataPointer)
cpCollisionHandler._fields_ = [
    ('typeA', cpCollisionType),
    ('typeB', cpCollisionType),
    ('beginFunc', cpCollisionBeginFunc),
    ('preSolveFunc', cpCollisionPreSolveFunc),
    ('postSolveFunc', cpCollisionPostSolveFunc),
    ('separateFunc', cpCollisionSeparateFunc),
    ('userData', cpDataPointer),
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
cpSpaceGetIterations = chipmunk_lib.cpSpaceGetIterations
cpSpaceGetIterations.restype = c_int
cpSpaceGetIterations.argtypes = [POINTER(cpSpace)]
cpSpaceSetIterations = chipmunk_lib.cpSpaceSetIterations
cpSpaceSetIterations.restype = None
cpSpaceSetIterations.argtypes = [POINTER(cpSpace), c_int]
cpSpaceGetGravity = chipmunk_lib.cpSpaceGetGravity
cpSpaceGetGravity.restype = cpVect
cpSpaceGetGravity.argtypes = [POINTER(cpSpace)]
cpSpaceSetGravity = chipmunk_lib.cpSpaceSetGravity
cpSpaceSetGravity.restype = None
cpSpaceSetGravity.argtypes = [POINTER(cpSpace), cpVect]
cpSpaceGetDamping = chipmunk_lib.cpSpaceGetDamping
cpSpaceGetDamping.restype = cpFloat
cpSpaceGetDamping.argtypes = [POINTER(cpSpace)]
cpSpaceSetDamping = chipmunk_lib.cpSpaceSetDamping
cpSpaceSetDamping.restype = None
cpSpaceSetDamping.argtypes = [POINTER(cpSpace), cpFloat]
cpSpaceGetIdleSpeedThreshold = chipmunk_lib.cpSpaceGetIdleSpeedThreshold
cpSpaceGetIdleSpeedThreshold.restype = cpFloat
cpSpaceGetIdleSpeedThreshold.argtypes = [POINTER(cpSpace)]
cpSpaceSetIdleSpeedThreshold = chipmunk_lib.cpSpaceSetIdleSpeedThreshold
cpSpaceSetIdleSpeedThreshold.restype = None
cpSpaceSetIdleSpeedThreshold.argtypes = [POINTER(cpSpace), cpFloat]
cpSpaceGetSleepTimeThreshold = chipmunk_lib.cpSpaceGetSleepTimeThreshold
cpSpaceGetSleepTimeThreshold.restype = cpFloat
cpSpaceGetSleepTimeThreshold.argtypes = [POINTER(cpSpace)]
cpSpaceSetSleepTimeThreshold = chipmunk_lib.cpSpaceSetSleepTimeThreshold
cpSpaceSetSleepTimeThreshold.restype = None
cpSpaceSetSleepTimeThreshold.argtypes = [POINTER(cpSpace), cpFloat]
cpSpaceGetCollisionSlop = chipmunk_lib.cpSpaceGetCollisionSlop
cpSpaceGetCollisionSlop.restype = cpFloat
cpSpaceGetCollisionSlop.argtypes = [POINTER(cpSpace)]
cpSpaceSetCollisionSlop = chipmunk_lib.cpSpaceSetCollisionSlop
cpSpaceSetCollisionSlop.restype = None
cpSpaceSetCollisionSlop.argtypes = [POINTER(cpSpace), cpFloat]
cpSpaceGetCollisionBias = chipmunk_lib.cpSpaceGetCollisionBias
cpSpaceGetCollisionBias.restype = cpFloat
cpSpaceGetCollisionBias.argtypes = [POINTER(cpSpace)]
cpSpaceSetCollisionBias = chipmunk_lib.cpSpaceSetCollisionBias
cpSpaceSetCollisionBias.restype = None
cpSpaceSetCollisionBias.argtypes = [POINTER(cpSpace), cpFloat]
cpSpaceGetCollisionPersistence = chipmunk_lib.cpSpaceGetCollisionPersistence
cpSpaceGetCollisionPersistence.restype = cpTimestamp
cpSpaceGetCollisionPersistence.argtypes = [POINTER(cpSpace)]
cpSpaceSetCollisionPersistence = chipmunk_lib.cpSpaceSetCollisionPersistence
cpSpaceSetCollisionPersistence.restype = None
cpSpaceSetCollisionPersistence.argtypes = [POINTER(cpSpace), cpTimestamp]
cpSpaceGetUserData = chipmunk_lib.cpSpaceGetUserData
cpSpaceGetUserData.restype = cpDataPointer
cpSpaceGetUserData.argtypes = [POINTER(cpSpace)]
cpSpaceSetUserData = chipmunk_lib.cpSpaceSetUserData
cpSpaceSetUserData.restype = None
cpSpaceSetUserData.argtypes = [POINTER(cpSpace), cpDataPointer]
cpSpaceGetStaticBody = chipmunk_lib.cpSpaceGetStaticBody
cpSpaceGetStaticBody.restype = POINTER(cpBody)
cpSpaceGetStaticBody.argtypes = [POINTER(cpSpace)]
cpSpaceGetCurrentTimeStep = chipmunk_lib.cpSpaceGetCurrentTimeStep
cpSpaceGetCurrentTimeStep.restype = cpFloat
cpSpaceGetCurrentTimeStep.argtypes = [POINTER(cpSpace)]
cpSpaceIsLocked = chipmunk_lib.cpSpaceIsLocked
cpSpaceIsLocked.restype = cpBool
cpSpaceIsLocked.argtypes = [POINTER(cpSpace)]
cpSpaceAddDefaultCollisionHandler = chipmunk_lib.cpSpaceAddDefaultCollisionHandler
cpSpaceAddDefaultCollisionHandler.restype = POINTER(cpCollisionHandler)
cpSpaceAddDefaultCollisionHandler.argtypes = [POINTER(cpSpace)]
cpSpaceAddCollisionHandler = chipmunk_lib.cpSpaceAddCollisionHandler
cpSpaceAddCollisionHandler.restype = POINTER(cpCollisionHandler)
cpSpaceAddCollisionHandler.argtypes = [POINTER(cpSpace), cpCollisionType, cpCollisionType]
cpSpaceAddWildcardHandler = chipmunk_lib.cpSpaceAddWildcardHandler
cpSpaceAddWildcardHandler.restype = POINTER(cpCollisionHandler)
cpSpaceAddWildcardHandler.argtypes = [POINTER(cpSpace), cpCollisionType]
cpSpaceAddShape = chipmunk_lib.cpSpaceAddShape
cpSpaceAddShape.restype = POINTER(cpShape)
cpSpaceAddShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddBody = chipmunk_lib.cpSpaceAddBody
cpSpaceAddBody.restype = POINTER(cpBody)
cpSpaceAddBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceAddConstraint = chipmunk_lib.cpSpaceAddConstraint
cpSpaceAddConstraint.restype = POINTER(cpConstraint)
cpSpaceAddConstraint.argtypes = [POINTER(cpSpace), POINTER(cpConstraint)]
cpSpaceRemoveShape = chipmunk_lib.cpSpaceRemoveShape
cpSpaceRemoveShape.restype = None
cpSpaceRemoveShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
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
cpSpaceAddPostStepCallback.restype = cpBool
cpSpaceAddPostStepCallback.argtypes = [POINTER(cpSpace), cpPostStepFunc, c_void_p, c_void_p]
cpSpacePointQueryFunc = function_pointer(None, POINTER(cpShape), cpVect, cpFloat, cpVect, c_void_p)
cpSpacePointQuery = chipmunk_lib.cpSpacePointQuery
cpSpacePointQuery.restype = None
cpSpacePointQuery.argtypes = [POINTER(cpSpace), cpVect, cpFloat, cpShapeFilter, cpSpacePointQueryFunc, c_void_p]
cpSpacePointQueryNearest = chipmunk_lib.cpSpacePointQueryNearest
cpSpacePointQueryNearest.restype = POINTER(cpShape)
cpSpacePointQueryNearest.argtypes = [POINTER(cpSpace), cpVect, cpFloat, cpShapeFilter, POINTER(cpPointQueryInfo)]
cpSpaceSegmentQueryFunc = function_pointer(None, POINTER(cpShape), cpVect, cpVect, cpFloat, c_void_p)
cpSpaceSegmentQuery = chipmunk_lib.cpSpaceSegmentQuery
cpSpaceSegmentQuery.restype = None
cpSpaceSegmentQuery.argtypes = [POINTER(cpSpace), cpVect, cpVect, cpFloat, cpShapeFilter, cpSpaceSegmentQueryFunc, c_void_p]
cpSpaceSegmentQueryFirst = chipmunk_lib.cpSpaceSegmentQueryFirst
cpSpaceSegmentQueryFirst.restype = POINTER(cpShape)
cpSpaceSegmentQueryFirst.argtypes = [POINTER(cpSpace), cpVect, cpVect, cpFloat, cpShapeFilter, POINTER(cpSegmentQueryInfo)]
cpSpaceBBQueryFunc = function_pointer(None, POINTER(cpShape), c_void_p)
cpSpaceBBQuery = chipmunk_lib.cpSpaceBBQuery
cpSpaceBBQuery.restype = None
cpSpaceBBQuery.argtypes = [POINTER(cpSpace), cpBB, cpShapeFilter, cpSpaceBBQueryFunc, c_void_p]
cpSpaceShapeQueryFunc = function_pointer(None, POINTER(cpShape), POINTER(cpContactPointSet), c_void_p)
cpSpaceShapeQuery = chipmunk_lib.cpSpaceShapeQuery
cpSpaceShapeQuery.restype = cpBool
cpSpaceShapeQuery.argtypes = [POINTER(cpSpace), POINTER(cpShape), cpSpaceShapeQueryFunc, c_void_p]
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
class cpSpaceDebugColor(Structure):
    pass
cpSpaceDebugColor._fields_ = [
    ('r', c_float),
    ('g', c_float),
    ('b', c_float),
    ('a', c_float),
]
cpSpaceDebugDrawCircleImpl = function_pointer(None, cpVect, cpFloat, cpFloat, cpSpaceDebugColor, cpSpaceDebugColor, cpDataPointer)
cpSpaceDebugDrawSegmentImpl = function_pointer(None, cpVect, cpVect, cpSpaceDebugColor, cpDataPointer)
cpSpaceDebugDrawFatSegmentImpl = function_pointer(None, cpVect, cpVect, cpFloat, cpSpaceDebugColor, cpSpaceDebugColor, cpDataPointer)
cpSpaceDebugDrawPolygonImpl = function_pointer(None, c_int, POINTER(cpVect), cpFloat, cpSpaceDebugColor, cpSpaceDebugColor, cpDataPointer)
cpSpaceDebugDrawDotImpl = function_pointer(None, cpFloat, cpVect, cpSpaceDebugColor, cpDataPointer)
cpSpaceDebugDrawColorForShapeImpl = function_pointer(cpSpaceDebugColor, POINTER(cpShape), cpDataPointer)

# values for enumeration 'cpSpaceDebugDrawFlags'
CP_SPACE_DEBUG_DRAW_SHAPES = 1
CP_SPACE_DEBUG_DRAW_CONSTRAINTS = 2
CP_SPACE_DEBUG_DRAW_COLLISION_POINTS = 4
cpSpaceDebugDrawFlags = c_int # enum
class cpSpaceDebugDrawOptions(Structure):
    pass
cpSpaceDebugDrawOptions._fields_ = [
    ('drawCircle', cpSpaceDebugDrawCircleImpl),
    ('drawSegment', cpSpaceDebugDrawSegmentImpl),
    ('drawFatSegment', cpSpaceDebugDrawFatSegmentImpl),
    ('drawPolygon', cpSpaceDebugDrawPolygonImpl),
    ('drawDot', cpSpaceDebugDrawDotImpl),
    ('flags', cpSpaceDebugDrawFlags),
    ('shapeOutlineColor', cpSpaceDebugColor),
    ('colorForShape', cpSpaceDebugDrawColorForShapeImpl),
    ('constraintColor', cpSpaceDebugColor),
    ('collisionPointColor', cpSpaceDebugColor),
    ('data', cpDataPointer),
]
cpSpaceDebugDraw = chipmunk_lib.cpSpaceDebugDraw
cpSpaceDebugDraw.restype = None
cpSpaceDebugDraw.argtypes = [POINTER(cpSpace), POINTER(cpSpaceDebugDrawOptions)]
cpSpatialIndexBBFunc = function_pointer(cpBB, c_void_p)
cpSpatialIndexIteratorFunc = function_pointer(None, c_void_p, c_void_p)
cpSpatialIndexQueryFunc = function_pointer(cpCollisionID, c_void_p, c_void_p, cpCollisionID, c_void_p)
cpSpatialIndexSegmentQueryFunc = function_pointer(cpFloat, c_void_p, c_void_p, c_void_p)
class cpSpatialIndexClass(Structure):
    pass
class cpSpatialIndex(Structure):
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
cpTrue = 1 # Variable c_int '1'
cpFalse = 0 # Variable c_int '0'
__all__ = ['cpDampedRotarySpringSetRestAngle',
           'cpArbiterIsFirstContact', 'cpBodyEachShape',
           'CP_BODY_TYPE_STATIC', 'cpBodyType',
           'cpArbiterCallWildcardPreSolveA',
           'cpArbiterCallWildcardPreSolveB', 'cpContactPointSet',
           'cpBodyGetMoment',
           'cpDampedRotarySpringGetSpringTorqueFunc',
           'cpPinJointSetAnchorB', 'cpPinJointSetAnchorA',
           'cpSpacePointQueryFunc', 'cpConstraintGetMaxBias',
           'cpSpaceDebugDrawOptions', 'cpSpaceGetCurrentTimeStep',
           'cpConstraintGetMaxForce', 'cpBodyKineticEnergy', 'cpBody',
           'cpPivotJointGetAnchorB', 'cpBodySetMass',
           'cpPivotJointGetAnchorA', 'cpArbiterSetContactPointSet',
           'cpCircleShapeSetOffset', 'cpVect',
           'cpConstraintIsGearJoint', 'cpPivotJointNew2',
           'cpSpatialIndexQueryFunc', 'cpSpaceDebugDrawFlags',
           'cpArbiterGetDepth', 'cpRatchetJointInit',
           'cpSpaceGetStaticBody', 'cpcalloc', 'cpPinJointAlloc',
           'cpBodyUpdatePosition', 'cpShapeSetDensity',
           'cpSpaceDestroy', 'cpAreaForCircle',
           'cpBodyShapeIteratorFunc', 'cpSlideJointAlloc',
           'cpBodyActivateStatic', 'cpGrooveJoint',
           'cpPinJointGetDist', 'cpShapeGetUserData',
           'cpRotaryLimitJointSetMin', 'cpPivotJointNew',
           'cpShapeSetCollisionType', 'cpConstraintPreSolveFunc',
           'cpCentroidForPoly', 'cpBoxShapeNew', 'cpBBTree',
           'cpCollisionType', 'cpConstraintGetImpulse',
           'cpSpaceAddBody', 'cpSpatialIndexInsertImpl',
           'cpConstraintSetMaxForce', 'cpFalse', 'realloc',
           'cpDampedRotarySpringGetRestAngle', 'cpBodySetForce',
           'cpRatchetJointGetRatchet', 'cpSpatialIndexCountImpl',
           'cpCollisionSeparateFunc', 'cpBoxShapeNew2',
           'cpBodyArbiterIteratorFunc', 'cpSpatialIndexQueryImpl',
           'cpSpaceHashResize', 'cpShapeGetCenterOfGravity',
           'cpSpaceGetGravity', 'cpAreaForSegment',
           'cpSpatialIndexCollideStatic', 'cpCollisionPostSolveFunc',
           'cpShapeGetArea', 'cpSpatialIndexContainsImpl', 'cpMat2x2',
           'cpDampedSpringAlloc', 'cpRotaryLimitJointAlloc',
           'cpSpaceDebugDrawDotImpl', 'cpShapeCacheBB',
           'cpSpaceBodyIteratorFunc',
           'cpSpatialIndexSegmentQueryFunc', 'cpMomentForCircle',
           'cpSimpleMotorJoint', 'cpSpaceRemoveConstraint',
           'cpDampedSpringGetRestLength', 'cpSpatialIndex',
           'cpDampedSpringSetSpringForceFunc',
           'cpSpaceDebugDrawSegmentImpl',
           'cpDampedSpringGetStiffness', 'cpConstraintFree',
           'cpArbiterGetPointA', 'cpArbiterGetPointB',
           'cpConstraintGetSpace', 'cpGrooveJointSetGrooveA',
           'cpGrooveJointSetGrooveB', 'cpSpaceGetIdleSpeedThreshold',
           'cpPolyShape', 'cpDampedRotarySpringSetStiffness',
           'cpRotaryLimitJointGetMin', 'cpRatchetJointAlloc',
           'cpConstraintPostSolveFunc', 'cpMomentForSegment',
           'cpShapeGetFriction', 'cpBBTreeNew', 'cpPivotJointAlloc',
           'cpSlideJointGetAnchorB', 'cpSlideJointGetAnchorA',
           'cpTrue', 'cpSegmentShapeInit', 'cpSimpleMotor',
           'cpSpaceContainsConstraint', 'cpSpaceAddConstraint',
           'cpSlideJointInit', 'cpArbiterSetUserData',
           'cpSpaceGetDamping', 'cpBodySetPositionUpdateFunc',
           'cpShapeGetCollisionType', 'cpBodyActivate',
           'cpConstraintIsDampedSpring', 'cpBodySetType',
           'cpShapeSetSensor', 'cpBodyGetCenterOfGravity', 'cpfree',
           'cpBodyGetAngle', 'cpBodySetVelocityUpdateFunc',
           'cpConstraintSetUserData', 'size_t', 'cpSlideJointGetMin',
           'cpSpaceShapeIteratorFunc', 'cpSpaceSetCollisionSlop',
           'cpShapeGetMass', 'cpSpaceReindexStatic',
           'cpBodyGetTorque', 'cpBodySetTorque', 'cpShapeFilter',
           'cpBodyWorldToLocal', 'cpArray',
           'cpSpatialIndexIteratorFunc', 'cpPolyShapeAlloc',
           'cpDampedSpringInit', 'cpBBTreeVelocityFunc',
           'cpSegmentQueryInfo', 'cpMomentForBox',
           'cpConstraintIsPivotJoint', 'cpArbiterGetUserData',
           'cpArbiterSetFriction', 'cpSpaceHashNew', 'cpConvexHull',
           'cpArbiterCallWildcardBeginA',
           'cpArbiterCallWildcardBeginB', 'cpBodyEachConstraint',
           'cpBodyApplyForceAtLocalPoint', 'cpShapeUpdate',
           'cpGearJointGetPhase', 'cpBodyApplyImpulseAtWorldPoint',
           'cpShapeSetUserData', 'cpSlideJoint',
           'cpBodyUpdateVelocity', 'cpSpatialIndexReindexQueryImpl',
           'cpBodySetVelocity', 'cpSpaceNew', 'cpSpaceInit',
           'cpConstraintGetUserData', 'cpPointQueryInfo',
           'cpShapeGetSurfaceVelocity', 'cpCircleShapeSetRadius',
           'cpBodyFree', 'free', 'cpPivotJointInit',
           'cpBBTreeSetVelocityFunc', 'CP_BODY_TYPE_KINEMATIC',
           'cpBodyGetVelocity', 'cpBodySetMoment',
           'cpSlideJointSetMin', 'cpSpaceSetSleepTimeThreshold',
           'cpSpaceDebugDrawFatSegmentImpl', 'cpShape', 'cpSpaceHash',
           'cpPinJoint', 'cpArbiterTotalKE',
           'cpArbiterCallWildcardPostSolveA',
           'cpArbiterCallWildcardPostSolveB', 'cpBodySleepWithGroup',
           'cpMomentForBox2', 'cpConstraintIsSimpleMotor',
           'cpPolyShapeGetVert', 'cpShapeSetElasticity',
           'cpGearJoint', 'cpArbiterGetShapes',
           'cpBodyGetVelocityAtWorldPoint', 'cpSpaceAddShape',
           'cpSimpleMotorGetRate', 'cpConstraintGetErrorBias',
           'cpDampedSpringSetStiffness', 'cpConstraintDestroy',
           'cpBodyConstraintIteratorFunc', 'cpShapeGetSpace',
           'cpBodyEachArbiter', 'cpSegmentShapeGetRadius',
           'cpGearJointSetRatio', 'cpSpaceGetCollisionBias',
           'cpConstraintSetCollideBodies', 'cpSweep1DInit',
           'cpRotaryLimitJointNew', 'cpDampedSpringGetAnchorB',
           'cpBodyIsSleeping', 'cpHashSet',
           'cpDampedSpringGetAnchorA', 'cpSpaceAddWildcardHandler',
           'cpGrooveJointGetGrooveA', 'cpGrooveJointGetGrooveB',
           'cpPinJointNew', 'CP_SPACE_DEBUG_DRAW_CONSTRAINTS',
           'cpSpaceEachConstraint', 'cpConstraintIsRotaryLimitJoint',
           'cpBoxShapeInit', 'cpSpaceEachShape', 'cpGearJointNew',
           'cprealloc', 'cpSpatialIndexBBFunc', 'cpSegmentShapeAlloc',
           'cpArbiterCallWildcardSeparateA',
           'cpArbiterCallWildcardSeparateB', 'cpPolyShapeSetVerts',
           'cpBB', 'cpBodyGetType', 'cpSegmentShapeGetNormal',
           'cpShapeDestroy', 'cpBodyPositionFunc',
           'cpSpaceGetUserData', 'cpGrooveJointNew',
           'cpSpaceSegmentQueryFunc', 'cpConstraintIsGrooveJoint',
           'cpConstraintSetPostSolveFunc',
           'cpDampedRotarySpringSetSpringTorqueFunc',
           'cpSlideJointGetMax', 'cpDampedRotarySpringAlloc',
           'cpRotaryLimitJoint', 'cpSpatialIndexSegmentQueryImpl',
           'cpRatchetJointSetAngle', 'cpDampedSpringNew',
           'cpSpaceBBQueryFunc', 'cpRatchetJointGetPhase',
           'cpSpaceSegmentQueryFirst', 'cpCircleShapeGetOffset',
           'cpGearJointInit', 'cpGrooveJointInit',
           'cpSpaceUseSpatialHash', 'cpPolyShapeSetRadius',
           'cpShapeSetFriction', 'cpMomentForPoly', 'cpBodyDestroy',
           'cpDataPointer', 'cpPivotJoint',
           'cpDampedRotarySpringSetDamping', 'cpSpatialIndexEachImpl',
           'cpArbiterIsRemoval', 'cpSpaceContainsShape',
           'cpSpaceHashInit', 'cpSpaceGetCollisionSlop',
           'cpSpaceReindexShape', 'cpPolyShapeInit',
           'cpSpatialIndexReindexImpl', 'cpShapeSegmentQuery',
           'cpSpaceAddDefaultCollisionHandler', 'cpSpaceAlloc',
           'cpCollisionPreSolveFunc', 'cpSpaceDebugDrawCircleImpl',
           'cpShapeSetFilter', 'cpSpaceSetDamping',
           'cpBodyApplyImpulseAtLocalPoint', 'cpArbiterGetNormal',
           'cpSweep1D', 'CP_SPACE_DEBUG_DRAW_COLLISION_POINTS',
           'cpCircleShape', 'cpBool', 'cpCollisionBeginFunc',
           'cpConstraintGetCollideBodies', 'cpSimpleMotorSetRate',
           'cpPostStepFunc', 'cpArbiterGetContactPointSet',
           'cpBodyNewKinematic', 'cpSlideJointSetMax',
           'cpBBTreeAlloc', 'cpConstraintGetBodyA',
           'cpConstraintGetBodyB', 'cpShapeGetSensor',
           'cpArbiterSetRestitution', 'cpSpaceRemoveBody',
           'cpSegmentShapeSetRadius', 'cpPivotJointSetAnchorB',
           'cpPivotJointSetAnchorA', 'cpBodySetCenterOfGravity',
           'cpConstraintIsPinJoint', 'cpSpaceRemoveShape',
           'cpBodySleep', 'cpSweep1DAlloc',
           'cpDampedRotarySpringTorqueFunc', 'cpSegmentShapeGetA',
           'cpSegmentShapeGetB', 'cpShapesCollide',
           'cpDampedSpringSetAnchorA', 'cpPinJointGetAnchorB',
           'cpPinJointGetAnchorA', 'cpShapeGetElasticity',
           'cpShapeSetBody', 'cpBodyApplyForceAtWorldPoint',
           'cpHashValue', 'cpSimpleMotorNew', 'cpSimpleMotorAlloc',
           'cpSpaceShapeQueryFunc', 'cpSpatialIndexDestroyImpl',
           'cpGroup', 'cpSpatialIndexReindexObjectImpl',
           'cpRotaryLimitJointInit', 'cpPolyShapeSetVertsRaw',
           'cpBodyNewStatic', 'cpConstraintSetPreSolveFunc',
           'cpPolyShapeGetRadius', 'cpArbiterGetFriction',
           'cpDampedRotarySpringGetStiffness', 'cpSlideJointNew',
           'cpDampedRotarySpringGetDamping', 'cpBodyGetRotation',
           'cpBodyGetVelocityAtLocalPoint',
           'cpSpaceGetCollisionPersistence',
           'cpSpaceAddCollisionHandler', 'CP_BODY_TYPE_DYNAMIC',
           'cpSpaceSetIdleSpeedThreshold', 'cpShapeGetBB',
           'cpRatchetJointNew', 'cpSpaceIsLocked',
           'cpSpaceSetGravity', 'cpDampedRotarySpringNew',
           'cpDampedRotarySpring', 'calloc',
           'cpSegmentShapeSetEndpoints', 'cpGrooveJointGetAnchorB',
           'cpSpaceGetSleepTimeThreshold', 'cpSpatialIndexRemoveImpl',
           'cpRatchetJointGetAngle', 'cpSpaceStep',
           'cpSimpleMotorInit', 'cpSweep1DNew', 'uint32_t',
           'cpConstraintSetMaxBias', 'cpSpacePointQuery',
           'cpCollisionHandler', 'cpPolyShapeGetCount',
           'cpBoxShapeInit2', 'cpBBTreeOptimize', 'cpDampedSpring',
           'cpBodySetAngle', 'cpSpaceSetIterations',
           'cpConstraintIsSlideJoint', 'cpSpaceReindexShapesForBody',
           'cpGrooveJointAlloc', 'cpBodyVelocityFunc',
           'cpSpaceShapeQuery', 'cpBodyGetUserData', 'cpTransform',
           'cpSpaceContainsBody', 'cpBodySetAngularVelocity',
           'cpSpace', 'cpShapeGetDensity', 'cpBodyAlloc',
           'cpSpaceHashAlloc', 'cpRatchetJointSetRatchet',
           'cpConstraintGetPreSolveFunc',
           'cpDampedSpringSetRestLength', 'cpDampedSpringForceFunc',
           'cpBodyLocalToWorld', 'cpSegmentShapeNew', 'cpBitmask',
           'cpArbiterIgnore', 'cpBodyGetMass', 'cpSpatialIndexClass',
           'cpCircleShapeAlloc', 'cpSegmentShape', 'cpConstraint',
           'cpArbiter', 'cpDampedSpringGetDamping', 'cpSpaceFree',
           'cpCircleShapeNew', 'cpDampedSpringSetDamping',
           'cpDampedSpringSetAnchorB', 'cpShapeSetMass',
           'cpArbiterGetCount', 'cpPolyShapeInitRaw',
           'cpGearJointAlloc', 'cpRotaryLimitJointSetMax',
           'cpGearJointSetPhase', 'cpSpaceDebugDrawPolygonImpl',
           'cpPolyShapeNew', 'cpConstraintIsDampedRotarySpring',
           'cpSpatialIndexFree', 'cpVersionString',
           'cpSpaceAddPostStepCallback', 'cpSpaceSetCollisionBias',
           'cpBodySetPosition', 'cpShapeFree',
           'cpConstraintSetErrorBias',
           'cpSpaceDebugDrawColorForShapeImpl',
           'cpSpaceConstraintIteratorFunc',
           'cpConstraintIsRatchetJoint', 'cpCircleShapeGetRadius',
           'cpSpaceGetIterations', 'cpPinJointInit',
           'cpSpacePointQueryNearest', 'cpSpaceSetUserData',
           'uintptr_t', 'cpShapePointQuery', 'cpSpaceEachBody',
           'cpBodyGetSpace', 'N17cpContactPointSet4DOT_25E',
           'cpBBTreeInit', 'cpTimestamp', 'cpShapeGetBody',
           'cpSegmentShapeSetNeighbors', 'CP_SPACE_DEBUG_DRAW_SHAPES',
           'cpSlideJointSetAnchorB', 'cpSlideJointSetAnchorA',
           'cpMessage', 'cpCollisionID', 'cpShapeGetFilter',
           'cpBodyNew', 'cpFloat', 'cpBodyGetForce',
           'cpSpaceSetCollisionPersistence', 'cpSpaceBBQuery',
           'cpBodyGetPosition', 'cpBodyGetAngularVelocity',
           'cpBodySetUserData', 'cpGrooveJointSetAnchorB',
           'cpShapeSetSurfaceVelocity', 'cpRatchetJointSetPhase',
           'cpArbiterTotalImpulse', 'cpPinJointSetDist',
           'cpSpaceDebugDraw', 'cpAreaForPoly',
           'cpArbiterSetSurfaceVelocity', 'cpDampedRotarySpringInit',
           'cpSpaceSegmentQuery', 'cpCircleShapeInit',
           'cpRatchetJoint', 'cpRotaryLimitJointGetMax',
           'cpShapeGetMoment', 'cpGearJointGetRatio', 'cpBodyInit',
           'cpDampedSpringGetSpringForceFunc',
           'cpArbiterGetSurfaceVelocity', 'cpSpaceDebugColor',
           'cpArbiterGetRestitution', 'cpConstraintGetPostSolveFunc',
           'cpArbiterGetBodies']
