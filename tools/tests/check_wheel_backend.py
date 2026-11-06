"""Check installed wheel backends on the GitHub-hosted and Pyodide runners.

Native x86-64 runners support AVX2; Pyodide wheels require Wasm SIMD. These are
CI assertions, not requirements for arbitrary machines or custom scalar builds.
"""

import platform
import struct
import sys

import pymunk
from pymunk._chipmunk import lib


if __name__ == "__main__":
    wasm_expected = sys.platform == "emscripten"
    avx2_expected = (
        not wasm_expected
        and struct.calcsize("P") == 8
        and platform.machine().lower() in ("x86_64", "amd64")
    )
    for backend, expected in (
        (lib.CP_CONTACT_SOLVER_AVX2, avx2_expected),
        (lib.CP_CONTACT_SOLVER_WASM_SIMD, wasm_expected),
    ):
        available = bool(lib.cpContactSolverIsAvailable(backend))
        assert available == expected, (
            f"Unexpected backend {backend} availability: {available}; "
            f"expected {expected} on {platform.machine()} "
            f"({struct.calcsize('P') * 8}-bit Python)"
        )

    space = pymunk.Space()
    assert lib.cpSpaceGetContactSolver(space._space) == lib.CP_CONTACT_SOLVER_ORIGINAL
    space.solver_mode = pymunk.SolverMode.AUTO
    expected = (lib.CP_CONTACT_SOLVER_WASM_SIMD if wasm_expected else
                lib.CP_CONTACT_SOLVER_AVX2 if avx2_expected else
                lib.CP_CONTACT_SOLVER_ORIGINAL)
    assert lib.cpSpaceGetContactSolver(space._space) == expected
