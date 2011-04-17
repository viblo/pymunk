
import sys
sys.path.insert(0,'..')
import tests.unittests
import tests.vec2d_unittest
import unittest

suite = unittest.TestLoader().loadTestsFromModule(tests.vec2d_unittest)
suite.addTests(unittest.TestLoader().loadTestsFromModule(tests.unittests))

if len(sys.argv) > 1:
    m = sys.argv[1]

    for t in suite:
        for x in t:
            if m in str(x.id()):
                unittest.TextTestRunner(verbosity=2).run(x)
            #dir(x)
else:
    unittest.TextTestRunner(verbosity=2).run(suite)

