#include <stdint.h>

#ifdef __APPLE__
   #import "TargetConditionals.h"
#endif

#ifndef cpcalloc
	#define cpcalloc calloc
#endif



typedef double cpFloat;
typedef struct cpVect{cpFloat x,y;} cpVect;
typedef void * cpDataPointer;

static const cpVect cpvzero = {0.0f,0.0f};

typedef struct cpBody cpBody;
/// Rigid body velocity update function type.
typedef void (*cpBodyVelocityFunc)(cpBody *body, cpVect gravity, cpFloat damping, cpFloat dt);
/// Rigid body position update function type.
typedef void (*cpBodyPositionFunc)(cpBody *body, cpFloat dt);



struct cpBody {
	/// Function that is called to integrate the body's velocity. (Defaults to cpBodyUpdateVelocity)
	cpBodyVelocityFunc velocity_func;
	
	/// Function that is called to integrate the body's position. (Defaults to cpBodyUpdatePosition)
	cpBodyPositionFunc position_func;
	
	/// Mass of the body.
	/// Must agree with cpBody.m_inv! Use cpBodySetMass() when changing the mass for this reason.
	cpFloat m;
	/// Mass inverse.
	cpFloat m_inv;
	
	/// Moment of inertia of the body.
	/// Must agree with cpBody.i_inv! Use cpBodySetMoment() when changing the moment for this reason.
	cpFloat i;
	/// Moment of inertia inverse.
	cpFloat i_inv;
	
	/// Position of the rigid body's center of gravity.
	cpVect p;
	/// Velocity of the rigid body's center of gravity.
	cpVect v;
	/// Force acting on the rigid body's center of gravity.
	cpVect f;
	
	/// Rotation of the body around it's center of gravity in radians.
	/// Must agree with cpBody.rot! Use cpBodySetAngle() when changing the angle for this reason.
	cpFloat a;
	/// Angular velocity of the body around it's center of gravity in radians/second.
	cpFloat w;
	/// Torque applied to the body around it's center of gravity.
	cpFloat t;
	
	/// Cached unit length vector representing the angle of the body.
	/// Used for fast rotations using cpvrotate().
	cpVect rot;
	
	/// User definable data pointer.
	/// Generally this points to your the game object class so you can access it
	/// when given a cpBody reference in a callback.
	cpDataPointer data;
	
	/// Maximum velocity allowed when updating the velocity.
	cpFloat v_limit;
	/// Maximum rotational rate (in radians/second) allowed when updating the angular velocity.
	cpFloat w_limit;
	
	// CP_PRIVATE(cpVect v_bias);
	// CP_PRIVATE(cpFloat w_bias);
	
	// CP_PRIVATE(cpSpace *space);
	
	// CP_PRIVATE(cpShape *shapeList);
	// CP_PRIVATE(cpArbiter *arbiterList);
	// CP_PRIVATE(cpConstraint *constraintList);
	
	// CP_PRIVATE(cpComponentNode node);
};
/// Allocate a cpBody.
cpBody *cpBodyAlloc(void);
/// Initialize a cpBody.
cpBody *cpBodyInit(cpBody *body, cpFloat m, cpFloat i);
/// Allocate and initialize a cpBody.
cpBody *cpBodyNew(cpFloat m, cpFloat i);


void cpBodySetMass(cpBody *body, cpFloat m);
void cpBodySetMoment(cpBody *body, cpFloat i);
//void cpBodySetAngle(cpBody *body, cpFloat a);
