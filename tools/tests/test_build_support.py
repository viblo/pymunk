"""Build-policy tests; no compiled pymunk extension is required."""

from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

from setuptools import Distribution, Extension
from setuptools.command.build_ext import build_ext
from setuptools.errors import CompileError

support = runpy.run_path(str(Path(__file__).resolve().parents[2] / "setup.py"))
PymunkBuildExt = support["PymunkBuildExt"]


class FakeCompiler:
    def __init__(self):
        self.compiler_type = "unix"
        self.available = True
        self.wasm_target = False
        self.simd_available = True
        self.calls = []
        self.force = False

    def compile(self, sources, **kwargs):
        self.calls.append((list(sources), kwargs))
        if Path(sources[0]).name == "pymunk_backend_probe.c":
            code = Path(sources[0]).read_text()
            available = self.available
            if "pymunk_emscripten_target_probe" in code:
                available = self.wasm_target
            elif "pymunk_wasm_simd_probe" in code:
                available = self.simd_available
            if not available:
                raise CompileError("unsupported target")
        return [source + ".o" for source in sources]


class BuildSupportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.extension = Extension(
            "pymunk._chipmunk",
            sources=["src/cpSpace.c", "src/cpContactSolverCpu.c",
                     "src/cpContactSolverAvx2.c", "src/cpContactSolverScalar.c",
                     "src/cpContactSolverWasm.c"],
            define_macros=[("CP_OVERRIDE_MESSAGE", None)],
            include_dirs=["Munk2D/include"],
            extra_compile_args=["-O2"],
        )
        self.command = PymunkBuildExt(Distribution({"ext_modules": [self.extension]}))
        self.command.ensure_finalized()
        self.command.build_temp = self.tmp.name
        self.command.compiler = FakeCompiler()

    def run_build(self):
        def build(command):
            self.forced = (bool(command.force), bool(command.compiler.force))
            for extension in command.extensions:
                self.link_args = list(extension.extra_link_args or [])
                command.compiler.compile(
                    extension.sources, macros=extension.define_macros,
                    extra_postargs=extension.extra_compile_args,
                )
        with patch.object(build_ext, "build_extensions", build):
            self.command.build_extensions()

    def flags_for(self, basename):
        for sources, options in reversed(self.command.compiler.calls):
            if any(Path(source).name == basename for source in sources):
                return options["extra_postargs"]
        self.fail("source not compiled: " + basename)

    def test_auto_enables_backend_and_isolates_flags(self):
        self.run_build()
        self.assertIn(("CP_AVX2_CONTACT_SOLVER", "1"), self.extension.define_macros)
        self.assertEqual(self.flags_for("cpSpace.c"), ["-O2"])
        self.assertEqual(self.flags_for("cpContactSolverCpu.c"), ["-O2"])
        self.assertEqual(self.flags_for("cpContactSolverAvx2.c"),
                         ["-O2", "-mavx2", "-ffp-contract=off", "-fno-lto"])
        self.assertEqual(self.flags_for("cpContactSolverScalar.c"), ["-O2", "-ffp-contract=off"])
        self.assertEqual(self.extension.extra_compile_args, ["-O2"])

    def test_real_compiler_failure_disables_backend(self):
        # Exercise the actual compiler's exception type, not just our fake's.
        # Private setuptools._distutils exception classes can differ from it.
        from distutils.ccompiler import new_compiler
        from distutils.sysconfig import customize_compiler

        compiler = new_compiler()
        customize_compiler(compiler)
        self.command.compiler = compiler
        self.assertFalse(self.command._probe(
            self.extension, "#error intentional probe failure\n", []
        ))

    def test_wasm_simd_is_required_and_flags_are_isolated(self):
        self.command.compiler.wasm_target = True
        self.extension.extra_link_args = ["-sSIDE_MODULE=2"]
        self.run_build()
        self.assertIn(("CP_AVX2_CONTACT_SOLVER", "0"), self.extension.define_macros)
        self.assertIn(("CP_WASM_SIMD_CONTACT_SOLVER", "1"), self.extension.define_macros)
        for source in ("cpSpace.c", "cpContactSolverCpu.c", "cpContactSolverAvx2.c"):
            self.assertEqual(self.flags_for(source), ["-O2"])
        self.assertEqual(self.flags_for("cpContactSolverWasm.c"),
                         ["-O2", "-msimd128", "-ffp-contract=off", "-fno-lto"])
        self.assertEqual(self.flags_for("cpContactSolverScalar.c"),
                         ["-O2", "-ffp-contract=off"])
        self.assertEqual(self.link_args, ["-sSIDE_MODULE=2", "-msimd128"])
        self.assertEqual(self.extension.extra_link_args, ["-sSIDE_MODULE=2"])
        self.assertEqual(self.extension.extra_compile_args, ["-O2"])

    def test_wasm_without_simd_fails_instead_of_publishing_scalar(self):
        self.command.compiler.wasm_target = True
        self.command.compiler.simd_available = False
        with self.assertRaisesRegex(CompileError, "requires.*SIMD"):
            self.run_build()
        self.assertFalse(any("src/cpSpace.c" in sources
                             for sources, options in self.command.compiler.calls))

    def test_changed_backend_forces_rebuild(self):
        self.command.compiler.available = False
        self.run_build()
        self.assertEqual(self.forced, (True, True))
        self.run_build()
        self.assertEqual(self.forced, (False, False))
        self.command.compiler.available = True
        self.run_build()
        self.assertEqual(self.forced, (True, True))
        self.command.compiler.available = False
        self.run_build()
        self.assertEqual(self.forced, (True, True))
        self.command.compiler.wasm_target = True
        self.run_build()
        self.assertEqual(self.forced, (True, True))
        self.assertEqual(self.link_args, ["-msimd128"])
        self.run_build()
        self.assertEqual(self.forced, (False, False))
        self.command.compiler.wasm_target = False
        self.run_build()
        self.assertEqual(self.forced, (True, True))
        self.assertEqual(self.link_args, [])
        for macro in ("CP_AVX2_CONTACT_SOLVER", "CP_WASM_SIMD_CONTACT_SOLVER"):
            self.assertEqual(sum(name == macro
                                 for name, value in self.extension.define_macros), 1)


if __name__ == "__main__":
    unittest.main()
