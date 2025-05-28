import weakref
from typing import Any

_dead_ref: weakref.ref[Any] = weakref.ref(set())
