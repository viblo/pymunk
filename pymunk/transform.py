from collections import namedtuple

class Transform(namedtuple('Transform', ['a','b','c','d','tx','ty'])):
    """Type used for 2x3 affine transforms.
    
    See wikipedia for details: 
    http://en.wikipedia.org/wiki/Affine_transformation
    
    The properties map to the matrix in this way: 
    
    = = ==
    = = ==
    a c tx
    b d ty
    = = ==
        
    An instance can be created in this way::
        >>> Transform(1,2,3,4,5,6)
        Transform(a=1, b=2, c=3, d=4, tx=5, ty=6)
    Or using the default identity in this way::
        >>> Transform.identity()
        Transform(a=1, b=0, c=0, d=1, tx=0, ty=0)
    Or overriding only some of the values (on a identity matrix):
        >>> Transform(b=3,ty=5)
        Transform(a=1, b=3, c=0, d=1, tx=0, ty=5)
    
        
    """
    __slots__ = ()
    
    def __new__(cls, a=1, b=0, c=0, d=1, tx=0, ty=0):
        self = super(Transform, cls).__new__(cls, a, b, c, d, tx, ty)
        return self
    
    @staticmethod
    def identity():
        """The identity transform"""
        return Transform(1,0,0,1,0,0)
