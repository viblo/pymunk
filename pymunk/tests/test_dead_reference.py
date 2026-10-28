import os
import subprocess
import sys
import textwrap
import unittest


class UnitTestDeadReference(unittest.TestCase):
    @unittest.skipIf(
        sys.platform in ("emscripten", "wasi", "ios", "android"),
        "Subprocesses are not available on this platform",
    )
    def test_detached_references_before_garbage_collection(self) -> None:
        # A fresh process avoids earlier tests collecting the sentinel's
        # temporary referent. A large nursery postpones PyPy's minor GC too.
        env = os.environ.copy()
        env["PYPY_GC_NURSERY"] = "64m"
        code = textwrap.dedent("""
            import gc
            gc.disable()
            import pymunk

            body = pymunk.Body(1, 1)
            shape = pymunk.Circle(body, 1)
            detached_shape = pymunk.Circle(None, 1)
            assert body.space is None, repr(body.space)
            assert shape.space is None, repr(shape.space)
            assert detached_shape.body is None, repr(detached_shape.body)
            assert shape.body is body

            # Check the guard only after verifying space is None, so the
            # original bug fails safely before an invalid native sleep call.
            try:
                body.sleep()
            except Exception:
                pass
            else:
                raise AssertionError('sleep accepted a body without a space')

            space = pymunk.Space()
            space.add(body, shape)
            assert body.space is space
            assert shape.space is space
            space.remove(shape, body)
            assert body.space is None
            assert shape.space is None
            shape.body = None
            assert shape.body is None

            gc.collect()
            assert body.space is None
            assert shape.space is None
            assert shape.body is None
            """)
        result = subprocess.run(
            [sys.executable, "-c", code],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
