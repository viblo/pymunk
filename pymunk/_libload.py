"""This module contain functions used to load the chipmunk dll/lib file"""

import imp
import os
import os.path
import platform
import sys


def load_library(ffi, libname, debug_lib=True):
    # lib gets loaded from
    # 32bit python: pymunk/libchipmunk.so, libchipmunk.dylib or chipmunk.dll
    # 64 bit python pymunk/libchipmunk64.so, libchipmunk.dylib or chipmunk64.dll

    s = platform.system()
    if sys.maxsize > 2 ** 32:
        arch = "64"
    else:
        arch = "32"

    # we use *nix library naming as default
    pattern = "lib%s.so"
    if s in ("Windows", "Microsoft"):
        pattern = "%s.dll"
    elif s == "Darwin":
        pattern = "lib%s.dylib"

    path = os.path.dirname(os.path.abspath(__file__))
    libfn = pattern % libname
    lib_path = os.path.join(path, libfn)
    # A frozen app may not:
    #   - have a site-packages.zip
    #   - or include the data inside the executable.
    # It may have a .so/.dll.dylib in a normal folder.
    try:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            # PyInstaller bundle. Assumes chipmunk.dll is in its root
            # i.e. something like this in the spec file:
            # binaries=[ ( pymunk.chipmunk_path, '.' ) ],
            lib_path = os.path.join(sys._MEIPASS, libfn)
        elif (
            not os.path.exists(lib_path)
            and hasattr(sys, "frozen")
            or hasattr(sys, "importers")
            or hasattr(imp, "is_frozen")
            and imp.is_frozen("__main__")
        ):

            if "site-packages.zip" in __file__:
                path = os.path.join(os.path.dirname(os.getcwd()), "Frameworks")
            else:
                path = os.path.dirname(os.path.abspath(sys.executable))
            lib_path = os.path.join(path, libfn)

    except:
        pass

    if debug_lib:
        print("Loading chipmunk for %s (%sbit) [%s]" % (s, arch, lib_path))
    try:
        lib = ffi.dlopen(lib_path)
    except OSError:
        print(
            """
Failed to load Pymunk library.

This error usually means that you don't have a compiled version of Chipmunk in
the correct spot where Pymunk can find it. If you tried to run Pymunk without
installing it properly this can be the result.

The good news is that it is usually enough (at least on *nix and OS X) to
run the build command:

You compile Chipmunk with
> python setup.py build_ext --inplace
and then verify with
> python -m pymunk.test

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
"""
        )
        raise
    return lib, lib_path
