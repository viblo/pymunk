from __future__ import absolute_import

if False:
    print("api mode")
    from pymunk._chipmunk_cffi_api import ffi, lib
else: 
    from pymunk._chipmunk_cffi_abi import ffi, lib 
    