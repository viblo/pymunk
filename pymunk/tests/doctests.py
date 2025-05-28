import doctest
import pkgutil
import sys
import unittest

import pymunk

ignores = ["pymunk_extension_build"]
all_dependencies = ["pygame", "pyglet", "matplotlib", "_pyglet"]


def load_tests(
    tests: unittest.TestSuite, dependencies: list[str] = []
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
        tests.addTests(
            # Exception details are different in Pypy, so they need ot be ignored.
            doctest.DocTestSuite(
                "pymunk." + modname, optionflags=doctest.IGNORE_EXCEPTION_DETAIL
            )
        )

    tests.addTests(
        # Exception details are different in Pypy, so they need ot be ignored.
        doctest.DocTestSuite(pymunk, optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
    )
    return tests


if __name__ == "__main__":
    print("running doctests")
    suite = unittest.TestSuite()
    load_tests(suite)
    res = unittest.TextTestRunner().run(suite)
    sys.exit(not res.wasSuccessful())
