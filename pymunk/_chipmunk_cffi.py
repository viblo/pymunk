if False:
    print("api mode")
    from . import _chipmunk_cffi_api
    lib = _chipmunk_cffi_api.lib
    ffi = _chipmunk_cffi_api.ffi
else:
    #print("abi mode")
    from . import _chipmunk_cffi_abi
    lib = _chipmunk_cffi_abi.lib
    ffi = _chipmunk_cffi_abi.ffi
