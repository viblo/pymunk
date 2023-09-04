extern "Python"
{

    // cpConstraint.h
    void ext_cpConstraintPreSolveFunc(cpConstraint *constraint, cpSpace *space);
    void ext_cpConstraintPostSolveFunc(cpConstraint *constraint, cpSpace *space);

    // cpBody.h
    void ext_cpBodyVelocityFunc(cpBody *body, cpVect gravity, cpFloat damping, cpFloat dt);
    void ext_cpBodyPositionFunc(cpBody *body, cpFloat dt);

    void ext_cpBodyShapeIteratorFunc(cpBody *body, cpShape *shape, void *data);
    void ext_cpBodyConstraintIteratorFunc(cpBody *body, cpConstraint *constraint, void *data);
    void ext_cpBodyArbiterIteratorFunc(cpBody *body, cpArbiter *arbiter, void *data);

    // cpSpace.h

    cpBool ext_cpCollisionBeginFunc(cpArbiter *arb, cpSpace *space, cpDataPointer userData);
    cpBool ext_cpCollisionPreSolveFunc(cpArbiter *arb, cpSpace *space, cpDataPointer userData);
    void ext_cpCollisionPostSolveFunc(cpArbiter *arb, cpSpace *space, cpDataPointer userData);
    void ext_cpCollisionSeparateFunc(cpArbiter *arb, cpSpace *space, cpDataPointer userData);

    void ext_cpSpacePointQueryFunc(cpShape *shape, cpVect point, cpFloat distance, cpVect gradient, void *data);
    void ext_cpSpaceSegmentQueryFunc(cpShape *shape, cpVect point, cpVect normal, cpFloat alpha, void *data);
    void ext_cpSpaceBBQueryFunc(cpShape *shape, void *data);
    void ext_cpSpaceShapeQueryFunc(cpShape *shape, cpContactPointSet *points, void *data);

    void ext_cpSpaceDebugDrawCircleImpl(cpVect pos, cpFloat angle, cpFloat radius, cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, cpDataPointer data);
    void ext_cpSpaceDebugDrawSegmentImpl(cpVect a, cpVect b, cpSpaceDebugColor color, cpDataPointer data);
    void ext_cpSpaceDebugDrawFatSegmentImpl(cpVect a, cpVect b, cpFloat radius, cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, cpDataPointer data);
    void ext_cpSpaceDebugDrawPolygonImpl(int count, const cpVect *verts, cpFloat radius, cpSpaceDebugColor outlineColor, cpSpaceDebugColor fillColor, cpDataPointer data);
    void ext_cpSpaceDebugDrawDotImpl(cpFloat size, cpVect pos, cpSpaceDebugColor color, cpDataPointer data);
    cpSpaceDebugColor ext_cpSpaceDebugDrawColorForShapeImpl(cpShape *shape, cpDataPointer data);

    void ext_cpSpaceBodyIteratorFunc(cpBody *body, void *data);
    void ext_cpSpaceShapeIteratorFunc(cpShape *shape, void *data);
    void ext_cpSpaceConstraintIteratorFunc(cpConstraint *constraint, void *data);

    // cpMarch.h
    cpFloat ext_cpMarchSampleFunc(cpVect point, void *data);
    void ext_cpMarchSegmentFunc(cpVect v0, cpVect v1, void *data);

    // chipmunk_structs.h
    void ext_cpConstraintPreStepImpl(cpConstraint *constraint, cpFloat dt);
    void ext_cpConstraintApplyCachedImpulseImpl(cpConstraint *constraint, cpFloat dt_coef);
    void ext_cpConstraintApplyImpulseImpl(cpConstraint *constraint, cpFloat dt);
    cpFloat ext_cpConstraintGetImpulseImpl(cpConstraint *constraint);
}
