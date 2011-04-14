
import sys
sys.path.insert(0,'..')
import tests.unittests
import tests.vec2d_unittest
import unittest

suite = unittest.TestLoader().loadTestsFromModule(tests.vec2d_unittest)
suite.addTests(unittest.TestLoader().loadTestsFromModule(tests.unittests))

unittest.TextTestRunner(verbosity=2).run(suite)

