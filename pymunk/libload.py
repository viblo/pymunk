import os.path
import platform
import sys, imp
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
            hasattr(imp, "is_frozen") and imp.is_forzen("__main__"):
            path = os.path.dirname(os.path.abspath(sys.executable))
    except:
        pass
    libfn_specific = None
    
    if s == 'Linux':
        libfn = "lib%s.so" % libname
        libfn_specific = "lib%s%s.so" % (libname, arch[:2])

    elif s == 'Windows':
        libfn = "%s.dll" % libname

    elif s == 'Darwin':
        libfn = "lib%s.dylib" % libname
        
    libfn = os.path.join(path, libfn)
    
    if libfn_specific != None:
        libfn_specific = os.path.join(path, libfn_specific)
        try:
            if print_path:
                print "Loading chipmunk for %s (%s) [%s]" % (s, arch, libfn_specific)
            lib = ctypes.cdll.LoadLibrary(libfn)
        except:
            if print_path:
                print "Loading chipmunk for %s (%s) [%s]" % (s, arch, libfn)
            lib = ctypes.cdll.LoadLibrary(libfn)    
    else:
        if print_path:
            print "Loading chipmunk for %s (%s) [%s]" % (s, arch, libfn)
        lib = ctypes.cdll.LoadLibrary(libfn)
    return lib
