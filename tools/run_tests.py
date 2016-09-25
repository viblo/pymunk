
import sys
sys.path.insert(0,'..')
import unittest
import doctest

from tests import *
from tests import doctests


ts = ["test_vec2d", "test_body", "test_common", "test_constraint", 
    "test_shape", "test_space", "test_arbiter", "test_bb", "test_transform",
    "test_shape_filter", "test_autogeometry"]

suite = unittest.TestSuite()   
for t in ts:
    suite.addTests(unittest.TestLoader().loadTestsFromName("tests." + t))

doctests.load_tests(None, suite, False)

if len(sys.argv) > 1:
    m = sys.argv[1]

    for t in suite:
        if isinstance(t, doctest.DocTestCase):
            if m.startswith("doctest"):
                unittest.TextTestRunner(verbosity=2).run(t)
        else:
            for x in t:
                if m in str(x.id()):
                    unittest.TextTestRunner(verbosity=2).run(x)
             
else:
    unittest.TextTestRunner(verbosity=2).run(suite)

