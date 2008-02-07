# This program is public domain.
# Author: Paul Kienzle
"""
ctypes load_library version which looks in the current directory
and on standard paths for the library file.
"""

import sys, os.path, ctypes
import inspect


def load_library(name, path=None):
    """
    ctypes library loader.

    ctypes wrappers needs the location of the libNeXus precompiled binary. 
    The function loadlibrary(name) looks in the usual places for the named 
    library.

    The following are checked in order:

        the path=dir optional argument          - All
        the directory containing the caller     - All
        os.environ['LD_LIBRARY_PATH']           - Unix
        os.environ['DYLD_LIBRARY_PATH']         - Darwin
        /usr/local/lib                          - Unix and Darwin
        /usr/lib                                - Unix and Darwin

    The extension is .dll for Windows, .dylib for Darwin and .so for other Unix.

    The import will raise an OSError exception if the library wasn't found
    or couldn't be loaded.  Note that on Windows in particular this may be
    because supporting dlls were not available on the path or in the directory
    of the dll.
    """

    # Check if we are given a path
    pathlist = [path] if path is not None and path != '' else []

    # Figure out where the caller is located
    if True: 
        # Use frame magic to get the directory containing the caller
        called_from = inspect.getframeinfo(inspect.currentframe().f_back)[0]
        pathlist.append(os.path.dirname(os.path.abspath(called_from)))
    else:
        # Require that ctload be in the directory containing the DLL
        pathlist.append(os.path.dirname(__file__))

    if sys.platform in ('win32','cygwin'):
        lib = name+'.dll'
    else:
        if sys.platform in ('darwin'):
            lib = name+'.dylib'
            ldenv = 'DYLD_LIBRARY_PATH'
        else:
            lib = name+'.so'
            ldenv = 'LD_LIBRARY_PATH'
        pathlist += [p for p in os.environ.get(ldenv,'').split(':') if p != '']
        pathlist += ['/usr/local/lib','/usr/lib']

    # Given a list of files, try loading the first one that is available.
    files = [os.path.join(p,lib) for p in pathlist]
    for file in files:
        if not os.path.isfile(file): continue
        try:
            return ctypes.CDLL(file)
        except:
            raise OSError, "%s code not be loaded: %s"%(file, sys.exc_info()[0])
    raise OSError, "Library not found in [%s]"%(", ".join(files))

