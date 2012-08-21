
import cffi

f = cffi.FFI()

f.cdef("""

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
""")

l = f.dlopen("./ex.so")

b = l.cpBodyNew(3,4)

print b.m, b.p.x
b.p.x = 3.5
print b.m, b.p.x

import timeit

import operator
import math

class Vec2d(): # this would be very fast in pypy
    #class Vec2d(ctypes.Structure):
    """2d vector class, supports vector and scalar operators,
       and also provides some high level functions
       """
    __slots__ = ['x', 'y']
     
    @classmethod
    def from_param(cls, arg):
        """Used by ctypes to automatically create Vec2ds"""
        return cls(arg)
     
    def getd(self):
        return {'x':self.x,'y':self.y}
        
    def __init__(self, x_or_pair=None, y = None):
        if x_or_pair != None:
            if y == None:
                self.x = x_or_pair[0]
                self.y = x_or_pair[1]
            else:
                self.x = x_or_pair
                self.y = y
  
    def __getitem__(self, key):
        
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    def __setitem__(self, key, value):
        
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    def update(self, *args, **kwargs):
        print 'update', args, kwargs
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v
   
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__
    
    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
 
    def cpvrotate(self, other):
        """Uses complex multiplication to rotate this vector by the other. """
        return Vec2d(self.x*other.x - self.y*other.y, self.x*other.y + self.y*other.x)
    

def run():
    b = l.cpBodyNew(15,17)
    for x in range(20000):
        s = 0
        for x in range(10):
            b.p = Vec2d(1,3).getd()
            v1 = Vec2d(b.p.x, b.p.y)
            
            v2 = Vec2d(1,3)
            b.p = (v1+v2.cpvrotate(v1)).getd()
            v3 = Vec2d(b.p.x, b.p.y)
            s+=v3.x+v3.y

                
def main():
    t = timeit.Timer('run()', "from __main__ import run") 
    print("runtime: %.2fs" % t.timeit(number=1))

if __name__ == '__main__':
    doprof = 0
    if not doprof: 
        main()
    else:
        import cProfile, pstats
        
        prof = cProfile.run("run()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats('cumulative', 'time', 'calls')
        stats.print_stats(30)
