"""This module contain functions used to load the chipmunk dll/lib file"""

import os.path
import platform
import sys, imp, os
 
def load_library(ffi, libname, debug_lib=True):
    # lib gets loaded from
    # 32bit python: pymunk/libchipmunk.so, libchipmunk.dylib or chipmunk.dll
    # 64 bit python pymunk/libchipmunk64.so, libchipmunk.dylib or chipmunk64.dll
    
    s = platform.system()
    if sys.maxsize > 2**32:
        arch = "64"
    else:
        arch = "32"
        
    path = os.path.dirname(os.path.abspath(__file__))
    
    try:
        if hasattr(sys, "frozen") or \
            hasattr(sys, "importers") or \
            hasattr(imp, "is_frozen") and imp.is_frozen("__main__"):
            if 'site-packages.zip' in __file__:
                path = os.path.join(os.path.dirname(os.getcwd()), 'Frameworks')
            else:
                path = os.path.dirname(os.path.abspath(sys.executable))
    except:
        pass
    
    # we use *nix library naming as default
    pattern = "lib%s.so"
    if s in ('Windows', 'Microsoft'):
        pattern = "%s.dll"    
    elif s == 'Darwin':
        pattern = "lib%s.dylib"
    
    libfn = os.path.join(path, pattern % libname)
    
    if debug_lib:
        print ("Loading chipmunk for %s (%sbit) [%s]" % (s, arch, libfn))
    try:
        lib = ffi.dlopen(libfn)
    except OSError: 
        print ("""
Failed to load Pymunk library.

This error usually means that you don't have a compiled version of Chipmunk in 
the correct spot where Pymunk can find it. If you tried to run Pymunk without
installing it properly this can be the result.

The good news is that it is usually enough (at least on *nix and OS X) to 
run the build command:

You compile Chipmunk with
> python setup.py build_ext --inplace
and then continue as usual with 
> cd examples
> python basic_test.py

(for complete instructions please see the readme file)

Another cause of this problem could be if you didnt included the Chipmunk 
library when using a freeze tool such as Py2exe or PyInstaller. Please see the
examples for how to include the library file when freezing a binary. 

If it still doesnt work, please report as a bug on the issue tracker at 
https://github.com/viblo/pymunk/issues
Remember to include information about your OS, which version of python you use 
and the version of pymunk you tried to run. A description of what you did to 
trigger the error is also good. Please include the exception traceback if any 
(usually found below this message).
""")
        raise
    return lib, libfn
