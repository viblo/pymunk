typedef struct cpVectArr cpVectArr;
struct cpVectArr {
	int num, max;
	cpVect *arr;
};
void cpSpaceGetBodyPositions(cpSpace *space, cpVectArr *arr);

//
// Functions to support pickle of arbiters the space has cached
//

cpTimestamp cpSpaceGetTimestamp(cpSpace *space);
void cpSpaceSetTimestamp(cpSpace *space, cpTimestamp stamp);

typedef void (*cpArbiterIteratorFunc)(cpArbiter *arb, void *data);
void cpSpaceEachCachedArbiter(cpSpace *space, cpArbiterIteratorFunc func, void *data);
extern "Python" {
    void ext_cpArbiterIteratorFunc(cpArbiter *arb, void *data);
}
void cpSpaceAddCachedArbiter(cpSpace *space, cpArbiter *arb);

cpArbiter *cpArbiterNew(void);