import os.path
import platform
import ctypes
 
def load_library(libname, print_path=True):
    # lib gets loaded from:
    # pymunk/libchipmunk32.so, -64.so, .dll or .dylib
     
    s = platform.system()
    arch, arch2 = platform.architecture()
 
    path = os.path.dirname(os.path.abspath(__file__))
    try:
        if hasattr(sys, "frozen") or \
            hasattr(sys, "importers") or \
            hassattr(imp, "is_frozen") and imp.is_forzen("__main__"):
            path = os.path.dirname(os.path.abspath(sys.executable))
    except:
        pass
    if s == 'Linux':
        libfn = "%s%s.so" % (libname, arch[:2])
        
    elif s == 'Windows':
        libfn = "%s.dll" % libname
        
    elif s == 'Darwin':
        libfn = "%s.dylib" % libname
 
    libfn = os.path.join(path, libfn)
    if print_path:
        print "Loading chipmunk for %s (%s) [%s]" % (s, arch, libfn)
    lib = ctypes.cdll.LoadLibrary(libfn)
 
    return lib
