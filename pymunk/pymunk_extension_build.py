import os
import os.path
import platform
from typing import List

from cffi import FFI  # type: ignore

ffibuilder = FFI()

with open("pymunk_cffi/chipmunk_cdef.h", "r") as f:
    ffibuilder.cdef(f.read())

# Callbacks need extra extern Python definitions
with open("pymunk_cffi/callbacks_cdef.h", "r") as f:
    ffibuilder.cdef(f.read())

hasty_space_include = ""
if platform.system() != "Windows":
    with open("pymunk_cffi/hastyspace_cdef.h", "r") as f:
        ffibuilder.cdef(f.read())
    hasty_space_include = """#include "chipmunk/cpHastySpace.h" """

source_folders = [os.path.join("Chipmunk2D", "src")]
sources = []
for folder in source_folders:
    for fn in os.listdir(folder):
        fn_path = os.path.join(folder, fn)
        if fn[-1] == "c":
            # Ignore cpHastySpace since it depends on pthread which
            # creates a dependency on libwinpthread-1.dll when built
            # with  mingw-w64 gcc.
            # Will prevent the code from being multithreaded, would be
            # good if some tests could be made to verify the performance
            # of this.
            if platform.system() != "Windows" or fn != "cpHastySpace.c":
                sources.append(fn_path)
            # sources.append(fn_path)
        elif fn[-1] == "o":
            os.remove(fn_path)

libraries: List[str] = []
# if os == linux:
#    libraries.append('m')

extra_compile_args = []
if platform.system() != "Windows":
    extra_compile_args.append("-std=c99")
# extra_compile_args.append('/Od')
# extra_compile_args.append('/DEBUG:FULL')
# , '/D_CHIPMUNK_FFI'],
with open("pymunk_cffi/extensions_cdef.h", "r") as f:
    ffibuilder.cdef(f.read())

with open("pymunk_cffi/extensions.c", "r") as f:
    custom_functions = f.read()

ffibuilder.set_source(
    "pymunk._chipmunk",  # name of the output C extension
    f"""
        //#include "chipmunk/chipmunk_types.h"
        //#include "chipmunk/cpVect.h"
        #include "chipmunk/chipmunk_ffi.h"
        #include "chipmunk/chipmunk.h"
        #include "chipmunk/chipmunk_unsafe.h"
        #include "chipmunk/cpPolyline.h"
        #include "chipmunk/cpMarch.h"
        
        {hasty_space_include}

        // from chipmunk_private.h
        // Ideally this should not come from here, but pickle needs it.
        void cpSpaceSetStaticBody(cpSpace *space, cpBody *body);

        {custom_functions}
    """,
    extra_compile_args=extra_compile_args,
    # extra_link_args=['/DEBUG:FULL'],
    include_dirs=[os.path.join("Chipmunk2D", "include")],
    sources=sources,
    libraries=libraries,
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True, debug=False)
