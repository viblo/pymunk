//
// Functions to support efficient batch API
//

typedef struct cpVectArray cpVectArray;
typedef struct cpFloatArray cpFloatArray;

struct cpVectArray
{
	int num, max;
	cpVect *arr;
};

struct cpFloatArray
{
	int num, max;
	cpFloat *arr;
};

cpVectArray *cpVectArrayNew(int size);
cpFloatArray *cpFloatArrayNew(int size);
void cpVectArrayFree(cpVectArray *arr);
void cpFloatArrayFree(cpFloatArray *arr);

void cpSpaceGetBodyPositions(cpSpace *space, cpVectArray *positionArr, cpFloatArray *angleArr);

//
// Functions to support pickle of arbiters the space has cached
//

cpHashValue cpShapeGetHashID(cpShape *shape);
void cpShapeSetHashID(cpShape *shape, cpHashValue id);

cpHashValue cpSpaceGetShapeIDCounter(cpSpace *space);
void cpSpaceSetShapeIDCounter(cpSpace *space, cpHashValue counter);

cpTimestamp cpSpaceGetTimestamp(cpSpace *space);
void cpSpaceSetTimestamp(cpSpace *space, cpTimestamp stamp);

void cpSpaceSetCurrentTimeStep(cpSpace *space, cpFloat curr_dt);

typedef void (*cpArbiterIteratorFunc)(cpArbiter *arb, void *data);
void cpSpaceEachCachedArbiter(cpSpace *space, cpArbiterIteratorFunc func, void *data);
extern "Python"
{
	void ext_cpArbiterIteratorFunc(cpArbiter *arb, void *data);
}
void cpSpaceAddCachedArbiter(cpSpace *space, cpArbiter *arb);

cpArbiter *cpArbiterNew(cpShape *a, cpShape *b);
typedef struct cpContact cpContact;

cpContact *cpContactArrAlloc(int count);
