import os
import sys
import ctypes
import ctypes.util

def load_library(libname, print_path=False):
    platform = sys.platform
    
    names = [libname]
    if platform == "darwin":
        names.append('dylib.%s.so' % libname)
    elif platform == "linux2":
        names.append('lib%s.so' % libname)

    for name in names:
        try:
            lib = ctypes.cdll.LoadLibrary(name)
            if print_path: print name
            return lib
        except OSError:
            if platform == "darwin":
                path = find_osx(lib)
            else:
                path = ctypes.util.find_library(name)
            if path:
                try:
                    lib = ctypes.cdll.LoadLibrary(path)
                    if print_path: print path
                except OSError:
                    pass
    raise ImportError("Library %s could not be found and loaded" % libname[0])

    
def find_osx(libname): 
    if 'LD_LIBRARY_PATH' in os.environ:
        ld_library_path = os.environ['LD_LIBRARY_PATH'].split(':')
    else:
        ld_library_path = []

    if 'DYLD_LIBRARY_PATH' in os.environ:
        dyld_library_path = os.environ['DYLD_LIBRARY_PATH'].split(':')
    else:
        dyld_library_path = []

    if 'DYLD_FALLBACK_LIBRARY_PATH' in os.environ:
        dyld_fallback_library_path = os.environ['DYLD_FALLBACK_LIBRARY_PATH'].split(':')
    else:
        dyld_fallback_library_path = [os.path.expanduser('~/lib'),'/usr/local/lib', '/usr/lib']
    
    search_paths = [os.path.join(p, libname) for p in ld_library_path]
    search_paths += [os.path.join(p, libname) for p in dyld_library_path]
    search_paths += [libname]
    search_paths += [os.path.join(p, libname) for p in dyld_fallback_library_path]

    for path in search_paths:
        if os.path.exists(path):
            return path

    return None