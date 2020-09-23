import doctest
import pkgutil
import sys
import unittest
from typing import Any, List

import pymunk


def load_tests(tests: unittest.TestSuite) -> None:
    for importer, modname, ispkg in pkgutil.iter_modules(pymunk.__path__):  # type: ignore
        try:
            tests.addTests(doctest.DocTestSuite("pymunk." + modname))
        except:
            print("Skipping " + modname)
    tests.addTests(doctest.DocTestSuite(pymunk))


if __name__ == "__main__":
    print("running doctests")
    suite = unittest.TestSuite()
    load_tests(suite)
    res = unittest.TextTestRunner().run(suite)
    sys.exit(not res.wasSuccessful())
