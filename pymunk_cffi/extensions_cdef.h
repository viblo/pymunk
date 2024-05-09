//
// Functions to support efficient batch API
//

typedef enum pmBatchableBodyFields
{
	BODY_ID = 1 << 0,
	POSITION = 1 << 1,
	ANGLE = 1 << 2,
	VELOCITY = 1 << 3,
	ANGULAR_VELOCITY = 1 << 4,
	FORCE = 1 << 5,
    TORQUE = 1 << 6,
} pmBatchableBodyFields;

typedef enum pmBatchableArbiterFields
{
	BODY_A_ID = 1 << 0,
	BODY_B_ID = 1 << 1,
	TOTAL_IMPULSE = 1 << 2,
	TOTAL_KE = 1 << 3,
	IS_FIRST_CONTACT = 1 << 4,
	NORMAL = 1 << 5,

	CONTACT_COUNT = 1 << 6,

	POINT_A_1 = 1 << 7,
	POINT_B_1 = 1 << 8,
	DISTANCE_1 = 1 << 9,

	POINT_A_2 = 1 << 10,
	POINT_B_2 = 1 << 11,
	DISTANCE_2 = 1 << 12,
} pmBatchableArbiterFields;

typedef struct pmFloatArray pmFloatArray;
typedef struct pmIntArray pmIntArray;
typedef struct pmBatchedData pmBatchedData;

struct pmFloatArray
{
	int num, max;
	cpFloat *arr;
};

struct pmIntArray
{
	int num, max;
	uintptr_t *arr;
};

struct pmBatchedData
{
	pmIntArray *intArray;
	pmFloatArray *floatArray;
	pmBatchableBodyFields fields;
};

pmFloatArray *pmFloatArrayNew(int size);
void pmFloatArrayFree(pmFloatArray *arr);
void pmFloatArrayPush(pmFloatArray *arr, cpFloat v);
cpFloat pmFloatArrayPop(pmFloatArray *arr);
void pmFloatArrayPushVect(pmFloatArray *arr, cpVect v);
cpVect pmFloatArrayPopVect(pmFloatArray *arr);

pmIntArray *pmIntArrayNew(int size);
void pmIntArrayFree(pmIntArray *arr);
void pmIntArrayPush(pmIntArray *arr, uintptr_t v);
uintptr_t pmIntArrayPop(pmIntArray *arr);

void pmSpaceBodyGetIteratorFuncBatched(cpBody *body, void *data);
void pmSpaceBodySetIteratorFuncBatched(cpBody *body, void *data);
void pmSpaceArbiterIteratorFuncBatched(cpArbiter *arbiter, void *data);

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

cpFloat defaultSpringForce(cpDampedSpring *spring, cpFloat dist);

cpFloat defaultSpringTorque(cpDampedRotarySpring *spring, cpFloat relativeAngle);