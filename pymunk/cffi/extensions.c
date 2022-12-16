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

cpTimestamp cpSpaceGetTimestamp(cpSpace *space) {
    return space->stamp;
}

void cpSpaceSetTimestamp(cpSpace *space, cpTimestamp stamp) {
    space->stamp = stamp;
}

typedef void (*cpArbiterIteratorFunc)(cpArbiter *arb, void *data);

void cpSpaceEachCachedArbiter(cpSpace *space, cpArbiterIteratorFunc func, void *data) {
    cpHashSetEach(space->cachedArbiters, (cpHashSetIteratorFunc) func, data);
}

void cpSpaceAddCachedArbiter(cpSpace *space, cpArbiter *arb) {

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
    
    // Update the arbiter's state
    cpArrayPush(space->arbiters, arb);
    
    cpfree(contacts);
}

cpArbiter *cpArbiterNew(cpShape *a, cpShape *b){
    cpArbiter *arb = (cpArbiter *)cpcalloc(1, sizeof(struct cpArbiter));
    return cpArbiterInit(arb, a, b);
}

// cpContact *cpContactArrAlloc(int count){
//     return (cpContact *)cpcalloc(count, sizeof(struct cpContact));
// }