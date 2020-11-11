import doctest
import pkgutil
import sys
import unittest
from typing import Any

import pymunk


def load_tests(tests: unittest.TestSuite) -> unittest.TestSuite:
    for importer, modname, ispkg in pkgutil.iter_modules(pymunk.__path__):  # type: ignore  # mypy issue #1422
        # try:
        tests.addTests(doctest.DocTestSuite("pymunk." + modname))

        # except Exception as e:
        #    print("Skipping " + modname, e)
    tests.addTests(doctest.DocTestSuite(pymunk))
    return tests


if __name__ == "__main__":
    print("running doctests")
    suite = unittest.TestSuite()
    load_tests(suite)
    res = unittest.TextTestRunner().run(suite)
    sys.exit(not res.wasSuccessful())
