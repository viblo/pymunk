import subprocess
import sys
import textwrap
import unittest


class UnitTestFreeThreading(unittest.TestCase):
    def test_import_does_not_enable_gil(self) -> None:
        if not hasattr(sys, "_is_gil_enabled"):
            self.skipTest("sys._is_gil_enabled is not available")

        if sys._is_gil_enabled():
            self.skipTest("GIL is already enabled")

        code = textwrap.dedent(
            """
            import sys

            before = sys._is_gil_enabled()
            import pymunk
            after = sys._is_gil_enabled()

            if before:
                raise SystemExit("GIL was enabled before importing pymunk")
            if after:
                raise SystemExit("importing pymunk enabled the GIL")
            """
        )

        subprocess.run([sys.executable, "-c", code], check=True)
