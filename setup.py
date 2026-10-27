import json
import os
from pathlib import Path
import tempfile

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.errors import CompileError, ExecError


_AVX2_PROBE = """
#include "chipmunk/chipmunk_types.h"
#if !(defined(__x86_64__) || defined(__amd64__) || defined(_M_X64)) || defined(_M_ARM64EC)
#error AVX2 contact solving requires an x86-64 target
#endif
#if !CP_USE_DOUBLES
#error AVX2 contact solving requires double precision
#endif
#include <immintrin.h>
void pymunk_avx2_probe(double *out, const double *in) {
    __m256d value = _mm256_loadu_pd(in);
    _mm256_storeu_pd(out, _mm256_add_pd(value, value));
    __m256i indices = _mm256_set1_epi64x(1);
    _mm256_storeu_si256((__m256i *)out, _mm256_add_epi64(indices, indices));
}
"""


def _compiler_flags(compiler_type):
    """Return (AVX2 flags, scalar FP flags), or None for unknown compilers."""
    if compiler_type == "msvc":
        return ["/arch:AVX2", "/fp:strict", "/GL-"], ["/fp:strict"]
    if compiler_type == "unix":
        return ["-mavx2", "-ffp-contract=off", "-fno-lto"], ["-ffp-contract=off"]
    return None


def _with_source_flags(compile_sources, source_flags):
    """Keep architecture flags local to their source, including under CFFI."""
    def compile(
        sources, output_dir=None, macros=None, include_dirs=None, debug=0,
        extra_preargs=None, extra_postargs=None, depends=None,
    ):
        groups = {}
        for source in sources:
            flags = tuple(source_flags.get(os.path.basename(source), ()))
            groups.setdefault(flags, []).append(source)
        objects = []
        for flags, group in groups.items():
            objects.extend(compile_sources(
                group, output_dir=output_dir, macros=macros,
                include_dirs=include_dirs, debug=debug,
                extra_preargs=extra_preargs,
                extra_postargs=list(extra_postargs or []) + list(flags),
                depends=depends,
            ))
        return objects
    return compile


class PymunkBuildExt(build_ext):
    def _probe_avx2(self, extension, flags):
        # Compile, never execute: wheels and cross builds must depend on the
        # compiler target, not the build host's CPU. A universal macOS build
        # must pass for every target slice or remain scalar-only.
        Path(self.build_temp).mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="avx2-probe-", dir=self.build_temp) as tmp:
            source = Path(tmp) / "pymunk_avx2_probe.c"
            source.write_text(_AVX2_PROBE)
            try:
                self.compiler.compile(
                    [str(source)], output_dir=tmp,
                    macros=extension.define_macros,
                    include_dirs=extension.include_dirs,
                    extra_postargs=list(extension.extra_compile_args or []) + flags,
                )
            # Use setuptools' public exceptions: importing its private
            # _distutils namespace can create different exception classes
            # from those raised by the active compiler.
            except (CompileError, ExecError, OSError):
                return False
        return True

    def build_extensions(self):
        flags = _compiler_flags(self.compiler.compiler_type)
        enabled = False
        for extension in self.extensions:
            if extension.name != "pymunk._chipmunk":
                continue
            enabled = bool(flags and self._probe_avx2(extension, flags[0]))
            extension.define_macros = [
                item for item in extension.define_macros
                if item[0] != "CP_AVX2_CONTACT_SOLVER"
            ] + [("CP_AVX2_CONTACT_SOLVER", "1" if enabled else "0")]
            self.announce(
                "Munk2D AVX2 contact solver: " + ("enabled" if enabled else "disabled"),
                level=2,
            )

        source_flags = {}
        if flags:
            source_flags["cpContactSolverScalar.c"] = flags[1]
            if enabled:
                source_flags["cpContactSolverAvx2.c"] = flags[0]
        # Distutils does not track macro/flag changes as object dependencies.
        # A changed probe result must not reuse incompatible objects or skip
        # linking an already existing extension.
        stamp = Path(self.build_temp) / "pymunk-avx2-config.json"
        config = json.dumps({"enabled": enabled, "source_flags": source_flags}, sort_keys=True)
        changed = not stamp.exists() or stamp.read_text() != config
        original_force = self.force
        compiler_force = self.compiler.force
        if changed:
            self.force = self.compiler.force = True
        stamp.parent.mkdir(parents=True, exist_ok=True)
        if stamp.exists():
            stamp.unlink()

        original_compile = self.compiler.compile
        self.compiler.compile = _with_source_flags(original_compile, source_flags)
        try:
            super().build_extensions()
            stamp.write_text(config)
        finally:
            self.compiler.compile = original_compile
            self.force = original_force
            self.compiler.force = compiler_force


if __name__ == "__main__":
    packages = ["pymunk", "pymunk.tests", "pymunk.examples"]
    exclude_package_data = {}
    if os.getenv("PYMUNK_BUILD_SLIM"):
        packages = ["pymunk", "pymunk.tests"]
        exclude_package_data = {"pymunk.examples": ["*.*"]}

    setup(
        cmdclass={"build_ext": PymunkBuildExt},
        packages=packages,
        exclude_package_data=exclude_package_data,
        cffi_modules=["pymunk/pymunk_extension_build.py:ffibuilder"],
    )
