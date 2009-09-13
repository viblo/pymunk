import os.path
import platform
import sys, imp, os
import ctypes
 
def load_library(libname, print_path=True):
    # lib gets loaded from:
    # pymunk/libchipmunk.so, libchipmunk.dylib or chipmunk.dll
     
    s = platform.system()
    arch, _ = platform.architecture()
 
    path = os.path.dirname(os.path.abspath(__file__))
    
    try:
        if hasattr(sys, "frozen") or \
            hasattr(sys, "importers") or \
            hasattr(imp, "is_frozen") and imp.is_forzen("__main__"):
            if 'site-packages.zip' in __file__:
                path = os.path.join(os.path.dirname(os.getcwd()), 'Frameworks')
            else:
                path = os.path.dirname(os.path.abspath(sys.executable))
    except:
        pass
    
    if s in ('Linux', 'FreeBSD'):
        libfn = "lib%s.so" % libname

    elif s in ('Windows', 'Microsoft'):
        libfn = "%s.dll" % libname

    elif s == 'Darwin':
        libfn = "lib%s.dylib" % libname
    
    # we use *nix library naming as default
    else: 
        libfn = "lib%s.so" % libname
    libfn = os.path.join(path, libfn)
    
    if print_path:
        print ("Loading chipmunk for %s (%s) [%s]" % (s, arch, libfn))
    lib = ctypes.cdll.LoadLibrary(libfn)
    return lib
