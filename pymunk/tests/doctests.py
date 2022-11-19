import doctest
import pkgutil
import sys
import unittest
from typing import Any, List

import pymunk

ignores = ["pymunk_extension_build"]
all_dependencies = ["pygame", "pyglet", "matplotlib", "_pyglet"]


def load_tests(
    tests: unittest.TestSuite, dependencies: List[str] = []
) -> unittest.TestSuite:
    for importer, modname, ispkg in pkgutil.iter_modules(pymunk.__path__):
        # try:
        skip = False
        if modname in ignores:
            skip = True
        for dep in all_dependencies:
            if modname.startswith(dep) and dep not in dependencies:
                skip = True
        if skip:
            continue
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
