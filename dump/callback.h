
typedef struct cpBody cpBody;
typedef struct cpArbiter cpArbiter;

struct cpBody {
    double m1;
    double m2;
    double m3;
    double m4;
    double m5;
    double m6;
};

struct cpArbiter {
    double x1;
    double x2;
    double x3;
    double x4;
    double x5;
    double x6;
};

typedef void (*cpBodyArbiterIteratorFunc)(cpBody *body, cpArbiter *arbiter, void *data);
/// Call @c func once for each arbiter that is currently active on the body.
void cpBodyEachArbiter(cpBody *body, cpBodyArbiterIteratorFunc func, void *data);

cpBody* cpBodyAlloc(void);
cpArbiter* cpArbiterAlloc(void);
