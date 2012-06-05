
from ctypes import * 
from .vec2d import Vec2d
cpVect = Vec2d
STRING = c_char_p

from .libload import load_library, platform_specific_functions
_lib_debug = True #Set to True to print the Chipmunk path.
chipmunk_lib = load_library("chipmunk", debug_lib=_lib_debug)
function_pointer = platform_specific_functions()['function_pointer']


STRING = c_char_p
WSTRING = c_wchar_p


def __va_arg_pack_len(): return __builtin_va_arg_pack_len () # macro
def FD_ZERO(fdsetp): return __FD_ZERO (fdsetp) # macro
# def CP_DefineSpaceStructGetter(type,member,name): return static inline type cpSpaceGet ##name(const cpSpace *space){return space->member;} # macro
def __GNUC_PREREQ(maj,min): return ((__GNUC__ << 16) + __GNUC_MINOR__ >= ((maj) << 16) + (min)) # macro
# def __LDBL_REDIR1_NTH(name,proto,alias): return name proto __THROW # macro
def FD_CLR(fd,fdsetp): return __FD_CLR (fd, fdsetp) # macro
# def __bswap_16(x): return (__extension__ ({ register unsigned short int __v, __x = (x); if (__builtin_constant_p (__x)) __v = __bswap_constant_16 (__x); else __asm__ ("rorw $8, %w0" : "=r" (__v) : "0" (__x) : "cc"); __v; })) # macro
# __WCHAR_MAX = __WCHAR_MAX__ # alias
# def __REDIRECT(name,proto,alias): return name proto __asm__ (__ASMNAME (#alias)) # macro
# __TIME_T_TYPE = __SLONGWORD_TYPE # alias
# __RLIM_T_TYPE = __ULONGWORD_TYPE # alias
def be32toh(x): return __bswap_32 (x) # macro
__quad_t = c_longlong
__SQUAD_TYPE = __quad_t # alias
# def __warndecl(name,msg): return extern void name (void) __attribute__((__warning__ (msg))) # macro
CP_SEGMENT_SHAPE = 1
def __CONCAT(x,y): return x ## y # macro
# __SWORD_TYPE = int # alias
# __SSIZE_T_TYPE = __SWORD_TYPE # alias
__u_quad_t = c_ulonglong
__UQUAD_TYPE = __u_quad_t # alias
__INO64_T_TYPE = __UQUAD_TYPE # alias
# __S32_TYPE = int # alias
# __PID_T_TYPE = __S32_TYPE # alias
# def __intN_t(N,MODE): return typedef int int ##N ##_t __attribute__ ((__mode__ (MODE))) # macro
# def __FDMASK(d): return ((__fd_mask) 1 << ((d) % __NFDBITS)) # macro
def __LONG_LONG_PAIR(HI,LO): return LO, HI # macro
def le16toh(x): return (x) # macro
# NULL = __null # alias
def WIFSIGNALED(status): return __WIFSIGNALED(__WAIT_INT(status)) # macro
# def cpConstraintCheckCast(constraint,struct): return cpAssertHard(constraint->CP_PRIVATE(klass) == struct ##GetClass(), "Constraint is not a "#struct) # macro
def FD_ISSET(fd,fdsetp): return __FD_ISSET (fd, fdsetp) # macro
__RLIM64_T_TYPE = __UQUAD_TYPE # alias
# __INO_T_TYPE = __ULONGWORD_TYPE # alias
# def CP_DefineArbiterStructSetter(type,member,name): return static inline void cpArbiterSet ##name(cpArbiter *arb, type value){arb->member = value;} # macro
# def __bswap_64(x): return (__extension__ ({ union { __extension__ unsigned long long int __ll; unsigned int __l[2]; } __w, __r; if (__builtin_constant_p (x)) __r.__ll = __bswap_constant_64 (x); else { __w.__ll = (x); __r.__l[0] = __bswap_32 (__w.__l[1]); __r.__l[1] = __bswap_32 (__w.__l[0]); } __r.__ll; })) # macro
_XOPEN_ = 1
__BIG_ENDIAN = 4321 # Variable c_int '4321'
BIG_ENDIAN = __BIG_ENDIAN # alias
# cpfatan2 = atan2 # alias
def __PMT(args): return args # macro
# def fpclassify(x): return (sizeof (x) == sizeof (float) ? __fpclassifyf (x) : sizeof (x) == sizeof (double) ? __fpclassify (x) : __fpclassifyl (x)) # macro
# cpfexp = exp # alias
def __WEXITSTATUS(status): return (((status) & 0xff00) >> 8) # macro
# def __LDBL_REDIR(name,proto): return name proto # macro
# cpfpow = pow # alias
def FD_SET(fd,fdsetp): return __FD_SET (fd, fdsetp) # macro
# __NLINK_T_TYPE = __UWORD_TYPE # alias
# def __FD_ISSET(fd,fdsp): return (__extension__ ({register char __result; __asm__ __volatile__ (__FD_ISSET_BT " %1,%2 ; setcb %b0" : "=q" (__result) : "r" (((int) (fd)) % __NFDBITS), "m" (__FDS_BITS (fdsp)[__FDELT (fd)]) : "cc"); __result; })) # macro
# __BLKCNT_T_TYPE = __SLONGWORD_TYPE # alias
def be64toh(x): return __bswap_64 (x) # macro
__LITTLE_ENDIAN = 1234 # Variable c_int '1234'
__BYTE_ORDER = __LITTLE_ENDIAN # alias
BYTE_ORDER = __BYTE_ORDER # alias
# def __LDBL_REDIR_NTH(name,proto): return name proto __THROW # macro
FP_NAN = 0
FP_NAN = FP_NAN # alias
# def __WIFSIGNALED(status): return (((signed char) (((status) & 0x7f) + 1) >> 1) > 0) # macro
_IEEE_ = -1
# def CP_DefineBodyStructSetter(type,member,name): return static inline void cpBodySet ##name(cpBody *body, const type value){ cpBodyActivate(body); cpBodyAssertSane(body); body->member = value; } # macro
def __W_STOPCODE(sig): return ((sig) << 8 | 0x7f) # macro
def __REDIRECT_LDBL(name,proto,alias): return __REDIRECT (name, proto, alias) # macro
# def __FD_ZERO(fdsp): return do { int __d0, __d1; __asm__ __volatile__ ("cld; rep; " __FD_ZERO_STOS : "=c" (__d0), "=D" (__d1) : "a" (0), "0" (sizeof (fd_set) / sizeof (__fd_mask)), "1" (&__FDS_BITS (fdsp)[0]) : "memory"); } while (0) # macro
# def CP_DefineArbiterStructProperty(type,member,name): return CP_DefineArbiterStructGetter(type, member, name) CP_DefineArbiterStructSetter(type, member, name) # macro
def major(dev): return gnu_dev_major (dev) # macro
# def CP_DefineSpaceStructProperty(type,member,name): return CP_DefineSpaceStructGetter(type, member, name) CP_DefineSpaceStructSetter(type, member, name) # macro
__PDP_ENDIAN = 3412 # Variable c_int '3412'
PDP_ENDIAN = __PDP_ENDIAN # alias
cpArbiterStateIgnore = 2
def __bos0(ptr): return __builtin_object_size (ptr, 0) # macro
FP_INFINITE = 1
FP_INFINITE = FP_INFINITE # alias
def __WCOREDUMP(status): return ((status) & __WCOREFLAG) # macro
# def cpAssertWarn(condition,...): return if(!(condition)) cpMessage(#condition, __FILE__, __LINE__, 0, 0, __VA_ARGS__) # macro
def isgreater(x,y): return __builtin_isgreater(x, y) # macro
# __ID_T_TYPE = __U32_TYPE # alias
def __ASMNAME(cname): return __ASMNAME2 (__USER_LABEL_PREFIX__, cname) # macro
# def CP_DefineConstraintGetter(struct,type,member,name): return static inline type struct ##Get ##name(const cpConstraint *constraint){ cpConstraintCheckCast(constraint, struct); return ((struct *)constraint)->member; } # macro
def __bswap_constant_16(x): return ((((x) >> 8) & 0xff) | (((x) & 0xff) << 8)) # macro
def __bswap_constant_32(x): return ((((x) & 0xff000000) >> 24) | (((x) & 0x00ff0000) >> 8) | (((x) & 0x0000ff00) << 8) | (((x) & 0x000000ff) << 24)) # macro
cpArbiterStateNormal = 1
# def isinf(x): return (sizeof (x) == sizeof (float) ? __isinff (x) : sizeof (x) == sizeof (double) ? __isinf (x) : __isinfl (x)) # macro
__DEV_T_TYPE = __UQUAD_TYPE # alias
def islessgreater(x,y): return __builtin_islessgreater(x, y) # macro
CP_POLY_SHAPE = 2
def __WIFSTOPPED(status): return (((status) & 0xff) == 0x7f) # macro
# cpfmod = fmod # alias
# def CP_DefineArbiterStructGetter(type,member,name): return static inline type cpArbiterGet ##name(const cpArbiter *arb){return arb->member;} # macro
__S64_TYPE = __quad_t # alias
def be16toh(x): return __bswap_16 (x) # macro
cpArbiterStateCached = 3
def alloca(size): return __builtin_alloca (size) # macro
# def __MATHDECLX(type,function,suffix,args,attrib): return __MATHDECL_1(type, function,suffix, args) __attribute__ (attrib); __MATHDECL_1(type, __CONCAT(__,function),suffix, args) __attribute__ (attrib) # macro
__OFF64_T_TYPE = __SQUAD_TYPE # alias
__FD_SETSIZE = 1024 # Variable c_int '1024'
FD_SETSIZE = __FD_SETSIZE # alias
# def CP_DefineConstraintProperty(struct,type,member,name): return CP_DefineConstraintGetter(struct, type, member, name) CP_DefineConstraintSetter(struct, type, member, name) # macro
# cpfceil = ceil # alias
def __P(args): return args # macro
def cpBodyAssertSane(body): return cpBodySanityCheck(body) # macro
def htole16(x): return (x) # macro
# __KEY_T_TYPE = __S32_TYPE # alias
# __USECONDS_T_TYPE = __U32_TYPE # alias
def WIFSTOPPED(status): return __WIFSTOPPED(__WAIT_INT(status)) # macro
# __FSFILCNT_T_TYPE = __ULONGWORD_TYPE # alias
def __FDELT(d): return ((d) / __NFDBITS) # macro
# __DADDR_T_TYPE = __S32_TYPE # alias
def makedev(maj,min): return gnu_dev_makedev (maj, min) # macro
# def __errordecl(name,msg): return extern void name (void) __attribute__((__error__ (msg))) # macro
def CP_PRIVATE(symbol): return symbol ##_private # macro
FP_ZERO = 2
FP_ZERO = FP_ZERO # alias
def __attribute_format_arg__(x): return __attribute__ ((__format_arg__ (x))) # macro
def __W_EXITCODE(ret,sig): return ((ret) << 8 | (sig)) # macro
def __va_arg_pack(): return __builtin_va_arg_pack () # macro
size_t = c_uint
calloc = chipmunk_lib.calloc
calloc.restype = c_void_p
calloc.argtypes = [size_t, size_t]
cpcalloc = calloc # alias
FP_NORMAL = 4
# __MODE_T_TYPE = __U32_TYPE # alias
def isgreaterequal(x,y): return __builtin_isgreaterequal(x, y) # macro
# def CP_DefineBodyStructProperty(type,member,name): return CP_DefineBodyStructGetter(type, member, name) CP_DefineBodyStructSetter(type, member, name) # macro
CP_NUM_SHAPES = 3
# def CP_DefineSpaceStructSetter(type,member,name): return static inline void cpSpaceSet ##name(cpSpace *space, type value){space->member = value;} # macro
# def CP_DefineConstraintStructProperty(type,member,name): return CP_DefineConstraintStructGetter(type, member, name) CP_DefineConstraintStructSetter(type, member, name) # macro
# def __bswap_32(x): return (__extension__ ({ register unsigned int __v, __x = (x); if (__builtin_constant_p (__x)) __v = __bswap_constant_32 (__x); else __asm__ ("bswap %0" : "=r" (__v) : "0" (__x)); __v; })) # macro
# def CP_DefineShapeStructSetter(type,member,name,activates): return static inline void cpShapeSet ##name(cpShape *shape, type value){ if(activates && shape->body) cpBodyActivate(shape->body); shape->member = value; } # macro
# __CLOCK_T_TYPE = __SLONGWORD_TYPE # alias
# def CP_DeclareShapeGetter(struct,type,name): return type struct ##Get ##name(const cpShape *shape) # macro
def __warnattr(msg): return __attribute__((__warning__ (msg))) # macro
def __WTERMSIG(status): return ((status) & 0x7f) # macro
def WIFEXITED(status): return __WIFEXITED(__WAIT_INT(status)) # macro
# def __WAIT_INT(status): return (*(int *) &(status)) # macro
# def CP_CONVEX_HULL(__count__,__verts__,__count_var__,__verts_var__): return cpVect *__verts_var__ = (cpVect *)alloca(__count__*sizeof(cpVect)); int __count_var__ = cpConvexHull(__count__, __verts__, __verts_var__, NULL, 0.0); # macro
# cpfsin = sin # alias
# def __LDBL_REDIR1(name,proto,alias): return name proto # macro
def htobe16(x): return __bswap_16 (x) # macro
LITTLE_ENDIAN = __LITTLE_ENDIAN # alias
def le64toh(x): return (x) # macro
def isless(x,y): return __builtin_isless(x, y) # macro
# def CP_DefineShapeStructGetter(type,member,name): return static inline type cpShapeGet ##name(const cpShape *shape){return shape->member;} # macro
FP_SUBNORMAL = 3
def islessequal(x,y): return __builtin_islessequal(x, y) # macro
# def __FD_CLR(fd,fdsp): return __asm__ __volatile__ (__FD_CLR_BTR " %1,%0" : "=m" (__FDS_BITS (fdsp)[__FDELT (fd)]) : "r" (((int) (fd)) % __NFDBITS) : "cc","memory") # macro
__U64_TYPE = __u_quad_t # alias
# def CP_DefineShapeStructProperty(type,member,name,activates): return CP_DefineShapeStructGetter(type, member, name) CP_DefineShapeStructSetter(type, member, name, activates) # macro
# cpfcos = cos # alias
# def __REDIRECT_NTH(name,proto,alias): return name proto __THROW __asm__ (__ASMNAME (#alias)) # macro
def WEXITSTATUS(status): return __WEXITSTATUS(__WAIT_INT(status)) # macro
# def cpAssertHard(condition,...): return if(!(condition)) cpMessage(#condition, __FILE__, __LINE__, 1, 1, __VA_ARGS__) # macro
def WTERMSIG(status): return __WTERMSIG(__WAIT_INT(status)) # macro
__NFDBITS = 32L # Variable c_uint '32u'
NFDBITS = __NFDBITS # alias
def WSTOPSIG(status): return __WSTOPSIG(__WAIT_INT(status)) # macro
_SVID_ = 0
def le32toh(x): return (x) # macro
__FSBLKCNT64_T_TYPE = __UQUAD_TYPE # alias
# def CP_DefineConstraintStructGetter(type,member,name): return static inline type cpConstraint ##Get ##name(const cpConstraint *constraint){return constraint->member;} # macro
realloc = chipmunk_lib.realloc
realloc.restype = c_void_p
realloc.argtypes = [c_void_p, size_t]
cprealloc = realloc # alias
__BLKCNT64_T_TYPE = __SQUAD_TYPE # alias
# def __nonnull(params): return __attribute__ ((__nonnull__ params)) # macro
def isunordered(u,v): return __builtin_isunordered(u, v) # macro
FP_NORMAL = FP_NORMAL # alias
# cpffloor = floor # alias
def __WSTOPSIG(status): return __WEXITSTATUS(status) # macro
def isnormal(x): return (fpclassify (x) == FP_NORMAL) # macro
_POSIX_ = 2
def __attribute_format_strfmon__(a,b): return __attribute__ ((__format__ (__strfmon__, a, b))) # macro
# def CP_DefineConstraintSetter(struct,type,member,name): return static inline void struct ##Set ##name(cpConstraint *constraint, type value){ cpConstraintCheckCast(constraint, struct); cpConstraintActivateBodies(constraint); ((struct *)constraint)->member = value; } # macro
# def __FD_SET(fd,fdsp): return __asm__ __volatile__ (__FD_SET_BTS " %1,%0" : "=m" (__FDS_BITS (fdsp)[__FDELT (fd)]) : "r" (((int) (fd)) % __NFDBITS) : "cc","memory") # macro
# _Mfloat_ = float # alias
def __WIFEXITED(status): return (__WTERMSIG(status) == 0) # macro
__FSFILCNT64_T_TYPE = __UQUAD_TYPE # alias
# def cpAssertSoft(condition,...): return if(!(condition)) cpMessage(#condition, __FILE__, __LINE__, 1, 0, __VA_ARGS__) # macro
def __STRING(x): return #x # macro
# def __FDS_BITS(set): return ((set)->fds_bits) # macro
free = chipmunk_lib.free
free.restype = None
free.argtypes = [c_void_p]
cpfree = free # alias
def __GLIBC_PREREQ(maj,min): return ((__GLIBC__ << 16) + __GLIBC_MINOR__ >= ((maj) << 16) + (min)) # macro
def htobe32(x): return __bswap_32 (x) # macro
FP_SUBNORMAL = FP_SUBNORMAL # alias
CP_CIRCLE_SHAPE = 0
# __BLKSIZE_T_TYPE = __SLONGWORD_TYPE # alias
# def CP_DefineConstraintStructSetter(type,member,name): return static inline void cpConstraint ##Set ##name(cpConstraint *constraint, type value){ cpConstraintActivateBodies(constraint); constraint->member = value; } # macro
_ISOC_ = 3
# def isnan(x): return (sizeof (x) == sizeof (float) ? __isnanf (x) : sizeof (x) == sizeof (double) ? __isnan (x) : __isnanl (x)) # macro
# def CP_ARBITER_GET_BODIES(arb,a,b): return cpBody *a, *b; cpArbiterGetBodies(arb, &a, &b); # macro
def __REDIRECT_NTH_LDBL(name,proto,alias): return __REDIRECT_NTH (name, proto, alias) # macro
# def isfinite(x): return (sizeof (x) == sizeof (float) ? __finitef (x) : sizeof (x) == sizeof (double) ? __finite (x) : __finitel (x)) # macro
# def signbit(x): return (sizeof (x) == sizeof (float) ? __signbitf (x) : sizeof (x) == sizeof (double) ? __signbit (x) : __signbitl (x)) # macro
def __WIFCONTINUED(status): return ((status) == __W_CONTINUED) # macro
# __FSBLKCNT_T_TYPE = __ULONGWORD_TYPE # alias
def WIFCONTINUED(status): return __WIFCONTINUED(__WAIT_INT(status)) # macro
# __SUSECONDS_T_TYPE = __SLONGWORD_TYPE # alias
# __CLOCKID_T_TYPE = __S32_TYPE # alias
def htole64(x): return (x) # macro
# def __bswap_constant_64(x): return ((((x) & 0xff00000000000000ull) >> 56) | (((x) & 0x00ff000000000000ull) >> 40) | (((x) & 0x0000ff0000000000ull) >> 24) | (((x) & 0x000000ff00000000ull) >> 8) | (((x) & 0x00000000ff000000ull) << 8) | (((x) & 0x0000000000ff0000ull) << 24) | (((x) & 0x000000000000ff00ull) << 40) | (((x) & 0x00000000000000ffull) << 56)) # macro
# def __NTH(fct): return fct throw () # macro
def htobe64(x): return __bswap_64 (x) # macro
def minor(dev): return gnu_dev_minor (dev) # macro
# cpfacos = acos # alias
# __GID_T_TYPE = __U32_TYPE # alias
# def __ASMNAME2(prefix,cname): return __STRING (prefix) cname # macro
# __OFF_T_TYPE = __SLONGWORD_TYPE # alias
# def __u_intN_t(N,MODE): return typedef unsigned int u_int ##N ##_t __attribute__ ((__mode__ (MODE))) # macro
# cpfsqrt = sqrt # alias
def htole32(x): return (x) # macro
# __UID_T_TYPE = __U32_TYPE # alias
# __SWBLK_T_TYPE = __SLONGWORD_TYPE # alias
def __bos(ptr): return __builtin_object_size (ptr, __USE_FORTIFY_LEVEL > 1) # macro
# def CP_ARBITER_GET_SHAPES(arb,a,b): return cpShape *a, *b; cpArbiterGetShapes(arb, &a, &b); # macro
# def CP_DefineBodyStructGetter(type,member,name): return static inline type cpBodyGet ##name(const cpBody *body){return body->member;} # macro
def __MATHCALLX(function,suffix,args,attrib): return __MATHDECLX (_Mdouble_,function,suffix, args, attrib) # macro
__FLOAT_WORD_ORDER = __BYTE_ORDER # alias
cpArbiterStateFirstColl = 0
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
cpConvexHull = chipmunk_lib.cpConvexHull
cpConvexHull.restype = c_int
cpConvexHull.argtypes = [c_int, POINTER(cpVect), POINTER(cpVect), POINTER(c_int), cpFloat]

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
class N17cpContactPointSet4DOT_22E(Structure):
    pass
#N17cpContactPointSet4DOT_22E._pack_ = 4
N17cpContactPointSet4DOT_22E._fields_ = [
    ('point', cpVect),
    ('normal', cpVect),
    ('dist', cpFloat),
]
cpContactPointSet._fields_ = [
    ('count', c_int),
    ('points', N17cpContactPointSet4DOT_22E * 4),
]
cpArbiterGetContactPointSet = chipmunk_lib.cpArbiterGetContactPointSet
cpArbiterGetContactPointSet.restype = cpContactPointSet
cpArbiterGetContactPointSet.argtypes = [POINTER(cpArbiter)]
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
cpPolyShape._fields_ = [
    ('shape', cpShape),
    ('numVerts', c_int),
    ('verts', POINTER(cpVect)),
    ('tVerts', POINTER(cpVect)),
    ('planes', POINTER(cpSplittingPlane)),
    ('tPlanes', POINTER(cpSplittingPlane)),
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
class cpNearestPointQueryInfo(Structure):
    pass
#cpNearestPointQueryInfo._pack_ = 4
cpNearestPointQueryInfo._fields_ = [
    ('shape', POINTER(cpShape)),
    ('p', cpVect),
    ('d', cpFloat),
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
WSTOPPED = 2 # Variable c_int '2'
_ATFILE_SOURCE = 1 # Variable c_int '1'
CP_BUFFER_BYTES = 32768 # Variable c_int '32768'
_POSIX_C_SOURCE = 200809 # Variable c_long '200809l'
NAN = 0.0 # Variable c_float '0.0f'
M_LOG10E = 0.43429448190325182 # Variable c_double '4.34294481903251816667932416748953983187675476074e-1'
__WCLONE = 2147483648L # Variable c_uint '-2147483648u'
__GNU_LIBRARY__ = 6 # Variable c_int '6'
_BITS_TYPESIZES_H = 1 # Variable c_int '1'
__USE_XOPEN = 1 # Variable c_int '1'
__USE_LARGEFILE64 = 1 # Variable c_int '1'
__GLIBC_HAVE_LONG_LONG = 1 # Variable c_int '1'
__USE_XOPEN2K8 = 1 # Variable c_int '1'
__WCOREFLAG = 128 # Variable c_int '128'
_STRUCT_TIMEVAL = 1 # Variable c_int '1'
__USE_POSIX2 = 1 # Variable c_int '1'
RAND_MAX = 2147483647 # Variable c_int '2147483647'
__SIZEOF_PTHREAD_RWLOCKATTR_T = 8 # Variable c_int '8'
CP_MAX_CONTACTS_PER_ARBITER = 4 # Variable c_int '4'
__SIZEOF_PTHREAD_CONDATTR_T = 4 # Variable c_int '4'
__STDC_IEC_559__ = 1 # Variable c_int '1'
_BITS_PTHREADTYPES_H = 1 # Variable c_int '1'
M_LN2 = 0.69314718055994529 # Variable c_double '6.93147180559945286226763982995180413126945495605e-1'
M_SQRT1_2 = 0.70710678118654757 # Variable c_double '7.07106781186547572737310929369414225220680236816e-1'
__USE_ATFILE = 1 # Variable c_int '1'
__time_t_defined = 1 # Variable c_int '1'
MATH_ERRNO = 1 # Variable c_int '1'
_SYS_SELECT_H = 1 # Variable c_int '1'
M_PI = 3.1415926535897931 # Variable c_double '3.14159265358979311599796346854418516159057617188e+0'
__SIZEOF_PTHREAD_MUTEXATTR_T = 4 # Variable c_int '4'
_POSIX_SOURCE = 1 # Variable c_int '1'
__BIT_TYPES_DEFINED__ = 1 # Variable c_int '1'
_ISOC99_SOURCE = 1 # Variable c_int '1'
__USE_POSIX = 1 # Variable c_int '1'
TLOSS = 5 # Variable c_int '5'
M_PI_2 = 1.5707963267948966 # Variable c_double '1.57079632679489655799898173427209258079528808594e+0'
DOMAIN = 1 # Variable c_int '1'
_STDLIB_H = 1 # Variable c_int '1'
M_PI_4 = 0.78539816339744828 # Variable c_double '7.85398163397448278999490867136046290397644042969e-1'
_ALLOCA_H = 1 # Variable c_int '1'
__clock_t_defined = 1 # Variable c_int '1'
WEXITED = 4 # Variable c_int '4'
CP_USE_DOUBLES = 1 # Variable c_int '1'
__USE_POSIX199309 = 1 # Variable c_int '1'
__FD_ISSET_BT = 'btl' # Variable STRING '(const char*)"btl"'
_BITS_WCHAR_H = 1 # Variable c_int '1'
__GLIBC_MINOR__ = 10 # Variable c_int '10'
M_E = 2.7182818284590451 # Variable c_double '2.71828182845904509079559829842764884233474731445e+0'
__clockid_t_defined = 1 # Variable c_int '1'
__timer_t_defined = 1 # Variable c_int '1'
__lldiv_t_defined = 1 # Variable c_int '1'
__FD_CLR_BTR = 'btrl' # Variable STRING '(const char*)"btrl"'
cpTrue = 1 # Variable c_int '1'
_SVID_SOURCE = 1 # Variable c_int '1'
__USE_XOPEN2K = 1 # Variable c_int '1'
__SIZEOF_PTHREAD_BARRIER_T = 20 # Variable c_int '20'
CP_VERSION_RELEASE = 1 # Variable c_int '1'
_SYS_TYPES_H = 1 # Variable c_int '1'
__WNOTHREAD = 536870912 # Variable c_int '536870912'
X_TLOSS = 14148475504056880.0 # Variable c_double '1.414847550405688e+16'
__timespec_defined = 1 # Variable c_int '1'
__USE_GNU = 1 # Variable c_int '1'
WUNTRACED = 2 # Variable c_int '2'
__USE_BSD = 1 # Variable c_int '1'
_SIGSET_NWORDS = 32L # Variable c_uint '32u'
PLOSS = 6 # Variable c_int '6'
M_LN10 = 2.3025850929940459 # Variable c_double '2.30258509299404590109361379290930926799774169922e+0'
cpFalse = 0 # Variable c_int '0'
__SIZEOF_PTHREAD_BARRIERATTR_T = 4 # Variable c_int '4'
_SIGSET_H_types = 1 # Variable c_int '1'
_MATH_H_MATHDEF = 1 # Variable c_int '1'
CP_ALL_LAYERS = 4294967295 # Variable c_uint '-1u'
__USE_SVID = 1 # Variable c_int '1'
__SIZEOF_PTHREAD_MUTEX_T = 24 # Variable c_int '24'
__USE_UNIX98 = 1 # Variable c_int '1'
__USE_ANSI = 1 # Variable c_int '1'
OVERFLOW = 3 # Variable c_int '3'
__USE_MISC = 1 # Variable c_int '1'
__GLIBC__ = 2 # Variable c_int '2'
__ldiv_t_defined = 1 # Variable c_int '1'
FP_ILOGB0 = -2147483648 # Variable c_int '-0x080000000'
M_LOG2E = 1.4426950408889634 # Variable c_double '1.44269504088896338700465094007086008787155151367e+0'
__W_CONTINUED = 65535 # Variable c_int '65535'
CP_VERSION_MAJOR = 6 # Variable c_int '6'
CP_ALLOW_PRIVATE_ACCESS = 0 # Variable c_int '0'
FP_ILOGBNAN = -2147483648 # Variable c_int '-0x080000000'
__FD_SET_BTS = 'btsl' # Variable STRING '(const char*)"btsl"'
M_2_SQRTPI = 1.1283791670955126 # Variable c_double '1.12837916709551255856069928995566442608833312988e+0'
_ENDIAN_H = 1 # Variable c_int '1'
_STDINT_H = 1 # Variable c_int '1'
__USE_FORTIFY_LEVEL = 0 # Variable c_int '0'
__SIZEOF_PTHREAD_RWLOCK_T = 32 # Variable c_int '32'
_BITS_BYTESWAP_H = 1 # Variable c_int '1'
WNOHANG = 1 # Variable c_int '1'
__STDC_ISO_10646__ = 200009 # Variable c_long '200009l'
_MATH_H = 1 # Variable c_int '1'
__STDC_IEC_559_COMPLEX__ = 1 # Variable c_int '1'
_SYS_SYSMACROS_H = 1 # Variable c_int '1'
__USE_XOPEN_EXTENDED = 1 # Variable c_int '1'
EXIT_SUCCESS = 0 # Variable c_int '0'
__USE_LARGEFILE = 1 # Variable c_int '1'
__SIZEOF_PTHREAD_COND_T = 48 # Variable c_int '48'
_FEATURES_H = 1 # Variable c_int '1'
HUGE_VAL = 0.0 # Variable c_double '0.0'
CP_VERSION_MINOR = 1 # Variable c_int '1'
__USE_POSIX199506 = 1 # Variable c_int '1'
_BITS_TYPES_H = 1 # Variable c_int '1'
M_1_PI = 0.31830988618379069 # Variable c_double '3.18309886183790691216444201927515678107738494873e-1'
UNDERFLOW = 4 # Variable c_int '4'
SING = 2 # Variable c_int '2'
__WCHAR_MIN = -2147483648 # Variable c_int '-0x080000000'
HUGE = 3.4028234663852886e+38 # Variable c_float '3.4028234663852885981170418348451692544e+38f'
M_2_PI = 0.63661977236758138 # Variable c_double '6.36619772367581382432888403855031356215476989746e-1'
_XOPEN_SOURCE_EXTENDED = 1 # Variable c_int '1'
CP_NO_GROUP = 0 # Variable c_uint '0u'
WNOWAIT = 16777216 # Variable c_int '16777216'
__WORDSIZE = 32 # Variable c_int '32'
_SYS_CDEFS_H = 1 # Variable c_int '1'
_LARGEFILE64_SOURCE = 1 # Variable c_int '1'
_XOPEN_SOURCE = 700 # Variable c_int '700'
__SIZEOF_PTHREAD_ATTR_T = 36 # Variable c_int '36'
__WALL = 1073741824 # Variable c_int '1073741824'
MATH_ERREXCEPT = 2 # Variable c_int '2'
HUGE_VALF = 0.0 # Variable c_float '0.0f'
__USE_ISOC95 = 1 # Variable c_int '1'
__USE_ISOC99 = 1 # Variable c_int '1'
WCONTINUED = 8 # Variable c_int '8'
EXIT_FAILURE = 1 # Variable c_int '1'
M_SQRT2 = 1.4142135623730951 # Variable c_double '1.41421356237309514547462185873882845044136047363e+0'
_BSD_SOURCE = 1 # Variable c_int '1'
_XLOCALE_H = 1 # Variable c_int '1'
_LARGEFILE_SOURCE = 1 # Variable c_int '1'
__FD_ZERO_STOS = 'stosl' # Variable STRING '(const char*)"stosl"'
frexpl = chipmunk_lib.frexpl
frexpl.restype = c_longdouble
frexpl.argtypes = [c_longdouble, POINTER(c_int)]
frexpf = chipmunk_lib.frexpf
frexpf.restype = c_float
frexpf.argtypes = [c_float, POINTER(c_int)]
frexp = chipmunk_lib.frexp
frexp.restype = c_double
frexp.argtypes = [c_double, POINTER(c_int)]
ldexpl = chipmunk_lib.ldexpl
ldexpl.restype = c_longdouble
ldexpl.argtypes = [c_longdouble, c_int]
ldexp = chipmunk_lib.ldexp
ldexp.restype = c_double
ldexp.argtypes = [c_double, c_int]
ldexpf = chipmunk_lib.ldexpf
ldexpf.restype = c_float
ldexpf.argtypes = [c_float, c_int]
modff = chipmunk_lib.modff
modff.restype = c_float
modff.argtypes = [c_float, POINTER(c_float)]
modf = chipmunk_lib.modf
modf.restype = c_double
modf.argtypes = [c_double, POINTER(c_double)]
modfl = chipmunk_lib.modfl
modfl.restype = c_longdouble
modfl.argtypes = [c_longdouble, POINTER(c_longdouble)]
__isinff = chipmunk_lib.__isinff
__isinff.restype = c_int
__isinff.argtypes = [c_float]
__isinfl = chipmunk_lib.__isinfl
__isinfl.restype = c_int
__isinfl.argtypes = [c_longdouble]
__isinf = chipmunk_lib.__isinf
__isinf.restype = c_int
__isinf.argtypes = [c_double]
__finitef = chipmunk_lib.__finitef
__finitef.restype = c_int
__finitef.argtypes = [c_float]
__finite = chipmunk_lib.__finite
__finite.restype = c_int
__finite.argtypes = [c_double]
__finitel = chipmunk_lib.__finitel
__finitel.restype = c_int
__finitel.argtypes = [c_longdouble]
isinff = chipmunk_lib.isinff
isinff.restype = c_int
isinff.argtypes = [c_float]
isinf = chipmunk_lib.isinf
isinf.restype = c_int
isinf.argtypes = [c_double]
isinfl = chipmunk_lib.isinfl
isinfl.restype = c_int
isinfl.argtypes = [c_longdouble]
finite = chipmunk_lib.finite
finite.restype = c_int
finite.argtypes = [c_double]
finitef = chipmunk_lib.finitef
finitef.restype = c_int
finitef.argtypes = [c_float]
finitel = chipmunk_lib.finitel
finitel.restype = c_int
finitel.argtypes = [c_longdouble]
copysignl = chipmunk_lib.copysignl
copysignl.restype = c_longdouble
copysignl.argtypes = [c_longdouble, c_longdouble]
copysignf = chipmunk_lib.copysignf
copysignf.restype = c_float
copysignf.argtypes = [c_float, c_float]
copysign = chipmunk_lib.copysign
copysign.restype = c_double
copysign.argtypes = [c_double, c_double]
__isnan = chipmunk_lib.__isnan
__isnan.restype = c_int
__isnan.argtypes = [c_double]
__isnanl = chipmunk_lib.__isnanl
__isnanl.restype = c_int
__isnanl.argtypes = [c_longdouble]
__isnanf = chipmunk_lib.__isnanf
__isnanf.restype = c_int
__isnanf.argtypes = [c_float]
isnanl = chipmunk_lib.isnanl
isnanl.restype = c_int
isnanl.argtypes = [c_longdouble]
isnanf = chipmunk_lib.isnanf
isnanf.restype = c_int
isnanf.argtypes = [c_float]
isnan = chipmunk_lib.isnan
isnan.restype = c_int
isnan.argtypes = [c_double]
scalbn = chipmunk_lib.scalbn
scalbn.restype = c_double
scalbn.argtypes = [c_double, c_int]
scalbnf = chipmunk_lib.scalbnf
scalbnf.restype = c_float
scalbnf.argtypes = [c_float, c_int]
scalbnl = chipmunk_lib.scalbnl
scalbnl.restype = c_longdouble
scalbnl.argtypes = [c_longdouble, c_int]
scalblnl = chipmunk_lib.scalblnl
scalblnl.restype = c_longdouble
scalblnl.argtypes = [c_longdouble, c_long]
scalblnf = chipmunk_lib.scalblnf
scalblnf.restype = c_float
scalblnf.argtypes = [c_float, c_long]
scalbln = chipmunk_lib.scalbln
scalbln.restype = c_double
scalbln.argtypes = [c_double, c_long]
__signbitl = chipmunk_lib.__signbitl
__signbitl.restype = c_int
__signbitl.argtypes = [c_longdouble]
__signbitf = chipmunk_lib.__signbitf
__signbitf.restype = c_int
__signbitf.argtypes = [c_float]
__signbit = chipmunk_lib.__signbit
__signbit.restype = c_int
__signbit.argtypes = [c_double]
float_t = c_longdouble
double_t = c_longdouble
pthread_t = c_ulong
class pthread_attr_t(Union):
    pass
pthread_attr_t._fields_ = [
    ('__size', c_char * 36),
    ('__align', c_long),
]
class __pthread_internal_slist(Structure):
    pass
__pthread_internal_slist._fields_ = [
    ('__next', POINTER(__pthread_internal_slist)),
]
__pthread_slist_t = __pthread_internal_slist
class __pthread_mutex_s(Structure):
    pass
class N15pthread_mutex_t17__pthread_mutex_s4DOT_10E(Union):
    pass
N15pthread_mutex_t17__pthread_mutex_s4DOT_10E._fields_ = [
    ('__spins', c_int),
    ('__list', __pthread_slist_t),
]
__pthread_mutex_s._anonymous_ = ['_0']
__pthread_mutex_s._fields_ = [
    ('__lock', c_int),
    ('__count', c_uint),
    ('__owner', c_int),
    ('__kind', c_int),
    ('__nusers', c_uint),
    ('_0', N15pthread_mutex_t17__pthread_mutex_s4DOT_10E),
]
class pthread_mutex_t(Union):
    pass
pthread_mutex_t._fields_ = [
    ('__data', __pthread_mutex_s),
    ('__size', c_char * 24),
    ('__align', c_long),
]
class pthread_mutexattr_t(Union):
    pass
pthread_mutexattr_t._fields_ = [
    ('__size', c_char * 4),
    ('__align', c_int),
]
class N14pthread_cond_t4DOT_13E(Structure):
    pass
#N14pthread_cond_t4DOT_13E._pack_ = 4
N14pthread_cond_t4DOT_13E._fields_ = [
    ('__lock', c_int),
    ('__futex', c_uint),
    ('__total_seq', c_ulonglong),
    ('__wakeup_seq', c_ulonglong),
    ('__woken_seq', c_ulonglong),
    ('__mutex', c_void_p),
    ('__nwaiters', c_uint),
    ('__broadcast_seq', c_uint),
]
class pthread_cond_t(Union):
    pass
#pthread_cond_t._pack_ = 4
pthread_cond_t._fields_ = [
    ('__data', N14pthread_cond_t4DOT_13E),
    ('__size', c_char * 48),
    ('__align', c_longlong),
]
class pthread_condattr_t(Union):
    pass
pthread_condattr_t._fields_ = [
    ('__size', c_char * 4),
    ('__align', c_int),
]
pthread_key_t = c_uint
pthread_once_t = c_int
class N16pthread_rwlock_t4DOT_16E(Structure):
    pass
N16pthread_rwlock_t4DOT_16E._fields_ = [
    ('__lock', c_int),
    ('__nr_readers', c_uint),
    ('__readers_wakeup', c_uint),
    ('__writer_wakeup', c_uint),
    ('__nr_readers_queued', c_uint),
    ('__nr_writers_queued', c_uint),
    ('__flags', c_ubyte),
    ('__shared', c_ubyte),
    ('__pad1', c_ubyte),
    ('__pad2', c_ubyte),
    ('__writer', c_int),
]
class pthread_rwlock_t(Union):
    pass
pthread_rwlock_t._fields_ = [
    ('__data', N16pthread_rwlock_t4DOT_16E),
    ('__size', c_char * 32),
    ('__align', c_long),
]
class pthread_rwlockattr_t(Union):
    pass
pthread_rwlockattr_t._fields_ = [
    ('__size', c_char * 8),
    ('__align', c_long),
]
pthread_spinlock_t = c_int
class pthread_barrier_t(Union):
    pass
pthread_barrier_t._fields_ = [
    ('__size', c_char * 20),
    ('__align', c_long),
]
class pthread_barrierattr_t(Union):
    pass
pthread_barrierattr_t._fields_ = [
    ('__size', c_char * 4),
    ('__align', c_int),
]
__sig_atomic_t = c_int
class __sigset_t(Structure):
    pass
__sigset_t._fields_ = [
    ('__val', c_ulong * 32),
]
class timeval(Structure):
    pass
__time_t = c_long
__suseconds_t = c_long
timeval._fields_ = [
    ('tv_sec', __time_t),
    ('tv_usec', __suseconds_t),
]
__u_char = c_ubyte
__u_short = c_ushort
__u_int = c_uint
__u_long = c_ulong
__int8_t = c_byte
__uint8_t = c_ubyte
__int16_t = c_short
__uint16_t = c_ushort
__int32_t = c_int
__uint32_t = c_uint
__int64_t = c_longlong
__uint64_t = c_ulonglong
__dev_t = __u_quad_t
__uid_t = c_uint
__gid_t = c_uint
__ino_t = c_ulong
__ino64_t = __u_quad_t
__mode_t = c_uint
__nlink_t = c_uint
__off_t = c_long
__off64_t = __quad_t
__pid_t = c_int
class __fsid_t(Structure):
    pass
__fsid_t._fields_ = [
    ('__val', c_int * 2),
]
__clock_t = c_long
__rlim_t = c_ulong
__rlim64_t = __u_quad_t
__id_t = c_uint
__useconds_t = c_uint
__daddr_t = c_int
__swblk_t = c_long
__key_t = c_int
__clockid_t = c_int
__timer_t = c_void_p
__blksize_t = c_long
__blkcnt_t = c_long
__blkcnt64_t = __quad_t
__fsblkcnt_t = c_ulong
__fsblkcnt64_t = __u_quad_t
__fsfilcnt_t = c_ulong
__fsfilcnt64_t = __u_quad_t
__ssize_t = c_int
__loff_t = __off64_t
__qaddr_t = POINTER(__quad_t)
__caddr_t = STRING
__intptr_t = c_int
__socklen_t = c_uint
class wait(Union):
    pass
class N4wait3DOT_0E(Structure):
    pass
N4wait3DOT_0E._fields_ = [
    ('__w_termsig', c_uint, 7),
    ('__w_coredump', c_uint, 1),
    ('__w_retcode', c_uint, 8),
    ('', c_uint, 16),
]
class N4wait3DOT_1E(Structure):
    pass
N4wait3DOT_1E._fields_ = [
    ('__w_stopval', c_uint, 8),
    ('__w_stopsig', c_uint, 8),
    ('', c_uint, 16),
]
wait._fields_ = [
    ('w_status', c_int),
    ('__wait_terminated', N4wait3DOT_0E),
    ('__wait_stopped', N4wait3DOT_1E),
]

# values for unnamed enumeration

# values for enumeration '_LIB_VERSION_TYPE'
_LIB_VERSION_TYPE = c_int # enum
class __exception(Structure):
    pass
#__exception._pack_ = 4
__exception._fields_ = [
    ('type', c_int),
    ('name', STRING),
    ('arg1', c_double),
    ('arg2', c_double),
    ('retval', c_double),
]
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
class div_t(Structure):
    pass
div_t._fields_ = [
    ('quot', c_int),
    ('rem', c_int),
]
class ldiv_t(Structure):
    pass
ldiv_t._fields_ = [
    ('quot', c_long),
    ('rem', c_long),
]
class lldiv_t(Structure):
    pass
#lldiv_t._pack_ = 4
lldiv_t._fields_ = [
    ('quot', c_longlong),
    ('rem', c_longlong),
]
__ctype_get_mb_cur_max = chipmunk_lib.__ctype_get_mb_cur_max
__ctype_get_mb_cur_max.restype = size_t
__ctype_get_mb_cur_max.argtypes = []
atof = chipmunk_lib.atof
atof.restype = c_double
atof.argtypes = [STRING]
atoi = chipmunk_lib.atoi
atoi.restype = c_int
atoi.argtypes = [STRING]
atol = chipmunk_lib.atol
atol.restype = c_long
atol.argtypes = [STRING]
atoll = chipmunk_lib.atoll
atoll.restype = c_longlong
atoll.argtypes = [STRING]
strtod = chipmunk_lib.strtod
strtod.restype = c_double
strtod.argtypes = [STRING, POINTER(STRING)]
strtof = chipmunk_lib.strtof
strtof.restype = c_float
strtof.argtypes = [STRING, POINTER(STRING)]
strtold = chipmunk_lib.strtold
strtold.restype = c_longdouble
strtold.argtypes = [STRING, POINTER(STRING)]
strtol = chipmunk_lib.strtol
strtol.restype = c_long
strtol.argtypes = [STRING, POINTER(STRING), c_int]
strtoul = chipmunk_lib.strtoul
strtoul.restype = c_ulong
strtoul.argtypes = [STRING, POINTER(STRING), c_int]
strtoq = chipmunk_lib.strtoq
strtoq.restype = c_longlong
strtoq.argtypes = [STRING, POINTER(STRING), c_int]
strtouq = chipmunk_lib.strtouq
strtouq.restype = c_ulonglong
strtouq.argtypes = [STRING, POINTER(STRING), c_int]
strtoll = chipmunk_lib.strtoll
strtoll.restype = c_longlong
strtoll.argtypes = [STRING, POINTER(STRING), c_int]
strtoull = chipmunk_lib.strtoull
strtoull.restype = c_ulonglong
strtoull.argtypes = [STRING, POINTER(STRING), c_int]
class __locale_struct(Structure):
    pass
__locale_t = POINTER(__locale_struct)
strtol_l = chipmunk_lib.strtol_l
strtol_l.restype = c_long
strtol_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtoul_l = chipmunk_lib.strtoul_l
strtoul_l.restype = c_ulong
strtoul_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtoll_l = chipmunk_lib.strtoll_l
strtoll_l.restype = c_longlong
strtoll_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtoull_l = chipmunk_lib.strtoull_l
strtoull_l.restype = c_ulonglong
strtoull_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtod_l = chipmunk_lib.strtod_l
strtod_l.restype = c_double
strtod_l.argtypes = [STRING, POINTER(STRING), __locale_t]
strtof_l = chipmunk_lib.strtof_l
strtof_l.restype = c_float
strtof_l.argtypes = [STRING, POINTER(STRING), __locale_t]
strtold_l = chipmunk_lib.strtold_l
strtold_l.restype = c_longdouble
strtold_l.argtypes = [STRING, POINTER(STRING), __locale_t]
l64a = chipmunk_lib.l64a
l64a.restype = STRING
l64a.argtypes = [c_long]
a64l = chipmunk_lib.a64l
a64l.restype = c_long
a64l.argtypes = [STRING]
random = chipmunk_lib.random
random.restype = c_long
random.argtypes = []
srandom = chipmunk_lib.srandom
srandom.restype = None
srandom.argtypes = [c_uint]
initstate = chipmunk_lib.initstate
initstate.restype = STRING
initstate.argtypes = [c_uint, STRING, size_t]
setstate = chipmunk_lib.setstate
setstate.restype = STRING
setstate.argtypes = [STRING]
class random_data(Structure):
    pass
int32_t = c_int32
random_data._fields_ = [
    ('fptr', POINTER(int32_t)),
    ('rptr', POINTER(int32_t)),
    ('state', POINTER(int32_t)),
    ('rand_type', c_int),
    ('rand_deg', c_int),
    ('rand_sep', c_int),
    ('end_ptr', POINTER(int32_t)),
]
random_r = chipmunk_lib.random_r
random_r.restype = c_int
random_r.argtypes = [POINTER(random_data), POINTER(int32_t)]
srandom_r = chipmunk_lib.srandom_r
srandom_r.restype = c_int
srandom_r.argtypes = [c_uint, POINTER(random_data)]
initstate_r = chipmunk_lib.initstate_r
initstate_r.restype = c_int
initstate_r.argtypes = [c_uint, STRING, size_t, POINTER(random_data)]
setstate_r = chipmunk_lib.setstate_r
setstate_r.restype = c_int
setstate_r.argtypes = [STRING, POINTER(random_data)]
rand = chipmunk_lib.rand
rand.restype = c_int
rand.argtypes = []
srand = chipmunk_lib.srand
srand.restype = None
srand.argtypes = [c_uint]
rand_r = chipmunk_lib.rand_r
rand_r.restype = c_int
rand_r.argtypes = [POINTER(c_uint)]
drand48 = chipmunk_lib.drand48
drand48.restype = c_double
drand48.argtypes = []
erand48 = chipmunk_lib.erand48
erand48.restype = c_double
erand48.argtypes = [POINTER(c_ushort)]
lrand48 = chipmunk_lib.lrand48
lrand48.restype = c_long
lrand48.argtypes = []
nrand48 = chipmunk_lib.nrand48
nrand48.restype = c_long
nrand48.argtypes = [POINTER(c_ushort)]
mrand48 = chipmunk_lib.mrand48
mrand48.restype = c_long
mrand48.argtypes = []
jrand48 = chipmunk_lib.jrand48
jrand48.restype = c_long
jrand48.argtypes = [POINTER(c_ushort)]
srand48 = chipmunk_lib.srand48
srand48.restype = None
srand48.argtypes = [c_long]
seed48 = chipmunk_lib.seed48
seed48.restype = POINTER(c_ushort)
seed48.argtypes = [POINTER(c_ushort)]
lcong48 = chipmunk_lib.lcong48
lcong48.restype = None
lcong48.argtypes = [POINTER(c_ushort)]
class drand48_data(Structure):
    pass
#drand48_data._pack_ = 4
drand48_data._fields_ = [
    ('__x', c_ushort * 3),
    ('__old_x', c_ushort * 3),
    ('__c', c_ushort),
    ('__init', c_ushort),
    ('__a', c_ulonglong),
]
drand48_r = chipmunk_lib.drand48_r
drand48_r.restype = c_int
drand48_r.argtypes = [POINTER(drand48_data), POINTER(c_double)]
erand48_r = chipmunk_lib.erand48_r
erand48_r.restype = c_int
erand48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data), POINTER(c_double)]
lrand48_r = chipmunk_lib.lrand48_r
lrand48_r.restype = c_int
lrand48_r.argtypes = [POINTER(drand48_data), POINTER(c_long)]
nrand48_r = chipmunk_lib.nrand48_r
nrand48_r.restype = c_int
nrand48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data), POINTER(c_long)]
mrand48_r = chipmunk_lib.mrand48_r
mrand48_r.restype = c_int
mrand48_r.argtypes = [POINTER(drand48_data), POINTER(c_long)]
jrand48_r = chipmunk_lib.jrand48_r
jrand48_r.restype = c_int
jrand48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data), POINTER(c_long)]
srand48_r = chipmunk_lib.srand48_r
srand48_r.restype = c_int
srand48_r.argtypes = [c_long, POINTER(drand48_data)]
seed48_r = chipmunk_lib.seed48_r
seed48_r.restype = c_int
seed48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data)]
lcong48_r = chipmunk_lib.lcong48_r
lcong48_r.restype = c_int
lcong48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data)]
malloc = chipmunk_lib.malloc
malloc.restype = c_void_p
malloc.argtypes = [size_t]
cfree = chipmunk_lib.cfree
cfree.restype = None
cfree.argtypes = [c_void_p]
valloc = chipmunk_lib.valloc
valloc.restype = c_void_p
valloc.argtypes = [size_t]
posix_memalign = chipmunk_lib.posix_memalign
posix_memalign.restype = c_int
posix_memalign.argtypes = [POINTER(c_void_p), size_t, size_t]
abort = chipmunk_lib.abort
abort.restype = None
abort.argtypes = []
on_exit = chipmunk_lib.on_exit
on_exit.restype = c_int
on_exit.argtypes = [function_pointer(None, c_int, c_void_p), c_void_p]
exit = chipmunk_lib.exit
exit.restype = None
exit.argtypes = [c_int]
quick_exit = chipmunk_lib.quick_exit
quick_exit.restype = None
quick_exit.argtypes = [c_int]
_Exit = chipmunk_lib._Exit
_Exit.restype = None
_Exit.argtypes = [c_int]
getenv = chipmunk_lib.getenv
getenv.restype = STRING
getenv.argtypes = [STRING]
__secure_getenv = chipmunk_lib.__secure_getenv
__secure_getenv.restype = STRING
__secure_getenv.argtypes = [STRING]
putenv = chipmunk_lib.putenv
putenv.restype = c_int
putenv.argtypes = [STRING]
setenv = chipmunk_lib.setenv
setenv.restype = c_int
setenv.argtypes = [STRING, STRING, c_int]
unsetenv = chipmunk_lib.unsetenv
unsetenv.restype = c_int
unsetenv.argtypes = [STRING]
clearenv = chipmunk_lib.clearenv
clearenv.restype = c_int
clearenv.argtypes = []
mktemp = chipmunk_lib.mktemp
mktemp.restype = STRING
mktemp.argtypes = [STRING]
mkstemp = chipmunk_lib.mkstemp
mkstemp.restype = c_int
mkstemp.argtypes = [STRING]
mkstemp64 = chipmunk_lib.mkstemp64
mkstemp64.restype = c_int
mkstemp64.argtypes = [STRING]
mkdtemp = chipmunk_lib.mkdtemp
mkdtemp.restype = STRING
mkdtemp.argtypes = [STRING]
mkostemp = chipmunk_lib.mkostemp
mkostemp.restype = c_int
mkostemp.argtypes = [STRING, c_int]
mkostemp64 = chipmunk_lib.mkostemp64
mkostemp64.restype = c_int
mkostemp64.argtypes = [STRING, c_int]
system = chipmunk_lib.system
system.restype = c_int
system.argtypes = [STRING]
canonicalize_file_name = chipmunk_lib.canonicalize_file_name
canonicalize_file_name.restype = STRING
canonicalize_file_name.argtypes = [STRING]
realpath = chipmunk_lib.realpath
realpath.restype = STRING
realpath.argtypes = [STRING, STRING]
__compar_fn_t = function_pointer(c_int, c_void_p, c_void_p)
comparison_fn_t = __compar_fn_t
__compar_d_fn_t = function_pointer(c_int, c_void_p, c_void_p, c_void_p)
bsearch = chipmunk_lib.bsearch
bsearch.restype = c_void_p
bsearch.argtypes = [c_void_p, c_void_p, size_t, size_t, __compar_fn_t]
qsort = chipmunk_lib.qsort
qsort.restype = None
qsort.argtypes = [c_void_p, size_t, size_t, __compar_fn_t]
qsort_r = chipmunk_lib.qsort_r
qsort_r.restype = None
qsort_r.argtypes = [c_void_p, size_t, size_t, __compar_d_fn_t, c_void_p]
abs = chipmunk_lib.abs
abs.restype = c_int
abs.argtypes = [c_int]
labs = chipmunk_lib.labs
labs.restype = c_long
labs.argtypes = [c_long]
llabs = chipmunk_lib.llabs
llabs.restype = c_longlong
llabs.argtypes = [c_longlong]
div = chipmunk_lib.div
div.restype = div_t
div.argtypes = [c_int, c_int]
ldiv = chipmunk_lib.ldiv
ldiv.restype = ldiv_t
ldiv.argtypes = [c_long, c_long]
lldiv = chipmunk_lib.lldiv
lldiv.restype = lldiv_t
lldiv.argtypes = [c_longlong, c_longlong]
ecvt = chipmunk_lib.ecvt
ecvt.restype = STRING
ecvt.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int)]
fcvt = chipmunk_lib.fcvt
fcvt.restype = STRING
fcvt.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int)]
gcvt = chipmunk_lib.gcvt
gcvt.restype = STRING
gcvt.argtypes = [c_double, c_int, STRING]
qecvt = chipmunk_lib.qecvt
qecvt.restype = STRING
qecvt.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int)]
qfcvt = chipmunk_lib.qfcvt
qfcvt.restype = STRING
qfcvt.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int)]
qgcvt = chipmunk_lib.qgcvt
qgcvt.restype = STRING
qgcvt.argtypes = [c_longdouble, c_int, STRING]
ecvt_r = chipmunk_lib.ecvt_r
ecvt_r.restype = c_int
ecvt_r.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
fcvt_r = chipmunk_lib.fcvt_r
fcvt_r.restype = c_int
fcvt_r.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
qecvt_r = chipmunk_lib.qecvt_r
qecvt_r.restype = c_int
qecvt_r.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
qfcvt_r = chipmunk_lib.qfcvt_r
qfcvt_r.restype = c_int
qfcvt_r.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
mblen = chipmunk_lib.mblen
mblen.restype = c_int
mblen.argtypes = [STRING, size_t]
mbtowc = chipmunk_lib.mbtowc
mbtowc.restype = c_int
mbtowc.argtypes = [WSTRING, STRING, size_t]
wctomb = chipmunk_lib.wctomb
wctomb.restype = c_int
wctomb.argtypes = [STRING, c_wchar]
mbstowcs = chipmunk_lib.mbstowcs
mbstowcs.restype = size_t
mbstowcs.argtypes = [WSTRING, STRING, size_t]
wcstombs = chipmunk_lib.wcstombs
wcstombs.restype = size_t
wcstombs.argtypes = [STRING, WSTRING, size_t]
rpmatch = chipmunk_lib.rpmatch
rpmatch.restype = c_int
rpmatch.argtypes = [STRING]
getsubopt = chipmunk_lib.getsubopt
getsubopt.restype = c_int
getsubopt.argtypes = [POINTER(STRING), POINTER(STRING), POINTER(STRING)]
posix_openpt = chipmunk_lib.posix_openpt
posix_openpt.restype = c_int
posix_openpt.argtypes = [c_int]
grantpt = chipmunk_lib.grantpt
grantpt.restype = c_int
grantpt.argtypes = [c_int]
unlockpt = chipmunk_lib.unlockpt
unlockpt.restype = c_int
unlockpt.argtypes = [c_int]
ptsname = chipmunk_lib.ptsname
ptsname.restype = STRING
ptsname.argtypes = [c_int]
ptsname_r = chipmunk_lib.ptsname_r
ptsname_r.restype = c_int
ptsname_r.argtypes = [c_int, STRING, size_t]
getpt = chipmunk_lib.getpt
getpt.restype = c_int
getpt.argtypes = []
getloadavg = chipmunk_lib.getloadavg
getloadavg.restype = c_int
getloadavg.argtypes = [POINTER(c_double), c_int]
sigset_t = __sigset_t
__fd_mask = c_long
class fd_set(Structure):
    pass
fd_set._fields_ = [
    ('fds_bits', __fd_mask * 32),
]
fd_mask = __fd_mask
select = chipmunk_lib.select
select.restype = c_int
select.argtypes = [c_int, POINTER(fd_set), POINTER(fd_set), POINTER(fd_set), POINTER(timeval)]
class timespec(Structure):
    pass
timespec._fields_ = [
    ('tv_sec', __time_t),
    ('tv_nsec', c_long),
]
pselect = chipmunk_lib.pselect
pselect.restype = c_int
pselect.argtypes = [c_int, POINTER(fd_set), POINTER(fd_set), POINTER(fd_set), POINTER(timespec), POINTER(__sigset_t)]
gnu_dev_major = chipmunk_lib.gnu_dev_major
gnu_dev_major.restype = c_uint
gnu_dev_major.argtypes = [c_ulonglong]
gnu_dev_minor = chipmunk_lib.gnu_dev_minor
gnu_dev_minor.restype = c_uint
gnu_dev_minor.argtypes = [c_ulonglong]
gnu_dev_makedev = chipmunk_lib.gnu_dev_makedev
gnu_dev_makedev.restype = c_ulonglong
gnu_dev_makedev.argtypes = [c_uint, c_uint]
u_char = __u_char
u_short = __u_short
u_int = __u_int
u_long = __u_long
quad_t = __quad_t
u_quad_t = __u_quad_t
fsid_t = __fsid_t
loff_t = __loff_t
ino_t = __ino_t
ino64_t = __ino64_t
dev_t = __dev_t
gid_t = __gid_t
mode_t = __mode_t
nlink_t = __nlink_t
uid_t = __uid_t
off_t = __off_t
off64_t = __off64_t
pid_t = __pid_t
id_t = __id_t
ssize_t = __ssize_t
daddr_t = __daddr_t
caddr_t = __caddr_t
key_t = __key_t
useconds_t = __useconds_t
suseconds_t = __suseconds_t
ulong = c_ulong
ushort = c_ushort
uint = c_uint
int8_t = c_int8
int16_t = c_int16
int64_t = c_int64
u_int8_t = c_ubyte
u_int16_t = c_ushort
u_int32_t = c_uint
u_int64_t = c_ulonglong
register_t = c_int
blksize_t = __blksize_t
blkcnt_t = __blkcnt_t
fsblkcnt_t = __fsblkcnt_t
fsfilcnt_t = __fsfilcnt_t
blkcnt64_t = __blkcnt64_t
fsblkcnt64_t = __fsblkcnt64_t
fsfilcnt64_t = __fsfilcnt64_t
clock_t = __clock_t
time_t = __time_t
clockid_t = __clockid_t
timer_t = __timer_t
class locale_data(Structure):
    pass
__locale_struct._fields_ = [
    ('__locales', POINTER(locale_data) * 13),
    ('__ctype_b', POINTER(c_ushort)),
    ('__ctype_tolower', POINTER(c_int)),
    ('__ctype_toupper', POINTER(c_int)),
    ('__names', STRING * 13),
]
locale_data._fields_ = [
]
locale_t = __locale_t
__all__ = ['_SVID_', '_ATFILE_SOURCE', 'cpArbiterIsFirstContact',
           'cpBodyEachShape', 'M_LOG10E', 'int_fast32_t',
           '__OFF64_T_TYPE', 'ldexpl', '__off64_t', '__int16_t',
           'cpSpaceBodyIteratorFunc', 'ldexpf', 'cpContactPointSet',
           '__WCOREFLAG', 'uint8_t', 'qecvt', '__timer_t_defined',
           'getloadavg', 'cpSpacePointQueryFunc',
           '__SIZEOF_PTHREAD_CONDATTR_T', 'makedev', 'wctomb',
           'cpConstraintGetImpulseImpl', 'rand_r', 'getpt', 'scalbnf',
           'scalbnl', '__USE_XOPEN_EXTENDED', 'islessgreater',
           'cpBodyActivate', 'cpBody', 'cpBodySetMass', '__time_t',
           '__WSTOPSIG', '__GLIBC_PREREQ', 'cpBoxShapeNew2',
           '__ASMNAME', 'M_PI', 'mbstowcs', 'htole32',
           '__SIZEOF_PTHREAD_MUTEXATTR_T', 'cpVect',
           'cpDampedRotarySpringGetClass', 'cpPivotJointNew2',
           'cpSpatialIndexQueryFunc', 'cpArbiterGetDepth', 'timer_t',
           'cpBodyNewStatic', 'div', 'gnu_dev_makedev', 'nrand48_r',
           'M_PI_2', '__uint64_t', 'cpInitChipmunk', 'M_PI_4',
           'cpcalloc', 'cpPinJointAlloc', 'cpBodyUpdatePosition',
           'scalblnl', 'cpSpaceDestroy', 'cpAreaForCircle',
           'cpBodyShapeIteratorFunc', '_POSIX_', '__USE_POSIX199309',
           'cpSlideJointAlloc', 'cpConstraintApplyImpulseImpl',
           'mktemp', '__clockid_t', 'cpGrooveJoint', '__timer_t',
           'M_E', 'grantpt', 'abs', 'id_t', '__WEXITSTATUS',
           'cpSpaceContainsShape', '__attribute_format_strfmon__',
           'strtol', 'cpNearestPointQueryInfo', 'be64toh',
           'cpRatchetJointGetClass', '__SIZEOF_PTHREAD_BARRIER_T',
           'cpConstraintPreSolveFunc', 'cpCentroidForPoly',
           'cpBoxShapeNew', 'cpBBTree', 'setstate_r',
           'cpCollisionType', '__u_long', 'wait', 'labs',
           '__WIFEXITED', 'cpSpaceArbiterApplyImpulseFunc',
           'cpSpatialIndexInsertImpl', 'pthread_t', 'M_LN10',
           'cpBBClampVect', 'cpFalse', '__locale_struct', '__PMT',
           'strtof', 'uint_fast8_t', '_LARGEFILE_SOURCE',
           'cpGrooveJointGetClass', 'realloc', '__mode_t',
           'CP_VERSION_MINOR', '__off_t', 'unlockpt',
           '_LIB_VERSION_TYPE', 'select', 'cpArbiterGetPoint',
           'u_quad_t', 'cpCollisionSeparateFunc',
           'canonicalize_file_name', 'cpBodyArbiterIteratorFunc',
           'fsfilcnt64_t', 'CP_VERSION_MAJOR',
           'CP_ALLOW_PRIVATE_ACCESS', 'cpBodyInitStatic',
           'cpSpatialIndexQueryImpl', 'daddr_t', 'cpSpaceHashResize',
           'FP_ILOGB0', 'uint_least32_t', 'int_least64_t', 'isless',
           'minor', 'cpSpatialIndexCollideStatic',
           'cpCollisionPostSolveFunc', 'isunordered',
           '__USE_FORTIFY_LEVEL', '__int8_t', 'strtoll_l',
           '__fsblkcnt64_t', '__FSFILCNT64_T_TYPE',
           'cpGrooveJointSetGrooveA', 'cpDampedSpringAlloc',
           'cpRotaryLimitJointAlloc', '_MATH_H', 'cpShapeCacheBB',
           'BIG_ENDIAN', 'off_t', 'pthread_barrierattr_t',
           'cpSpatialIndexSegmentQueryFunc', '__FSBLKCNT64_T_TYPE',
           'cpMomentForCircle', '__uint16_t', 'pid_t',
           '__lldiv_t_defined', 'cpSpaceRemoveConstraint',
           'cpBodyActivateStatic', 'cpvtoangle', 'cpSpatialIndex',
           'cpShapeSegmentQueryImpl', 'HUGE_VAL', 'cpLayers',
           'u_int8_t', 'cpConstraintFree', '__WALL', 'cpBodyInit',
           '__ino64_t', 'cpAreaForSegment', 'M_1_PI',
           'cpSegmentShape', 'cpGrooveJointSetGrooveB', 'UNDERFLOW',
           'strtold', 'l64a', 'FD_ZERO', '__fsblkcnt_t', 'strtoll',
           '__locale_t', 'lcong48', 'cpPolyShape', 'HUGE',
           '__WIFCONTINUED', 'cpRatchetJointAlloc', 'M_2_PI',
           'lrand48', 'cpBodyApplyForce', 'cpMomentForSegment',
           '__WORDSIZE', '_IEEE_', 'cpBBTreeNew', 'cpPivotJointAlloc',
           'cpSimpleMotorGetClass', 'bsearch', 'cpvslerpconst',
           'WEXITED', '_XOPEN_SOURCE',
           'cpSpaceNearestPointQueryNearest', 'mrand48_r', 'cpTrue',
           'cpSegmentShapeInit', 'srand48_r', 'key_t', '__USE_ISOC95',
           'uint', 'cpSimpleMotor', 'drand48_data', '__GLIBC__',
           'cpCircleShapeGetOffset', 'N4wait3DOT_0E',
           'cpSlideJointInit', '__secure_getenv', '__rlim64_t',
           'M_LN2', '__pthread_internal_slist',
           '_XOPEN_SOURCE_EXTENDED', 'cpBodyApplyImpulse',
           '__exception', 'ssize_t', '_XLOCALE_H',
           'cpPinJointGetClass', 'cpSpaceContainsConstraint',
           'jrand48_r', 'le32toh', 'cpSpaceBBQueryFunc',
           'cpSpaceActivateShapesTouchingShape', '__FD_ZERO_STOS',
           'cpfree', '__LONG_LONG_PAIR', '__WCOREDUMP', 'qfcvt_r',
           'finitef', 'pthread_mutexattr_t', 'size_t', '__USE_XOPEN',
           'cpSpaceShapeIteratorFunc', '__time_t_defined', 'strtol_l',
           'cpSpaceReindexStatic', '__USE_POSIX2', 'blkcnt_t',
           'uint_least16_t', 'cpArray',
           'cpSpaceRemoveCollisionHandler', '__qaddr_t', '__NFDBITS',
           'cpPolyShapeAlloc', 'cpDampedSpringInit',
           'cpBBTreeVelocityFunc', 'cpSegmentQueryInfo',
           '__W_EXITCODE', '__key_t', 'islessequal', 'LITTLE_ENDIAN',
           'u_char', 'cpCircleShapeSetOffset', 'uid_t',
           'cpConvexHull', 'u_int64_t', 'u_int16_t', 'cpShapeType',
           'ldexp', 'finite', 'sigset_t', 'CP_SEGMENT_SHAPE',
           'cpShapeUpdate', 'gcvt', '__blksize_t', '__int32_t',
           'modf', '__USE_POSIX', 'cpPolyShapeNew',
           '_BITS_TYPESIZES_H', 'cpSlideJoint', 'CP_POLY_SHAPE',
           'cpBodyUpdateVelocity', 'cpShapeDestroyImpl',
           '_POSIX_SOURCE', 'CP_NUM_SHAPES', 'clock_t', 'WIFSIGNALED',
           'int_fast64_t', 'uint_fast16_t', '__useconds_t',
           '_BITS_WCHAR_H', '__GLIBC_MINOR__', 'cpSpaceNew',
           'cpShapeClass', '__INO64_T_TYPE', 'div_t',
           '__clockid_t_defined', 'cpSpaceInit', '__fsfilcnt64_t',
           '__BYTE_ORDER', '__SQUAD_TYPE',
           'N16pthread_rwlock_t4DOT_16E', 'uint_least8_t',
           'pthread_barrier_t', '__gid_t', '__signbit', 'u_int32_t',
           'pthread_rwlock_t', 'cpCircleShapeSetRadius', 'cpBodyFree',
           'cpSpatialIndexIteratorFunc', 'free', 'cpPivotJointInit',
           'CP_VERSION_RELEASE', '_SYS_TYPES_H',
           'cpBBTreeSetVelocityFunc', '__P',
           'cpConstraintPreStepImpl', 'qsort_r', '__USE_GNU',
           'WUNTRACED', 'cpBodySetMoment', 'random_r', 'htobe16',
           '__WNOTHREAD', 'pthread_attr_t',
           '__attribute_format_arg__', '__u_int', 'cpShape', 'ino_t',
           'M_LOG2E', '_POSIX_C_SOURCE', 'major',
           'cpContactBufferHeader', 'cpSpaceHash', 'qsort', 'valloc',
           'mbtowc', '__W_STOPCODE', 'cpPinJoint', 'cpArbiterTotalKE',
           '__USE_SVID', 'pthread_spinlock_t', 'cpBBWrapVect',
           '__pthread_slist_t', '__USE_ANSI', 'fsblkcnt_t', 'mkdtemp',
           '__ldiv_t_defined', 'cpBodySleepWithGroup', 'ecvt',
           'cpMomentForBox2', 'cpPolyShapeGetVert',
           'cpShapeNearestPointQueryImpl', '_ALLOCA_H',
           '__W_CONTINUED', 'system', '__bswap_constant_32',
           'comparison_fn_t', 'cpGearJoint', 'ino64_t',
           '__USE_ISOC99', 'le16toh', '__DEV_T_TYPE', '__FD_SET_BTS',
           'cpSpaceAddShape', 'mkstemp64', 'ecvt_r',
           'cpConstraintDestroy', '__uint8_t',
           'cpBodyConstraintIteratorFunc',
           'CP_MAX_CONTACTS_PER_ARBITER', '__SIZEOF_PTHREAD_RWLOCK_T',
           '__caddr_t', 'strtod_l', '__blkcnt64_t', 'mkostemp',
           '__STDC_ISO_10646__', 'cpBodyEachArbiter', '_Exit',
           'strtouq', 'cpSegmentShapeGetRadius', 'copysignl',
           'cpGearJointSetRatio', 'cpSpatialIndexRemoveImpl',
           '__USE_LARGEFILE', '__SIZEOF_PTHREAD_COND_T', 'cpSweep1D',
           'cpSweep1DInit', '_FEATURES_H', 'cpArbiterStateCached',
           'cpRotaryLimitJointNew', 'uint64_t', 'WCONTINUED',
           '__REDIRECT_NTH_LDBL', 'pthread_cond_t', 'cpvforangle',
           'cpGearJointGetClass', '_BITS_TYPES_H', 'cpHashSet',
           'pselect', 'PDP_ENDIAN', '__ctype_get_mb_cur_max',
           'cpPinJointNew', 'FP_ZERO', 'SING', '__rlim_t',
           '__FLOAT_WORD_ORDER', 'N4wait3DOT_1E',
           'cpSpaceEachConstraint', 'nlink_t', '__UQUAD_TYPE',
           'cpArbiterThread', 'timeval',
           'cpArbiterTotalImpulseWithFriction',
           'N17cpContactPointSet4DOT_22E',
           'cpRotaryLimitJointGetClass', 'frexpl', 'cpSpaceEachShape',
           '__FD_ISSET_BT', 'cpGearJointNew', '__u_char',
           'cpSpaceRemoveStaticShape', 'frexpf', 'cprealloc',
           'realpath', 'ulong', 'cpArbiterState', 'HUGE_VALF',
           '__clock_t', 'fsfilcnt_t', 'int8_t', '__WIFSTOPPED',
           'cpBB', '__finitel', 'N14pthread_cond_t4DOT_13E',
           'srand48', '__fsfilcnt_t', 'cpSegmentShapeGetNormal',
           'cpShapeDestroy', 'cpBodyPositionFunc', '__quad_t',
           'cpGrooveJointNew', 'cpSpaceSegmentQueryFunc', '__uid_t',
           'MATH_ERRNO', 'WTERMSIG', '__pthread_mutex_s',
           'CP_BUFFER_BYTES', 'a64l', '__USE_ATFILE', 'random',
           'cpvslerp', '__GNU_LIBRARY__', 'cpRatchetJointInit',
           '__swblk_t', 'mode_t', 'strtoull', '__USE_LARGEFILE64',
           'cpDampedRotarySpringAlloc', 'cpRotaryLimitJoint',
           'cpSpatialIndexSegmentQueryImpl', 'htobe64', 'strtod',
           'gid_t', 'cpDampedSpringNew', 'frexp', 'lrand48_r',
           'strtof_l', 'posix_memalign', 'strtoq', '__loff_t',
           'intptr_t', 'cpCollisionHandler', 'FD_CLR', 'int_fast8_t',
           '__RLIM64_T_TYPE', 'erand48_r', 'cpSpaceSegmentQueryFirst',
           'cpSpaceAddConstraint', 'cpGearJointInit',
           'cpGrooveJointInit', 'cpSpaceUseSpatialHash', 'ptsname_r',
           '__GLIBC_HAVE_LONG_LONG', 'cpBodySetPos', 'cpvstr',
           'cpMomentForPoly', '__WCLONE', 'FP_NAN', 'cpBodyDestroy',
           'cpDataPointer', 'cpArbiterStateNormal', 'cpPivotJoint',
           'cpSpatialIndexEachImpl', 'cpSpaceHashInit',
           'cpPivotJointNew', 'cpSpaceReindexShape',
           'cpPolyShapeInit', 'cpSpatialIndexReindexImpl',
           'cpShapeSegmentQuery', 'quad_t', '__bos', 'be32toh',
           '_STDLIB_H', 'strtoul', '__ssize_t', 'finitel',
           'cpSpaceAlloc', 'abort', 'cpCollisionPreSolveFunc',
           'qgcvt', 'lcong48_r', 'quick_exit', 'int16_t', '__FDELT',
           'CP_USE_DOUBLES', 'jrand48', '__warnattr', '__sigset_t',
           'isnan', 'cpArbiterGetNormal', 'cpCircleShape',
           'uint_fast64_t', 'cpBool', 'cpCollisionBeginFunc',
           'WIFCONTINUED', 'cpPostStepFunc', 'ldiv_t',
           'cpArbiterGetContactPointSet', 'FP_INFINITE',
           'cpBBTreeAlloc', 'scalbln', 'copysign', '__USE_XOPEN2K',
           '__FD_SETSIZE', 'cpSpaceRemoveBody',
           'cpBodyGetVelAtWorldPoint', 'htole16',
           'cpSegmentShapeSetRadius', '__intptr_t', 'X_TLOSS',
           'seed48_r', '__timespec_defined', 'ushort', 'M_SQRT1_2',
           '__blkcnt_t', 'PLOSS', 'clockid_t', 'fd_set', 'caddr_t',
           'blkcnt64_t', 'uint16_t', 'cpSpaceRemoveShape', 'srandom',
           '__SIZEOF_PTHREAD_BARRIERATTR_T', 'cpBodySleep',
           'double_t', 'off64_t', 'ptsname', 'cpSweep1DAlloc',
           'alloca', 'cpDampedRotarySpringTorqueFunc',
           'cpSegmentShapeGetA', 'cpSegmentShapeGetB', '__USE_MISC',
           '__isnanf', '__BIT_TYPES_DEFINED__', 'htole64',
           'getsubopt', '__compar_d_fn_t',
           'cpSpaceNearestPointQueryFunc', 'WIFEXITED',
           'N15pthread_mutex_t17__pthread_mutex_s4DOT_10E',
           '__finite', 'FP_ILOGBNAN', 'gnu_dev_major',
           'cpSpatialIndexContainsImpl', 'cpShapeSetBody',
           'M_2_SQRTPI', '__isnan', 'cpHashValue', '_STDINT_H',
           'cpSimpleMotorNew', 'fcvt_r', '_BITS_BYTESWAP_H',
           'WSTOPSIG', 'WNOHANG', 'cpArbiterStateFirstColl',
           '__dev_t', 'cpSimpleMotorAlloc', 'cpSpaceShapeQueryFunc',
           'cpSpatialIndexDestroyImpl', '_SYS_SYSMACROS_H', 'cpGroup',
           'drand48', 'cpSpaceHashNew', 'EXIT_SUCCESS',
           '__suseconds_t', 'cpSpatialIndexReindexObjectImpl',
           'scalblnf', 'u_long', 'cpRotaryLimitJointInit', 'qfcvt',
           'strtold_l', 'cpSpaceAddBody', 'on_exit', 'malloc',
           'cpSpatialIndexBBFunc', '__USE_POSIX199506', '__S64_TYPE',
           '__BIG_ENDIAN', 'srand', 'cpSlideJointNew', 'uintmax_t',
           '__WTERMSIG', 'cpSpaceSetDefaultCollisionHandler',
           'int_fast16_t', 'cpConstraintPostSolveFunc', 'time_t',
           'u_short', 'cpBodyGetVelAtLocalPoint',
           'cpSpaceAddCollisionHandler', 'cpMomentForBox',
           'CP_NO_GROUP', 'fsblkcnt64_t', 'cpRatchetJointNew',
           '_SYS_CDEFS_H', 'pthread_rwlockattr_t', 'setstate',
           'cpShapeCacheDataImpl', 'CP_ALL_LAYERS', 'timespec',
           'cpSpaceBBQuery', '__SIZEOF_PTHREAD_ATTR_T',
           'cpDampedRotarySpringNew', 'cpSlideJointGetClass',
           'isinff', 'cpDampedRotarySpring', 'isnanf', 'calloc',
           'isinfl', 'cpSegmentShapeSetEndpoints', '__REDIRECT_LDBL',
           'cpPolyShapeSetVerts', 'isnanl', 'srandom_r',
           'cpSpaceAddStaticShape', 'CP_PRIVATE',
           'cpPolyShapeGetNumVerts', 'cpSegmentShapeAlloc',
           'drand48_r', 'cpSpaceStep', 'cpSimpleMotorInit',
           '__int64_t', 'nrand48', 'pthread_mutex_t', 'cpBodyAlloc',
           'cpSweep1DNew', 'uint32_t', 'cpvlength', 'cpPolyValidate',
           'suseconds_t', '__MATHCALLX', 'be16toh', 'WSTOPPED',
           'cpBoxShapeInit', 'cpSpacePointQuery', '__isinff',
           '__LITTLE_ENDIAN', 'NAN', '__isinfl', 'pthread_condattr_t',
           'cpBoxShapeInit2', 'pthread_once_t', '__fsid_t', '_ISOC_',
           'cpBBTreeOptimize', 'cpDampedSpring', 'cpBodySetAngle',
           'random_data', 'atoll', 'isnormal', '__uint32_t',
           '__USE_XOPEN2K8', '_STRUCT_TIMEVAL', 'ldiv',
           'cpSpaceReindexShapesForBody', '_XOPEN_', 'WNOWAIT',
           'cpGrooveJointAlloc', 'RAND_MAX', 'setenv',
           'cpBodyVelocityFunc', 'cpSpaceShapeQuery', '__PDP_ENDIAN',
           'cpBodyEachConstraint', 'int32_t', '__u_short', 'loff_t',
           'cpSpaceContainsBody', 'blksize_t', 'cpSpace', 'scalbn',
           '__STDC_IEC_559__', '_BITS_PTHREADTYPES_H', 'WIFSTOPPED',
           'cpSpaceHashAlloc', 'FP_NORMAL', 'register_t',
           'gnu_dev_minor', '_SYS_SELECT_H', 'float_t', 'mblen',
           'cpDampedSpringForceFunc', 'cpSplittingPlane',
           'cpSegmentShapeNew', '__nlink_t', '__compar_fn_t', 'modfl',
           'TLOSS', 'cpArbiterIgnore', 'DOMAIN', 'lldiv', 'rpmatch',
           'cpCircleShapeAlloc', 'mrand48', 'llabs', 'seed48',
           '__clock_t_defined', '__pid_t', 'cpContact', '__id_t',
           'cpConstraint', 'cpArbiter', 'cpArbiterStateIgnore',
           'int_least8_t', 'cpSpaceFree', '__bswap_constant_16',
           'cpCircleShapeNew', 'qecvt_r', '__signbitf',
           '_ISOC99_SOURCE', 'exit', '__signbitl', 'cpRecenterPoly',
           'int_least16_t', '__FD_CLR_BTR',
           'cpConstraintApplyCachedImpulseImpl', 'cpArbiterGetCount',
           'isgreaterequal', '_SVID_SOURCE', 'FD_ISSET',
           'cpGearJointAlloc', 'cpSpatialIndexCountImpl',
           'FP_SUBNORMAL', 'cfree', 'rand', 'cpSpatialIndexFree',
           'cpVersionString', 'cpSpaceAddPostStepCallback',
           '__USE_BSD', '__CONCAT', 'cpShapeFree', 'copysignf',
           'fcvt', '_SIGSET_H_types', 'CP_CIRCLE_SHAPE',
           'uint_least64_t', '_MATH_H_MATHDEF', 'mkostemp64',
           'isgreater', '__SIZEOF_PTHREAD_MUTEX_T', '__USE_UNIX98',
           'dev_t', 'cpShapeNearestPointQuery', 'OVERFLOW',
           'cpSpaceConstraintIteratorFunc', 'cpBodyAssertSane',
           'putenv', 'cpCircleShapeGetRadius', 'cpPinJointInit',
           '__daddr_t', '__sig_atomic_t', 'uintptr_t',
           'cpShapePointQuery', 'cpSpaceEachBody', 'u_int', 'getenv',
           'htobe32', 'atoi', '__fd_mask', 'atol', 'wcstombs',
           'pthread_key_t', '__finitef', 'cpSpaceNearestPointQuery',
           'atof', '__STDC_IEC_559_COMPLEX__', 'strtoull_l',
           'erand48', 'locale_data', 'cpBBTreeInit', 'cpTimestamp',
           'intmax_t', 'cpSegmentShapeSetNeighbors', '_ENDIAN_H',
           'useconds_t', 'cpPivotJointGetClass', 'fd_mask',
           'cpMessage', '__U64_TYPE', 'cpBodyNew', 'FD_SET',
           '__isnanl', 'cpConstraintClass', 'cpFloat', 'initstate',
           '__STRING', 'int64_t', 'cpBodySanityCheck',
           'cpSpatialIndexReindexQueryImpl', '__WCHAR_MIN',
           'uint_fast32_t', 'WEXITSTATUS', 'le64toh', '__GNUC_PREREQ',
           'BYTE_ORDER', '__BLKCNT64_T_TYPE', 'posix_openpt',
           'lldiv_t', 'cpBodyResetForces', 'cpSpacePointQueryFirst',
           'int_least32_t', '__SIZEOF_PTHREAD_RWLOCKATTR_T',
           '__u_quad_t', 'modff', 'clearenv', 'mkstemp',
           'cpArbiterTotalImpulse', '_BSD_SOURCE',
           'cpSpatialIndexClass', 'fsid_t', '_LARGEFILE64_SOURCE',
           'unsetenv', '__va_arg_pack', 'FD_SETSIZE', 'initstate_r',
           'cpAreaForPoly', 'cpResetShapeIdCounter', '__ino_t',
           'cpDampedRotarySpringInit', '_SIGSET_NWORDS', 'isinf',
           '__va_arg_pack_len', 'cpSpaceSegmentQuery', '__bos0',
           'cpComponentNode', 'cpCircleShapeInit', 'cpRatchetJoint',
           'strtoul_l', 'locale_t', '__isinf',
           'cpDampedSpringGetClass', '__socklen_t', 'EXIT_FAILURE',
           'M_SQRT2', 'MATH_ERREXCEPT', 'NFDBITS']
