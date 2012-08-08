#include <stdlib.h>
#include <float.h>
#include <math.h>

#include "ex.h"

cpBody*
cpBodyAlloc(void)
{
	return (cpBody *)cpcalloc(1, sizeof(cpBody));
}

cpBody *
cpBodyInit(cpBody *body, cpFloat m, cpFloat i)
{
	//body->space = NULL;
	//body->shapeList = NULL;
	//body->arbiterList = NULL;
	//body->constraintList = NULL;
	
	//body->velocity_func = cpBodyUpdateVelocity;
	//body->position_func = cpBodyUpdatePosition;
	
	//cpComponentNode node = {NULL, NULL, 0.0f};
	//body->node = node;
	
	body->p = cpvzero;
	body->v = cpvzero;
	body->f = cpvzero;
	
	body->w = 0.0f;
	body->t = 0.0f;
	
	// body->v_bias = cpvzero;
	// body->w_bias = 0.0f;
	
	body->v_limit = (cpFloat)INFINITY;
	body->w_limit = (cpFloat)INFINITY;
	
	body->data = NULL;
	
	// Setters must be called after full initialization so the sanity checks don't assert on garbage data.
	cpBodySetMass(body, m);
	cpBodySetMoment(body, i);
	//cpBodySetAngle(body, 0.0f);
	
	return body;
}

cpBody*
cpBodyNew(cpFloat m, cpFloat i)
{
	return cpBodyInit(cpBodyAlloc(), m, i);
}

void
cpBodySetMass(cpBody *body, cpFloat mass)
{
	//cpBodyActivate(body);
	body->m = mass;
	body->m_inv = 1.0f/mass;
}

void
cpBodySetMoment(cpBody *body, cpFloat moment)
{
	///cpBodyActivate(body);
	body->i = moment;
	body->i_inv = 1.0f/moment;
}
