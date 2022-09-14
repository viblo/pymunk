from __future__ import absolute_import

import _cffi_backend  # type: ignore # for PyInstaller, py2exe and other bundlers

from ._chipmunk import ffi, lib  # type: ignore

ffi = ffi
lib = lib

__all__ = ["ffi", "lib"]
