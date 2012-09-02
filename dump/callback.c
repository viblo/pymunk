#include <stdlib.h>
#include "callback.h"

cpBody*
cpBodyAlloc(void)
{
	cpBody * b = (cpBody *)calloc(1, sizeof(cpBody));
    b->m3 = 1.2;
    return b;
}

cpArbiter*
cpArbiterAlloc(void)
{
	cpArbiter * a = (cpArbiter *)calloc(1, sizeof(cpArbiter));
    a->x3 = 1.3;
    return a;
}

void
cpBodyEachArbiter(cpBody *body, cpBodyArbiterIteratorFunc func, void *data)
{
	cpArbiter *arb = cpArbiterAlloc();
	func(body, arb, data);
}