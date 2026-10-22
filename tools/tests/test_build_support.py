"""Build-policy tests; no compiled pymunk extension is required."""

import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

from setuptools import Distribution, Extension
from setuptools.command.build_ext import build_ext
from setuptools._distutils.errors import CompileError, DistutilsSetupError

support = runpy.run_path(str(Path(__file__).resolve().parents[2] / "pymunk_build_support.py"))
PymunkBuildExt = support["PymunkBuildExt"]


class FakeCompiler:
    def __init__(self, compiler_type="unix", available=True):
        self.compiler_type = compiler_type
        self.available = available
        self.calls = []
        self.force = False

    def compile(self, sources, **kwargs):
        self.calls.append((list(sources), kwargs))
        if Path(sources[0]).name == "pymunk_avx2_probe.c":
            self.probe = Path(sources[0]).read_text()
            if not self.available:
                raise CompileError("unsupported target")
        return [source + ".o" for source in sources]


class BuildSupportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.extension = Extension(
            "pymunk._chipmunk",
            sources=["src/cpSpace.c", "src/cpContactSolverCpu.c",
                     "src/cpContactSolverAvx2.c", "src/cpContactSolverScalar.c"],
            define_macros=[("CP_OVERRIDE_MESSAGE", None)],
            include_dirs=["Munk2D/include"],
            extra_compile_args=["-O2"],
        )
        self.command = PymunkBuildExt(Distribution({"ext_modules": [self.extension]}))
        self.command.ensure_finalized()
        self.command.build_temp = self.tmp.name
        self.command.compiler = FakeCompiler()

    def run_build(self, mode="auto", failure=False):
        def build(command):
            self.forced = (bool(command.force), bool(command.compiler.force))
            if failure:
                raise CompileError("build failed")
            for extension in command.extensions:
                command.compiler.compile(
                    extension.sources, macros=extension.define_macros,
                    extra_postargs=extension.extra_compile_args,
                )
        with patch.dict(os.environ, {"PYMUNK_AVX2": mode}):
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
        self.assertIn("_M_X64", self.command.compiler.probe)
        self.assertIn("!CP_USE_DOUBLES", self.command.compiler.probe)

    def test_auto_falls_back_when_target_probe_fails(self):
        self.command.compiler.available = False
        self.run_build()
        self.assertIn(("CP_AVX2_CONTACT_SOLVER", "0"), self.extension.define_macros)
        self.assertEqual(self.flags_for("cpContactSolverAvx2.c"), ["-O2"])

    def test_off_skips_probe(self):
        self.run_build("off")
        self.assertFalse(hasattr(self.command.compiler, "probe"))
        self.assertIn(("CP_AVX2_CONTACT_SOLVER", "0"), self.extension.define_macros)

    def test_on_requires_successful_probe(self):
        self.command.compiler.available = False
        with self.assertRaisesRegex(DistutilsSetupError, "compile probe failed"):
            self.run_build("on")

    def test_unknown_compiler_defaults_to_disabled(self):
        self.command.compiler.compiler_type = "unknown"
        self.run_build()
        self.assertIn(("CP_AVX2_CONTACT_SOLVER", "0"), self.extension.define_macros)
        self.assertFalse(hasattr(self.command.compiler, "probe"))

    def test_invalid_mode(self):
        with self.assertRaisesRegex(DistutilsSetupError, "auto, on, or off"):
            self.run_build("yes")

    def test_msvc_flags(self):
        self.command.compiler.compiler_type = "msvc"
        self.run_build()
        self.assertEqual(self.flags_for("cpContactSolverAvx2.c"),
                         ["-O2", "/arch:AVX2", "/fp:strict", "/GL-"])
        self.assertEqual(self.flags_for("cpContactSolverScalar.c"), ["-O2", "/fp:strict"])
        self.assertEqual(self.flags_for("cpContactSolverCpu.c"), ["-O2"])

    def test_restores_compiler_and_force_after_failure(self):
        compile_method = self.command.compiler.compile
        with self.assertRaises(CompileError):
            self.run_build(failure=True)
        self.assertEqual(self.command.compiler.compile, compile_method)
        self.assertFalse(self.command.compiler.force)
        self.assertFalse(self.command.force)
        self.assertFalse((Path(self.tmp.name) / "pymunk-avx2-config.json").exists())

    def test_changed_backend_forces_rebuild(self):
        self.run_build("off")
        self.assertEqual(self.forced, (True, True))
        self.run_build("off")
        self.assertEqual(self.forced, (False, False))
        self.run_build("auto")
        self.assertEqual(self.forced, (True, True))
        self.assertEqual(sum(name == "CP_AVX2_CONTACT_SOLVER"
                             for name, value in self.extension.define_macros), 1)


if __name__ == "__main__":
    unittest.main()
