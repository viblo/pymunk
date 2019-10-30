h = """

    ///////////////////////////////////////////
    // chipmunk_types.h
    ///////////////////////////////////////////

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

    ///////////////////////////////////////////
    // chipmunk.h
    ///////////////////////////////////////////

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

    ///////////////////////////////////////////
    // cpVect.h
    ///////////////////////////////////////////

    ///////////////////////////////////////////
    // cbBB.h
    ///////////////////////////////////////////

    typedef struct cpBB{
        cpFloat l, b, r ,t;
    } cpBB;

    ///////////////////////////////////////////
    // cpTransform.h
    ///////////////////////////////////////////

    ///////////////////////////////////////////
    // cpSpatialIndex.h
    ///////////////////////////////////////////

    ///////////////////////////////////////////
    // cpArbiter.h
    ///////////////////////////////////////////

    #define CP_MAX_CONTACTS_PER_ARBITER 2
    /// Get the restitution (elasticity) that will be applied to the pair of colliding objects.
    cpFloat cpArbiterGetRestitution(const cpArbiter *arb);
    /// Override the restitution (elasticity) that will be applied to the pair of colliding objects.
    void cpArbiterSetRestitution(cpArbiter *arb, cpFloat restitution);
    /// Get the friction coefficient that will be applied to the pair of colliding objects.
    cpFloat cpArbiterGetFriction(const cpArbiter *arb);
    /// Override the friction coefficient that will be applied to the pair of colliding objects.
    void cpArbiterSetFriction(cpArbiter *arb, cpFloat friction);

    // Get the relative surface velocity of the two shapes in contact.
    cpVect cpArbiterGetSurfaceVelocity(cpArbiter *arb);

    // Override the relative surface velocity of the two shapes in contact.
    // By default this is calculated to be the difference of the two surface velocities clamped to the tangent plane.
    void cpArbiterSetSurfaceVelocity(cpArbiter *arb, cpVect vr);

    /// Get the user data pointer associated with this pair of colliding objects.
    cpDataPointer cpArbiterGetUserData(const cpArbiter *arb);
    /// Set a user data point associated with this pair of colliding objects.
    /// If you need to perform any cleanup for this pointer, you must do it yourself, in the separate callback for instance.
    void cpArbiterSetUserData(cpArbiter *arb, cpDataPointer userData);

    /// Calculate the total impulse including the friction that was applied by this arbiter.
    /// This function should only be called from a post-solve, post-step or cpBodyEachArbiter callback.
    cpVect cpArbiterTotalImpulse(const cpArbiter *arb);
    /// Calculate the amount of energy lost in a collision including static, but not dynamic friction.
    /// This function should only be called from a post-solve, post-step or cpBodyEachArbiter callback.
    cpFloat cpArbiterTotalKE(const cpArbiter *arb);

    /// Mark a collision pair to be ignored until the two objects separate.
    /// Pre-solve and post-solve callbacks will not be called, but the separate callback will be called.
    cpBool cpArbiterIgnore(cpArbiter *arb);

    /// Return the colliding shapes involved for this arbiter.
    /// The order of their cpSpace.collision_type values will match
    /// the order set when the collision handler was registered.
    void cpArbiterGetShapes(const cpArbiter *arb, cpShape **a, cpShape **b);

    /// Return the colliding bodies involved for this arbiter.
    /// The order of the cpSpace.collision_type the bodies are associated with values will match
    /// the order set when the collision handler    was registered.
    void cpArbiterGetBodies(const cpArbiter *arb, cpBody **a, cpBody **b);

    /// A struct that wraps up the important collision data for an arbiter.
    struct cpContactPointSet {
        /// The number of contact points in the set.
        int count;

        /// The normal of the collision.
        cpVect normal;

        /// The array of contact points.
        struct {
            /// The position of the contact on the surface of each shape.
            cpVect pointA, pointB;
            /// Penetration distance of the two shapes. Overlapping means it will be negative.
            /// This value is calculated as cpvdot(cpvsub(point2, point1), normal) and is ignored by cpArbiterSetContactPointSet().
            cpFloat distance;
        } points[CP_MAX_CONTACTS_PER_ARBITER];
    };

    /// Return a contact set from an arbiter.
    cpContactPointSet cpArbiterGetContactPointSet(const cpArbiter *arb);

    /// Replace the contact point set for an arbiter.
    /// This can be a very powerful feature, but use it with caution!
    void cpArbiterSetContactPointSet(cpArbiter *arb, cpContactPointSet *set);

    /// Returns true if this is the first step a pair of objects started colliding.
    cpBool cpArbiterIsFirstContact(const cpArbiter *arb);
    /// Returns true if the separate callback is due to a shape being removed from the space.
    cpBool cpArbiterIsRemoval(const cpArbiter *arb);

    /// Get the number of contact points for this arbiter.
    int cpArbiterGetCount(const cpArbiter *arb);
    /// Get the normal of the collision.
    cpVect cpArbiterGetNormal(const cpArbiter *arb);
    /// Get the position of the @c ith contact point on the surface of the first shape.
    cpVect cpArbiterGetPointA(const cpArbiter *arb, int i);
    /// Get the position of the @c ith contact point on the surface of the second shape.
    cpVect cpArbiterGetPointB(const cpArbiter *arb, int i);
    /// Get the depth of the @c ith contact point.
    cpFloat cpArbiterGetDepth(const cpArbiter *arb, int i);

    /// If you want a custom callback to invoke the wildcard callback for the first collision type, you must call this function explicitly.
    /// You must decide how to handle the wildcard's return value since it may disagree with the other wildcard handler's return value or your own.
    cpBool cpArbiterCallWildcardBeginA(cpArbiter *arb, cpSpace *space);
    /// If you want a custom callback to invoke the wildcard callback for the second collision type, you must call this function explicitly.
    /// You must decide how to handle the wildcard's return value since it may disagree with the other wildcard handler's return value or your own.
    cpBool cpArbiterCallWildcardBeginB(cpArbiter *arb, cpSpace *space);

    /// If you want a custom callback to invoke the wildcard callback for the first collision type, you must call this function explicitly.
    /// You must decide how to handle the wildcard's return value since it may disagree with the other wildcard handler's return value or your own.
    cpBool cpArbiterCallWildcardPreSolveA(cpArbiter *arb, cpSpace *space);
    /// If you want a custom callback to invoke the wildcard callback for the second collision type, you must call this function explicitly.
    /// You must decide how to handle the wildcard's return value since it may disagree with the other wildcard handler's return value or your own.
    cpBool cpArbiterCallWildcardPreSolveB(cpArbiter *arb, cpSpace *space);

    /// If you want a custom callback to invoke the wildcard callback for the first collision type, you must call this function explicitly.
    void cpArbiterCallWildcardPostSolveA(cpArbiter *arb, cpSpace *space);
    /// If you want a custom callback to invoke the wildcard callback for the second collision type, you must call this function explicitly.
    void cpArbiterCallWildcardPostSolveB(cpArbiter *arb, cpSpace *space);

    /// If you want a custom callback to invoke the wildcard callback for the first collision type, you must call this function explicitly.
    void cpArbiterCallWildcardSeparateA(cpArbiter *arb, cpSpace *space);
    /// If you want a custom callback to invoke the wildcard callback for the second collision type, you must call this function explicitly.
    void cpArbiterCallWildcardSeparateB(cpArbiter *arb, cpSpace *space);

    ///////////////////////////////////////////
    // cpBody.h
    ///////////////////////////////////////////

    /// @defgroup cpBody cpBody
    /// Chipmunk's rigid body type. Rigid bodies hold the physical properties of an object like
    /// it's mass, and position and velocity of it's center of gravity. They don't have an shape on their own.
    /// They are given a shape by creating collision shapes (cpShape) that point to the body.
    /// @{

    typedef enum cpBodyType {
        /// A dynamic body is one that is affected by gravity, forces, and collisions.
        /// This is the default body type.
        CP_BODY_TYPE_DYNAMIC,
        /// A kinematic body is an infinite mass, user controlled body that is not affected by gravity, forces or collisions.
        /// Instead the body only moves based on it's velocity.
        /// Dynamic bodies collide normally with kinematic bodies, though the kinematic body will be unaffected.
        /// Collisions between two kinematic bodies, or a kinematic body and a static body produce collision callbacks, but no collision response.
        CP_BODY_TYPE_KINEMATIC,
        /// A static body is a body that never (or rarely) moves. If you move a static body, you must call one of the cpSpaceReindex*() functions.
        /// Chipmunk uses this information to optimize the collision detection.
        /// Static bodies do not produce collision callbacks when colliding with other static bodies.
        CP_BODY_TYPE_STATIC,
    } cpBodyType;

    /// Rigid body velocity update function type.
    typedef void (*cpBodyVelocityFunc)(cpBody *body, cpVect gravity, cpFloat damping, cpFloat dt);
    /// Rigid body position update function type.
    typedef void (*cpBodyPositionFunc)(cpBody *body, cpFloat dt);

    /// Allocate a cpBody.
    cpBody* cpBodyAlloc(void);
    /// Initialize a cpBody.
    cpBody* cpBodyInit(cpBody *body, cpFloat mass, cpFloat moment);
    /// Allocate and initialize a cpBody.
    cpBody* cpBodyNew(cpFloat mass, cpFloat moment);

    /// Allocate and initialize a cpBody, and set it as a kinematic body.
    cpBody* cpBodyNewKinematic(void);
    /// Allocate and initialize a cpBody, and set it as a static body.
    cpBody* cpBodyNewStatic(void);

    /// Destroy a cpBody.
    void cpBodyDestroy(cpBody *body);
    /// Destroy and free a cpBody.
    void cpBodyFree(cpBody *body);

    // Defined in cpSpace.c
    /// Wake up a sleeping or idle body.
    void cpBodyActivate(cpBody *body);
    /// Wake up any sleeping or idle bodies touching a static body.
    void cpBodyActivateStatic(cpBody *body, cpShape *filter);

    /// Force a body to fall asleep immediately.
    void cpBodySleep(cpBody *body);
    /// Force a body to fall asleep immediately along with other bodies in a group.
    void cpBodySleepWithGroup(cpBody *body, cpBody *group);

    /// Returns true if the body is sleeping.
    cpBool cpBodyIsSleeping(const cpBody *body);

    /// Get the type of the body.
    cpBodyType cpBodyGetType(cpBody *body);
    /// Set the type of the body.
    void cpBodySetType(cpBody *body, cpBodyType type);

    /// Get the space this body is added to.
    cpSpace* cpBodyGetSpace(const cpBody *body);

    /// Get the mass of the body.
    cpFloat cpBodyGetMass(const cpBody *body);
    /// Set the mass of the body.
    void cpBodySetMass(cpBody *body, cpFloat m);

    /// Get the moment of inertia of the body.
    cpFloat cpBodyGetMoment(const cpBody *body);
    /// Set the moment of inertia of the body.
    void cpBodySetMoment(cpBody *body, cpFloat i);

    /// Set the position of a body.
    cpVect cpBodyGetPosition(const cpBody *body);
    /// Set the position of the body.
    void cpBodySetPosition(cpBody *body, cpVect pos);

    /// Get the offset of the center of gravity in body local coordinates.
    cpVect cpBodyGetCenterOfGravity(const cpBody *body);
    /// Set the offset of the center of gravity in body local coordinates.
    void cpBodySetCenterOfGravity(cpBody *body, cpVect cog);

    /// Get the velocity of the body.
    cpVect cpBodyGetVelocity(const cpBody *body);
    /// Set the velocity of the body.
    void cpBodySetVelocity(cpBody *body, cpVect velocity);

    /// Get the force applied to the body for the next time step.
    cpVect cpBodyGetForce(const cpBody *body);
    /// Set the force applied to the body for the next time step.
    void cpBodySetForce(cpBody *body, cpVect force);

    /// Get the angle of the body.
    cpFloat cpBodyGetAngle(const cpBody *body);
    /// Set the angle of a body.
    void cpBodySetAngle(cpBody *body, cpFloat a);

    /// Get the angular velocity of the body.
    cpFloat cpBodyGetAngularVelocity(const cpBody *body);
    /// Set the angular velocity of the body.
    void cpBodySetAngularVelocity(cpBody *body, cpFloat angularVelocity);

    /// Get the torque applied to the body for the next time step.
    cpFloat cpBodyGetTorque(const cpBody *body);
    /// Set the torque applied to the body for the next time step.
    void cpBodySetTorque(cpBody *body, cpFloat torque);

    /// Get the rotation vector of the body. (The x basis vector of it's transform.)
    cpVect cpBodyGetRotation(const cpBody *body);

    /// Get the user data pointer assigned to the body.
    cpDataPointer cpBodyGetUserData(const cpBody *body);
    /// Set the user data pointer assigned to the body.
    void cpBodySetUserData(cpBody *body, cpDataPointer userData);

    /// Set the callback used to update a body's velocity.
    void cpBodySetVelocityUpdateFunc(cpBody *body, cpBodyVelocityFunc velocityFunc);
    /// Set the callback used to update a body's position.
    /// NOTE: It's not generally recommended to override this unless you call the default position update function.
    void cpBodySetPositionUpdateFunc(cpBody *body, cpBodyPositionFunc positionFunc);

    /// Default velocity integration function..
    void cpBodyUpdateVelocity(cpBody *body, cpVect gravity, cpFloat damping, cpFloat dt);
    /// Default position integration function.
    void cpBodyUpdatePosition(cpBody *body, cpFloat dt);

    /// Convert body relative/local coordinates to absolute/world coordinates.
    cpVect cpBodyLocalToWorld(const cpBody *body, const cpVect point);
    /// Convert body absolute/world coordinates to  relative/local coordinates.
    cpVect cpBodyWorldToLocal(const cpBody *body, const cpVect point);

    /// Apply a force to a body. Both the force and point are expressed in world coordinates.
    void cpBodyApplyForceAtWorldPoint(cpBody *body, cpVect force, cpVect point);
    /// Apply a force to a body. Both the force and point are expressed in body local coordinates.
    void cpBodyApplyForceAtLocalPoint(cpBody *body, cpVect force, cpVect point);

    /// Apply an impulse to a body. Both the impulse and point are expressed in world coordinates.
    void cpBodyApplyImpulseAtWorldPoint(cpBody *body, cpVect impulse, cpVect point);
    /// Apply an impulse to a body. Both the impulse and point are expressed in body local coordinates.
    void cpBodyApplyImpulseAtLocalPoint(cpBody *body, cpVect impulse, cpVect point);

    /// Get the velocity on a body (in world units) at a point on the body in world coordinates.
    cpVect cpBodyGetVelocityAtWorldPoint(const cpBody *body, cpVect point);
    /// Get the velocity on a body (in world units) at a point on the body in local coordinates.
    cpVect cpBodyGetVelocityAtLocalPoint(const cpBody *body, cpVect point);

    /// Get the amount of kinetic energy contained by the body.
    cpFloat cpBodyKineticEnergy(const cpBody *body);

    /// Body/shape iterator callback function type.
    typedef void (*cpBodyShapeIteratorFunc)(cpBody *body, cpShape *shape, void *data);
    /// Call @c func once for each shape attached to @c body and added to the space.
    void cpBodyEachShape(cpBody *body, cpBodyShapeIteratorFunc func, void *data);

    /// Body/constraint iterator callback function type.
    typedef void (*cpBodyConstraintIteratorFunc)(cpBody *body, cpConstraint *constraint, void *data);
    /// Call @c func once for each constraint attached to @c body and added to the space.
    void cpBodyEachConstraint(cpBody *body, cpBodyConstraintIteratorFunc func, void *data);

    /// Body/arbiter iterator callback function type.
    typedef void (*cpBodyArbiterIteratorFunc)(cpBody *body, cpArbiter *arbiter, void *data);
    /// Call @c func once for each arbiter that is currently active on the body.
    void cpBodyEachArbiter(cpBody *body, cpBodyArbiterIteratorFunc func, void *data);


    ///////////////////////////////////////////
    // cpShape.h
    ///////////////////////////////////////////


    /// Point query info struct.
    typedef struct cpPointQueryInfo {
        /// The nearest shape, NULL if no shape was within range.
        const cpShape *shape;
        /// The closest point on the shape's surface. (in world space coordinates)
        cpVect point;
        /// The distance to the point. The distance is negative if the point is inside the shape.
        cpFloat distance;
        /// The gradient of the signed distance function.
        /// The value should be similar to info.p/info.d, but accurate even for very small values of info.d.
        cpVect gradient;
    } cpPointQueryInfo;

    /// Segment query info struct.
    typedef struct cpSegmentQueryInfo {
        /// The shape that was hit, or NULL if no collision occured.
        const cpShape *shape;
        /// The point of impact.
        cpVect point;
        /// The normal of the surface hit.
        cpVect normal;
        /// The normalized distance along the query segment in the range [0, 1].
        cpFloat alpha;
    } cpSegmentQueryInfo;

    /// Fast collision filtering type that is used to determine if two objects collide before calling collision or query callbacks.
    typedef struct cpShapeFilter {
        /// Two objects with the same non-zero group value do not collide.
        /// This is generally used to group objects in a composite object together to disable self collisions.
        cpGroup group;
        /// A bitmask of user definable categories that this object belongs to.
        /// The category/mask combinations of both objects in a collision must agree for a collision to occur.
        cpBitmask categories;
        /// A bitmask of user definable category types that this object object collides with.
        /// The category/mask combinations of both objects in a collision must agree for a collision to occur.
        cpBitmask mask;
    } cpShapeFilter;

    /// Collision filter value for a shape that will collide with anything except CP_SHAPE_FILTER_NONE.
    // static const cpShapeFilter CP_SHAPE_FILTER_ALL = {CP_NO_GROUP, CP_ALL_CATEGORIES, CP_ALL_CATEGORIES};
    /// Collision filter value for a shape that does not collide with anything.
    // static const cpShapeFilter CP_SHAPE_FILTER_NONE = {CP_NO_GROUP, ~CP_ALL_CATEGORIES, ~CP_ALL_CATEGORIES};

    /// Create a new collision filter.
    /*static inline cpShapeFilter
    cpShapeFilterNew(cpGroup group, cpBitmask categories, cpBitmask mask)
    {
        cpShapeFilter filter = {group, categories, mask};
        return filter;
    }
    */
    /// Destroy a shape.
    void cpShapeDestroy(cpShape *shape);
    /// Destroy and Free a shape.
    void cpShapeFree(cpShape *shape);

    /// Update, cache and return the bounding box of a shape based on the body it's attached to.
    cpBB cpShapeCacheBB(cpShape *shape);
    /// Update, cache and return the bounding box of a shape with an explicit transformation.
    cpBB cpShapeUpdate(cpShape *shape, cpTransform transform);

    /// Perform a nearest point query. It finds the closest point on the surface of shape to a specific point.
    /// The value returned is the distance between the points. A negative distance means the point is inside the shape.
    cpFloat cpShapePointQuery(const cpShape *shape, cpVect p, cpPointQueryInfo *out);

    /// Perform a segment query against a shape. @c info must be a pointer to a valid cpSegmentQueryInfo structure.
    cpBool cpShapeSegmentQuery(const cpShape *shape, cpVect a, cpVect b, cpFloat radius, cpSegmentQueryInfo *info);

    /// Return contact information about two shapes.
    cpContactPointSet cpShapesCollide(const cpShape *a, const cpShape *b);

    /// The cpSpace this body is added to.
    cpSpace* cpShapeGetSpace(const cpShape *shape);

    /// The cpBody this shape is connected to.
    cpBody* cpShapeGetBody(const cpShape *shape);
    /// Set the cpBody this shape is connected to.
    /// Can only be used if the shape is not currently added to a space.
    void cpShapeSetBody(cpShape *shape, cpBody *body);

    /// Get the mass of the shape if you are having Chipmunk calculate mass properties for you.
    cpFloat cpShapeGetMass(cpShape *shape);
    /// Set the mass of this shape to have Chipmunk calculate mass properties for you.
    void cpShapeSetMass(cpShape *shape, cpFloat mass);

    /// Get the density of the shape if you are having Chipmunk calculate mass properties for you.
    cpFloat cpShapeGetDensity(cpShape *shape);
    /// Set the density  of this shape to have Chipmunk calculate mass properties for you.
    void cpShapeSetDensity(cpShape *shape, cpFloat density);

    /// Get the calculated moment of inertia for this shape.
    cpFloat cpShapeGetMoment(cpShape *shape);
    /// Get the calculated area of this shape.
    cpFloat cpShapeGetArea(cpShape *shape);
    /// Get the centroid of this shape.
    cpVect cpShapeGetCenterOfGravity(cpShape *shape);

    /// Get the bounding box that contains the shape given it's current position and angle.
    cpBB cpShapeGetBB(const cpShape *shape);

    /// Get if the shape is set to be a sensor or not.
    cpBool cpShapeGetSensor(const cpShape *shape);
    /// Set if the shape is a sensor or not.
    void cpShapeSetSensor(cpShape *shape, cpBool sensor);

    /// Get the elasticity of this shape.
    cpFloat cpShapeGetElasticity(const cpShape *shape);
    /// Set the elasticity of this shape.
    void cpShapeSetElasticity(cpShape *shape, cpFloat elasticity);

    /// Get the friction of this shape.
    cpFloat cpShapeGetFriction(const cpShape *shape);
    /// Set the friction of this shape.
    void cpShapeSetFriction(cpShape *shape, cpFloat friction);

    /// Get the surface velocity of this shape.
    cpVect cpShapeGetSurfaceVelocity(const cpShape *shape);
    /// Set the surface velocity of this shape.
    void cpShapeSetSurfaceVelocity(cpShape *shape, cpVect surfaceVelocity);

    /// Get the user definable data pointer of this shape.
    cpDataPointer cpShapeGetUserData(const cpShape *shape);
    /// Set the user definable data pointer of this shape.
    void cpShapeSetUserData(cpShape *shape, cpDataPointer userData);

    /// Set the collision type of this shape.
    cpCollisionType cpShapeGetCollisionType(const cpShape *shape);
    /// Get the collision type of this shape.
    void cpShapeSetCollisionType(cpShape *shape, cpCollisionType collisionType);

    /// Get the collision filtering parameters of this shape.
    cpShapeFilter cpShapeGetFilter(const cpShape *shape);
    /// Set the collision filtering parameters of this shape.
    void cpShapeSetFilter(cpShape *shape, cpShapeFilter filter);


    /// @}
    /// @defgroup cpCircleShape cpCircleShape

    /// Allocate a circle shape.
    cpCircleShape* cpCircleShapeAlloc(void);
    /// Initialize a circle shape.
    cpCircleShape* cpCircleShapeInit(cpCircleShape *circle, cpBody *body, cpFloat radius, cpVect offset);
    /// Allocate and initialize a circle shape.
    cpShape* cpCircleShapeNew(cpBody *body, cpFloat radius, cpVect offset);

    /// Get the offset of a circle shape.
    cpVect cpCircleShapeGetOffset(const cpShape *shape);
    /// Get the radius of a circle shape.
    cpFloat cpCircleShapeGetRadius(const cpShape *shape);

    /// @}
    /// @defgroup cpSegmentShape cpSegmentShape

    /// Allocate a segment shape.
    cpSegmentShape* cpSegmentShapeAlloc(void);
    /// Initialize a segment shape.
    cpSegmentShape* cpSegmentShapeInit(cpSegmentShape *seg, cpBody *body, cpVect a, cpVect b, cpFloat radius);
    /// Allocate and initialize a segment shape.
    cpShape* cpSegmentShapeNew(cpBody *body, cpVect a, cpVect b, cpFloat radius);

    /// Let Chipmunk know about the geometry of adjacent segments to avoid colliding with endcaps.
    void cpSegmentShapeSetNeighbors(cpShape *shape, cpVect prev, cpVect next);

    /// Get the first endpoint of a segment shape.
    cpVect cpSegmentShapeGetA(const cpShape *shape);
    /// Get the second endpoint of a segment shape.
    cpVect cpSegmentShapeGetB(const cpShape *shape);
    /// Get the normal of a segment shape.
    cpVect cpSegmentShapeGetNormal(const cpShape *shape);
    /// Get the first endpoint of a segment shape.
    cpFloat cpSegmentShapeGetRadius(const cpShape *shape);

    /// @}

    ///////////////////////////////////////////
    // cpPolyShape.h
    ///////////////////////////////////////////

    /// @defgroup cpPolyShape cpPolyShape
    /// @{

    /// Allocate a polygon shape.
    cpPolyShape* cpPolyShapeAlloc(void);
    /// Initialize a polygon shape with rounded corners.
    /// A convex hull will be created from the vertexes.
    cpPolyShape* cpPolyShapeInit(cpPolyShape *poly, cpBody *body, int count, const cpVect *verts, cpTransform transform, cpFloat radius);
    /// Initialize a polygon shape with rounded corners.
    /// The vertexes must be convex with a counter-clockwise winding.
    cpPolyShape* cpPolyShapeInitRaw(cpPolyShape *poly, cpBody *body, int count, const cpVect *verts, cpFloat radius);
    /// Allocate and initialize a polygon shape with rounded corners.
    /// A convex hull will be created from the vertexes.
    cpShape* cpPolyShapeNew(cpBody *body, int count, const cpVect *verts, cpTransform transform, cpFloat radius);
    /// Allocate and initialize a polygon shape with rounded corners.
    /// The vertexes must be convex with a counter-clockwise winding.
    cpShape* cpPolyShapeNewRaw(cpBody *body, int count, const cpVect *verts, cpFloat radius);

    /// Initialize a box shaped polygon shape with rounded corners.
    cpPolyShape* cpBoxShapeInit(cpPolyShape *poly, cpBody *body, cpFloat width, cpFloat height, cpFloat radius);
    /// Initialize an offset box shaped polygon shape with rounded corners.
    cpPolyShape* cpBoxShapeInit2(cpPolyShape *poly, cpBody *body, cpBB box, cpFloat radius);
    /// Allocate and initialize a box shaped polygon shape.
    cpShape* cpBoxShapeNew(cpBody *body, cpFloat width, cpFloat height, cpFloat radius);
    /// Allocate and initialize an offset box shaped polygon shape.
    cpShape* cpBoxShapeNew2(cpBody *body, cpBB box, cpFloat radius);

    /// Get the number of verts in a polygon shape.
    int cpPolyShapeGetCount(const cpShape *shape);
    /// Get the @c ith vertex of a polygon shape.
    cpVect cpPolyShapeGetVert(const cpShape *shape, int index);
    /// Get the radius of a polygon shape.
    cpFloat cpPolyShapeGetRadius(const cpShape *shape);

    ///////////////////////////////////////////
    // cpConstraint.h
    ///////////////////////////////////////////

    /// Callback function type that gets called before solving a joint.
    typedef void (*cpConstraintPreSolveFunc)(cpConstraint *constraint, cpSpace *space);
    /// Callback function type that gets called after solving a joint.
    typedef void (*cpConstraintPostSolveFunc)(cpConstraint *constraint, cpSpace *space);

    /// Destroy a constraint.
    void cpConstraintDestroy(cpConstraint *constraint);
    /// Destroy and free a constraint.
    void cpConstraintFree(cpConstraint *constraint);

    /// Get the cpSpace this constraint is added to.
    cpSpace* cpConstraintGetSpace(const cpConstraint *constraint);

    /// Get the first body the constraint is attached to.
    cpBody* cpConstraintGetBodyA(const cpConstraint *constraint);

    /// Get the second body the constraint is attached to.
    cpBody* cpConstraintGetBodyB(const cpConstraint *constraint);

    /// Get the maximum force that this constraint is allowed to use.
    cpFloat cpConstraintGetMaxForce(const cpConstraint *constraint);
    /// Set the maximum force that this constraint is allowed to use. (defaults to INFINITY)
    void cpConstraintSetMaxForce(cpConstraint *constraint, cpFloat maxForce);

    /// Get rate at which joint error is corrected.
    cpFloat cpConstraintGetErrorBias(const cpConstraint *constraint);
    /// Set rate at which joint error is corrected.
    /// Defaults to pow(1.0 - 0.1, 60.0) meaning that it will
    /// correct 10% of the error every 1/60th of a second.
    void cpConstraintSetErrorBias(cpConstraint *constraint, cpFloat errorBias);

    /// Get the maximum rate at which joint error is corrected.
    cpFloat cpConstraintGetMaxBias(const cpConstraint *constraint);
    /// Set the maximum rate at which joint error is corrected. (defaults to INFINITY)
    void cpConstraintSetMaxBias(cpConstraint *constraint, cpFloat maxBias);

    /// Get if the two bodies connected by the constraint are allowed to collide or not.
    cpBool cpConstraintGetCollideBodies(const cpConstraint *constraint);
    /// Set if the two bodies connected by the constraint are allowed to collide or not. (defaults to cpFalse)
    void cpConstraintSetCollideBodies(cpConstraint *constraint, cpBool collideBodies);

    /// Get the pre-solve function that is called before the solver runs.
    cpConstraintPreSolveFunc cpConstraintGetPreSolveFunc(const cpConstraint *constraint);
    /// Set the pre-solve function that is called before the solver runs.
    void cpConstraintSetPreSolveFunc(cpConstraint *constraint, cpConstraintPreSolveFunc preSolveFunc);

    /// Get the post-solve function that is called before the solver runs.
    cpConstraintPostSolveFunc cpConstraintGetPostSolveFunc(const cpConstraint *constraint);
    /// Set the post-solve function that is called before the solver runs.
    void cpConstraintSetPostSolveFunc(cpConstraint *constraint, cpConstraintPostSolveFunc postSolveFunc);

    /// Get the user definable data pointer for this constraint
    cpDataPointer cpConstraintGetUserData(const cpConstraint *constraint);
    /// Set the user definable data pointer for this constraint
    void cpConstraintSetUserData(cpConstraint *constraint, cpDataPointer userData);

    /// Get the last impulse applied by this constraint.
    cpFloat cpConstraintGetImpulse(cpConstraint *constraint);

    ///////////////////////////////////////////
    // cpPinJoint.h
    ///////////////////////////////////////////

    /// Check if a constraint is a pin joint.
    cpBool cpConstraintIsPinJoint(const cpConstraint *constraint);

    /// Allocate a pin joint.
    cpPinJoint* cpPinJointAlloc(void);
    /// Initialize a pin joint.
    cpPinJoint* cpPinJointInit(cpPinJoint *joint, cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB);
    /// Allocate and initialize a pin joint.
    cpConstraint* cpPinJointNew(cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB);

    /// Get the location of the first anchor relative to the first body.
    cpVect cpPinJointGetAnchorA(const cpConstraint *constraint);
    /// Set the location of the first anchor relative to the first body.
    void cpPinJointSetAnchorA(cpConstraint *constraint, cpVect anchorA);

    /// Get the location of the second anchor relative to the second body.
    cpVect cpPinJointGetAnchorB(const cpConstraint *constraint);
    /// Set the location of the second anchor relative to the second body.
    void cpPinJointSetAnchorB(cpConstraint *constraint, cpVect anchorB);

    /// Get the distance the joint will maintain between the two anchors.
    cpFloat cpPinJointGetDist(const cpConstraint *constraint);
    /// Set the distance the joint will maintain between the two anchors.
    void cpPinJointSetDist(cpConstraint *constraint, cpFloat dist);

    ///////////////////////////////////////////
    // cpSlideJoint.h
    ///////////////////////////////////////////

    /// Check if a constraint is a slide joint.
    cpBool cpConstraintIsSlideJoint(const cpConstraint *constraint);

    /// Allocate a slide joint.
    cpSlideJoint* cpSlideJointAlloc(void);
    /// Initialize a slide joint.
    cpSlideJoint* cpSlideJointInit(cpSlideJoint *joint, cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB, cpFloat min, cpFloat max);
    /// Allocate and initialize a slide joint.
    cpConstraint* cpSlideJointNew(cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB, cpFloat min, cpFloat max);

    /// Get the location of the first anchor relative to the first body.
    cpVect cpSlideJointGetAnchorA(const cpConstraint *constraint);
    /// Set the location of the first anchor relative to the first body.
    void cpSlideJointSetAnchorA(cpConstraint *constraint, cpVect anchorA);

    /// Get the location of the second anchor relative to the second body.
    cpVect cpSlideJointGetAnchorB(const cpConstraint *constraint);
    /// Set the location of the second anchor relative to the second body.
    void cpSlideJointSetAnchorB(cpConstraint *constraint, cpVect anchorB);

    /// Get the minimum distance the joint will maintain between the two anchors.
    cpFloat cpSlideJointGetMin(const cpConstraint *constraint);
    /// Set the minimum distance the joint will maintain between the two anchors.
    void cpSlideJointSetMin(cpConstraint *constraint, cpFloat min);

    /// Get the maximum distance the joint will maintain between the two anchors.
    cpFloat cpSlideJointGetMax(const cpConstraint *constraint);
    /// Set the maximum distance the joint will maintain between the two anchors.
    void cpSlideJointSetMax(cpConstraint *constraint, cpFloat max);

    ///////////////////////////////////////////
    // cpPivotJoint.h
    ///////////////////////////////////////////

    /// Check if a constraint is a slide joint.
    cpBool cpConstraintIsPivotJoint(const cpConstraint *constraint);

    /// Allocate a pivot joint
    cpPivotJoint* cpPivotJointAlloc(void);
    /// Initialize a pivot joint.
    cpPivotJoint* cpPivotJointInit(cpPivotJoint *joint, cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB);
    /// Allocate and initialize a pivot joint.
    cpConstraint* cpPivotJointNew(cpBody *a, cpBody *b, cpVect pivot);
    /// Allocate and initialize a pivot joint with specific anchors.
    cpConstraint* cpPivotJointNew2(cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB);

    /// Get the location of the first anchor relative to the first body.
    cpVect cpPivotJointGetAnchorA(const cpConstraint *constraint);
    /// Set the location of the first anchor relative to the first body.
    void cpPivotJointSetAnchorA(cpConstraint *constraint, cpVect anchorA);

    /// Get the location of the second anchor relative to the second body.
    cpVect cpPivotJointGetAnchorB(const cpConstraint *constraint);
    /// Set the location of the second anchor relative to the second body.
    void cpPivotJointSetAnchorB(cpConstraint *constraint, cpVect anchorB);

    ///////////////////////////////////////////
    // cpGrooveJoint.h
    ///////////////////////////////////////////

    /// Check if a constraint is a slide joint.
    cpBool cpConstraintIsGrooveJoint(const cpConstraint *constraint);

    /// Allocate a groove joint.
    cpGrooveJoint* cpGrooveJointAlloc(void);
    /// Initialize a groove joint.
    cpGrooveJoint* cpGrooveJointInit(cpGrooveJoint *joint, cpBody *a, cpBody *b, cpVect groove_a, cpVect groove_b, cpVect anchorB);
    /// Allocate and initialize a groove joint.
    cpConstraint* cpGrooveJointNew(cpBody *a, cpBody *b, cpVect groove_a, cpVect groove_b, cpVect anchorB);

    /// Get the first endpoint of the groove relative to the first body.
    cpVect cpGrooveJointGetGrooveA(const cpConstraint *constraint);
    /// Set the first endpoint of the groove relative to the first body.
    void cpGrooveJointSetGrooveA(cpConstraint *constraint, cpVect grooveA);

    /// Get the first endpoint of the groove relative to the first body.
    cpVect cpGrooveJointGetGrooveB(const cpConstraint *constraint);
    /// Set the first endpoint of the groove relative to the first body.
    void cpGrooveJointSetGrooveB(cpConstraint *constraint, cpVect grooveB);

    /// Get the location of the second anchor relative to the second body.
    cpVect cpGrooveJointGetAnchorB(const cpConstraint *constraint);
    /// Set the location of the second anchor relative to the second body.
    void cpGrooveJointSetAnchorB(cpConstraint *constraint, cpVect anchorB);

    ///////////////////////////////////////////
    //cpDampedSpring.h
    ///////////////////////////////////////////

    /// Check if a constraint is a slide joint.
    cpBool cpConstraintIsDampedSpring(const cpConstraint *constraint);

    /// Function type used for damped spring force callbacks.
    typedef cpFloat (*cpDampedSpringForceFunc)(cpConstraint *spring, cpFloat dist);

    /// Allocate a damped spring.
    cpDampedSpring* cpDampedSpringAlloc(void);
    /// Initialize a damped spring.
    cpDampedSpring* cpDampedSpringInit(cpDampedSpring *joint, cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB, cpFloat restLength, cpFloat stiffness, cpFloat damping);
    /// Allocate and initialize a damped spring.
    cpConstraint* cpDampedSpringNew(cpBody *a, cpBody *b, cpVect anchorA, cpVect anchorB, cpFloat restLength, cpFloat stiffness, cpFloat damping);

    /// Get the location of the first anchor relative to the first body.
    cpVect cpDampedSpringGetAnchorA(const cpConstraint *constraint);
    /// Set the location of the first anchor relative to the first body.
    void cpDampedSpringSetAnchorA(cpConstraint *constraint, cpVect anchorA);

    /// Get the location of the second anchor relative to the second body.
    cpVect cpDampedSpringGetAnchorB(const cpConstraint *constraint);
    /// Set the location of the second anchor relative to the second body.
    void cpDampedSpringSetAnchorB(cpConstraint *constraint, cpVect anchorB);

    /// Get the rest length of the spring.
    cpFloat cpDampedSpringGetRestLength(const cpConstraint *constraint);
    /// Set the rest length of the spring.
    void cpDampedSpringSetRestLength(cpConstraint *constraint, cpFloat restLength);

    /// Get the stiffness of the spring in force/distance.
    cpFloat cpDampedSpringGetStiffness(const cpConstraint *constraint);
    /// Set the stiffness of the spring in force/distance.
    void cpDampedSpringSetStiffness(cpConstraint *constraint, cpFloat stiffness);

    /// Get the damping of the spring.
    cpFloat cpDampedSpringGetDamping(const cpConstraint *constraint);
    /// Set the damping of the spring.
    void cpDampedSpringSetDamping(cpConstraint *constraint, cpFloat damping);

    /// Get the damping of the spring.
    cpDampedSpringForceFunc cpDampedSpringGetSpringForceFunc(const cpConstraint *constraint);
    /// Set the damping of the spring.
    void cpDampedSpringSetSpringForceFunc(cpConstraint *constraint, cpDampedSpringForceFunc springForceFunc);


    ///////////////////////////////////////////
    //cpDampedRotarySpring.h
    ///////////////////////////////////////////

    /// Check if a constraint is a damped rotary springs.
    cpBool cpConstraintIsDampedRotarySpring(const cpConstraint *constraint);

    /// Function type used for damped rotary spring force callbacks.
    typedef cpFloat (*cpDampedRotarySpringTorqueFunc)(struct cpConstraint *spring, cpFloat relativeAngle);

    /// Allocate a damped rotary spring.
    cpDampedRotarySpring* cpDampedRotarySpringAlloc(void);
    /// Initialize a damped rotary spring.
    cpDampedRotarySpring* cpDampedRotarySpringInit(cpDampedRotarySpring *joint, cpBody *a, cpBody *b, cpFloat restAngle, cpFloat stiffness, cpFloat damping);
    /// Allocate and initialize a damped rotary spring.
    cpConstraint* cpDampedRotarySpringNew(cpBody *a, cpBody *b, cpFloat restAngle, cpFloat stiffness, cpFloat damping);

    /// Get the rest length of the spring.
    cpFloat cpDampedRotarySpringGetRestAngle(const cpConstraint *constraint);
    /// Set the rest length of the spring.
    void cpDampedRotarySpringSetRestAngle(cpConstraint *constraint, cpFloat restAngle);

    /// Get the stiffness of the spring in force/distance.
    cpFloat cpDampedRotarySpringGetStiffness(const cpConstraint *constraint);
    /// Set the stiffness of the spring in force/distance.
    void cpDampedRotarySpringSetStiffness(cpConstraint *constraint, cpFloat stiffness);

    /// Get the damping of the spring.
    cpFloat cpDampedRotarySpringGetDamping(const cpConstraint *constraint);
    /// Set the damping of the spring.
    void cpDampedRotarySpringSetDamping(cpConstraint *constraint, cpFloat damping);

    /// Get the damping of the spring.
    cpDampedRotarySpringTorqueFunc cpDampedRotarySpringGetSpringTorqueFunc(const cpConstraint *constraint);
    /// Set the damping of the spring.
    void cpDampedRotarySpringSetSpringTorqueFunc(cpConstraint *constraint, cpDampedRotarySpringTorqueFunc springTorqueFunc);

    ///////////////////////////////////////////
    //cpRotaryLimitJoint.h
    ///////////////////////////////////////////

    /// Check if a constraint is a damped rotary springs.
    cpBool cpConstraintIsRotaryLimitJoint(const cpConstraint *constraint);

    /// Allocate a damped rotary limit joint.
    cpRotaryLimitJoint* cpRotaryLimitJointAlloc(void);
    /// Initialize a damped rotary limit joint.
    cpRotaryLimitJoint* cpRotaryLimitJointInit(cpRotaryLimitJoint *joint, cpBody *a, cpBody *b, cpFloat min, cpFloat max);
    /// Allocate and initialize a damped rotary limit joint.
    cpConstraint* cpRotaryLimitJointNew(cpBody *a, cpBody *b, cpFloat min, cpFloat max);

    /// Get the minimum distance the joint will maintain between the two anchors.
    cpFloat cpRotaryLimitJointGetMin(const cpConstraint *constraint);
    /// Set the minimum distance the joint will maintain between the two anchors.
    void cpRotaryLimitJointSetMin(cpConstraint *constraint, cpFloat min);

    /// Get the maximum distance the joint will maintain between the two anchors.
    cpFloat cpRotaryLimitJointGetMax(const cpConstraint *constraint);
    /// Set the maximum distance the joint will maintain between the two anchors.
    void cpRotaryLimitJointSetMax(cpConstraint *constraint, cpFloat max);

    ///////////////////////////////////////////
    //cpRatchetJoint.h
    ///////////////////////////////////////////

    /// Check if a constraint is a damped rotary springs.
    cpBool cpConstraintIsRatchetJoint(const cpConstraint *constraint);

    /// Allocate a ratchet joint.
    cpRatchetJoint* cpRatchetJointAlloc(void);
    /// Initialize a ratched joint.
    cpRatchetJoint* cpRatchetJointInit(cpRatchetJoint *joint, cpBody *a, cpBody *b, cpFloat phase, cpFloat ratchet);
    /// Allocate and initialize a ratchet joint.
    cpConstraint* cpRatchetJointNew(cpBody *a, cpBody *b, cpFloat phase, cpFloat ratchet);

    /// Get the angle of the current ratchet tooth.
    cpFloat cpRatchetJointGetAngle(const cpConstraint *constraint);
    /// Set the angle of the current ratchet tooth.
    void cpRatchetJointSetAngle(cpConstraint *constraint, cpFloat angle);

    /// Get the phase offset of the ratchet.
    cpFloat cpRatchetJointGetPhase(const cpConstraint *constraint);
    /// Get the phase offset of the ratchet.
    void cpRatchetJointSetPhase(cpConstraint *constraint, cpFloat phase);

    /// Get the angular distance of each ratchet.
    cpFloat cpRatchetJointGetRatchet(const cpConstraint *constraint);
    /// Set the angular distance of each ratchet.
    void cpRatchetJointSetRatchet(cpConstraint *constraint, cpFloat ratchet);


    ///////////////////////////////////////////
    //cpGearJoint.h
    ///////////////////////////////////////////

    /// Check if a constraint is a damped rotary springs.
    cpBool cpConstraintIsGearJoint(const cpConstraint *constraint);

    /// Allocate a gear joint.
    cpGearJoint* cpGearJointAlloc(void);
    /// Initialize a gear joint.
    cpGearJoint* cpGearJointInit(cpGearJoint *joint, cpBody *a, cpBody *b, cpFloat phase, cpFloat ratio);
    /// Allocate and initialize a gear joint.
    cpConstraint* cpGearJointNew(cpBody *a, cpBody *b, cpFloat phase, cpFloat ratio);

    /// Get the phase offset of the gears.
    cpFloat cpGearJointGetPhase(const cpConstraint *constraint);
    /// Set the phase offset of the gears.
    void cpGearJointSetPhase(cpConstraint *constraint, cpFloat phase);

    /// Get the angular distance of each ratchet.
    cpFloat cpGearJointGetRatio(const cpConstraint *constraint);
    /// Set the ratio of a gear joint.
    void cpGearJointSetRatio(cpConstraint *constraint, cpFloat ratio);


    ///////////////////////////////////////////
    //cpSimpleMotor.h
    ///////////////////////////////////////////

    /// Opaque struct type for damped rotary springs.
    typedef struct cpSimpleMotor cpSimpleMotor;

    /// Check if a constraint is a damped rotary springs.
    cpBool cpConstraintIsSimpleMotor(const cpConstraint *constraint);

    /// Allocate a simple motor.
    cpSimpleMotor* cpSimpleMotorAlloc(void);
    /// initialize a simple motor.
    cpSimpleMotor* cpSimpleMotorInit(cpSimpleMotor *joint, cpBody *a, cpBody *b, cpFloat rate);
    /// Allocate and initialize a simple motor.
    cpConstraint* cpSimpleMotorNew(cpBody *a, cpBody *b, cpFloat rate);

    /// Get the rate of the motor.
    cpFloat cpSimpleMotorGetRate(const cpConstraint *constraint);
    /// Set the rate of the motor.
    void cpSimpleMotorSetRate(cpConstraint *constraint, cpFloat rate);


    ///////////////////////////////////////////
    //cpSpace.h
    ///////////////////////////////////////////

    /// Collision begin event function callback type.
    /// Returning false from a begin callback causes the collision to be ignored until
    /// the the separate callback is called when the objects stop colliding.
    typedef cpBool (*cpCollisionBeginFunc)(cpArbiter *arb, cpSpace *space, cpDataPointer userData);
    /// Collision pre-solve event function callback type.
    /// Returning false from a pre-step callback causes the collision to be ignored until the next step.
    typedef cpBool (*cpCollisionPreSolveFunc)(cpArbiter *arb, cpSpace *space, cpDataPointer userData);
    /// Collision post-solve event function callback type.
    typedef void (*cpCollisionPostSolveFunc)(cpArbiter *arb, cpSpace *space, cpDataPointer userData);
    /// Collision separate event function callback type.
    typedef void (*cpCollisionSeparateFunc)(cpArbiter *arb, cpSpace *space, cpDataPointer userData);

    /// Struct that holds function callback pointers to configure custom collision handling.
    /// Collision handlers have a pair of types; when a collision occurs between two shapes that have these types, the collision handler functions are triggered.
    struct cpCollisionHandler {
        /// Collision type identifier of the first shape that this handler recognizes.
        /// In the collision handler callback, the shape with this type will be the first argument. Read only.
        const cpCollisionType typeA;
        /// Collision type identifier of the second shape that this handler recognizes.
        /// In the collision handler callback, the shape with this type will be the second argument. Read only.
        const cpCollisionType typeB;
        /// This function is called when two shapes with types that match this collision handler begin colliding.
        cpCollisionBeginFunc beginFunc;
        /// This function is called each step when two shapes with types that match this collision handler are colliding.
        /// It's called before the collision solver runs so that you can affect a collision's outcome.
        cpCollisionPreSolveFunc preSolveFunc;
        /// This function is called each step when two shapes with types that match this collision handler are colliding.
        /// It's called after the collision solver runs so that you can read back information about the collision to trigger events in your game.
        cpCollisionPostSolveFunc postSolveFunc;
        /// This function is called when two shapes with types that match this collision handler stop colliding.
        cpCollisionSeparateFunc separateFunc;
        /// This is a user definable context pointer that is passed to all of the collision handler functions.
        cpDataPointer userData;
    };

    // TODO: Make timestep a parameter?


    //MARK: Memory and Initialization

    /// Allocate a cpSpace.
    cpSpace* cpSpaceAlloc(void);
    /// Initialize a cpSpace.
    cpSpace* cpSpaceInit(cpSpace *space);
    /// Allocate and initialize a cpSpace.
    cpSpace* cpSpaceNew(void);

    /// Destroy a cpSpace.
    void cpSpaceDestroy(cpSpace *space);
    /// Destroy and free a cpSpace.
    void cpSpaceFree(cpSpace *space);


    //MARK: Properties

    /// Number of iterations to use in the impulse solver to solve contacts and other constraints.
    int cpSpaceGetIterations(const cpSpace *space);
    void cpSpaceSetIterations(cpSpace *space, int iterations);

    /// Gravity to pass to rigid bodies when integrating velocity.
    cpVect cpSpaceGetGravity(const cpSpace *space);
    void cpSpaceSetGravity(cpSpace *space, cpVect gravity);

    /// Damping rate expressed as the fraction of velocity bodies retain each second.
    /// A value of 0.9 would mean that each body's velocity will drop 10% per second.
    /// The default value is 1.0, meaning no damping is applied.
    /// @note This damping value is different than those of cpDampedSpring and cpDampedRotarySpring.
    cpFloat cpSpaceGetDamping(const cpSpace *space);
    void cpSpaceSetDamping(cpSpace *space, cpFloat damping);

    /// Speed threshold for a body to be considered idle.
    /// The default value of 0 means to let the space guess a good threshold based on gravity.
    cpFloat cpSpaceGetIdleSpeedThreshold(const cpSpace *space);
    void cpSpaceSetIdleSpeedThreshold(cpSpace *space, cpFloat idleSpeedThreshold);

    /// Time a group of bodies must remain idle in order to fall asleep.
    /// Enabling sleeping also implicitly enables the the contact graph.
    /// The default value of INFINITY disables the sleeping algorithm.
    cpFloat cpSpaceGetSleepTimeThreshold(const cpSpace *space);
    void cpSpaceSetSleepTimeThreshold(cpSpace *space, cpFloat sleepTimeThreshold);

    /// Amount of encouraged penetration between colliding shapes.
    /// Used to reduce oscillating contacts and keep the collision cache warm.
    /// Defaults to 0.1. If you have poor simulation quality,
    /// increase this number as much as possible without allowing visible amounts of overlap.
    cpFloat cpSpaceGetCollisionSlop(const cpSpace *space);
    void cpSpaceSetCollisionSlop(cpSpace *space, cpFloat collisionSlop);

    /// Determines how fast overlapping shapes are pushed apart.
    /// Expressed as a fraction of the error remaining after each second.
    /// Defaults to pow(1.0 - 0.1, 60.0) meaning that Chipmunk fixes 10% of overlap each frame at 60Hz.
    cpFloat cpSpaceGetCollisionBias(const cpSpace *space);
    void cpSpaceSetCollisionBias(cpSpace *space, cpFloat collisionBias);

    /// Number of frames that contact information should persist.
    /// Defaults to 3. There is probably never a reason to change this value.
    cpTimestamp cpSpaceGetCollisionPersistence(const cpSpace *space);
    void cpSpaceSetCollisionPersistence(cpSpace *space, cpTimestamp collisionPersistence);

    /// User definable data pointer.
    /// Generally this points to your game's controller or game state
    /// class so you can access it when given a cpSpace reference in a callback.
    cpDataPointer cpSpaceGetUserData(const cpSpace *space);
    void cpSpaceSetUserData(cpSpace *space, cpDataPointer userData);

    /// The Space provided static body for a given cpSpace.
    /// This is merely provided for convenience and you are not required to use it.
    cpBody* cpSpaceGetStaticBody(const cpSpace *space);

    /// Returns the current (or most recent) time step used with the given space.
    /// Useful from callbacks if your time step is not a compile-time global.
    cpFloat cpSpaceGetCurrentTimeStep(const cpSpace *space);

    /// returns true from inside a callback when objects cannot be added/removed.
    cpBool cpSpaceIsLocked(cpSpace *space);


    //MARK: Collision Handlers

    /// Create or return the existing collision handler that is called for all collisions that are not handled by a more specific collision handler.
    cpCollisionHandler *cpSpaceAddDefaultCollisionHandler(cpSpace *space);
    /// Create or return the existing collision handler for the specified pair of collision types.
    /// If wildcard handlers are used with either of the collision types, it's the responibility of the custom handler to invoke the wildcard handlers.
    cpCollisionHandler *cpSpaceAddCollisionHandler(cpSpace *space, cpCollisionType a, cpCollisionType b);
    /// Create or return the existing wildcard collision handler for the specified type.
    cpCollisionHandler *cpSpaceAddWildcardHandler(cpSpace *space, cpCollisionType type);


    //MARK: Add/Remove objects

    /// Add a collision shape to the simulation.
    /// If the shape is attached to a static body, it will be added as a static shape.
    cpShape* cpSpaceAddShape(cpSpace *space, cpShape *shape);
    /// Add a rigid body to the simulation.
    cpBody* cpSpaceAddBody(cpSpace *space, cpBody *body);
    /// Add a constraint to the simulation.
    cpConstraint* cpSpaceAddConstraint(cpSpace *space, cpConstraint *constraint);

    /// Remove a collision shape from the simulation.
    void cpSpaceRemoveShape(cpSpace *space, cpShape *shape);
    /// Remove a rigid body from the simulation.
    void cpSpaceRemoveBody(cpSpace *space, cpBody *body);
    /// Remove a constraint from the simulation.
    void cpSpaceRemoveConstraint(cpSpace *space, cpConstraint *constraint);

    /// Test if a collision shape has been added to the space.
    cpBool cpSpaceContainsShape(cpSpace *space, cpShape *shape);
    /// Test if a rigid body has been added to the space.
    cpBool cpSpaceContainsBody(cpSpace *space, cpBody *body);
    /// Test if a constraint has been added to the space.
    cpBool cpSpaceContainsConstraint(cpSpace *space, cpConstraint *constraint);

    //MARK: Post-Step Callbacks

    /// Post Step callback function type.
    typedef void (*cpPostStepFunc)(cpSpace *space, void *key, void *data);
    /// Schedule a post-step callback to be called when cpSpaceStep() finishes.
    /// You can only register one callback per unique value for @c key.
    /// Returns true only if @c key has never been scheduled before.
    /// It's possible to pass @c NULL for @c func if you only want to mark @c key as being used.
    cpBool cpSpaceAddPostStepCallback(cpSpace *space, cpPostStepFunc func, void *key, void *data);


    //MARK: Queries

    // TODO: Queries and iterators should take a cpSpace parametery.
    // TODO: They should also be abortable.

    /// Nearest point query callback function type.
    typedef void (*cpSpacePointQueryFunc)(cpShape *shape, cpVect point, cpFloat distance, cpVect gradient, void *data);
    /// Query the space at a point and call @c func for each shape found.
    void cpSpacePointQuery(cpSpace *space, cpVect point, cpFloat maxDistance, cpShapeFilter filter, cpSpacePointQueryFunc func, void *data);
    /// Query the space at a point and return the nearest shape found. Returns NULL if no shapes were found.
    cpShape *cpSpacePointQueryNearest(cpSpace *space, cpVect point, cpFloat maxDistance, cpShapeFilter filter, cpPointQueryInfo *out);

    /// Segment query callback function type.
    typedef void (*cpSpaceSegmentQueryFunc)(cpShape *shape, cpVect point, cpVect normal, cpFloat alpha, void *data);
    /// Perform a directed line segment query (like a raycast) against the space calling @c func for each shape intersected.
    void cpSpaceSegmentQuery(cpSpace *space, cpVect start, cpVect end, cpFloat radius, cpShapeFilter filter, cpSpaceSegmentQueryFunc func, void *data);
    /// Perform a directed line segment query (like a raycast) against the space and return the first shape hit. Returns NULL if no shapes were hit.
    cpShape *cpSpaceSegmentQueryFirst(cpSpace *space, cpVect start, cpVect end, cpFloat radius, cpShapeFilter filter, cpSegmentQueryInfo *out);

    /// Rectangle Query callback function type.
    typedef void (*cpSpaceBBQueryFunc)(cpShape *shape, void *data);
    /// Perform a fast rectangle query on the space calling @c func for each shape found.
    /// Only the shape's bounding boxes are checked for overlap, not their full shape.
    void cpSpaceBBQuery(cpSpace *space, cpBB bb, cpShapeFilter filter, cpSpaceBBQueryFunc func, void *data);

    /// Shape query callback function type.
    typedef void (*cpSpaceShapeQueryFunc)(cpShape *shape, cpContactPointSet *points, void *data);
    /// Query a space for any shapes overlapping the given shape and call @c func for each shape found.
    cpBool cpSpaceShapeQuery(cpSpace *space, cpShape *shape, cpSpaceShapeQueryFunc func, void *data);


    //MARK: Iteration

    /// Space/body iterator callback function type.
    typedef void (*cpSpaceBodyIteratorFunc)(cpBody *body, void *data);
    /// Call @c func for each body in the space.
    void cpSpaceEachBody(cpSpace *space, cpSpaceBodyIteratorFunc func, void *data);

    /// Space/body iterator callback function type.
    typedef void (*cpSpaceShapeIteratorFunc)(cpShape *shape, void *data);
    /// Call @c func for each shape in the space.
    void cpSpaceEachShape(cpSpace *space, cpSpaceShapeIteratorFunc func, void *data);

    /// Space/constraint iterator callback function type.
    typedef void (*cpSpaceConstraintIteratorFunc)(cpConstraint *constraint, void *data);
    /// Call @c func for each shape in the space.
    void cpSpaceEachConstraint(cpSpace *space, cpSpaceConstraintIteratorFunc func, void *data);


    //MARK: Indexing

    /// Update the collision detection info for the static shapes in the space.
    void cpSpaceReindexStatic(cpSpace *space);
    /// Update the collision detection data for a specific shape in the space.
    void cpSpaceReindexShape(cpSpace *space, cpShape *shape);
    /// Update the collision detection data for all shapes attached to a body.
    void cpSpaceReindexShapesForBody(cpSpace *space, cpBody *body);

    /// Switch the space to use a spatial has as it's spatial index.
    void cpSpaceUseSpatialHash(cpSpace *space, cpFloat dim, int count);


    //MARK: Time Stepping

    /// Step the space forward in time by @c dt.
    void cpSpaceStep(cpSpace *space, cpFloat dt);


    //MARK: Debug API

    /// Color type to use with the space debug drawing API.
    typedef struct cpSpaceDebugColor {
        float r, g, b, a;
    } cpSpaceDebugColor;

    /// Callback type for a function that draws a filled, stroked circle.
    typedef void (*cpSpaceDebugDrawCircleImpl)(cpVect pos, cpFloat angle, cpFloat radius, cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, cpDataPointer data);
    /// Callback type for a function that draws a line segment.
    typedef void (*cpSpaceDebugDrawSegmentImpl)(cpVect a, cpVect b, cpSpaceDebugColor color, cpDataPointer data);
    /// Callback type for a function that draws a thick line segment.
    typedef void (*cpSpaceDebugDrawFatSegmentImpl)(cpVect a, cpVect b, cpFloat radius, cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, cpDataPointer data);
    /// Callback type for a function that draws a convex polygon.
    typedef void (*cpSpaceDebugDrawPolygonImpl)(int count, const cpVect *verts, cpFloat radius, cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, cpDataPointer data);
    /// Callback type for a function that draws a dot.
    typedef void (*cpSpaceDebugDrawDotImpl)(cpFloat size, cpVect pos, cpSpaceDebugColor color, cpDataPointer data);
    /// Callback type for a function that returns a color for a given shape. This gives you an opportunity to color shapes based on how they are used in your engine.
    typedef cpSpaceDebugColor (*cpSpaceDebugDrawColorForShapeImpl)(cpShape *shape, cpDataPointer data);

    typedef enum cpSpaceDebugDrawFlags {
        CP_SPACE_DEBUG_DRAW_SHAPES = 1,
        CP_SPACE_DEBUG_DRAW_CONSTRAINTS = 2,
        CP_SPACE_DEBUG_DRAW_COLLISION_POINTS = 4,
    } cpSpaceDebugDrawFlags;

    /// Struct used with cpSpaceDebugDraw() containing drawing callbacks and other drawing settings.
    typedef struct cpSpaceDebugDrawOptions {
        /// Function that will be invoked to draw circles.
        cpSpaceDebugDrawCircleImpl drawCircle;
        /// Function that will be invoked to draw line segments.
        cpSpaceDebugDrawSegmentImpl drawSegment;
        /// Function that will be invoked to draw thick line segments.
        cpSpaceDebugDrawFatSegmentImpl drawFatSegment;
        /// Function that will be invoked to draw convex polygons.
        cpSpaceDebugDrawPolygonImpl drawPolygon;
        /// Function that will be invoked to draw dots.
        cpSpaceDebugDrawDotImpl drawDot;

        /// Flags that request which things to draw (collision shapes, constraints, contact points).
        cpSpaceDebugDrawFlags flags;
        /// Outline color passed to the drawing function.
        cpSpaceDebugColor shapeOutlineColor;
        /// Function that decides what fill color to draw shapes using.
        cpSpaceDebugDrawColorForShapeImpl colorForShape;
        /// Color passed to drawing functions for constraints.
        cpSpaceDebugColor constraintColor;
        /// Color passed to drawing functions for collision points.
        cpSpaceDebugColor collisionPointColor;

        /// User defined context pointer passed to all of the callback functions as the 'data' argument.
        cpDataPointer data;
    } cpSpaceDebugDrawOptions;

    /// Debug draw the current state of the space using the supplied drawing options.
    void cpSpaceDebugDraw(cpSpace *space, cpSpaceDebugDrawOptions *options);


    ///////////////////////////////////////////
    // chipmunk.h
    ///////////////////////////////////////////

    extern const char *cpVersionString;


    ///////////////////////////////////////////
    // GENERAL
    ///////////////////////////////////////////


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

    ///////////////////////////////////////////
    // chipmunk_ffi.h
    ///////////////////////////////////////////

    typedef cpBB (*cpBBNewForExtents)(const cpVect c, const cpFloat hw, const cpFloat hh);
    static cpBBNewForExtents _cpBBNewForExtents;

    typedef cpBB (*cpBBNewForCircle)(const cpVect p, const cpFloat r);
    static cpBBNewForCircle _cpBBNewForCircle;

    typedef cpBool (*cpBBIntersects)(const cpBB a, const cpBB b);
    static cpBBIntersects _cpBBIntersects;

    typedef cpBool (*cpBBContainsBB)(const cpBB bb, const cpBB other);
    static cpBBContainsBB _cpBBContainsBB;

    typedef cpBool (*cpBBContainsVect)(const cpBB bb, const cpVect v);
    static cpBBContainsVect _cpBBContainsVect;

    typedef cpBB (*cpBBMerge)(const cpBB a, const cpBB b);
    static cpBBMerge _cpBBMerge;

    typedef cpBB (*cpBBExpand)(const cpBB bb, const cpVect v);
    static cpBBExpand _cpBBExpand;

    typedef cpVect (*cpBBCenter)(cpBB bb);
    static cpBBCenter _cpBBCenter;

    typedef cpFloat (*cpBBArea)(cpBB bb);
    static cpBBArea _cpBBArea;

    typedef cpFloat (*cpBBMergedArea)(cpBB a, cpBB b);
    static cpBBMergedArea _cpBBMergedArea;

    typedef cpFloat (*cpBBSegmentQuery)(cpBB bb, cpVect a, cpVect b);
    static cpBBSegmentQuery _cpBBSegmentQuery;

    typedef cpBool (*cpBBIntersectsSegment)(cpBB bb, cpVect a, cpVect b);
    static cpBBIntersectsSegment _cpBBIntersectsSegment;

    typedef cpVect (*cpBBClampVect)(const cpBB bb, const cpVect v);
    static cpBBClampVect _cpBBClampVect;

    ///////////////////////////////////////////
    // chipmunk_unsafe.h
    ///////////////////////////////////////////

    /// Set the radius of a circle shape.
    void cpCircleShapeSetRadius(cpShape *shape, cpFloat radius);
    /// Set the offset of a circle shape.
    void cpCircleShapeSetOffset(cpShape *shape, cpVect offset);

    /// Set the endpoints of a segment shape.
    void cpSegmentShapeSetEndpoints(cpShape *shape, cpVect a, cpVect b);
    /// Set the radius of a segment shape.
    void cpSegmentShapeSetRadius(cpShape *shape, cpFloat radius);

    /// Set the vertexes of a poly shape.
    void cpPolyShapeSetVerts(cpShape *shape, int count, cpVect *verts, cpTransform transform);
    void cpPolyShapeSetVertsRaw(cpShape *shape, int count, cpVect *verts);
    /// Set the radius of a poly shape.
    void cpPolyShapeSetRadius(cpShape *shape, cpFloat radius);

    ///////////////////////////////////////////
    // cpMarch.h
    ///////////////////////////////////////////

    /// Function type used as a callback from the marching squares algorithm to sample an image function.
    /// It passes you the point to sample and your context pointer, and you return the density.
    typedef cpFloat (*cpMarchSampleFunc)(cpVect point, void *data);

    /// Function type used as a callback from the marching squares algorithm to output a line segment.
    /// It passes you the two endpoints and your context pointer.
    typedef void (*cpMarchSegmentFunc)(cpVect v0, cpVect v1, void *data);

    /// Trace an anti-aliased contour of an image along a particular threshold.
    /// The given number of samples will be taken and spread across the bounding box area using the sampling function and context.
    /// The segment function will be called for each segment detected that lies along the density contour for @c threshold.
    void cpMarchSoft(
    cpBB bb, unsigned long x_samples, unsigned long y_samples, cpFloat threshold,
    cpMarchSegmentFunc segment, void *segment_data,
    cpMarchSampleFunc sample, void *sample_data
    );

    /// Trace an aliased curve of an image along a particular threshold.
    /// The given number of samples will be taken and spread across the bounding box area using the sampling function and context.
    /// The segment function will be called for each segment detected that lies along the density contour for @c threshold.
    void cpMarchHard(
    cpBB bb, unsigned long x_samples, unsigned long y_samples, cpFloat threshold,
    cpMarchSegmentFunc segment, void *segment_data,
    cpMarchSampleFunc sample, void *sample_data
    );

    ///////////////////////////////////////////
    // cpPolyline.h
    ///////////////////////////////////////////

    // Polylines are just arrays of vertexes.
    // They are looped if the first vertex is equal to the last.
    // cpPolyline structs are intended to be passed by value and destroyed when you are done with them.
    typedef struct cpPolyline {
      int count, capacity;
      cpVect verts[];
    } cpPolyline;

    /// Destroy and free a polyline instance.
    void cpPolylineFree(cpPolyline *line);

    /// Returns true if the first vertex is equal to the last.
    cpBool cpPolylineIsClosed(cpPolyline *line);

    /**
        Returns a copy of a polyline simplified by using the Douglas-Peucker algorithm.
        This works very well on smooth or gently curved shapes, but not well on straight edged or angular shapes.
    */
    cpPolyline *cpPolylineSimplifyCurves(cpPolyline *line, cpFloat tol);

    /**
        Returns a copy of a polyline simplified by discarding "flat" vertexes.
        This works well on straigt edged or angular shapes, not as well on smooth shapes.
    */
    cpPolyline *cpPolylineSimplifyVertexes(cpPolyline *line, cpFloat tol);

    /// Get the convex hull of a polyline as a looped polyline.
    cpPolyline *cpPolylineToConvexHull(cpPolyline *line, cpFloat tol);


    /// Polyline sets are collections of polylines, generally built by cpMarchSoft() or cpMarchHard().
    typedef struct cpPolylineSet {
      int count, capacity;
      cpPolyline **lines;
    } cpPolylineSet;

    /// Allocate a new polyline set.
    cpPolylineSet *cpPolylineSetAlloc(void);

    /// Initialize a new polyline set.
    cpPolylineSet *cpPolylineSetInit(cpPolylineSet *set);

    /// Allocate and initialize a polyline set.
    cpPolylineSet *cpPolylineSetNew(void);

    /// Destroy a polyline set.
    void cpPolylineSetDestroy(cpPolylineSet *set, cpBool freePolylines);

    /// Destroy and free a polyline set.
    void cpPolylineSetFree(cpPolylineSet *set, cpBool freePolylines);

    /**
        Add a line segment to a polyline set.
        A segment will either start a new polyline, join two others, or add to or loop an existing polyline.
        This is mostly intended to be used as a callback directly from cpMarchSoft() or cpMarchHard().
    */
    void cpPolylineSetCollectSegment(cpVect v0, cpVect v1, cpPolylineSet *lines);

    /**
        Get an approximate convex decomposition from a polyline.
        Returns a cpPolylineSet of convex hulls that match the original shape to within 'tol'.
        NOTE: If the input is a self intersecting polygon, the output might end up overly simplified.
    */

    cpPolylineSet *cpPolylineConvexDecomposition(cpPolyline *line, cpFloat tol);

    //#define cpPolylineConvexDecomposition_BETA cpPolylineConvexDecomposition
    //cpPolylineSet *cpPolylineConvexDecomposition_BETA(cpPolyline *line, cpFloat tol);

    struct cpHastySpace;
    typedef struct cpHastySpace cpHastySpace;

    cpSpace *cpHastySpaceNew(void);
    void cpHastySpaceFree(cpSpace *space);

    void cpHastySpaceSetThreads(cpSpace *space, unsigned long threads);

    unsigned long cpHastySpaceGetThreads(cpSpace *space);

    void cpHastySpaceStep(cpSpace *space, cpFloat dt);
"""

# for packaging tools to pick up lextab, and yacctab dependencies.
# https://github.com/viblo/pymunk/issues/151
try:
    import pycparser.lextab
    import pycparser.yacctab
except:
    pass

from cffi import FFI
ffi = FFI()
ffi.cdef(h)

from ._libload import load_library
try:
    import pymunkoptions
    _lib_debug = pymunkoptions.options["debug"]
except:
    _lib_debug = True #Set to True to print the Chipmunk path.
lib, lib_path = load_library(ffi, "chipmunk", debug_lib=_lib_debug)
