from cffi import FFI
ffi = FFI()
ffi.cdef("""
    
    // chipmunk_types.h
    
    typedef double cpFloat;
    typedef unsigned char cpBool;
    typedef void * cpDataPointer;
	typedef uintptr_t cpCollisionType;
	typedef uintptr_t cpGroup;
	typedef unsigned int cpBitmask;
	typedef unsigned int cpTimestamp;                    
	typedef struct cpVect{cpFloat x,y;} cpVect;	
	typedef struct cpTransform {
		cpFloat a, b, c, d, tx, ty;
	} cpTransform;    
            
    // chipmunk.h
    
    typedef struct cpArray cpArray;
    typedef struct cpHashSet cpHashSet;

    typedef struct cpBody cpBody;

    typedef struct cpShape cpShape;
    typedef struct cpCircleShape cpCircleShape;
    typedef struct cpSegmentShape cpSegmentShape;
    typedef struct cpPolyShape cpPolyShape;

    typedef struct cpConstraint cpConstraint;
    typedef struct cpPinJoint cpPinJoint;
    typedef struct cpSlideJoint cpSlideJoint;
    typedef struct cpPivotJoint cpPivotJoint;
    typedef struct cpGrooveJoint cpGrooveJoint;
    typedef struct cpDampedSpring cpDampedSpring;
    typedef struct cpDampedRotarySpring cpDampedRotarySpring;
    typedef struct cpRotaryLimitJoint cpRotaryLimitJoint;
    typedef struct cpRatchetJoint cpRatchetJoint;
    typedef struct cpGearJoint cpGearJoint;
    typedef struct cpSimpleMotorJoint cpSimpleMotorJoint;

    typedef struct cpCollisionHandler cpCollisionHandler;
    typedef struct cpContactPointSet cpContactPointSet;
    typedef struct cpArbiter cpArbiter;

    typedef struct cpSpace cpSpace;
    
    // cpVect.h
    
    // cbBB.h
    typedef struct cpBB{
        cpFloat l, b, r ,t;
    } cpBB;

    // cpTransform.h
    //cpSpatialIndex.h
    //cpArbiter.h
    //cpBody.h
    //



    // GENERAL
    
    
    /// Calculate the moment of inertia for a circle.
    /// @c r1 and @c r2 are the inner and outer diameters. A solid circle has an inner diameter of 0.
    cpFloat cpMomentForCircle(cpFloat m, cpFloat r1, cpFloat r2, cpVect offset);

    /// Calculate area of a hollow circle.
    /// @c r1 and @c r2 are the inner and outer diameters. A solid circle has an inner diameter of 0.
    cpFloat cpAreaForCircle(cpFloat r1, cpFloat r2);

    /// Calculate the moment of inertia for a line segment.
    /// Beveling radius is not supported.
    cpFloat cpMomentForSegment(cpFloat m, cpVect a, cpVect b, cpFloat radius);

    /// Calculate the area of a fattened (capsule shaped) line segment.
    cpFloat cpAreaForSegment(cpVect a, cpVect b, cpFloat radius);

    /// Calculate the moment of inertia for a solid polygon shape assuming it's center of gravity is at it's centroid. The offset is added to each vertex.
    cpFloat cpMomentForPoly(cpFloat m, int count, const cpVect *verts, cpVect offset, cpFloat radius);

    /// Calculate the signed area of a polygon. A Clockwise winding gives positive area.
    /// This is probably backwards from what you expect, but matches Chipmunk's the winding for poly shapes.
    cpFloat cpAreaForPoly(const int count, const cpVect *verts, cpFloat radius);

    /// Calculate the natural centroid of a polygon.
    cpVect cpCentroidForPoly(const int count, const cpVect *verts);

    /// Calculate the moment of inertia for a solid box.
    cpFloat cpMomentForBox(cpFloat m, cpFloat width, cpFloat height);

    /// Calculate the moment of inertia for a solid box.
    cpFloat cpMomentForBox2(cpFloat m, cpBB box);

    // SPACE
        
    cpSpace* cpSpaceNew(void);
    void cpSpaceStep(cpSpace *space, cpFloat dt);


""")
lib = "chipmunk.dll"
C = ffi.dlopen(lib)                     # loads the entire C namespace

