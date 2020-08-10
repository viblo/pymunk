from typing import NamedTuple

class Transform(NamedTuple):
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
    a: float = 1
    b: float = 0
    c: float = 0
    d: float = 1
    tx: float = 0
    ty: float = 0
    
    @staticmethod
    def identity() -> 'Transform':
        """The identity transform"""
        return Transform(1,0,0,1,0,0)
