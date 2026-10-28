"""Check backend availability on the native GitHub-hosted wheel test runners.

Their x86-64 CPUs support AVX2. This is a CI assertion, not a requirement for
running Pymunk's ordinary tests on arbitrary machines or scalar-only builds.
"""

import platform
import struct

from pymunk._chipmunk import lib


if __name__ == "__main__":
    expected = (
        struct.calcsize("P") == 8
        and platform.machine().lower() in ("x86_64", "amd64")
    )
    available = bool(lib.cpContactSolverIsAvailable(lib.CP_CONTACT_SOLVER_AVX2))
    assert available == expected, (
        f"Unexpected AVX2 backend availability: {available}; "
        f"expected {expected} on {platform.machine()} "
        f"({struct.calcsize('P') * 8}-bit Python)"
    )
