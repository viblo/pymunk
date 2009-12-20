import os.path
import platform
import sys, imp, os
import ctypes
 
def platform_specific_functions():
    # use stddecl on windows, cdecl on all other platforms
    
    d = {'library_loader' : ctypes.cdll
        ,'function_pointer' : ctypes.CFUNCTYPE
        }
    
    if platform.system() in ('Windows', 'Microsoft'):
        d['library_loader'] = ctypes.windll
        d['function_pointer'] = ctypes.WINFUNCTYPE
        
    return d
    
 
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
    try:
        lib = platform_specific_functions()['library_loader'].LoadLibrary(libfn)
    except OSError: 
        print ("""
Failed to load pymunk library.

This error usually means that you don't have a compiled version of chipmunk in 
the correct spot where pymunk can find it. Usually its enough (at least on 
*nix & macos) to simply run the compile command first before installing and 
then retry again:

You compile chipmunk with
> python setup.py build_chipmunk
and then continue as usual with 
> python setup.py install
> cd examples
> python demo_contact.py

(for complete instructions please see the readme file)

If it still doesnt work, please report as a bug on the issue tracker at 
http://code.google.com/p/pymunk/issues
Remember to include information about your OS and version of python. Please 
include the exception traceback as well (usually found below this message).
""")
        raise
    return lib
