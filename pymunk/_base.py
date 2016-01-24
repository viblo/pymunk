from ctypes import *
from .vec2d import Vec2d

# Contains some base types for internal pymunk use


if sizeof(c_void_p) == 4: 
    uintptr_t = c_uint 
else: 
    uintptr_t = c_ulonglong
cpGroup = uintptr_t
cpBitmask = c_uint
cpFloat = c_double
