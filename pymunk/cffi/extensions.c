#include "chipmunk/chipmunk_private.h"

//
// Functions to support efficient batch API
//

typedef struct cpVectArr cpVectArr;


struct cpVectArr {
	int num, max;
	cpVect *arr;
};

void cpSpaceBodyIteratorFuncForPositions(cpBody *body, void *data){
    cpVectArr *arr = (cpVectArr*)data;
    cpVect v = cpBodyGetPosition(body);
    if (arr->num == (arr->max - 1) || arr->num == arr->max) {
        arr->max = 3*(arr->max + 1)/2;
        arr->arr = (cpVect*)cprealloc(arr->arr, arr->max*sizeof(cpVect));
    }
    arr->arr[arr->num] = v;
    arr->num++;
    
}

void cpSpaceGetBodyPositions(cpSpace *space, cpVectArr *arr) {
    cpSpaceEachBody(space, cpSpaceBodyIteratorFuncForPositions, arr);
	
}

//
// Functions to support pickle of arbiters the space has cached
//
typedef struct cpContact cpContact;

cpHashValue cpShapeGetHashID(cpShape *shape){
    return shape->hashid;
}
void cpShapeSetHashID(cpShape *shape, cpHashValue id){
    shape->hashid = id;
}


cpHashValue cpSpaceGetShapeIDCounter(cpSpace *space){
    return space->shapeIDCounter;
}
void cpSpaceSetShapeIDCounter(cpSpace *space, cpHashValue counter){
    space->shapeIDCounter = counter;
}

cpTimestamp cpSpaceGetTimestamp(cpSpace *space) {
    return space->stamp;
}

void cpSpaceSetTimestamp(cpSpace *space, cpTimestamp stamp) {
    space->stamp = stamp;
}

void cpSpaceSetCurrentTimeStep(cpSpace *space, cpFloat curr_dt) {
	space->curr_dt = curr_dt;
}

typedef void (*cpArbiterIteratorFunc)(cpArbiter *arb, void *data);

void cpSpaceEachCachedArbiter(cpSpace *space, cpArbiterIteratorFunc func, void *data) {
    cpHashSetEach(space->cachedArbiters, (cpHashSetIteratorFunc) func, data);
}

void cpSpaceTest(cpSpace *space) {
    struct cpContact *contacts2 = cpContactBufferGetArray(space);
    return;
}
static inline cpCollisionHandler *
cpSpaceLookupHandler(cpSpace *space, cpCollisionType a, cpCollisionType b, cpCollisionHandler *defaultValue)
{
	cpCollisionType types[] = {a, b};
	cpCollisionHandler *handler = (cpCollisionHandler *)cpHashSetFind(space->collisionHandlers, CP_HASH_PAIR(a, b), types);
	return (handler ? handler : defaultValue);
}

void cpSpaceAddCachedArbiter(cpSpace *space, cpArbiter *arb) {
    // Need to init the contact buffer
    cpSpacePushFreshContactBuffer(space);
    
    int numContacts = arb->count;
    struct cpContact *contacts = arb->contacts;
    // Restore contact values back to the space's contact buffer memory
    arb->contacts = cpContactBufferGetArray(space);
    
    memcpy(arb->contacts, contacts, numContacts*sizeof(struct cpContact));
    cpSpacePushContacts(space, numContacts);
    
    // Reinsert the arbiter into the arbiter cache
    const cpShape *a = arb->a, *b = arb->b;
    const cpShape *shape_pair[] = {a, b};
    cpHashValue arbHashID = CP_HASH_PAIR((cpHashValue)a, (cpHashValue)b);
    cpHashSetInsert(space->cachedArbiters, arbHashID, shape_pair, NULL, arb);

    // Set handlers to their defaults
    cpCollisionType typeA = a->type, typeB = b->type;
	cpCollisionHandler *defaultHandler = &space->defaultHandler;
	cpCollisionHandler *handler = arb->handler = cpSpaceLookupHandler(space, typeA, typeB, defaultHandler);
	
	// Check if the types match, but don't swap for a default handler which use the wildcard for type A.
	cpBool swapped = arb->swapped = (typeA != handler->typeA && handler->typeA != CP_WILDCARD_COLLISION_TYPE);
	
	if(handler != defaultHandler || space->usesWildcards){
		// The order of the main handler swaps the wildcard handlers too. Uffda.
		arb->handlerA = cpSpaceLookupHandler(space, (swapped ? typeB : typeA), CP_WILDCARD_COLLISION_TYPE, &cpCollisionHandlerDoNothing);
		arb->handlerB = cpSpaceLookupHandler(space, (swapped ? typeA : typeB), CP_WILDCARD_COLLISION_TYPE, &cpCollisionHandlerDoNothing);
	}

    // Update the arbiter's state
    cpArrayPush(space->arbiters, arb);
    
    cpfree(contacts);
}

cpArbiter *cpArbiterNew(cpShape *a, cpShape *b) {
    cpArbiter *arb = (cpArbiter *)cpcalloc(1, sizeof(struct cpArbiter));
    return cpArbiterInit(arb, a, b);
}


cpContact *cpContactArrAlloc(int count){
    return (cpContact *)cpcalloc(count, sizeof(struct cpContact));
}