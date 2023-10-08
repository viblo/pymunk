
///////////////////////////////////////////
// cpHastySpace.h
///////////////////////////////////////////

struct cpHastySpace;
typedef struct cpHastySpace cpHastySpace;

cpSpace *cpHastySpaceNew(void);
void cpHastySpaceFree(cpSpace *space);

void cpHastySpaceSetThreads(cpSpace *space, unsigned long threads);

unsigned long cpHastySpaceGetThreads(cpSpace *space);

void cpHastySpaceStep(cpSpace *space, cpFloat dt);