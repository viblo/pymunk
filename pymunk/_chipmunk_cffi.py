from cffi import FFI
ffi = FFI()
ffi.cdef("""
    typedef float cpFloat;
    
""")
lib = "chipmunk.dll"
C = ffi.dlopen(lib)                     # loads the entire C namespace

