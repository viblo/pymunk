from ctypes import *
from ._base import *

class ShapeFilter(Structure):
    """
    
    Chipmunk has two primary means of ignoring collisions: groups and 
    category masks.

    Groups are used to ignore collisions between parts on a complex object. A 
    ragdoll is a good example. When jointing an arm onto the torso, you'll 
    want them to allow them to overlap. Groups allow you to do exactly that. 
    Shapes that have the same group don't generate collisions. So by placing 
    all of the shapes in a ragdoll in the same group, you'll prevent it from 
    colliding against other parts of itself. Category masks allow you to mark 
    which categories an object belongs to and which categories it collidies 
    with.

    For example, a game has four collision categories: player (0), enemy (1), 
    player bullet (2), and enemy bullet (3). Neither players nor enemies 
    should not collide with their own bullets, and bullets should not collide 
    with other bullets. However, players collide with enemy bullets, and 
    enemies collide with player bullets.

    ============= =============== =============
    Object        Object Category Category Mask
    ============= =============== =============
    Player        1               4, 5       
    Enemy         2               2, 3, 4
    Player Bullet 3               1, 5
    Enemy Bullet  4               2, 5
    Walls         5               1, 2, 3, 4
    ============= =============== =============
    
    Note that everything in this example collides with walls. Additionally, 
    the enemies collide with eachother.

    By default, objects exist in every category and collide with every category.

    Objects can fall into multiple categories. For instance, you might have a 
    category for a red team, and have a red player bullet. In the above 
    example, each object only has one category. If you make use of multiple 
    categories on an object, you may also wish to consider replacing the 
    ShapeFilter class and the cpShapeFilterReject() function in 
    chipmunk_private.h to customize it to better suit your game's needs.

    The default type of categories and mask in ShapeFilter is unsigned int 
    which has a resolution of 32 bits on most systems. You can redefine 
    cpBitmask in chipmunk_types.h if you need more bits to work with.

    There is one last way of filtering collisions using collision handlers. 
    See the section on callbacks for more information. Collision handlers can 
    be more flexible, but can be slower. Fast collision filtering rejects 
    collisions before running the expensive collision detection code, so 
    using groups or category masks is preferred.

    """
    __slots__ = ['group', 'categories', 'mask']
    
    @classmethod
    def from_param(cls, arg):
        """Used by ctypes to automatically create ShapeFilters"""
        return cls(arg)
        
    def __init__(self, group_or_tuple=None, categories = None, mask = None):
        """ShapeFilter constructor. 
        
        Call with empty arguments (`f = ShapeFilter()`) to create a 
        filter that dont filter out any categories or masks.
        """
        if group_or_tuple != None:
            if categories == None:
                self.group = group_or_tuple.group
                self.categories = group_or_tuple.categories
                self.mask = group_or_tuple.mask
            else:
                self.group = group_or_tuple
                self.categories = categories
                self.mask = mask
        if group_or_tuple == None and categories == None and mask == None:
            self.group = 0
            self.categories = 0xffffffff
            self.mask = 0xffffffff
 
    def __len__(self):
        return 3
 
    def __getitem__(self, key):
        if key == 0:
            return self.group
        elif key == 1:
            return self.categories
        elif key == 2:
            return self.mask
        else:
            raise IndexError("Invalid subscript "+str(key)+" to ShapeFilter")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.group = value
        elif key == 1:
            self.categories = value
        elif key == 2:
            self.mask = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to ShapeFilter")
 
    # String representaion (for debugging)
    def __repr__(self):
        return 'ShapeFilter(%s, 0x%x, 0x%x)' % (self.group, self.categories, self.mask)
    
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            
            return tuple(other) == tuple(self)
        else:
            return False
            
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return tuple(other) != tuple(self)
        else:
            return True
    
    
    
ShapeFilter._fields_ = [
    ('group', cpGroup),
    ('categories', cpBitmask),
    ('mask', cpBitmask),
]



from . import _chipmunk_cffi
cp = _chipmunk_cffi.C
ffi = _chipmunk_cffi.ffi
from .vec2d import Vec2d

class Transform2():
    """Type used for 2x3 affine transforms.
    
    See wikipedia for details: 
    http://en.wikipedia.org/wiki/Affine_transformation
    
    The properties map to the matrix in this way: 
    
    = = ==
    = = ==
    a c tx
    b d ty
    = = ==
        
    An instance can be created with args or kwargs::
        >>> Transform()
        Transform(1.0,0.0,0.0,1.0,0.0,0.0)
        >>> Transform(1, 2, 3, 4, 5, 6)
        Transform(1.0,2.0,3.0,4.0,5.0,6.0)
        >>> Transform(1, d=4, tx=5)
        Transform(1.0,0.0,0.0,4.0,5.0,0.0)
        
    """
    
class Transform(list):
    """Type used for 2x3 affine transforms.
    
    See wikipedia for details: 
    http://en.wikipedia.org/wiki/Affine_transformation
    
    The properties map to the matrix in this way: 
    
    = = ==
    = = ==
    a c tx
    b d ty
    = = ==
        
    An instance can be created with args or kwargs::
        >>> Transform()
        Transform(0.0,0.0,0.0,0.0,0.0,0.0)
        >>> Transform(1,2,3,4,5,6)
        Transform(1.0,2.0,3.0,4.0,5.0,6.0)
        >>> Transform(1, d=4, tx=5)
        Transform(1.0,0.0,0.0,4.0,5.0,0.0)
        
    """
    __slots__ = ['a', 'b', 'c', 'd', 'tx', 'ty']
    
    a = 0
    b = 0
    c = 0
    d = 0
    tx = 0
    ty = 0
    
    def __init__(self, a=0, b=0, c=0, d=0, tx=0, ty=0):
        super(list, self).__init__([a,b,c,d,tx,ty])
        return 
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.tx = tx
        self.ty = ty 
    
    @staticmethod
    def identity():
        """The identity transform"""
        return Transform(1,0,0,1,0,0)
        
    def __repr__(self):
        return 'Transform(%s,%s,%s,%s,%s,%s)' % (self.a, self.b, self.c, self.d, self.tx, self.ty)
    