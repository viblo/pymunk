from  _chipmunk_cffi import ffi, lib

_space = lib.cpSpaceNew()
_body = lib.cpBodyNew(1, 1)
_shape = lib.cpCircleShapeNew(_body, 10, (0,0))
lib.cpSpaceAddShape(_space, _shape)

info = ffi.new("cpPointQueryInfo *")
f = ffi.new("cpShapeFilter *")
f.group = 0
f.categories = 0
f.mask = 0
fa = f[0]

x = lib.cpSpacePointQueryNearest(_space, (4,0), 0, f[0], info)
print x
